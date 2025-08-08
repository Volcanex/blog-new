"""
API endpoints for the first-post page - Modular Blog Architecture Demo.
Each page can define its own Flask routes here.
"""

from flask import Blueprint, jsonify, request
from shared.database import get_db
from datetime import datetime

# Create a blueprint for this page's routes
bp = Blueprint('first_post', __name__, url_prefix='/api/first-post')

@bp.route('/hello')
def hello():
    """Simple hello endpoint demonstrating page-specific APIs"""
    return jsonify({
        'message': 'Hello from the Modular Blog Architecture page!',
        'page': 'first-post',
        'architecture': 'modular',
        'timestamp': datetime.now().isoformat()
    })

@bp.route('/architecture-info')
def architecture_info():
    """Get technical details about the blog architecture"""
    return jsonify({
        'page': 'first-post',
        'architecture_type': 'modular',
        'features': {
            'self_contained_pages': True,
            'custom_api_endpoints': True,
            'per_page_assets': True,
            'isolated_styling': True,
            'nosql_database': True
        },
        'technologies': [
            'Python 3.11+',
            'Flask',
            'File-based NoSQL',
            'Modern CSS Grid',
            'Responsive Design'
        ],
        'color_palette': [
            '#c4d6b0',  # Light green
            '#477998',  # Blue
            '#291f1e',  # Dark brown
            '#f64740',  # Red
            '#a3333d'   # Dark red
        ],
        'scalability_features': [
            'Microservice extraction ready',
            'CDN optimization',
            'Database sharding capability',
            'Independent deployments'
        ],
        'endpoints_demo': [
            '/api/first-post/hello',
            '/api/first-post/architecture-info',
            '/api/first-post/comments'
        ]
    })

@bp.route('/comments', methods=['GET', 'POST'])
def comments():
    """Comment system demonstrating database integration"""
    db = get_db()
    
    if request.method == 'GET':
        # Get comments for this page
        comments = db.get_page_data('first-post', 'comments', [])
        return jsonify({
            'comments': comments,
            'total': len(comments),
            'page': 'first-post'
        })
    
    elif request.method == 'POST':
        # Add a new comment
        data = request.get_json()
        if not data or 'comment' not in data:
            return jsonify({'error': 'Comment text is required'}), 400
        
        if len(data['comment'].strip()) == 0:
            return jsonify({'error': 'Comment cannot be empty'}), 400
        
        # Get existing comments
        comments = db.get_page_data('first-post', 'comments', [])
        
        # Create new comment with enhanced structure
        new_comment = {
            'id': len(comments) + 1,
            'comment': data['comment'].strip(),
            'author': data.get('author', 'Anonymous Architecture Enthusiast'),
            'timestamp': datetime.now().isoformat(),
            'page': 'first-post',
            'likes': 0,
            'topic': 'modular-architecture'
        }
        comments.append(new_comment)
        
        # Save back to database
        success = db.set_page_data('first-post', 'comments', comments)
        
        if success:
            return jsonify({
                'success': True,
                'comment': new_comment,
                'total_comments': len(comments)
            }), 201
        else:
            return jsonify({'error': 'Failed to save comment'}), 500

@bp.route('/page-stats')
def page_stats():
    """Get statistics about this page"""
    db = get_db()
    
    # Get page views (increment on each call)
    views = db.get_page_data('first-post', 'views', 0)
    db.set_page_data('first-post', 'views', views + 1)
    
    # Get comment count
    comments = db.get_page_data('first-post', 'comments', [])
    
    return jsonify({
        'page': 'first-post',
        'views': views + 1,
        'total_comments': len(comments),
        'last_updated': '2025-01-15',
        'categories': ['architecture', 'web-development', 'technical'],
        'reading_time_estimate': '8 minutes',
        'architecture_complexity': 'Advanced'
    })