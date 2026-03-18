# Modular Blog Generator

A scalable, modular blog system where each page is completely self-contained with its own styling, assets, and API endpoints.

🔗 **Repository:** [github.com/Volcanex/blog-new](https://github.com/Volcanex/blog-new)

## Architecture

```
pages/
├── first-post/
│   ├── config.json      # Page metadata
│   ├── content.md       # HTML content + CSS
│   ├── api.py          # Flask API endpoints
│   └── assets/         # Page-specific assets
└── tech-setup/
    ├── config.json
    ├── content.md  
    ├── api.py
    └── assets/
        └── config-files/
            └── vscode-settings.json

output/                  # Generated static files
├── index.html          # Homepage
├── first-post.html     # Individual pages  
└── assets/             # Copied page assets
    ├── first-post/
    └── tech-setup/

shared/
├── database.py         # NoSQL database layer
└── endpoints/          # Common endpoints (optional)
```

## Key Features

- **Page Isolation**: Each page has its own CSS, HTML, and assets
- **Modular APIs**: Each page can define custom Flask endpoints
- **Endpoint Collision Detection**: Automatic detection and warnings for conflicting API routes
- **Asset Management**: Per-page assets with automatic copying
- **NoSQL Database**: File-based database with page-scoped data
- **Scalable**: Ready for microservice extraction
- **AI-Optimized**: Designed for rapid AI-assisted development

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Compile the blog:**
   ```bash
   python3 compile.py
   ```

3. **Serve static files only:**
   ```bash
   python3 server.py
   ```

4. **Serve with API endpoints:**
   ```bash
   python3 flask_server.py
   ```

5. **Test the APIs:**
   ```bash
   python3 test_api.py
   ```

## Creating a New Page

1. **Create page directory:**
   ```bash
   mkdir pages/my-new-post
   mkdir pages/my-new-post/assets
   ```

2. **Create config.json:**
   ```json
   {
       "title": "My New Post",
       "slug": "my-new-post", 
       "date": "2025-01-15",
       "description": "Description of my post",
       "categories": ["category1", "category2"]
   }
   ```

3. **Create content.md:**
   ```html
   <style>
   body { font-family: Arial, sans-serif; }
   </style>

   <html>
   <h1>My New Post</h1>
   <p>Content goes here...</p>
   </html>
   ```

4. **Create api.py (optional):**
   ```python
   from flask import Blueprint, jsonify
   from shared.database import get_db

   bp = Blueprint('my_new_post', __name__, url_prefix='/api/my-new-post')

   @bp.route('/my-hello')  # Use page-specific route names
   def hello():
       return jsonify({'message': 'Hello from my new post!'})
   ```

5. **Add assets** (optional):
   Add any images, files, etc. to `pages/my-new-post/assets/`

6. **Compile and serve:**
   ```bash
   python3 compile.py
   python3 flask_server.py
   ```

## API Endpoints

### Global Endpoints
- `GET /api/health` - Server health check
- `GET /api/pages` - List all pages
- `GET /api/server-details` - Get server hardware stats (CPU, RAM, GPU)

### Publishing API (New)
Programmatic post management with automatic compile.py triggering:

- `POST /api/posts/create` - Create a new blog post
  ```json
  {
    "slug": "my-new-post",
    "title": "My New Post",
    "content": "# Markdown content",
    "description": "Optional description",
    "date": "2026-01-21",
    "categories": ["tech", "blog"],
    "auto_compile": true
  }
  ```

- `PUT /api/posts/update/<slug>` - Update existing post (partial updates supported)
  ```json
  {
    "title": "Updated Title",
    "content": "Updated content",
    "description": "New description",
    "categories": ["updated"],
    "auto_compile": true
  }
  ```

- `DELETE /api/posts/delete/<slug>` - Delete a post
  - Query param: `auto_compile=true` (default)

- `POST /api/posts/compile` - Manually trigger compile.py
  - Protected by compile lock to prevent concurrent executions
  - 60-second timeout

### Page-specific Endpoints
Each page defines its own endpoints at `/api/{page-slug}/...`

### Assets
- Static assets: `/assets/{page-slug}/{asset-path}`
- Example: `/assets/travel-memories/photos/tokyo.jpg`

## Database

The system uses a simple file-based NoSQL database:
- Data stored in `data/{page-slug}/{collection}.json`
- Page-scoped collections prevent conflicts
- Thread-safe operations

Example usage in page APIs:
```python
from shared.database import get_db

db = get_db()
comments = db.get_page_data('my-page', 'comments', [])
db.set_page_data('my-page', 'comments', comments)
```

## Deployment

### Quick Deployment
```bash
./full-deploy.sh  # Complete build and deployment
./deploy.sh      # Deploy only (after compile)
```

### Manual Deployment
- Compile static files with `compile.py`
- Deploy `output/` directory to any static host
- Run Flask API on server for dynamic features

### Future (Scalable)
- Extract page APIs to separate microservices
- Use real NoSQL database (Firestore, MongoDB)
- CDN for static assets
- Container orchestration

## Files

- `compile.py` - Modular compiler with extensionless URL support
- `flask_server.py` - Flask server with auto-registered APIs and collision detection
- `shared/database.py` - NoSQL database layer
- `deploy.sh` - Deployment script with collision warnings
- `full-deploy.sh` - Complete build and deployment pipeline
- `test_api.py` - API testing script
- `server.py` - Simple static file server
- `prompt.md` - Complete development guide for AI assistants

## Endpoint Collision Prevention

The system automatically detects conflicting API routes and displays warnings:

- Routes are checked during Flask server startup
- Deployment scripts show collision warnings
- **Best Practice**: Use page-specific route prefixes (e.g., `/my-page-data` instead of `/data`)
- See `prompt.md` for detailed naming conventions