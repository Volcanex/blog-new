# 📝 Adding New Pages to the Modular Blog

This guide covers everything you need to know to add new pages, use APIs, and work with the database in your modular blog system.

## 🗂️ Directory Structure Overview

Each page is completely self-contained in its own directory:

```
pages/
└── your-page-name/
    ├── config.json      # Page metadata (required)
    ├── content.md       # HTML content + CSS (required)
    ├── api.py          # Flask API endpoints (optional)
    └── assets/         # Page-specific assets (optional)
        ├── images/
        ├── documents/
        └── any-file.ext
```

## 🚀 Step-by-Step: Adding a New Page

### Step 1: Create the Page Directory

```bash
mkdir -p pages/my-new-page/assets
```

### Step 2: Create `config.json`

This file contains all the page metadata:

```json
{
    "title": "My New Page Title",
    "slug": "my-new-page",
    "date": "2025-01-15",
    "description": "A brief description of what this page is about",
    "categories": ["category1", "category2", "tag"]
}
```

**Fields explained:**
- `title`: Display title (shown in browser tab and homepage)
- `slug`: URL-friendly name (must match directory name)
- `date`: Publication date (YYYY-MM-DD format, used for sorting)
- `description`: Brief summary (shown on homepage)
- `categories`: Array of tags/categories for organization

### Step 3: Create `content.md`

This contains your page's HTML and CSS. The format is:

```html
<style>
/* Your page-specific CSS goes here */
body {
    font-family: 'Georgia', serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f5f5f5;
}

h1 {
    color: #2c3e50;
    border-bottom: 3px solid #3498db;
    padding-bottom: 10px;
}

.highlight {
    background-color: #f1c40f;
    padding: 2px 6px;
    border-radius: 4px;
}

.custom-section {
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin: 20px 0;
}
</style>

<html>
<!-- Your HTML content goes here -->
<div class="meta">Published on January 15, 2025 | Categories: category1, category2</div>

<h1>My New Page Title</h1>

<p>Welcome to my new page! This content is <span class="highlight">completely self-contained</span> with its own styling.</p>

<div class="custom-section">
    <h2>Custom Section</h2>
    <p>This section has its own styling defined in the CSS above.</p>
    
    <ul>
        <li>Each page has its own CSS</li>
        <li>No shared dependencies</li>
        <li>Complete design freedom</li>
    </ul>
</div>

<p>You can reference assets like this:</p>
<img src="/assets/my-new-page/images/sample.jpg" alt="Sample image">

<p>Or link to files:</p>
<a href="/assets/my-new-page/documents/report.pdf">Download Report</a>
</html>
```

**Important notes:**
- CSS must be in `<style>` tags at the top
- HTML content goes in `<html>` tags
- Asset URLs follow pattern: `/assets/{page-slug}/{file-path}`
- Each page is completely isolated - no shared CSS or dependencies

### Step 4: Create API Endpoints (Optional)

Create `api.py` to add custom endpoints for your page:

```python
"""
API endpoints for my-new-page.
Each page can define its own Flask routes here.
"""

from flask import Blueprint, jsonify, request, abort
from shared.database import get_db
from datetime import datetime

# Create a blueprint for this page's routes
bp = Blueprint('my_new_page', __name__, url_prefix='/api/my-new-page')

@bp.route('/hello')
def hello():
    """Simple hello endpoint"""
    return jsonify({
        'message': 'Hello from my new page!',
        'page': 'my-new-page',
        'timestamp': datetime.now().isoformat()
    })

@bp.route('/info')
def page_info():
    """Get information about this page"""
    return jsonify({
        'page_name': 'my-new-page',
        'features': [
            'Custom API endpoints',
            'Database integration',
            'Asset management',
            'Self-contained styling'
        ],
        'endpoints': [
            '/api/my-new-page/hello',
            '/api/my-new-page/info',
            '/api/my-new-page/comments',
            '/api/my-new-page/data'
        ]
    })

# Database integration examples
@bp.route('/comments', methods=['GET', 'POST'])
def comments():
    """Handle comments for this page"""
    db = get_db()
    
    if request.method == 'GET':
        # Get all comments for this page
        comments = db.get_page_data('my-new-page', 'comments', [])
        return jsonify({
            'comments': comments,
            'total': len(comments)
        })
    
    elif request.method == 'POST':
        # Add a new comment
        data = request.get_json()
        
        # Validate input
        if not data or 'comment' not in data:
            return jsonify({'error': 'Comment text is required'}), 400
        
        if len(data['comment'].strip()) == 0:
            return jsonify({'error': 'Comment cannot be empty'}), 400
        
        # Get existing comments
        comments = db.get_page_data('my-new-page', 'comments', [])
        
        # Create new comment
        new_comment = {
            'id': len(comments) + 1,
            'comment': data['comment'].strip(),
            'author': data.get('author', 'Anonymous'),
            'timestamp': datetime.now().isoformat(),
            'likes': 0
        }
        
        # Add to comments list
        comments.append(new_comment)
        
        # Save back to database
        success = db.set_page_data('my-new-page', 'comments', comments)
        
        if success:
            return jsonify({
                'success': True,
                'comment': new_comment,
                'total_comments': len(comments)
            }), 201
        else:
            return jsonify({'error': 'Failed to save comment'}), 500

@bp.route('/comments/<int:comment_id>/like', methods=['POST'])
def like_comment(comment_id):
    """Like a specific comment"""
    db = get_db()
    comments = db.get_page_data('my-new-page', 'comments', [])
    
    # Find the comment
    comment = None
    for c in comments:
        if c.get('id') == comment_id:
            comment = c
            break
    
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404
    
    # Increment likes
    comment['likes'] = comment.get('likes', 0) + 1
    
    # Save back to database
    success = db.set_page_data('my-new-page', 'comments', comments)
    
    if success:
        return jsonify({
            'success': True,
            'comment_id': comment_id,
            'new_likes': comment['likes']
        })
    else:
        return jsonify({'error': 'Failed to update likes'}), 500

@bp.route('/data', methods=['GET', 'POST', 'DELETE'])
def custom_data():
    """Handle custom data for this page"""
    db = get_db()
    
    if request.method == 'GET':
        # Get custom data
        data = db.get_page_data('my-new-page', 'custom_data', {})
        return jsonify({
            'data': data,
            'keys': list(data.keys()) if isinstance(data, dict) else []
        })
    
    elif request.method == 'POST':
        # Set custom data
        new_data = request.get_json()
        
        if not new_data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Get existing data
        existing_data = db.get_page_data('my-new-page', 'custom_data', {})
        
        # Merge with new data
        if isinstance(existing_data, dict) and isinstance(new_data, dict):
            existing_data.update(new_data)
        else:
            existing_data = new_data
        
        # Save back to database
        success = db.set_page_data('my-new-page', 'custom_data', existing_data)
        
        if success:
            return jsonify({
                'success': True,
                'data': existing_data
            })
        else:
            return jsonify({'error': 'Failed to save data'}), 500
    
    elif request.method == 'DELETE':
        # Clear all custom data
        success = db.delete_page_data('my-new-page', 'custom_data')
        
        if success:
            return jsonify({'success': True, 'message': 'Data cleared'})
        else:
            return jsonify({'error': 'Failed to delete data'}), 500

# File/Asset related endpoints
@bp.route('/assets')
def list_assets():
    """List all assets for this page"""
    import os
    from pathlib import Path
    
    assets_dir = Path('pages/my-new-page/assets')
    
    if not assets_dir.exists():
        return jsonify({'assets': [], 'total': 0})
    
    assets = []
    for file_path in assets_dir.rglob('*'):
        if file_path.is_file():
            relative_path = str(file_path.relative_to(assets_dir))
            assets.append({
                'filename': file_path.name,
                'path': relative_path,
                'url': f'/assets/my-new-page/{relative_path}',
                'size': file_path.stat().st_size,
                'type': file_path.suffix.lower()
            })
    
    return jsonify({
        'assets': assets,
        'total': len(assets),
        'base_url': '/assets/my-new-page/'
    })
```

### Step 5: Add Assets (Optional)

Put any files your page needs in the `assets/` directory:

```bash
# Example asset structure
pages/my-new-page/assets/
├── images/
│   ├── header-image.jpg
│   └── gallery/
│       ├── photo1.jpg
│       └── photo2.jpg
├── documents/
│   ├── report.pdf
│   └── data.csv
└── config/
    └── settings.json
```

Assets are automatically copied to `output/assets/my-new-page/` during compilation.

## 🗄️ Database Usage Guide

The blog uses a simple file-based NoSQL database. Here's how to use it:

### Basic Database Operations

```python
from shared.database import get_db

# Get database instance
db = get_db()

# Store data for your page
db.set_page_data('my-new-page', 'collection_name', data)

# Retrieve data for your page
data = db.get_page_data('my-new-page', 'collection_name', default_value)

# Append to a list collection
db.append_to_page_collection('my-new-page', 'items', new_item)

# Delete a collection
db.delete_page_data('my-new-page', 'collection_name')
```

### Database Structure

Data is stored in `data/{page-slug}/{collection}.json`:

```
data/
├── my-new-page/
│   ├── comments.json
│   ├── custom_data.json
│   └── settings.json
├── shared/
│   └── global_config.json
└── another-page/
    └── posts.json
```

### Common Data Patterns

**1. Comments System:**
```python
# Get comments
comments = db.get_page_data('my-page', 'comments', [])

# Add comment
new_comment = {
    'id': len(comments) + 1,
    'text': 'Comment text',
    'author': 'Author name',
    'timestamp': datetime.now().isoformat()
}
comments.append(new_comment)
db.set_page_data('my-page', 'comments', comments)
```

**2. Page Views Counter:**
```python
# Increment view count
views = db.get_page_data('my-page', 'views', 0)
db.set_page_data('my-page', 'views', views + 1)
```

**3. User Settings:**
```python
# Store user preferences
settings = {
    'theme': 'dark',
    'notifications': True,
    'language': 'en'
}
db.set_page_data('my-page', 'user_settings', settings)
```

**4. Form Submissions:**
```python
# Store form data
submissions = db.get_page_data('my-page', 'form_submissions', [])
new_submission = {
    'id': len(submissions) + 1,
    'name': data['name'],
    'email': data['email'],
    'message': data['message'],
    'timestamp': datetime.now().isoformat()
}
db.append_to_page_collection('my-page', 'form_submissions', new_submission)
```

## 🔌 API Endpoint Patterns

### URL Structure
- Global endpoints: `/api/health`, `/api/pages`
- Page endpoints: `/api/{page-slug}/{endpoint}`
- Assets: `/assets/{page-slug}/{file-path}`

### Common Endpoint Types

**1. Information Endpoints:**
```python
@bp.route('/info')
def get_info():
    return jsonify({'page': 'my-page', 'version': '1.0'})
```

**2. CRUD Operations:**
```python
@bp.route('/items', methods=['GET', 'POST'])
@bp.route('/items/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_items(item_id=None):
    # Handle different HTTP methods
    pass
```

**3. File Operations:**
```python
@bp.route('/upload', methods=['POST'])
def upload_file():
    # Handle file uploads to assets directory
    pass
```

## 🚀 Deployment Process

### After Creating Your Page

1. **Compile the blog:**
   ```bash
   ./compile.sh
   ```

2. **Deploy with APIs:**
   ```bash
   ./deploy.sh
   ```

3. **Or do both at once:**
   ```bash
   ./full-deploy.sh
   ```

### Your page will be available at:
- **Static page:** `http://localhost:5000/my-new-page.html`
- **API endpoints:** `http://localhost:5000/api/my-new-page/*`
- **Assets:** `http://localhost:5000/assets/my-new-page/*`

## 🧪 Testing Your Page

### Test API Endpoints

Create a simple test script or use curl:

```bash
# Test basic endpoint
curl http://localhost:5000/api/my-new-page/hello

# Test POST endpoint
curl -X POST http://localhost:5000/api/my-new-page/comments \
  -H "Content-Type: application/json" \
  -d '{"comment": "Test comment", "author": "Test User"}'

# Test GET with data
curl http://localhost:5000/api/my-new-page/comments
```

### Test in Browser

1. Visit `http://localhost:5000/my-new-page.html`
2. Check that assets load correctly
3. Test any interactive features
4. Verify styling is applied correctly

## 💡 Best Practices

### 1. Page Naming
- Use kebab-case for directory names: `my-new-page`
- Keep slugs short and descriptive
- Match directory name with slug in config.json

### 2. CSS Organization
- Keep all CSS at the top in `<style>` tags
- Use specific class names to avoid conflicts
- Test styling in isolation

### 3. API Design
- Use RESTful endpoints when possible
- Include proper error handling
- Validate all input data
- Use appropriate HTTP status codes

### 4. Database Usage
- Use descriptive collection names
- Include timestamps in records
- Handle missing data gracefully
- Keep data structures simple

### 5. Assets Management
- Organize assets in subdirectories
- Use descriptive filenames
- Optimize images for web
- Reference assets with correct paths

## 🔍 Troubleshooting

### Common Issues

**1. Page not showing up:**
- Check that `config.json` and `content.md` exist
- Verify JSON syntax in config.json
- Run `./compile.sh` to regenerate

**2. API endpoints not working:**
- Check that `api.py` has a `bp` blueprint
- Verify Flask server is running
- Check logs: `tail -f logs/flask_server.log`

**3. Assets not loading:**
- Verify asset paths in HTML: `/assets/{page-slug}/{file}`
- Check that assets exist in `pages/{page}/assets/`
- Recompile to copy assets: `./compile.sh`

**4. Database errors:**
- Check file permissions in `data/` directory
- Verify JSON syntax if editing files manually
- Use database methods, don't edit files directly

### Getting Help

- Check `README.md` for general setup
- Look at existing pages for examples
- Review `shared/database.py` for database methods
- Check Flask server logs for API errors

## 📋 Quick Reference

### File Requirements
- `config.json` ✅ Required
- `content.md` ✅ Required  
- `api.py` ⚪ Optional
- `assets/` ⚪ Optional

### Key URLs
- Static: `/{slug}.html`
- API: `/api/{slug}/endpoint`
- Assets: `/assets/{slug}/file`
- Health: `/api/health`

### Essential Commands
```bash
./setup-venv.sh      # One-time setup
./full-deploy.sh     # Complete deployment
./compile.sh         # Just compile
./deploy.sh          # Just deploy
./stop_server.sh     # Stop server
```

This system gives you complete freedom to create unique, self-contained pages while providing powerful API and database capabilities when needed!