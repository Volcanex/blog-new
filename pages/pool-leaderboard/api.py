"""
Pool Leaderboard API - ELO rating system for pool players
"""

from flask import Blueprint, jsonify, request
from shared.database import get_db
from datetime import datetime
import math

bp = Blueprint('pool_leaderboard', __name__, url_prefix='/api/pool-leaderboard')

class PoolEloSystem:
    @staticmethod
    def calculate_expected_score(rating_a, rating_b):
        """Calculate expected score for player A against player B"""
        return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))
    
    @staticmethod
    def calculate_k_factor(games_played, rating, is_winner=True, last_played=None):
        """Calculate K-factor based on games played, rating, and activity"""
        base_k = 40 if games_played < 20 else (
            20 if rating >= 2200 else
            28 if rating >= 1800 else
            35
        )
        
        # Enhanced new player boost - double K for first 5 games
        if games_played < 5:
            new_player_boost = 2.0  # Double K-factor for first 5 games
        elif games_played < 10:
            new_player_boost = 1.6  # Reduced boost for games 5-10
        else:
            new_player_boost = 1.0
        
        # Check for returning player after long break
        returning_player_boost = 1.0
        if last_played and games_played >= 5:
            from datetime import datetime
            try:
                last_game = datetime.fromisoformat(last_played)
                time_since = datetime.now() - last_game
                # If more than 2 months (60 days) since last game
                if time_since.days > 60:
                    returning_player_boost = 1.8  # Boost for returning players
            except:
                pass  # If date parsing fails, use default
        
        # Weight wins more heavily for faster convergence
        win_multiplier = 1.3 if is_winner else 0.9
        
        # Apply all multipliers
        final_k = base_k * new_player_boost * returning_player_boost * win_multiplier
        
        return int(final_k)

@bp.route('/players')
def get_players():
    """Get all players sorted by ELO rating"""
    db = get_db()
    players = db.get_page_data('pool-leaderboard', 'players', {})
    
    # Convert to sorted list
    player_list = []
    for name, data in players.items():
        player_data = data.copy()
        player_data['name'] = name
        if player_data['games_played'] > 0:
            player_data['win_rate'] = round((player_data['wins'] / player_data['games_played']) * 100, 1)
        else:
            player_data['win_rate'] = 0.0
        player_list.append(player_data)
    
    # Sort by rating (highest first)
    player_list.sort(key=lambda x: x['rating'], reverse=True)
    
    return jsonify({
        'players': player_list,
        'total_players': len(player_list),
        'last_updated': datetime.now().isoformat()
    })

@bp.route('/authenticate', methods=['POST'])
def authenticate():
    """Authenticate a user as an active player"""
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    name = data['name'].strip().lower()
    if not name:
        return jsonify({'error': 'Name cannot be empty'}), 400
    
    db = get_db()
    players = db.get_page_data('pool-leaderboard', 'players', {})
    
    if name not in players:
        return jsonify({'error': 'Player not found in leaderboard'}), 404
    
    # Store session info (in real app, this would use proper session management)
    session_data = {
        'name': name,
        'authenticated': True,
        'timestamp': datetime.now().isoformat()
    }
    
    return jsonify({
        'success': True,
        'player': players[name],
        'session': session_data
    })

@bp.route('/record-game', methods=['POST'])
def record_game():
    """Record a new game result"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON data required'}), 400
    
    required_fields = ['winner', 'loser', 'margin']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    winner = data['winner'].strip().lower()
    loser = data['loser'].strip().lower()
    margin = data.get('margin', 'close')
    
    if winner == loser:
        return jsonify({'error': 'Winner and loser cannot be the same'}), 400
    
    db = get_db()
    players = db.get_page_data('pool-leaderboard', 'players', {})
    
    if winner not in players or loser not in players:
        return jsonify({'error': 'One or both players not found'}), 404
    
    # Calculate ELO changes
    winner_rating = players[winner]['rating']
    loser_rating = players[loser]['rating']
    
    # Expected scores
    winner_expected = PoolEloSystem.calculate_expected_score(winner_rating, loser_rating)
    loser_expected = PoolEloSystem.calculate_expected_score(loser_rating, winner_rating)
    
    # Margin adjustments
    margin_multiplier = {
        'close': 1.0,
        'comfortable': 1.1,
        'decisive': 1.2
    }.get(margin, 1.0)
    
    # K-factors with activity boost
    winner_k = PoolEloSystem.calculate_k_factor(
        players[winner]['games_played'], 
        winner_rating, 
        True, 
        players[winner].get('last_played')
    )
    loser_k = PoolEloSystem.calculate_k_factor(
        players[loser]['games_played'], 
        loser_rating, 
        False, 
        players[loser].get('last_played')
    )
    
    # Rating changes
    winner_change = winner_k * margin_multiplier * (1 - winner_expected)
    loser_change = loser_k * margin_multiplier * (0 - loser_expected)
    
    # Update player data
    old_winner_rating = players[winner]['rating']
    old_loser_rating = players[loser]['rating']
    
    players[winner]['rating'] += round(winner_change)
    players[winner]['games_played'] += 1
    players[winner]['wins'] += 1
    players[winner]['last_played'] = datetime.now().isoformat()
    
    players[loser]['rating'] += round(loser_change)
    players[loser]['games_played'] += 1
    players[loser]['losses'] += 1
    players[loser]['last_played'] = datetime.now().isoformat()
    
    # Save updated data
    db.set_page_data('pool-leaderboard', 'players', players)
    
    # Record game history
    game_record = {
        'id': datetime.now().timestamp(),
        'winner': winner,
        'loser': loser,
        'margin': margin,
        'winner_rating_before': old_winner_rating,
        'loser_rating_before': old_loser_rating,
        'winner_rating_after': players[winner]['rating'],
        'loser_rating_after': players[loser]['rating'],
        'winner_change': round(winner_change),
        'loser_change': round(loser_change),
        'timestamp': datetime.now().isoformat()
    }
    
    db.append_to_page_collection('pool-leaderboard', 'game_history', game_record)
    
    return jsonify({
        'success': True,
        'game': game_record,
        'winner_new_rating': players[winner]['rating'],
        'loser_new_rating': players[loser]['rating']
    })

@bp.route('/recent-games')
def recent_games():
    """Get recent game history"""
    db = get_db()
    games = db.get_page_data('pool-leaderboard', 'game_history', [])
    
    # Sort by timestamp (most recent first) and limit to 20
    games.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    recent_games = games[:20]
    
    return jsonify({
        'games': recent_games,
        'total_games': len(games)
    })

@bp.route('/reset-data', methods=['POST'])
def reset_data():
    """Reset all current players to 1000 ELO"""
    db = get_db()
    
    # Get current players and reset their ratings to 1000
    current_players = db.get_page_data('pool-leaderboard', 'players', {})
    
    # Reset all current players to 1000 ELO, keeping their created dates
    for player_name, player_data in current_players.items():
        current_players[player_name] = {
            "rating": 1000,
            "games_played": 0,
            "wins": 0,
            "losses": 0,
            "created": player_data.get('created', datetime.now().isoformat()),
            "last_played": None
        }
    
    # Save to database
    db.set_page_data('pool-leaderboard', 'players', current_players)
    db.set_page_data('pool-leaderboard', 'game_history', [])
    
    return jsonify({
        'success': True,
        'message': f'All {len(current_players)} players reset to 1000 ELO',
        'players_count': len(current_players)
    })

@bp.route('/init-data', methods=['POST'])
def init_data():
    """Initialize pool data from existing system (one-time setup)"""
    db = get_db()
    
    # Check if data already exists
    existing_players = db.get_page_data('pool-leaderboard', 'players', {})
    if existing_players:
        return jsonify({'error': 'Data already initialized'}), 400
    
    # Initial player data from the existing pool system
    initial_players = {
        "oli": {
            "rating": 1229,
            "games_played": 19,
            "wins": 8,
            "losses": 11,
            "created": "2025-07-13T05:33:04.790098",
            "last_played": "2025-07-23T07:37:18.789035"
        },
        "jack": {
            "rating": 1343,
            "games_played": 21,
            "wins": 11,
            "losses": 10,
            "created": "2025-07-13T05:33:19.788895",
            "last_played": "2025-07-26T15:25:19.038975"
        },
        "gabriel": {
            "rating": 1392,
            "games_played": 19,
            "wins": 12,
            "losses": 7,
            "created": "2025-07-13T05:33:30.567499",
            "last_played": "2025-07-26T15:25:19.038953"
        },
        "jen": {
            "rating": 1166,
            "games_played": 7,
            "wins": 2,
            "losses": 5,
            "created": "2025-07-13T05:33:41.539030",
            "last_played": "2025-07-19T11:01:45.289063"
        },
        "jess": {
            "rating": 1212,
            "games_played": 2,
            "wins": 1,
            "losses": 1,
            "created": "2025-07-13T05:34:58.288934",
            "last_played": "2025-07-13T07:43:38.289190"
        }
    }
    
    # Save to database
    db.set_page_data('pool-leaderboard', 'players', initial_players)
    db.set_page_data('pool-leaderboard', 'game_history', [])
    
    return jsonify({
        'success': True,
        'message': 'Pool data initialized successfully',
        'players_count': len(initial_players)
    })

@bp.route('/add-player', methods=['POST'])
def add_player():
    """Add a new player to the system"""
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    name = data['name'].strip().lower()
    if not name:
        return jsonify({'error': 'Name cannot be empty'}), 400
    
    db = get_db()
    players = db.get_page_data('pool-leaderboard', 'players', {})
    
    if name in players:
        return jsonify({'error': 'Player already exists'}), 400
    
    # Add new player with default rating
    initial_rating = data.get('initial_rating', 1200)
    players[name] = {
        "rating": initial_rating,
        "games_played": 0,
        "wins": 0,
        "losses": 0,
        "created": datetime.now().isoformat(),
        "last_played": None
    }
    
    db.set_page_data('pool-leaderboard', 'players', players)
    
    return jsonify({
        'success': True,
        'message': f'Player {name} added successfully',
        'player': players[name]
    })

@bp.route('/delete-game', methods=['POST'])
def delete_game():
    """Delete a recent game (within 20 minutes)"""
    data = request.get_json()
    if not data or 'game_id' not in data:
        return jsonify({'error': 'Game ID is required'}), 400
    
    game_id = data['game_id']
    
    db = get_db()
    games = db.get_page_data('pool-leaderboard', 'game_history', [])
    players = db.get_page_data('pool-leaderboard', 'players', {})
    
    # Find the game to delete
    game_to_delete = None
    for i, game in enumerate(games):
        if game.get('id') == game_id:
            # Check if game is within 20 minutes
            game_time = datetime.fromisoformat(game['timestamp'])
            time_diff = datetime.now() - game_time
            if time_diff.total_seconds() > 1200:  # 20 minutes
                return jsonify({'error': 'Can only delete games within 20 minutes'}), 400
            
            game_to_delete = games.pop(i)
            break
    
    if not game_to_delete:
        return jsonify({'error': 'Game not found'}), 404
    
    # Reverse the ELO changes
    winner = game_to_delete['winner']
    loser = game_to_delete['loser']
    
    if winner in players and loser in players:
        # Reverse rating changes
        players[winner]['rating'] = game_to_delete['winner_rating_before']
        players[winner]['games_played'] -= 1
        players[winner]['wins'] -= 1
        
        players[loser]['rating'] = game_to_delete['loser_rating_before']
        players[loser]['games_played'] -= 1
        players[loser]['losses'] -= 1
        
        # Save updated data
        db.set_page_data('pool-leaderboard', 'players', players)
        db.set_page_data('pool-leaderboard', 'game_history', games)
        
        return jsonify({
            'success': True,
            'message': 'Game deleted and ratings restored',
            'deleted_game': game_to_delete
        })
    else:
        return jsonify({'error': 'Players not found'}), 404

@bp.route('/average-rating')
def get_average_rating():
    """Get the average rating of all players"""
    db = get_db()
    players = db.get_page_data('pool-leaderboard', 'players', {})
    
    if not players:
        return jsonify({'average_rating': 1200})
    
    total_rating = sum(player['rating'] for player in players.values())
    average = round(total_rating / len(players))
    
    return jsonify({
        'average_rating': average,
        'total_players': len(players)
    })

@bp.route('/remove-player', methods=['POST'])
def remove_player():
    """Remove a player from the system"""
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Player name is required'}), 400
    
    name = data['name'].strip().lower()
    if not name:
        return jsonify({'error': 'Name cannot be empty'}), 400
    
    db = get_db()
    players = db.get_page_data('pool-leaderboard', 'players', {})
    
    if name not in players:
        return jsonify({'error': 'Player not found'}), 404
    
    # Remove player
    removed_player = players.pop(name)
    
    # Save updated data
    db.set_page_data('pool-leaderboard', 'players', players)
    
    return jsonify({
        'success': True,
        'message': f'Player {name} removed successfully',
        'removed_player': removed_player,
        'remaining_players': len(players)
    })