"""
API endpoints for the first-post page.
Each page can define its own Flask routes here.
"""

from flask import Blueprint, jsonify, request
from shared.database import get_db

# Create a blueprint for this page's routes
bp = Blueprint('first_post', __name__, url_prefix='/api/first-post')

@bp.route('/hello')
def hello():
    """Simple hello endpoint for this page"""
    return jsonify({
        'message': 'Hello from first-post!',
        'page': 'first-post'
    })

@bp.route('/comments', methods=['GET', 'POST'])
def comments():
    """Handle comments for this post"""
    db = get_db()
    
    if request.method == 'GET':
        # Get comments for this page
        comments = db.get_page_data('first-post', 'comments', [])
        return jsonify({'comments': comments})
    
    elif request.method == 'POST':
        # Add a new comment
        data = request.get_json()
        if not data or 'comment' not in data:
            return jsonify({'error': 'Comment required'}), 400
        
        # Get existing comments
        comments = db.get_page_data('first-post', 'comments', [])
        
        # Add new comment (in real app, you'd sanitize and validate)
        new_comment = {
            'id': len(comments) + 1,
            'comment': data['comment'],
            'timestamp': data.get('timestamp')
        }
        comments.append(new_comment)
        
        # Save back to database
        db.set_page_data('first-post', 'comments', comments)
        
        return jsonify({'success': True, 'comment': new_comment})