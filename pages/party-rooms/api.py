"""
Party Rooms API - Real-time multiplayer room management with WebSockets
Uses existing WebSocket infrastructure from shared utilities
"""

from flask import Blueprint, jsonify, request
from flask_socketio import emit, join_room, leave_room
from shared.websocket_utils import (
    WebSocketRoomManager,
    websocket_success_response,
    websocket_error_handler,
    validate_websocket_data
)
from datetime import datetime
import random
import string

bp = Blueprint('party_rooms', __name__, url_prefix='/api/party-rooms')

# Global room manager
room_manager = WebSocketRoomManager()

def generate_room_code(length=5):
    """Generate a random room code"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def get_unique_room_code():
    """Generate a unique room code that doesn't exist yet"""
    while True:
        code = generate_room_code()
        if not room_manager.get_room(code):
            return code

@bp.route('/create-room', methods=['POST'])
def create_room():
    """Create a new room via HTTP (returns room code)"""
    data = request.json
    username = data.get('username', 'Anonymous')
    max_players = data.get('max_players', 20)

    room_code = get_unique_room_code()
    room = room_manager.create_room(room_id=room_code, max_players=max_players)

    room.data['host'] = username
    room.data['created_at'] = datetime.now().isoformat()
    room.data['messages'] = []
    room.data['current_vote'] = None

    return jsonify({
        'success': True,
        'room_code': room_code,
        'room': room.to_dict()
    })

@bp.route('/room/<room_code>', methods=['GET'])
def get_room(room_code):
    """Get room information via HTTP"""
    room_code = room_code.upper()
    room = room_manager.get_room(room_code)

    if not room:
        return jsonify({'error': 'Room not found'}), 404

    return jsonify({
        'success': True,
        'room': room.to_dict()
    })

@bp.route('/stats', methods=['GET'])
def get_stats():
    """Get room manager statistics"""
    return jsonify({
        'success': True,
        'stats': room_manager.get_stats()
    })

def register_websocket_handlers(socketio):
    """Register WebSocket event handlers"""

    @socketio.on('connect', namespace='/party-rooms')
    def on_connect():
        emit('connected', websocket_success_response({
            'message': 'Connected to party rooms',
            'namespace': '/party-rooms'
        }))

    @socketio.on('disconnect', namespace='/party-rooms')
    def on_disconnect():
        # Clean up empty rooms
        room_manager.cleanup_empty_rooms()

    @socketio.on('join_room', namespace='/party-rooms')
    def handle_join_room(data):
        """Handle user joining a room"""
        valid, message = validate_websocket_data(data, ['room_code', 'username'])
        if not valid:
            return websocket_error_handler(message)

        room_code = data['room_code'].upper()
        username = data['username']

        room = room_manager.get_room(room_code)
        if not room:
            return websocket_error_handler('Room not found')

        # Check if room is full
        if room.is_full():
            return websocket_error_handler('Room is full')

        # Check if username already exists
        existing_usernames = [
            p['data'].get('username') for p in room.players.values()
        ]
        original_username = username
        counter = 1
        while username in existing_usernames:
            username = f"{original_username}{counter}"
            counter += 1

        # Add player to room
        player_id = request.sid
        success, msg = room.add_player(player_id, {
            'username': username,
            'is_host': username == room.data.get('host'),
            'joined_at': datetime.now().isoformat()
        })

        if not success:
            return websocket_error_handler(msg)

        # Join the Socket.IO room
        join_room(room_code)

        # Send room info to the joining user
        emit('room_joined', websocket_success_response({
            'room_code': room_code,
            'username': username,
            'is_host': username == room.data.get('host'),
            'room': room.to_dict(),
            'participants': [
                {
                    'username': p['data'].get('username'),
                    'is_host': p['data'].get('is_host', False),
                    'joined_at': p['data'].get('joined_at')
                }
                for p in room.players.values()
            ]
        }))

        # Notify everyone in the room
        emit('user_joined', {
            'username': username,
            'participant_count': room.get_player_count(),
            'participants': [
                {
                    'username': p['data'].get('username'),
                    'is_host': p['data'].get('is_host', False)
                }
                for p in room.players.values()
            ]
        }, room=room_code, namespace='/party-rooms')

    @socketio.on('leave_room', namespace='/party-rooms')
    def handle_leave_room(data):
        """Handle user leaving a room"""
        valid, message = validate_websocket_data(data, ['room_code'])
        if not valid:
            return websocket_error_handler(message)

        room_code = data['room_code'].upper()
        player_id = request.sid

        room = room_manager.get_room(room_code)
        if not room:
            return websocket_error_handler('Room not found')

        if player_id not in room.players:
            return websocket_error_handler('Player not in room')

        username = room.players[player_id]['data'].get('username')
        was_host = room.players[player_id]['data'].get('is_host', False)

        # Remove player from room
        room.remove_player(player_id)
        leave_room(room_code)

        # If room is empty, delete it
        if room.get_player_count() == 0:
            room_manager.remove_room(room_code)
        else:
            # If host left, assign new host
            if was_host and room.get_player_count() > 0:
                new_host_id = list(room.players.keys())[0]
                room.players[new_host_id]['data']['is_host'] = True
                new_host_username = room.players[new_host_id]['data'].get('username')
                room.data['host'] = new_host_username

                emit('new_host', {
                    'new_host': new_host_username
                }, room=new_host_id, namespace='/party-rooms')

            # Notify remaining participants
            emit('user_left', {
                'username': username,
                'participant_count': room.get_player_count(),
                'participants': [
                    {
                        'username': p['data'].get('username'),
                        'is_host': p['data'].get('is_host', False)
                    }
                    for p in room.players.values()
                ]
            }, room=room_code, namespace='/party-rooms')

        emit('room_left', websocket_success_response({'message': 'Left room successfully'}))

    @socketio.on('send_message', namespace='/party-rooms')
    def handle_send_message(data):
        """Handle chat message"""
        valid, message = validate_websocket_data(data, ['room_code', 'message'])
        if not valid:
            return websocket_error_handler(message)

        room_code = data['room_code'].upper()
        player_id = request.sid

        room = room_manager.get_room(room_code)
        if not room or player_id not in room.players:
            return websocket_error_handler('Player not in room')

        username = room.players[player_id]['data'].get('username')
        message_text = data['message']

        # Store message in room data
        if 'messages' not in room.data:
            room.data['messages'] = []

        room.data['messages'].append({
            'username': username,
            'message': message_text,
            'timestamp': datetime.now().isoformat()
        })

        # Broadcast to room
        emit('new_message', {
            'username': username,
            'message': message_text,
            'timestamp': datetime.now().isoformat()
        }, room=room_code, namespace='/party-rooms')

    @socketio.on('start_vote', namespace='/party-rooms')
    def handle_start_vote(data):
        """Handle starting a vote"""
        valid, message = validate_websocket_data(data, ['room_code', 'question', 'options'])
        if not valid:
            return websocket_error_handler(message)

        room_code = data['room_code'].upper()
        player_id = request.sid

        room = room_manager.get_room(room_code)
        if not room or player_id not in room.players:
            return websocket_error_handler('Player not in room')

        username = room.players[player_id]['data'].get('username')

        vote_data = {
            'question': data['question'],
            'options': data['options'],
            'votes': {},
            'started_by': username,
            'started_at': datetime.now().isoformat()
        }

        room.data['current_vote'] = vote_data

        emit('vote_started', vote_data, room=room_code, namespace='/party-rooms')

    @socketio.on('cast_vote', namespace='/party-rooms')
    def handle_cast_vote(data):
        """Handle casting a vote"""
        valid, message = validate_websocket_data(data, ['room_code', 'option'])
        if not valid:
            return websocket_error_handler(message)

        room_code = data['room_code'].upper()
        player_id = request.sid

        room = room_manager.get_room(room_code)
        if not room or player_id not in room.players:
            return websocket_error_handler('Player not in room')

        if 'current_vote' not in room.data or not room.data['current_vote']:
            return websocket_error_handler('No active vote')

        username = room.players[player_id]['data'].get('username')
        option = data['option']

        room.data['current_vote']['votes'][username] = option

        # Calculate vote counts
        vote_counts = {}
        for opt in room.data['current_vote']['options']:
            vote_counts[opt] = 0

        for vote in room.data['current_vote']['votes'].values():
            if vote in vote_counts:
                vote_counts[vote] += 1

        emit('vote_update', {
            'vote_counts': vote_counts,
            'total_votes': len(room.data['current_vote']['votes']),
            'total_participants': room.get_player_count()
        }, room=room_code, namespace='/party-rooms')

    @socketio.on('end_vote', namespace='/party-rooms')
    def handle_end_vote(data):
        """Handle ending a vote"""
        valid, message = validate_websocket_data(data, ['room_code'])
        if not valid:
            return websocket_error_handler(message)

        room_code = data['room_code'].upper()
        player_id = request.sid

        room = room_manager.get_room(room_code)
        if not room or player_id not in room.players:
            return websocket_error_handler('Player not in room')

        if 'current_vote' in room.data and room.data['current_vote']:
            final_vote = room.data['current_vote']
            room.data['current_vote'] = None

            emit('vote_ended', {
                'final_vote': final_vote
            }, room=room_code, namespace='/party-rooms')

    @socketio.on('game_action', namespace='/party-rooms')
    def handle_game_action(data):
        """Handle generic game actions for custom games"""
        valid, message = validate_websocket_data(data, ['room_code', 'action'])
        if not valid:
            return websocket_error_handler(message)

        room_code = data['room_code'].upper()
        player_id = request.sid

        room = room_manager.get_room(room_code)
        if not room or player_id not in room.players:
            return websocket_error_handler('Player not in room')

        username = room.players[player_id]['data'].get('username')

        # Broadcast game action to all participants
        emit('game_action_broadcast', {
            'username': username,
            'action': data.get('action'),
            'payload': data.get('payload'),
            'timestamp': datetime.now().isoformat()
        }, room=room_code, namespace='/party-rooms')
