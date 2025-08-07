"""
API endpoints for the travel-memories page.
"""

from flask import Blueprint, jsonify, request
from shared.database import get_db

bp = Blueprint('travel_memories', __name__, url_prefix='/api/travel-memories')

@bp.route('/locations')
def get_locations():
    """Get the locations visited during the Japan trip"""
    locations = [
        {
            'city': 'Tokyo',
            'highlights': ['Tsukiji Market', 'Shibuya', 'bustling streets'],
            'experience': 'Urban adventure'
        },
        {
            'city': 'Kyoto', 
            'highlights': ['serene temples', 'traditional architecture'],
            'experience': 'Cultural immersion'
        },
        {
            'city': 'Hakone',
            'highlights': ['traditional ryokan', 'hot springs'],
            'experience': 'Relaxation and tradition'
        }
    ]
    return jsonify({'locations': locations})

@bp.route('/travel-tips', methods=['GET', 'POST'])
def travel_tips():
    """Handle travel tips from visitors"""
    db = get_db()
    
    if request.method == 'GET':
        tips = db.get_page_data('travel-memories', 'travel_tips', [])
        return jsonify({'tips': tips})
    
    elif request.method == 'POST':
        data = request.get_json()
        if not data or 'tip' not in data:
            return jsonify({'error': 'Travel tip required'}), 400
        
        tips = db.get_page_data('travel-memories', 'travel_tips', [])
        
        new_tip = {
            'id': len(tips) + 1,
            'tip': data['tip'],
            'location': data.get('location', ''),
            'category': data.get('category', 'general'),
            'submitted_by': data.get('submitted_by', 'anonymous')
        }
        tips.append(new_tip)
        
        db.set_page_data('travel-memories', 'travel_tips', tips)
        
        return jsonify({'success': True, 'tip': new_tip})

@bp.route('/photo-gallery')
def photo_gallery():
    """Get list of photos (placeholder - would integrate with assets)"""
    # In a real implementation, this would scan the assets directory
    # for images and return metadata
    photos = [
        {'filename': 'tokyo-street.jpg', 'caption': 'Busy street in Shibuya'},
        {'filename': 'ryokan-garden.jpg', 'caption': 'Beautiful garden at the ryokan'},
        {'filename': 'kyoto-temple.jpg', 'caption': 'Ancient temple in Kyoto'}
    ]
    return jsonify({'photos': photos})