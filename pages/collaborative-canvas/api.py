"""
API endpoints and WebSocket handlers for Collaborative Canvas
"""

from flask import Blueprint, jsonify, request
from flask_socketio import emit, join_room, leave_room
from shared.database import get_db
from shared.websocket_utils import WebSocketRoomManager, websocket_success_response, websocket_error_handler, validate_websocket_data
from datetime import datetime
import json

bp = Blueprint('collaborative_canvas', __name__, url_prefix='/api/collaborative-canvas')

# Global room manager for the single collaborative canvas
canvas_room_manager = WebSocketRoomManager()
CANVAS_ROOM_ID = "main_canvas"
MAX_PLAYERS = 8

# Create a startup backup to preserve any existing canvas data
def create_startup_backup():
    """Create a backup of existing canvas data on server startup"""
    try:
        db = get_db()
        canvas_state = db.get_page_data('collaborative-canvas', 'current_canvas', {})
        
        if canvas_state.get('strokes'):
            db.append_to_page_collection('collaborative-canvas', 'canvas_backups', {
                'strokes': canvas_state['strokes'].copy(),
                'timestamp': datetime.now().isoformat(),
                'stroke_count': len(canvas_state['strokes']),
                'backup_reason': 'Server startup backup',
                'server_restart': True
            })
            print(f"Created startup backup with {len(canvas_state['strokes'])} strokes")
    except Exception as e:
        print(f"Failed to create startup backup: {e}")

# Create startup backup
create_startup_backup()

@bp.route('/canvas-info')
def get_canvas_info():
    """Get current canvas state and player information"""
    db = get_db()
    
    # Get current canvas state
    canvas_state = db.get_page_data('collaborative-canvas', 'current_canvas', {
        'strokes': [],
        'last_updated': datetime.now().isoformat(),
        'created_by': None
    })
    
    # Get room statistics
    room = canvas_room_manager.get_room(CANVAS_ROOM_ID)
    player_count = room.get_player_count() if room else 0
    
    return jsonify({
        'canvas_state': canvas_state,
        'player_count': player_count,
        'max_players': MAX_PLAYERS,
        'room_full': player_count >= MAX_PLAYERS,
        'last_updated': canvas_state.get('last_updated')
    })

@bp.route('/save-canvas', methods=['POST'])
def save_canvas():
    """Manually save current canvas state"""
    data = request.get_json()
    if not data or 'strokes' not in data:
        return jsonify({'error': 'Canvas strokes required'}), 400
    
    db = get_db()
    canvas_state = {
        'strokes': data['strokes'],
        'last_updated': datetime.now().isoformat(),
        'saved_manually': True
    }
    
    db.set_page_data('collaborative-canvas', 'current_canvas', canvas_state)
    
    # Also save to history
    db.append_to_page_collection('collaborative-canvas', 'canvas_history', {
        'strokes': data['strokes'],
        'timestamp': datetime.now().isoformat(),
        'stroke_count': len(data['strokes'])
    })
    
    return jsonify({'success': True, 'saved_at': canvas_state['last_updated']})

@bp.route('/canvas-backups')
def get_canvas_backups():
    """Get list of canvas backups for recovery purposes"""
    db = get_db()
    backups = db.get_page_data('collaborative-canvas', 'canvas_backups', [])
    
    # Sort by timestamp (most recent first) and limit to last 10
    backups.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    recent_backups = backups[:10]
    
    return jsonify({
        'backups': recent_backups,
        'total_backups': len(backups),
        'current_stroke_count': len(db.get_page_data('collaborative-canvas', 'current_canvas', {}).get('strokes', []))
    })

def register_websocket_handlers(socketio):
    """Register WebSocket event handlers for collaborative canvas"""
    
    @socketio.on('connect', namespace='/collaborative-canvas')
    def on_connect():
        emit('connected', websocket_success_response({
            'message': 'Connected to collaborative canvas',
            'namespace': '/collaborative-canvas'
        }))
    
    @socketio.on('disconnect', namespace='/collaborative-canvas')
    def on_disconnect():
        from flask import request
        
        # Try to find and remove the disconnected player from any room
        room = canvas_room_manager.get_room(CANVAS_ROOM_ID)
        if room:
            # Look for player by session ID (this is imperfect but helps)
            session_id = request.sid
            players_to_remove = []
            
            for player_id, player_data in room.players.items():
                # Remove players that have been inactive for a while
                # This is a heuristic approach since we don't have perfect session tracking
                try:
                    joined_time = datetime.fromisoformat(player_data['joined_at'])
                    time_since_join = datetime.now() - joined_time
                    # If they've been "in" for more than 30 minutes, consider them stale
                    if time_since_join.total_seconds() > 1800:  # 30 minutes
                        players_to_remove.append(player_id)
                except:
                    pass
            
            # Remove stale players
            for player_id in players_to_remove:
                room.remove_player(player_id)
                print(f"Removed stale player {player_id} on disconnect cleanup")
        
        # Clean up empty rooms
        canvas_room_manager.cleanup_empty_rooms()
        
        # Broadcast updated player count
        room = canvas_room_manager.get_room(CANVAS_ROOM_ID)
        player_count = room.get_player_count() if room else 0
        
        if room:
            emit('player_count_update', {
                'player_count': player_count,
                'max_players': MAX_PLAYERS,
                'room_full': player_count >= MAX_PLAYERS
            }, room=CANVAS_ROOM_ID)
    
    @socketio.on('join_canvas', namespace='/collaborative-canvas')
    def join_canvas(data):
        """Join the collaborative canvas room"""
        valid, message = validate_websocket_data(data, ['player_id'])
        if not valid:
            return websocket_error_handler(message)
        
        player_id = data['player_id']
        
        # Get or create the main canvas room
        room = canvas_room_manager.get_room(CANVAS_ROOM_ID)
        if not room:
            room = canvas_room_manager.create_room(CANVAS_ROOM_ID, MAX_PLAYERS)
        
        # Check if room is full
        if room.is_full():
            # Try to clean up any stale connections first
            cleaned = canvas_room_manager.cleanup_empty_rooms()
            room = canvas_room_manager.get_room(CANVAS_ROOM_ID)  # Refresh room reference
            
            # If still full after cleanup, reject new player
            if room and room.is_full():
                # As a last resort, kick the oldest player if they seem inactive
                if len(room.players) >= MAX_PLAYERS:
                    # Find oldest player (first in the dict)
                    oldest_player_id = list(room.players.keys())[0]
                    room.remove_player(oldest_player_id)
                    print(f"Kicked oldest player {oldest_player_id} to make room for new player")
                    
                    # Notify that a player was removed due to inactivity
                    emit('player_kicked', {
                        'kicked_player_id': oldest_player_id,
                        'reason': 'Inactive - made room for new player',
                        'player_count': room.get_player_count()
                    }, room=CANVAS_ROOM_ID)
            
            # If still somehow full, show error
            if room and room.is_full():
                emit('canvas_full', websocket_error_handler("Canvas is full (8 players max). Please wait for someone to leave."))
                return
        
        # Debug: print room status
        print(f"Room status: {room.get_player_count()}/{MAX_PLAYERS} players")
        
        # Add player to room
        success, message = room.add_player(player_id, {
            'joined_at': datetime.now().isoformat(),
            'name': data.get('name', f'Player {player_id[:8]}')
        })
        
        if not success:
            return websocket_error_handler(message)
        
        # Join the socket room
        join_room(CANVAS_ROOM_ID)
        
        # Determine if this player is the host (first player)
        is_host = room.get_player_count() == 1
        if is_host:
            room.data['host'] = player_id
        
        # Send current canvas state to the new joiner
        db = get_db()
        canvas_state = db.get_page_data('collaborative-canvas', 'current_canvas', {
            'strokes': [],
            'last_updated': datetime.now().isoformat()
        })
        
        emit('canvas_joined', websocket_success_response({
            'room_id': CANVAS_ROOM_ID,
            'player_count': room.get_player_count(),
            'max_players': MAX_PLAYERS,
            'is_host': is_host,
            'canvas_state': canvas_state
        }))
        
        print(f"Player {player_id} joined canvas, sending {len(canvas_state.get('strokes', []))} strokes")
        
        # Notify all players of the new joiner
        emit('player_joined', {
            'player_id': player_id,
            'player_name': data.get('name', f'Player {player_id[:8]}'),
            'player_count': room.get_player_count(),
            'max_players': MAX_PLAYERS,
            'room_full': room.is_full()
        }, room=CANVAS_ROOM_ID)
    
    @socketio.on('leave_canvas', namespace='/collaborative-canvas')
    def leave_canvas(data):
        """Leave the collaborative canvas"""
        valid, message = validate_websocket_data(data, ['player_id'])
        if not valid:
            return websocket_error_handler(message)
        
        player_id = data['player_id']
        room = canvas_room_manager.get_room(CANVAS_ROOM_ID)
        
        if not room:
            return websocket_error_handler("Canvas room not found")
        
        # Check if this player is the host
        was_host = room.data.get('host') == player_id
        
        # Remove player from room
        room.remove_player(player_id)
        leave_room(CANVAS_ROOM_ID)
        
        # Always save a backup when anyone leaves (not just host)
        db = get_db()
        canvas_state = db.get_page_data('collaborative-canvas', 'current_canvas', {
            'strokes': [],
            'last_updated': datetime.now().isoformat()
        })
        
        # Save backup on every player leave to prevent data loss
        if canvas_state.get('strokes'):
            db.append_to_page_collection('collaborative-canvas', 'canvas_backups', {
                'strokes': canvas_state['strokes'].copy(),
                'timestamp': datetime.now().isoformat(),
                'stroke_count': len(canvas_state['strokes']),
                'backup_reason': f'Player {player_id} left (was_host: {was_host})',
                'player_id': player_id
            })
            print(f"Saved canvas backup when {player_id} left ({len(canvas_state['strokes'])} strokes)")
        
        # If host left and there are still players, assign new host
        if was_host and room.get_player_count() > 0:
            # Assign new host (first remaining player)
            if room.players:
                new_host = list(room.players.keys())[0]
                room.data['host'] = new_host
                
                emit('new_host_assigned', {
                    'new_host': new_host,
                    'message': 'You are now the host!'
                }, room=new_host)
        
        # Clean up empty rooms
        if room.get_player_count() == 0:
            canvas_room_manager.remove_room(CANVAS_ROOM_ID)
        
        # Notify remaining players
        emit('player_left', {
            'player_id': player_id,
            'player_count': room.get_player_count(),
            'max_players': MAX_PLAYERS,
            'room_full': False,
            'was_host': was_host
        }, room=CANVAS_ROOM_ID)
        
        emit('canvas_left', websocket_success_response({'message': 'Left canvas successfully'}))
    
    @socketio.on('draw_stroke', namespace='/collaborative-canvas')
    def draw_stroke(data):
        """Handle drawing stroke from a player"""
        valid, message = validate_websocket_data(data, ['player_id', 'stroke'])
        if not valid:
            return websocket_error_handler(message)
        
        player_id = data['player_id']
        stroke_data = data['stroke']
        
        room = canvas_room_manager.get_room(CANVAS_ROOM_ID)
        if not room or player_id not in room.players:
            return websocket_error_handler("Player not in canvas room")
        
        # Validate stroke data
        if not isinstance(stroke_data, dict):
            return websocket_error_handler("Invalid stroke data format")
        
        required_stroke_fields = ['x', 'y', 'color']
        for field in required_stroke_fields:
            if field not in stroke_data:
                return websocket_error_handler(f"Stroke missing {field}")
        
        # Validate color is one of the allowed colors
        allowed_colors = ['black', 'white', 'red', 'blue', 'green', 'yellow', 'orange']
        if stroke_data['color'] not in allowed_colors:
            return websocket_error_handler(f"Color must be one of: {', '.join(allowed_colors)}")
        
        # Add timestamp and player info to stroke
        stroke_data['timestamp'] = datetime.now().isoformat()
        stroke_data['player_id'] = player_id
        
        # Save stroke to database for persistence - IMMEDIATELY save each stroke
        db = get_db()
        canvas_state = db.get_page_data('collaborative-canvas', 'current_canvas', {
            'strokes': [],
            'last_updated': datetime.now().isoformat(),
            'stroke_count': 0
        })
        canvas_state['strokes'].append(stroke_data)
        canvas_state['last_updated'] = datetime.now().isoformat()
        canvas_state['stroke_count'] = len(canvas_state['strokes'])
        
        # Save immediately - never lose strokes
        db.set_page_data('collaborative-canvas', 'current_canvas', canvas_state)
        
        # Also save to backup/history periodically (every 50 strokes)
        if canvas_state['stroke_count'] % 50 == 0:
            db.append_to_page_collection('collaborative-canvas', 'canvas_backups', {
                'strokes': canvas_state['strokes'].copy(),
                'timestamp': datetime.now().isoformat(),
                'stroke_count': canvas_state['stroke_count'],
                'backup_reason': f'Periodic backup at {canvas_state["stroke_count"]} strokes'
            })
            print(f"Saved canvas backup at {canvas_state['stroke_count']} strokes")
        
        # Broadcast stroke to all other players in the room
        emit('stroke_received', {
            'stroke': stroke_data,
            'from_player': player_id
        }, room=CANVAS_ROOM_ID, include_self=False)
        
        # Acknowledge stroke to sender
        emit('stroke_acknowledged', websocket_success_response({
            'stroke_id': stroke_data.get('id', 'unknown'),
            'total_strokes': len(canvas_state['strokes'])
        }))
    
    # Note: Clear canvas functionality removed to maintain communal permanent canvas
    
    @socketio.on('request_canvas_state', namespace='/collaborative-canvas')
    def request_canvas_state(data):
        """Request current canvas state (for sync purposes)"""
        valid, message = validate_websocket_data(data, ['player_id'])
        if not valid:
            return websocket_error_handler(message)
        
        player_id = data['player_id']
        room = canvas_room_manager.get_room(CANVAS_ROOM_ID)
        
        if not room or player_id not in room.players:
            return websocket_error_handler("Player not in canvas room")
        
        # Send current canvas state
        db = get_db()
        canvas_state = db.get_page_data('collaborative-canvas', 'current_canvas', {
            'strokes': [],
            'last_updated': datetime.now().isoformat()
        })
        
        emit('canvas_state_update', websocket_success_response({
            'canvas_state': canvas_state,
            'player_count': room.get_player_count()
        }))