# AI Prompt: Creating New Pages for Modular Blog System

This document provides everything an AI needs to create new pages for this modular blog system. Each page is completely self-contained with its own styling, assets, and API endpoints.

## System Overview

This is a modular blog system where each page operates independently. The architecture follows this structure:

```
pages/
├── {page-slug}/
│   ├── config.json      # Page metadata and configuration
│   ├── content.md       # HTML content + CSS styling
│   ├── api.py          # Custom Flask API endpoints (optional)
│   └── assets/         # Page-specific resources (optional)
│       ├── images/
│       ├── documents/
│       └── data/
```

## Database System

The blog uses a thread-safe, file-based NoSQL database located in `shared/database.py`. Key features:

- **Page-scoped data**: Each page has its own data namespace to prevent conflicts
- **JSON storage**: Data stored in `data/{page-slug}/{collection}.json`
- **Thread-safe**: Uses locks for concurrent access
- **Simple API**: Similar to Firestore/MongoDB

### Database Usage Examples

```python
from shared.database import get_db

# Get database instance
db = get_db()

# Page-scoped data (recommended for page-specific data)
comments = db.get_page_data('my-page', 'comments', [])
db.set_page_data('my-page', 'comments', comments)
db.append_to_page_collection('my-page', 'comments', new_comment)

# Shared data (for global application data)
site_config = db.get_shared_data('config', {})
db.set_shared_data('config', site_config)

# List operations
collections = db.list_page_collections('my-page')
all_pages = db.list_pages()
```

## Step-by-Step Page Creation Guide

### 1. Create Directory Structure

```bash
mkdir pages/my-new-page
mkdir pages/my-new-page/assets
```

### 2. Create config.json

The configuration file defines page metadata:

```json
{
    "title": "My New Page Title",
    "slug": "my-new-page",
    "date": "2025-01-15",
    "description": "A brief description of what this page is about",
    "categories": ["category1", "category2"]
}
```

**Required fields:**
- `title`: Display name of the page
- `slug`: URL-friendly identifier (must match directory name)
- `date`: Publication date (YYYY-MM-DD format)

**Optional fields:**
- `description`: Brief page description for homepage
- `categories`: Array of category strings for organization

### 3. Create content.md

This file contains both CSS styling and HTML content:

```html
<style>
/* Page-specific CSS goes here */
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
    line-height: 1.6;
    color: #333;
    background: #fff;
    margin: 0;
    padding: 24px;
    max-width: 800px;
    margin: 0 auto;
}

h1 {
    color: #2c3e50;
    font-size: 2rem;
    margin-bottom: 1rem;
}

.highlight {
    background: #f39c12;
    padding: 2px 6px;
    border-radius: 4px;
    color: white;
}

/* Add more styles as needed */
</style>

<html>
<div class="container">
    <h1>My New Page Title</h1>
    
    <p>This is the main content of my page. I can use any HTML and it will be styled by the CSS above.</p>
    
    <p>I can reference assets like images: <code>/assets/my-new-page/images/example.jpg</code></p>
    
    <div class="highlight">This is a highlighted section</div>
    
    <h2>Subsection</h2>
    <p>More content here...</p>
</div>
</html>
```

**Important Notes:**
- CSS must be wrapped in `<style></style>` tags
- HTML content must be wrapped in `<html></html>` tags
- Assets are accessed via `/assets/{page-slug}/path/to/file`

### 4. Create api.py (Optional)

If your page needs dynamic functionality, create API endpoints:

```python
"""
API endpoints for my-new-page
"""

from flask import Blueprint, jsonify, request
from shared.database import get_db
from datetime import datetime

# Create blueprint with page-specific URL prefix
bp = Blueprint('my_new_page', __name__, url_prefix='/api/my-new-page')

@bp.route('/hello')
def hello():
    """Simple hello endpoint"""
    return jsonify({
        'message': 'Hello from my new page!',
        'page': 'my-new-page',
        'timestamp': datetime.now().isoformat()
    })

@bp.route('/data', methods=['GET', 'POST'])
def handle_data():
    """Example of database integration"""
    db = get_db()
    
    if request.method == 'GET':
        # Get page-specific data
        data = db.get_page_data('my-new-page', 'user_data', [])
        return jsonify({
            'data': data,
            'count': len(data)
        })
    
    elif request.method == 'POST':
        # Save new data
        new_entry = request.get_json()
        if not new_entry:
            return jsonify({'error': 'JSON data required'}), 400
        
        # Add timestamp and ID
        new_entry['id'] = datetime.now().timestamp()
        new_entry['timestamp'] = datetime.now().isoformat()
        
        # Append to collection
        success = db.append_to_page_collection('my-new-page', 'user_data', new_entry)
        
        if success:
            return jsonify({'success': True, 'entry': new_entry}), 201
        else:
            return jsonify({'error': 'Failed to save data'}), 500

@bp.route('/stats')
def page_stats():
    """Get page statistics"""
    db = get_db()
    
    # Increment page views
    views = db.get_page_data('my-new-page', 'views', 0)
    db.set_page_data('my-new-page', 'views', views + 1)
    
    # Get other stats
    data_count = len(db.get_page_data('my-new-page', 'user_data', []))
    
    return jsonify({
        'page': 'my-new-page',
        'views': views + 1,
        'data_entries': data_count,
        'last_updated': datetime.now().isoformat()
    })
```

**API Guidelines:**
- Use descriptive blueprint names (avoid conflicts)
- URL prefix should be `/api/{page-slug}`
- **IMPORTANT**: Start endpoint routes with the page name to avoid collisions (e.g., `/pool-players`, `/pool-games` for pool-leaderboard page)
- Import `get_db()` from `shared.database` for data persistence
- Use page-scoped data: `db.get_page_data(page_slug, collection, default)`
- Return JSON responses with appropriate HTTP status codes
- Handle errors gracefully
- The system will warn about endpoint collisions during deployment

### 5. Add Assets (Optional)

Place any images, documents, or data files in the `assets/` directory:

```
pages/my-new-page/assets/
├── images/
│   ├── hero-banner.jpg
│   └── diagram.png
├── documents/
│   └── reference.pdf
└── data/
    └── sample.json
```

**Asset Access:**
- From HTML: `/assets/my-new-page/images/hero-banner.jpg`
- From API: Use Flask's `send_from_directory` if needed

## Build and Deploy Process

### 1. Compile the Blog

```bash
python3 compile_v2.py
```

This will:
- Generate static HTML files in `output/`
- Copy all page assets to `output/assets/{page-slug}/`
- Create homepage with page listings

### 2. Test Static Version

```bash
python3 server.py
```

Serves static files only (no API functionality).

### 3. Test with APIs

```bash
python3 flask_server.py
```

Serves static files AND automatically registers all page APIs.

### 4. Test APIs

```bash
python3 test_api.py
```

Tests all available endpoints.

## Endpoint Collision Detection

The system automatically detects and warns about conflicting API routes:

### How It Works

1. **During Flask Server Startup**: All registered routes are analyzed for conflicts
2. **Collision Detection**: Routes with identical paths and methods are flagged
3. **Warning Display**: Detailed warnings show conflicting pages and recommendations
4. **Deployment Integration**: Both `deploy.sh` and `full-deploy.sh` check for warnings

### Example Collision Warning

```
⚠️  WARNING: Route collision detected!
   Route: /api/my-page/data {'GET', 'POST'}
   Page 'page-one' conflicts with page 'page-two'
   Recommendation: Use page-specific route names
```

### Best Practices to Avoid Collisions

- **Use page-specific prefixes**: `/my-page-users` instead of `/users`
- **Include page context**: `/pool-players` instead of `/players`
- **Avoid generic names**: `/data`, `/info`, `/stats` are likely to conflict
- **Be descriptive**: `/blog-comments` instead of `/comments`

## System Endpoints

### Global Endpoints

- `GET /api/health` - Server health check
- `GET /api/pages` - List all pages with metadata

### Page Endpoints

Each page with an `api.py` file gets its own endpoints at `/api/{page-slug}/...`

### Asset Endpoints

- Static assets: `/assets/{page-slug}/{asset-path}`
- Example: `/assets/my-new-page/images/hero-banner.jpg`

## Design Guidelines

### CSS Best Practices

1. **Use modern CSS**: Flexbox, Grid, CSS variables
2. **Mobile-first**: Include responsive design
3. **Color schemes**: Choose cohesive color palettes
4. **Typography**: Use system fonts or web fonts
5. **Accessibility**: Ensure good contrast and readability

### Example Color Palettes

```css
/* Tech Theme */
:root {
    --primary: #2c3e50;    /* Dark blue */
    --secondary: #3498db;  /* Light blue */
    --accent: #e74c3c;     /* Red */
    --text: #2c3e50;       /* Dark blue */
    --background: #ecf0f1; /* Light gray */
}

/* Nature Theme */
:root {
    --primary: #27ae60;    /* Green */
    --secondary: #2ecc71;  /* Light green */
    --accent: #f39c12;     /* Orange */
    --text: #2c3e50;       /* Dark blue */
    --background: #f8f9fa; /* Off-white */
}
```

### Common CSS Patterns

```css
/* Container with max width */
.container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

/* Card design */
.card {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    padding: 24px;
    margin-bottom: 20px;
}

/* Button styles */
.button {
    background: var(--primary);
    color: white;
    padding: 12px 24px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    transition: background 0.2s;
}

.button:hover {
    background: var(--secondary);
}

/* Responsive design */
@media (max-width: 768px) {
    .container {
        padding: 16px;
    }
    
    h1 {
        font-size: 1.5rem;
    }
}
```

## Common Page Types

### Blog Post

Focus on readability, typography, and content structure.

```html
<style>
article {
    max-width: 700px;
    margin: 0 auto;
    font-family: Georgia, serif;
    line-height: 1.8;
}

.meta {
    color: #666;
    font-size: 0.9rem;
    margin-bottom: 2rem;
}

h1, h2, h3 {
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
}
</style>

<html>
<article>
    <div class="meta">Published on January 15, 2025</div>
    <h1>Blog Post Title</h1>
    <p>Content goes here...</p>
</article>
</html>
```

### Portfolio/Gallery

Emphasize visual content with grid layouts.

```html
<style>
.gallery {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    margin: 20px 0;
}

.gallery-item {
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.gallery-item img {
    width: 100%;
    height: 200px;
    object-fit: cover;
}
</style>

<html>
<div class="gallery">
    <div class="gallery-item">
        <img src="/assets/my-page/images/item1.jpg" alt="Item 1">
        <div class="description">Description</div>
    </div>
</div>
</html>
```

### Interactive Dashboard

Combine APIs with dynamic content.

```html
<style>
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin: 20px 0;
}

.stat-card {
    background: white;
    padding: 20px;
    border-radius: 8px;
    border-left: 4px solid var(--primary);
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.stat-number {
    font-size: 2rem;
    font-weight: bold;
    color: var(--primary);
}
</style>

<html>
<div class="dashboard">
    <h1>Dashboard</h1>
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-number">42</div>
            <div>Total Users</div>
        </div>
    </div>
    <button onclick="loadData()">Refresh Data</button>
</div>

<script>
async function loadData() {
    const response = await fetch('/api/my-page/stats');
    const data = await response.json();
    // Update UI with data
}
</script>
</html>
```

## Testing Your Page

### 1. Basic Compilation Test

```bash
python3 compile_v2.py
```

Check for any errors during compilation.

### 2. Static Content Test

```bash
python3 server.py
```

Visit `http://localhost:5000/my-new-page.html` to test static content.

### 3. API Test

```bash
python3 flask_server.py
```

Test your API endpoints:
- `GET http://localhost:5000/api/my-new-page/hello`
- etc.

### 4. Asset Test

Verify assets are accessible:
- `http://localhost:5000/assets/my-new-page/images/example.jpg`

## Troubleshooting

### Common Issues

1. **Page not compiling**: Check config.json syntax and content.md structure
2. **Assets not loading**: Verify file paths and asset directory structure
3. **API not working**: Check blueprint registration and import statements
4. **Database errors**: Ensure proper error handling and page-scoped data access
5. **CSS not applying**: Verify `<style>` tags are properly closed

### Debug Steps

1. Check console output during compilation
2. Verify all required files exist
3. Test API endpoints with curl or browser dev tools
4. Check browser console for JavaScript errors
5. Inspect generated HTML files in `output/` directory

## Advanced Features

### Custom JavaScript

Add interactivity to your pages:

```html
<script>
// Fetch data from your API
async function loadComments() {
    try {
        const response = await fetch('/api/my-page/comments');
        const data = await response.json();
        displayComments(data.comments);
    } catch (error) {
        console.error('Error loading comments:', error);
    }
}

function displayComments(comments) {
    const container = document.getElementById('comments');
    container.innerHTML = comments.map(comment => 
        `<div class="comment">
            <strong>${comment.author}</strong>: ${comment.text}
            <small>${comment.timestamp}</small>
        </div>`
    ).join('');
}

// Load comments when page loads
document.addEventListener('DOMContentLoaded', loadComments);
</script>
```

### WebSocket Support

For real-time features, extend the Flask server to support WebSockets in your page's API.

### Form Handling

Create interactive forms that save to the database:

```html
<form id="contact-form">
    <input type="text" name="name" placeholder="Your Name" required>
    <textarea name="message" placeholder="Your Message" required></textarea>
    <button type="submit">Submit</button>
</form>

<script>
document.getElementById('contact-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData);
    
    const response = await fetch('/api/my-page/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    
    if (response.ok) {
        alert('Message sent successfully!');
        e.target.reset();
    } else {
        alert('Error sending message');
    }
});
</script>
```

## Recent Development Improvements

### Extensionless URLs (August 2025)
- Compiler now generates both `.html` files and `directory/index.html` for SEO-friendly URLs
- Flask server automatically handles extensionless routes (e.g., `/my-page` works alongside `/my-page.html`)
- Homepage links use clean URLs without extensions

### Enhanced Architecture Diagrams
- Improved visual representation showing Development vs Runtime aspects
- Clear separation of HTML Blueprint, API Blueprint, and Data Namespace concepts
- Better documentation of how pages work in practice

### AI-Optimized Development
- System designed specifically for AI-assisted rapid development
- Minimal coupling between components for better AI code generation
- Simple, predictable patterns that AI can easily replicate

### Database Integration
- File-based JSON storage with page-scoped namespaces
- Thread-safe operations for concurrent access
- Simple API similar to Firestore/MongoDB for familiar patterns

This system provides complete flexibility while maintaining clean separation between pages. Each page can have its own unique design, functionality, and data without affecting other pages.