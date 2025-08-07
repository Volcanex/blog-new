"""
API endpoints for the tech-setup page.
"""

from flask import Blueprint, jsonify, request
from shared.database import get_db

bp = Blueprint('tech_setup', __name__, url_prefix='/api/tech-setup')

@bp.route('/tools')
def get_tools():
    """Get the list of development tools"""
    tools = {
        'editor': 'VS Code',
        'version_control': 'Git with GitHub',
        'terminal': 'Zsh with Oh My Zsh',
        'language': 'Python 3.11+',
        'containerization': 'Docker',
        'package_manager': ['pip', 'npm']
    }
    return jsonify({'tools': tools})

@bp.route('/workflow')
def get_workflow():
    """Get the development workflow steps"""
    workflow = [
        'Planning and design',
        'Setting up the project structure', 
        'Writing code with tests',
        'Code review and refactoring',
        'Deployment and monitoring'
    ]
    return jsonify({'workflow': workflow})

@bp.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    """Handle tool recommendations from visitors"""
    db = get_db()
    
    if request.method == 'GET':
        recommendations = db.get_page_data('tech-setup', 'recommendations', [])
        return jsonify({'recommendations': recommendations})
    
    elif request.method == 'POST':
        data = request.get_json()
        if not data or 'tool' not in data:
            return jsonify({'error': 'Tool name required'}), 400
        
        recommendations = db.get_page_data('tech-setup', 'recommendations', [])
        
        new_rec = {
            'id': len(recommendations) + 1,
            'tool': data['tool'],
            'category': data.get('category', 'other'),
            'description': data.get('description', ''),
            'submitted_by': data.get('submitted_by', 'anonymous')
        }
        recommendations.append(new_rec)
        
        db.set_page_data('tech-setup', 'recommendations', recommendations)
        
        return jsonify({'success': True, 'recommendation': new_rec})