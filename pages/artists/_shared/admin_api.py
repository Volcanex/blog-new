"""
Shared admin API endpoints for all artist sites.
These endpoints handle common functionality like file uploads, page editing, etc.
"""

import os
import json
import shutil
import socket
import subprocess
from pathlib import Path
from flask import Blueprint, jsonify, request, abort, send_file, Response, stream_with_context
from werkzeug.utils import secure_filename
import sys

# Add parent directory to path to import auth
sys.path.insert(0, str(Path(__file__).parent))
from auth import require_artist_auth, get_authenticated_artist, get_all_artists

bp = Blueprint('artist_admin', __name__, url_prefix='/api/adze')

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}
MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024  # 2GB

# Only block files that could be dangerous on a server
BLOCKED_EXTENSIONS = {'exe', 'bat', 'cmd', 'sh', 'php', 'py', 'rb', 'pl', 'cgi', 'jsp', 'asp', 'aspx', 'htaccess'}


def allowed_file(filename, allowed_extensions=None):
    """Check file is not a blocked type. All other extensions are allowed."""
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext not in BLOCKED_EXTENSIONS


def get_artist_path(artist_slug):
    """Get the path to an artist's directory"""
    return Path(f'pages/artists/{artist_slug}')


def get_page_path(artist_slug, page_slug):
    """Get the path to a specific page within an artist's directory"""
    return get_artist_path(artist_slug) / page_slug


# ── Dashboard ──────────────────────────────────────────────────────────────

@bp.route('/dashboard')
def dashboard():
    """Serve the admin dashboard HTML"""
    dashboard_path = Path(__file__).parent / 'dashboard.html'

    if not dashboard_path.exists():
        return jsonify({'error': 'Dashboard template not found'}), 404

    return send_file(dashboard_path)


@bp.route('/logo.png')
def serve_logo():
    """Serve the Adze Studio logo"""
    logo_path = Path(__file__).parent / 'adze-logo.png'
    if not logo_path.exists():
        abort(404)
    return send_file(logo_path, mimetype='image/png')

@bp.route('/favicon.png')
def serve_favicon():
    """Serve the Adze Studio favicon"""
    fav_path = Path(__file__).parent / 'adze-favicon.png'
    if not fav_path.exists():
        abort(404)
    return send_file(fav_path, mimetype='image/png')


# ── List Pages ─────────────────────────────────────────────────────────────

@bp.route('/list-pages', methods=['GET'])
def list_pages():
    """
    List all pages for an artist.
    Requires X-Artist-Slug and X-Admin-Token headers.
    """
    artist_slug = get_authenticated_artist()

    if not artist_slug:
        abort(401, description='Authentication required')

    artist_path = get_artist_path(artist_slug)

    if not artist_path.exists():
        return jsonify({'error': 'Artist not found'}), 404

    pages = []

    for item in artist_path.iterdir():
        if item.is_dir():
            config_file = item / 'config.json'
            content_file = item / 'content.md'

            if config_file.exists() and content_file.exists():
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        config = json.load(f)

                    pages.append({
                        'slug': item.name,
                        'title': config.get('title', item.name),
                        'path': str(item.relative_to('pages')),
                        'config': config
                    })
                except (json.JSONDecodeError, IOError):
                    continue

    return jsonify({
        'artist': artist_slug,
        'pages': pages
    })


# ── Get Page Content ───────────────────────────────────────────────────────

@bp.route('/get-page-content', methods=['GET'])
def get_page_content():
    """
    Get the content of a specific page.
    Query params: page_slug
    Headers: X-Artist-Slug, X-Admin-Token
    """
    artist_slug = get_authenticated_artist()

    if not artist_slug:
        abort(401, description='Authentication required')

    page_slug = request.args.get('page_slug')

    if not page_slug:
        return jsonify({'error': 'page_slug parameter required'}), 400

    page_path = get_page_path(artist_slug, page_slug)
    config_file = page_path / 'config.json'
    content_file = page_path / 'content.md'

    if not config_file.exists() or not content_file.exists():
        return jsonify({'error': 'Page not found'}), 404

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        with open(content_file, 'r', encoding='utf-8') as f:
            content = f.read()

        return jsonify({
            'slug': page_slug,
            'config': config,
            'content': content
        })

    except (json.JSONDecodeError, IOError) as e:
        return jsonify({'error': f'Error reading page: {str(e)}'}), 500


# ── Edit Page ──────────────────────────────────────────────────────────────

@bp.route('/edit-page', methods=['POST'])
def edit_page():
    """
    Edit a page's content and/or config.
    JSON body: {page_slug, content?, config?}
    Headers: X-Artist-Slug, X-Admin-Token
    """
    artist_slug = get_authenticated_artist()

    if not artist_slug:
        abort(401, description='Authentication required')

    data = request.get_json()

    if not data or 'page_slug' not in data:
        return jsonify({'error': 'page_slug required'}), 400

    page_slug = data['page_slug']
    page_path = get_page_path(artist_slug, page_slug)

    if not page_path.exists():
        return jsonify({'error': 'Page not found'}), 404

    try:
        # Update content.md if provided
        if 'content' in data:
            content_file = page_path / 'content.md'
            with open(content_file, 'w', encoding='utf-8') as f:
                f.write(data['content'])

        # Update config.json if provided
        if 'config' in data:
            config_file = page_path / 'config.json'
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(data['config'], f, indent=4, ensure_ascii=False)

        # Trigger compile to regenerate static files
        compile_script = Path.cwd() / 'compile.py'
        if compile_script.exists():
            import subprocess
            subprocess.run(['python3', str(compile_script)], check=False)

        return jsonify({
            'success': True,
            'message': 'Page updated successfully',
            'page_slug': page_slug
        })

    except IOError as e:
        return jsonify({'error': f'Error writing page: {str(e)}'}), 500


# ── Create Page ────────────────────────────────────────────────────────────

@bp.route('/create-page', methods=['POST'])
def create_page():
    """
    Create a new page for an artist.
    JSON body: {page_slug, title, content?, config?}
    Headers: X-Artist-Slug, X-Admin-Token
    """
    artist_slug = get_authenticated_artist()

    if not artist_slug:
        abort(401, description='Authentication required')

    data = request.get_json()

    if not data or 'page_slug' not in data or 'title' not in data:
        return jsonify({'error': 'page_slug and title required'}), 400

    page_slug = secure_filename(data['page_slug'])
    page_path = get_page_path(artist_slug, page_slug)

    if page_path.exists():
        return jsonify({'error': 'Page already exists'}), 400

    try:
        # Create page directory
        page_path.mkdir(parents=True, exist_ok=True)

        # Create config.json
        default_config = {
            'title': data['title'],
            'slug': page_slug,
            'description': data.get('description', ''),
            'categories': data.get('categories', [])
        }

        # Merge with provided config
        if 'config' in data:
            default_config.update(data['config'])

        config_file = page_path / 'config.json'
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4, ensure_ascii=False)

        # Create content.md
        default_content = data.get('content', '<html>\n<h1>New Page</h1>\n<p>Start editing...</p>\n</html>')
        content_file = page_path / 'content.md'
        with open(content_file, 'w', encoding='utf-8') as f:
            f.write(default_content)

        # Trigger compile
        compile_script = Path.cwd() / 'compile.py'
        if compile_script.exists():
            import subprocess
            subprocess.run(['python3', str(compile_script)], check=False)

        return jsonify({
            'success': True,
            'message': 'Page created successfully',
            'page_slug': page_slug,
            'path': str(page_path.relative_to('pages'))
        })

    except IOError as e:
        return jsonify({'error': f'Error creating page: {str(e)}'}), 500


# ── Upload File ────────────────────────────────────────────────────────────

@bp.route('/upload-file', methods=['POST'])
def upload_file():
    """
    Upload a file to an artist's assets directory.
    Form data: file, page_slug (optional)
    Headers: X-Artist-Slug, X-Admin-Token

    If page_slug is provided, uploads to pages/artists/{artist}/page_slug/assets/
    Otherwise uploads to pages/artists/{artist}/assets/
    """
    artist_slug = get_authenticated_artist()

    if not artist_slug:
        abort(401, description='Authentication required')

    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400

    try:
        filename = secure_filename(file.filename)
        page_slug = request.form.get('page_slug')
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

        # Determine upload directory
        if page_slug:
            upload_dir = get_page_path(artist_slug, page_slug) / 'assets'
        else:
            base_assets = get_artist_path(artist_slug) / 'assets'
            # Route images into assets/images/, fonts into assets/fonts/, rest into assets/
            if ext in ('png', 'jpg', 'jpeg', 'gif', 'webp', 'svg', 'ico', 'bmp', 'tiff'):
                upload_dir = base_assets / 'images'
            elif ext in ('woff', 'woff2', 'ttf', 'otf', 'eot'):
                upload_dir = base_assets / 'fonts'
            else:
                upload_dir = base_assets

        upload_dir.mkdir(parents=True, exist_ok=True)

        file_path = upload_dir / filename
        file.save(str(file_path))

        # Also copy to output directory so nginx can serve it immediately
        rel_path = str(file_path.relative_to(get_artist_path(artist_slug) / 'assets'))
        output_path = Path('output/artists') / artist_slug / 'assets' / rel_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(file_path), str(output_path))

        return jsonify({
            'success': True,
            'filename': filename,
            'path': str(file_path.relative_to('pages')),
            'url': f'../assets/{rel_path}'
        })

    except IOError as e:
        return jsonify({'error': f'Error uploading file: {str(e)}'}), 500


# ── Delete Page ────────────────────────────────────────────────────────────

@bp.route('/delete-page', methods=['POST'])
def delete_page():
    """
    Delete a page.
    JSON body: {page_slug}
    Headers: X-Artist-Slug, X-Admin-Token
    """
    artist_slug = get_authenticated_artist()

    if not artist_slug:
        abort(401, description='Authentication required')

    data = request.get_json()

    if not data or 'page_slug' not in data:
        return jsonify({'error': 'page_slug required'}), 400

    page_slug = data['page_slug']
    page_path = get_page_path(artist_slug, page_slug)

    if not page_path.exists():
        return jsonify({'error': 'Page not found'}), 404

    try:
        shutil.rmtree(page_path)

        # Trigger compile
        compile_script = Path.cwd() / 'compile.py'
        if compile_script.exists():
            import subprocess
            subprocess.run(['python3', str(compile_script)], check=False)

        return jsonify({
            'success': True,
            'message': 'Page deleted successfully',
            'page_slug': page_slug
        })

    except IOError as e:
        return jsonify({'error': f'Error deleting page: {str(e)}'}), 500


# ── List Assets ────────────────────────────────────────────────────────────

@bp.route('/list-assets', methods=['GET'])
def list_assets():
    """
    List all assets for an artist.
    Headers: X-Artist-Slug, X-Admin-Token
    """
    artist_slug = get_authenticated_artist()

    if not artist_slug:
        abort(401, description='Authentication required')

    artist_path = get_artist_path(artist_slug)
    assets_dir = artist_path / 'assets'

    if not assets_dir.exists():
        return jsonify({'artist': artist_slug, 'assets': []})

    assets = []
    for asset_file in assets_dir.rglob('*'):
        if asset_file.is_file():
            relative = asset_file.relative_to(assets_dir)
            ext = asset_file.suffix.lower()
            is_image = ext in ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg')
            assets.append({
                'filename': asset_file.name,
                'path': str(relative),
                'url': f'../assets/{relative}',
                'size': asset_file.stat().st_size,
                'is_image': is_image
            })

    assets.sort(key=lambda a: a['filename'])
    return jsonify({'artist': artist_slug, 'assets': assets})


# ── Artist Info ────────────────────────────────────────────────────────────

@bp.route('/artist-info', methods=['GET'])
def artist_info():
    """
    Get info about the authenticated artist.
    Headers: X-Artist-Slug, X-Admin-Token
    """
    artist_slug = get_authenticated_artist()

    if not artist_slug:
        abort(401, description='Authentication required')

    artist_path = get_artist_path(artist_slug)
    config_file = artist_path / 'config.json'

    if not config_file.exists():
        return jsonify({'error': 'Artist config not found'}), 404

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # Don't expose the admin token
        config.pop('admin_token', None)

        return jsonify({
            'slug': artist_slug,
            'config': config
        })

    except (json.JSONDecodeError, IOError) as e:
        return jsonify({'error': f'Error reading config: {str(e)}'}), 500


# ── Update Domain ─────────────────────────────────────────────────────────

@bp.route('/update-domain', methods=['POST'])
def update_domain():
    """
    Update the domain field in an artist's config.json.
    Body: { "domain": "example.com" }
    Headers: X-Artist-Slug, X-Admin-Token
    """
    artist_slug = get_authenticated_artist()
    if not artist_slug:
        abort(401, description='Authentication required')

    data = request.get_json()
    domain = (data.get('domain') or '').strip().lower()

    artist_path = get_artist_path(artist_slug)
    config_file = artist_path / 'config.json'

    if not config_file.exists():
        return jsonify({'error': 'Artist config not found'}), 404

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        config['domain'] = domain

        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

        return jsonify({'success': True, 'domain': domain})
    except (json.JSONDecodeError, IOError) as e:
        return jsonify({'error': f'Error updating config: {str(e)}'}), 500


# ── Update Site Config ────────────────────────────────────────────────────

@bp.route('/update-site-config', methods=['POST'])
def update_site_config():
    """
    Update an artist's config.json (safe fields only).
    Body: { "config": { "name": "...", "favicon": "images/icon.png", ... } }
    Headers: X-Artist-Slug, X-Admin-Token
    """
    artist_slug = get_authenticated_artist()
    if not artist_slug:
        abort(401, description='Authentication required')

    data = request.get_json()
    new_config = data.get('config', {})

    artist_path = get_artist_path(artist_slug)
    config_file = artist_path / 'config.json'

    if not config_file.exists():
        return jsonify({'error': 'Artist config not found'}), 404

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # Only allow safe fields to be updated
        allowed = ['name', 'description', 'contact_email', 'domain', 'favicon']
        for key in allowed:
            if key in new_config:
                config[key] = new_config[key]

        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

        return jsonify({'success': True})
    except (json.JSONDecodeError, IOError) as e:
        return jsonify({'error': f'Error updating config: {str(e)}'}), 500


# ── Google Fonts ──────────────────────────────────────────────────────────

@bp.route('/install-google-font', methods=['POST'])
def install_google_font():
    """
    Download a Google Font to the artist's assets/fonts/ directory.
    Body: { "family": "Roboto" }
    Downloads the TTF files for all available weights.
    """
    artist_slug = get_authenticated_artist()
    if not artist_slug:
        abort(401, description='Authentication required')

    data = request.get_json()
    family = data.get('family', '').strip()
    if not family:
        return jsonify({'error': 'Font family required'}), 400

    artist_path = get_artist_path(artist_slug)
    fonts_dir = artist_path / 'assets' / 'fonts'
    fonts_dir.mkdir(parents=True, exist_ok=True)

    # Also ensure output directory exists
    output_fonts_dir = Path('output') / 'artists' / artist_slug / 'assets' / 'fonts'
    output_fonts_dir.mkdir(parents=True, exist_ok=True)

    import urllib.request
    import re

    try:
        # Fetch the CSS from Google Fonts with a user-agent that returns TTF
        # Request common weights + italic variants
        encoded = family.replace(' ', '+')
        css_url = f"https://fonts.googleapis.com/css2?family={encoded}:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900"
        req = urllib.request.Request(css_url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            css_text = resp.read().decode('utf-8')

        # Parse out the font URLs and weights from the CSS
        # Pattern: font-weight: 400; ... src: url(https://...) format('truetype')
        blocks = re.split(r'@font-face\s*\{', css_text)
        downloaded = []

        for block in blocks[1:]:  # Skip first empty split
            weight_match = re.search(r'font-weight:\s*(\d+)', block)
            style_match = re.search(r'font-style:\s*(\w+)', block)
            url_match = re.search(r'src:\s*url\(([^)]+)\)', block)

            if not url_match:
                continue

            font_url = url_match.group(1)
            weight = weight_match.group(1) if weight_match else '400'
            style = style_match.group(1) if style_match else 'normal'

            # Determine file extension from URL
            ext = 'ttf'
            if '.woff2' in font_url:
                ext = 'woff2'
            elif '.woff' in font_url:
                ext = 'woff'

            # Sanitize family name for filename
            safe_family = re.sub(r'[^a-zA-Z0-9]', '-', family).lower().strip('-')
            style_suffix = f'-{style}' if style != 'normal' else ''
            filename = f'{safe_family}-{weight}{style_suffix}.{ext}'

            # Download the font file
            font_req = urllib.request.Request(font_url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            with urllib.request.urlopen(font_req, timeout=30) as font_resp:
                font_data = font_resp.read()

            # Save to both source and output
            (fonts_dir / filename).write_bytes(font_data)
            (output_fonts_dir / filename).write_bytes(font_data)

            downloaded.append({
                'filename': filename,
                'weight': weight,
                'style': style,
                'size': len(font_data)
            })

        if not downloaded:
            return jsonify({'error': f'Could not download any font files for "{family}"'}), 400

        return jsonify({
            'success': True,
            'family': family,
            'files': downloaded,
            'css_hint': f"@font-face {{ font-family: '{family}'; src: url('../assets/fonts/{downloaded[0]['filename']}'); }}"
        })

    except urllib.error.URLError as e:
        return jsonify({'error': f'Failed to fetch font: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error installing font: {str(e)}'}), 500


@bp.route('/google-fonts-list', methods=['GET'])
def google_fonts_list():
    """Proxy Google Fonts metadata for the font browser (fallback if direct CORS fails)."""
    artist_slug = get_authenticated_artist()
    if not artist_slug:
        abort(401, description='Authentication required')

    import urllib.request

    try:
        req = urllib.request.Request('https://fonts.google.com/metadata/fonts', headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        fonts = [{'family': f['family'], 'category': f.get('category', ''), 'fonts': f.get('fonts', {})} for f in data.get('familyMetadataList', [])[:1500]]
        return jsonify({'fonts': fonts})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── List Widgets ──────────────────────────────────────────────────────────

@bp.route('/list-widgets', methods=['GET'])
def list_widgets():
    """
    List all custom widgets for an artist.
    Each widget is a .js file in pages/artists/{slug}/widgets/
    Headers: X-Artist-Slug, X-Admin-Token
    """
    artist_slug = get_authenticated_artist()

    if not artist_slug:
        abort(401, description='Authentication required')

    widgets_dir = get_artist_path(artist_slug) / 'widgets'

    if not widgets_dir.exists():
        return jsonify({'artist': artist_slug, 'widgets': []})

    widgets = []
    for f in sorted(widgets_dir.iterdir()):
        if f.is_file() and f.suffix == '.js':
            widgets.append({
                'name': f.stem,
                'filename': f.name
            })

    return jsonify({'artist': artist_slug, 'widgets': widgets})


@bp.route('/get-widget', methods=['GET'])
def get_widget():
    """
    Get the JS content of a widget file.
    Query params: filename
    Headers: X-Artist-Slug, X-Admin-Token
    """
    artist_slug = get_authenticated_artist()

    if not artist_slug:
        abort(401, description='Authentication required')

    filename = request.args.get('filename')
    if not filename:
        return jsonify({'error': 'filename parameter required'}), 400

    filename = secure_filename(filename)
    widget_path = get_artist_path(artist_slug) / 'widgets' / filename

    if not widget_path.exists():
        return jsonify({'error': 'Widget not found'}), 404

    return send_file(widget_path, mimetype='application/javascript')


# ── Domain Check ──────────────────────────────────────────────────────────

SERVER_IPV4 = '151.226.233.153'
SERVER_IPV6 = '2a06:5902:39c1:9900:92a9:f065:784e:2260'

@bp.route('/check-domain', methods=['GET'])
def check_domain():
    """
    Check if an artist's configured domain has correct DNS and SSL.
    Headers: X-Artist-Slug, X-Admin-Token
    """
    artist_slug = get_authenticated_artist()
    if not artist_slug:
        abort(401, description='Authentication required')

    artist_path = get_artist_path(artist_slug)
    config_file = artist_path / 'config.json'

    if not config_file.exists():
        return jsonify({'error': 'Artist config not found'}), 404

    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)

    domain = config.get('domain', '').strip()
    if not domain:
        return jsonify({
            'domain': '',
            'status': 'not_configured',
            'message': 'No domain configured. Set one in the Config tab.'
        })

    result = {
        'domain': domain,
        'dns_a': None,
        'dns_aaaa': None,
        'dns_ok': False,
        'nginx_ok': False,
        'ssl_ok': False,
        'status': 'unknown',
        'message': ''
    }

    # Check DNS A record
    try:
        a_records = socket.getaddrinfo(domain, None, socket.AF_INET)
        result['dns_a'] = list(set(addr[4][0] for addr in a_records))
    except socket.gaierror:
        result['dns_a'] = []

    # Check DNS AAAA record
    try:
        aaaa_records = socket.getaddrinfo(domain, None, socket.AF_INET6)
        result['dns_aaaa'] = list(set(addr[4][0] for addr in aaaa_records))
    except socket.gaierror:
        result['dns_aaaa'] = []

    # Check if DNS points to this server
    a_match = SERVER_IPV4 in (result['dns_a'] or [])
    aaaa_match = any(SERVER_IPV6 in addr for addr in (result['dns_aaaa'] or []))
    result['dns_ok'] = a_match or aaaa_match

    # Check nginx config
    nginx_conf = Path(f'/etc/nginx/sites-available/{domain}')
    nginx_enabled = Path(f'/etc/nginx/sites-enabled/{domain}')
    # Also check if domain appears in the main blog config
    main_conf = Path('/etc/nginx/sites-available/blog')
    nginx_in_main = False
    if main_conf.exists():
        try:
            nginx_in_main = domain in main_conf.read_text()
        except:
            pass
    result['nginx_ok'] = nginx_conf.exists() or nginx_enabled.exists() or nginx_in_main

    # Check SSL certificate (needs root, so handle permission errors)
    try:
        cert_path = Path(f'/etc/letsencrypt/live/{domain}/fullchain.pem')
        result['ssl_ok'] = cert_path.exists()
    except (PermissionError, OSError):
        # Can't read letsencrypt dir without root — check via subprocess instead
        try:
            r = subprocess.run(['sudo', 'test', '-f', f'/etc/letsencrypt/live/{domain}/fullchain.pem'],
                               capture_output=True, timeout=3)
            result['ssl_ok'] = r.returncode == 0
        except:
            result['ssl_ok'] = False

    # Determine overall status
    if not result['dns_ok']:
        result['status'] = 'dns_pending'
        result['message'] = f'DNS not pointing to this server. Add an A record for {domain} pointing to {SERVER_IPV4}'
    elif not result['nginx_ok']:
        result['status'] = 'nginx_needed'
        result['message'] = 'DNS is correct. Nginx config needed.'
    elif not result['ssl_ok']:
        result['status'] = 'ssl_needed'
        result['message'] = 'DNS and Nginx configured. SSL certificate needed.'
    else:
        result['status'] = 'live'
        result['message'] = f'{domain} is fully configured and live.'

    # Generate setup commands
    result['server_ipv4'] = SERVER_IPV4
    result['server_ipv6'] = SERVER_IPV6
    result['slug'] = artist_slug

    return jsonify(result)


# ── Export Site ────────────────────────────────────────────────────────────

@bp.route('/export-site', methods=['GET'])
def export_site():
    """
    Export the artist's site as a downloadable .zip.
    Includes: compiled HTML, assets, api.py source, and a README.
    Headers: X-Artist-Slug, X-Admin-Token
    """
    import zipfile
    import io
    import time

    artist_slug = get_authenticated_artist()
    if not artist_slug:
        abort(401, description='Authentication required')

    artist_path = get_artist_path(artist_slug)
    output_path = Path('output/artists') / artist_slug

    if not output_path.exists():
        return jsonify({'error': 'No compiled site found. Save a page first.'}), 404

    # Build zip in memory
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        # 1. Compiled HTML + assets from output/
        for file_path in sorted(output_path.rglob('*')):
            if file_path.is_file():
                arcname = str(file_path.relative_to(output_path))
                zf.write(file_path, f'site/{arcname}')

        # 2. api.py source if it exists
        api_file = artist_path / 'api.py'
        if api_file.exists():
            zf.write(api_file, 'api/api.py')

        # 3. Feature config
        config_file = artist_path / 'config.json'
        if config_file.exists():
            zf.write(config_file, 'api/config.json')

        # 4. Source content.md files (for re-editing elsewhere)
        for page_dir in sorted(artist_path.iterdir()):
            if page_dir.is_dir() and page_dir.name not in ('assets', 'widgets', '__pycache__', '.snapshots', 'backups'):
                content_file = page_dir / 'content.md'
                config_json = page_dir / 'config.json'
                if content_file.exists():
                    zf.write(content_file, f'source/{page_dir.name}/content.md')
                if config_json.exists():
                    zf.write(config_json, f'source/{page_dir.name}/config.json')

        # 5. README
        readme = f"""# {artist_slug} — Site Export
Exported: {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())}

## What's in this zip

### site/
Your complete, ready-to-host website. Every page is a folder with an
index.html file. Assets (images, fonts) are in site/assets/.

To host this anywhere: upload the contents of site/ to any static
hosting provider (Netlify, Vercel, GitHub Pages, any web server).
The site is fully self-contained with relative paths — no server needed.

### source/
The raw content.md and config.json files for each page. These are the
editable source files used by the dashboard. Format:
  <style>CSS here</style>
  <html>HTML here</html>

### api/ (if present)
Your custom backend code (api.py) and artist config. This is a Flask
Blueprint — to run it elsewhere you'll need Python + Flask:
  pip install flask
  # See api.py for the Blueprint definition
  # You'll need to adapt it to your hosting setup

Note: features like bookings are pre-built modules that aren't included
in this export. The api.py file contains only your custom endpoints.
"""
        zf.writestr('README.md', readme)

    buf.seek(0)
    timestamp = time.strftime('%Y%m%d', time.gmtime())
    filename = f'{artist_slug}-export-{timestamp}.zip'

    return send_file(
        buf,
        mimetype='application/zip',
        as_attachment=True,
        download_name=filename
    )


# ── Delete Site ────────────────────────────────────────────────────────────

@bp.route('/delete-site', methods=['POST'])
def delete_site():
    """
    Permanently delete an artist's entire site.
    Removes source files, compiled output, and data.
    Headers: X-Artist-Slug, X-Admin-Token
    """
    artist_slug = get_authenticated_artist()
    if not artist_slug:
        abort(401, description='Authentication required')

    artist_path = get_artist_path(artist_slug)
    output_path = Path('output/artists') / artist_slug

    if not artist_path.exists():
        return jsonify({'error': 'Artist directory not found'}), 404

    try:
        # Remove source
        if artist_path.exists():
            shutil.rmtree(str(artist_path))
        # Remove compiled output
        if output_path.exists():
            shutil.rmtree(str(output_path))
        return jsonify({'ok': True, 'message': 'Site deleted permanently.'})
    except Exception as e:
        return jsonify({'error': f'Delete failed: {str(e)}'}), 500


# ── Snapshots ──────────────────────────────────────────────────────────────

@bp.route('/list-snapshots', methods=['GET'])
def list_snapshots():
    """
    List all snapshots for an artist.
    Headers: X-Artist-Slug, X-Admin-Token
    """
    artist_slug = get_authenticated_artist()
    if not artist_slug:
        abort(401)

    snap_dir = get_artist_path(artist_slug) / '.snapshots'
    if not snap_dir.exists():
        return jsonify({'snapshots': []})

    snapshots = []
    for f in sorted(snap_dir.glob('*.tar.gz'), reverse=True):
        # Parse name: 2026-03-27T08-15-30_my-snapshot-name.tar.gz
        stem = f.stem.replace('.tar', '')
        parts = stem.split('_', 1)
        timestamp = parts[0] if parts else stem
        name = parts[1].replace('-', ' ') if len(parts) > 1 else 'Unnamed'
        snapshots.append({
            'filename': f.name,
            'name': name,
            'timestamp': timestamp,
            'size': f.stat().st_size,
        })

    return jsonify({'snapshots': snapshots})


@bp.route('/create-snapshot', methods=['POST'])
def create_snapshot():
    """
    Create a tarball snapshot of the artist's site (excluding assets/ and widgets/).
    Headers: X-Artist-Slug, X-Admin-Token
    Body: { "name": "optional snapshot name" }
    """
    import tarfile
    import time

    artist_slug = get_authenticated_artist()
    if not artist_slug:
        abort(401)

    data = request.get_json() or {}
    name = data.get('name', 'manual').strip()
    # Sanitise name for filename
    safe_name = name.lower().replace(' ', '-')
    safe_name = ''.join(c for c in safe_name if c.isalnum() or c == '-')[:40]

    artist_path = get_artist_path(artist_slug)
    snap_dir = artist_path / '.snapshots'
    snap_dir.mkdir(exist_ok=True)

    timestamp = time.strftime('%Y-%m-%dT%H-%M-%S', time.gmtime())
    filename = f'{timestamp}_{safe_name}.tar.gz'
    snap_path = snap_dir / filename

    EXCLUDE_DIRS = {'assets', 'widgets', '.snapshots', '__pycache__', 'backups'}

    try:
        with tarfile.open(str(snap_path), 'w:gz') as tar:
            for item in sorted(artist_path.iterdir()):
                if item.name in EXCLUDE_DIRS:
                    continue
                arcname = item.name
                tar.add(str(item), arcname=arcname)

        # Prune old snapshots — keep max 30
        snaps = sorted(snap_dir.glob('*.tar.gz'), reverse=True)
        for old in snaps[30:]:
            old.unlink()

        return jsonify({
            'ok': True,
            'filename': filename,
            'size': snap_path.stat().st_size,
        })

    except Exception as e:
        return jsonify({'error': f'Snapshot failed: {str(e)}'}), 500


@bp.route('/restore-snapshot', methods=['POST'])
def restore_snapshot():
    """
    Restore a snapshot. Extracts the tarball over the artist directory
    (replacing pages, config, api.py — but NOT assets/ or widgets/).
    Headers: X-Artist-Slug, X-Admin-Token
    Body: { "filename": "2026-03-27T08-15-30_name.tar.gz" }
    """
    import tarfile

    artist_slug = get_authenticated_artist()
    if not artist_slug:
        abort(401)

    data = request.get_json() or {}
    filename = data.get('filename', '')
    if not filename or '..' in filename:
        return jsonify({'error': 'Invalid filename'}), 400

    artist_path = get_artist_path(artist_slug)
    snap_path = artist_path / '.snapshots' / filename

    if not snap_path.exists():
        return jsonify({'error': 'Snapshot not found'}), 404

    PRESERVE_DIRS = {'assets', 'widgets', '.snapshots', '__pycache__', 'backups'}

    try:
        # Remove current files (except preserved dirs)
        for item in artist_path.iterdir():
            if item.name in PRESERVE_DIRS:
                continue
            if item.is_dir():
                shutil.rmtree(str(item))
            else:
                item.unlink()

        # Extract snapshot
        with tarfile.open(str(snap_path), 'r:gz') as tar:
            tar.extractall(str(artist_path))

        return jsonify({'ok': True, 'message': 'Snapshot restored. Click Save to recompile.'})

    except Exception as e:
        return jsonify({'error': f'Restore failed: {str(e)}'}), 500


@bp.route('/delete-snapshot', methods=['POST'])
def delete_snapshot():
    """
    Delete a snapshot file.
    Headers: X-Artist-Slug, X-Admin-Token
    Body: { "filename": "..." }
    """
    artist_slug = get_authenticated_artist()
    if not artist_slug:
        abort(401)

    data = request.get_json() or {}
    filename = data.get('filename', '')
    if not filename or '..' in filename:
        return jsonify({'error': 'Invalid filename'}), 400

    snap_path = get_artist_path(artist_slug) / '.snapshots' / filename
    if not snap_path.exists():
        return jsonify({'error': 'Snapshot not found'}), 404

    try:
        snap_path.unlink()
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'error': f'Delete failed: {str(e)}'}), 500


# ── Claude Code Terminal ──────────────────────────────────────────────────

# Track active Claude sessions per artist: { artist_slug: session_id }
# Persisted to disk so sessions survive server restarts
import threading
import uuid
import time

_CLAUDE_SESSIONS_FILE = Path(__file__).parent.parent / '_claude_sessions.json'

def _load_claude_sessions():
    try:
        if _CLAUDE_SESSIONS_FILE.exists():
            return json.loads(_CLAUDE_SESSIONS_FILE.read_text())
    except:
        pass
    return {}

def _save_claude_sessions(sessions):
    try:
        _CLAUDE_SESSIONS_FILE.write_text(json.dumps(sessions, indent=2))
    except:
        pass

_claude_sessions = _load_claude_sessions()


def _get_artist_system_prompt(artist_slug):
    """Build a system prompt that scopes Claude to the artist's directory."""
    artist_path = get_artist_path(artist_slug)
    config_path = artist_path / 'config.json'
    abs_artist_path = str(Path.cwd() / artist_path)

    artist_config = {}
    if config_path.exists():
        try:
            artist_config = json.loads(config_path.read_text())
        except:
            pass

    artist_name = artist_config.get('name', artist_slug)
    description = artist_config.get('description', '')
    features = artist_config.get('features', [])

    # List pages
    pages = []
    for d in sorted(artist_path.iterdir()):
        if d.is_dir() and d.name not in ('assets', 'widgets', '__pycache__', '.snapshots', 'backups'):
            content_file = d / 'content.md'
            if content_file.exists():
                pages.append(d.name)

    pages_str = ', '.join(pages) if pages else 'none yet'

    # Check for custom api.py
    api_file = artist_path / 'api.py'
    has_api = api_file.exists()
    api_content = ''
    if has_api:
        try:
            api_content = api_file.read_text()
        except:
            pass

    # Build API section
    api_section = ''
    if has_api or features:
        api_section = f"""

BACKEND API:
- Your site can have a custom backend at api.py in this directory
- {'You currently have api.py — read it to understand the existing endpoints before making changes' if has_api else 'No api.py exists yet — you can create one to add custom backend features'}
- Active features from config.json: {', '.join(features) if features else 'none'}
- Feature backends live in _shared/features/ (NOT in this directory) — do NOT edit those
- Custom api.py pattern:
  ```python
  from flask import Blueprint, jsonify, request
  bp = Blueprint('artist_{artist_slug}', __name__, url_prefix='/api/artists/{artist_slug}')

  @bp.route('/my-endpoint')
  def my_endpoint():
      return jsonify({{'ok': True}})
  ```
- The blueprint MUST be named `bp` and set url_prefix to `/api/artists/{artist_slug}`
- For data storage, use JSON files in this directory (e.g. `data.json`)
- After editing api.py, tell the user the server needs a restart to pick up changes
- NEVER import from or modify files outside this artist directory
- NEVER use database connections, subprocess calls, or network requests in api.py
- Keep it simple — Flask Blueprint with JSON file storage only"""

    return f"""You are an AI assistant helping {artist_name} edit their portfolio website.

Greet {artist_name} warmly by name on first message.

WORKING DIRECTORY: {abs_artist_path}
You are STRICTLY sandboxed to this directory. All file operations MUST be within it.
NEVER read, write, list, or access files outside {abs_artist_path}.
NEVER access other artists' directories or any parent directories.
If a user asks you to look at another artist's site or files outside your directory, refuse politely.

SITE STRUCTURE:
- Each page is a folder with content.md and config.json
- content.md format: <style>CSS here</style>\\n<html>HTML here</html>
- Assets go in assets/images/ and assets/fonts/
- Asset references in content use relative paths: ../assets/images/photo.jpg
- Current pages: {pages_str}

ARTIST INFO:
- Name: {artist_name}
- Description: {description}
- Slug: {artist_slug}

CAPABILITIES:
- Read and edit any page's content.md or config.json
- Read and edit the site-level config.json in this directory (name, description, domain, favicon, etc.)
- Create new pages: mkdir pagename, then create content.md and config.json inside it
- View and manage assets in assets/images/ and assets/fonts/
- Make CSS/HTML changes across multiple pages at once
- Read and edit api.py for custom backend endpoints
- You have FULL file system access within this artist directory

SITE CONFIG (config.json in the root of this directory):
- "favicon": path relative to assets/ (e.g. "images/favicon.png") — used at compile time in the HTML <head>
- "name": artist display name
- "description": site description
- "domain": custom domain (e.g. "mysite.com")
- "contact_email": contact email
- To set a favicon, ensure the image exists in assets/ then update config.json's "favicon" field
- After config changes, tell the user to click Save to recompile
{api_section}

CREATING A NEW PAGE:
1. mkdir {abs_artist_path}/pagename
2. Create config.json: {{"title": "Page Title", "slug": "artists/{artist_slug}/pagename", "description": "...", "categories": []}}
3. Create content.md: copy the <style>...</style>\\n<html>...</html> pattern from an existing page like home/content.md
4. Update the nav in other pages to link to the new page: <a href="../pagename/">Page Title</a>
5. Tell the user to click Save in the dashboard — this runs compile and publishes changes

CRITICAL — SLUG FORMAT:
- Page slugs MUST always start with "artists/{artist_slug}/" e.g. "artists/{artist_slug}/pagename"
- NEVER use a bare slug like "photography" or "gallery" — this will OVERWRITE main blog pages!
- Always use the full path: "artists/{artist_slug}/photography" NOT "photography"

OFF LIMITS — DO NOT TOUCH:
- The widgets/ directory — widgets run with dashboard privileges (auth tokens, page write access)
- They must be created by Gabriel, not by you
- If the user asks for a widget, tell them to text Gabriel
- You CAN suggest building a self-contained admin page within the site instead (a regular page with password protection that calls api.py endpoints)

IMPORTANT:
- After making changes, tell the user to click Save in the dashboard to compile and publish
- Keep responses concise and friendly
- When editing content.md, always preserve the <style>...</style>\\n<html>...</html> format
- Use the artist's existing design patterns (fonts, colours, layout) when creating new content
- When creating pages, copy the full CSS from an existing page so styling is consistent"""


@bp.route('/claude-stream', methods=['POST'])
def claude_stream():
    """Stream Claude CLI output via SSE. Requires auth."""
    artist_slug = get_authenticated_artist()
    if not artist_slug:
        abort(401)

    data = request.get_json()
    prompt = data.get('prompt', '').strip()
    if not prompt:
        return jsonify({'error': 'Prompt required'}), 400

    artist_path = get_artist_path(artist_slug)
    abs_artist_path = str(Path.cwd() / artist_path)

    # Get or create session ID for this artist
    session_id = _claude_sessions.get(artist_slug)
    session_exists = session_id is not None

    if not session_exists:
        session_id = str(uuid.uuid4())
        _claude_sessions[artist_slug] = session_id
        _save_claude_sessions(_claude_sessions)

        # Auto-snapshot before new Vibe Coder session
        try:
            import tarfile, time as _time
            snap_dir = artist_path / '.snapshots'
            snap_dir.mkdir(exist_ok=True)
            ts = _time.strftime('%Y-%m-%dT%H-%M-%S', _time.gmtime())
            snap_path = snap_dir / f'{ts}_auto-before-vibe-coder.tar.gz'
            _excl = {'assets', 'widgets', '.snapshots', '__pycache__', 'backups'}
            with tarfile.open(str(snap_path), 'w:gz') as tar:
                for item in sorted(artist_path.iterdir()):
                    if item.name not in _excl:
                        tar.add(str(item), arcname=item.name)
            # Prune to 30
            for old in sorted(snap_dir.glob('*.tar.gz'), reverse=True)[30:]:
                old.unlink()
        except Exception:
            pass  # Don't block the session if snapshot fails

    system_prompt = _get_artist_system_prompt(artist_slug)

    # Find claude binary path
    claude_bin = shutil.which('claude') or '/usr/local/bin/claude'

    # Build claude CLI args
    args = [
        claude_bin,
        '-p', prompt,
        '--output-format', 'stream-json',
        '--verbose',
    ]

    if session_exists:
        args.extend(['--resume', session_id])
    else:
        args.extend(['--session-id', session_id])
        args.extend(['--system-prompt', system_prompt])

    # acceptEdits mode: auto-approves file operations within cwd (the artist dir)
    # but BLOCKS access to files outside cwd (other artists, system files, _shared)
    # This is enforced by Claude CLI at the permission level — not just prompt-based
    args.extend(['--permission-mode', 'acceptEdits'])

    def generate():
        env = os.environ.copy()
        # Remove CLAUDECODE to avoid nested session detection
        env.pop('CLAUDECODE', None)

        try:
            proc = subprocess.Popen(
                args,
                cwd=abs_artist_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                bufsize=1,
            )

            buffer = ''
            for chunk in iter(lambda: proc.stdout.read(4096), b''):
                buffer += chunk.decode('utf-8', errors='replace')
                lines = buffer.split('\n')
                buffer = lines[-1]  # Keep incomplete line

                for line in lines[:-1]:
                    line = line.strip()
                    if line:
                        yield f"data: {line}\n\n"

            # Flush remaining buffer
            if buffer.strip():
                yield f"data: {buffer.strip()}\n\n"

            proc.wait()

            # If process failed, report but only reset session on fatal errors
            if proc.returncode != 0:
                stderr_out = proc.stderr.read().decode('utf-8', errors='replace')
                error_msg = stderr_out.strip() if stderr_out.strip() else f'Process exited with code {proc.returncode}'
                error_data = json.dumps({
                    'type': 'error',
                    'error': error_msg,
                    'exit_code': proc.returncode
                })
                yield f"data: {error_data}\n\n"

                # Only reset session if it's a session-related error (invalid/corrupt session)
                if 'invalid session' in error_msg.lower() or 'session' in error_msg.lower() and 'not found' in error_msg.lower():
                    _claude_sessions.pop(artist_slug, None)
                    _save_claude_sessions(_claude_sessions)

            yield "data: {\"type\": \"stream_end\"}\n\n"

        except FileNotFoundError:
            error_data = json.dumps({
                'type': 'error',
                'error': 'Claude CLI not found. Is it installed?'
            })
            yield f"data: {error_data}\n\n"
        except Exception as e:
            error_data = json.dumps({
                'type': 'error',
                'error': str(e)
            })
            yield f"data: {error_data}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no',  # Disable nginx buffering
        }
    )


@bp.route('/list-endpoints', methods=['GET'])
def list_endpoints():
    """
    List all API endpoints relevant to this artist.
    Returns shared admin endpoints + any custom artist api.py endpoints.
    Headers: X-Artist-Slug, X-Admin-Token
    """
    from flask import current_app
    artist_slug = get_authenticated_artist()
    if not artist_slug:
        abort(401, description='Authentication required')

    # Friendly descriptions for known shared endpoints
    SHARED_DESCRIPTIONS = {
        'list-pages': {'summary': 'List all your pages', 'detail': 'Returns a list of every page on your site with its title and slug.'},
        'get-page-content': {'summary': 'Get a page\'s content', 'detail': 'Fetches the HTML and CSS content for a specific page.'},
        'edit-page': {'summary': 'Update a page', 'detail': 'Save new content or config for one of your pages.'},
        'create-page': {'summary': 'Create a new page', 'detail': 'Add a brand new page to your site.'},
        'delete-page': {'summary': 'Delete a page', 'detail': 'Permanently remove a page from your site.'},
        'upload-file': {'summary': 'Upload a file', 'detail': 'Upload images, fonts, or other files to your assets.'},
        'list-assets': {'summary': 'List your files', 'detail': 'See all uploaded images, fonts, and other files.'},
        'artist-info': {'summary': 'Your site info', 'detail': 'Get your site name, description, and settings.'},
        'list-widgets': {'summary': 'List dashboard widgets', 'detail': 'See what custom tools are available in your dashboard.'},
        'check-domain': {'summary': 'Check domain status', 'detail': 'See if your custom domain is set up correctly (DNS, SSL, etc).'},
        'list-endpoints': {'summary': 'List API endpoints', 'detail': 'Returns this list of all available API endpoints (you\'re looking at it!).'},
        'export-site': {'summary': 'Export your site', 'detail': 'Downloads a .zip of your complete site — compiled HTML, assets, source files, and API code.'},
    }

    # Load feature descriptions dynamically
    feature_descriptions = {}
    try:
        from features import bookings as bookings_feature
        if hasattr(bookings_feature, 'ENDPOINT_DESCRIPTIONS'):
            feature_descriptions['bookings'] = bookings_feature.ENDPOINT_DESCRIPTIONS
    except ImportError:
        pass

    endpoints = []

    # Collect all routes from the Flask app
    for rule in current_app.url_map.iter_rules():
        route = rule.rule
        methods = sorted(rule.methods - {'HEAD', 'OPTIONS'})
        if not methods:
            continue

        # Shared admin endpoints (skip dashboard/streaming/internal)
        if route.startswith('/api/adze/'):
            short = route.replace('/api/adze/', '')
            if short in ('dashboard', 'get-widget', 'claude-stream', 'claude-reset'):
                continue
            desc = SHARED_DESCRIPTIONS.get(short, {})
            endpoints.append({
                'url': route,
                'methods': methods,
                'source': 'shared',
                'name': short,
                'summary': desc.get('summary', short.replace('-', ' ').title()),
                'detail': desc.get('detail', ''),
                'auth': True,
            })

        # Artist-scoped endpoints (features + custom api.py)
        elif f'/api/artists/{artist_slug}' in route:
            tail = route.split(f'/api/artists/{artist_slug}/')[-1] if f'/api/artists/{artist_slug}/' in route else route.split('/')[-1]
            parts = tail.split('/')

            # Check if this is a known feature (e.g. bookings/submit)
            feature_name = parts[0] if parts else ''
            endpoint_name = parts[1] if len(parts) > 1 else ''
            feat_descs = feature_descriptions.get(feature_name, {})
            ep_desc = feat_descs.get(endpoint_name, {})

            if ep_desc:
                # Known feature endpoint — use its descriptions
                endpoints.append({
                    'url': route,
                    'methods': methods,
                    'source': 'feature',
                    'feature': feature_name,
                    'name': tail,
                    'summary': ep_desc.get('summary', tail.replace('/', ' ').title()),
                    'detail': ep_desc.get('detail', ''),
                    'auth': ep_desc.get('auth', True),
                })
            else:
                # Custom api.py endpoint
                endpoints.append({
                    'url': route,
                    'methods': methods,
                    'source': 'custom',
                    'name': tail or 'root',
                    'summary': tail.replace('-', ' ').replace('_', ' ').replace('/', ' ').title() if tail else 'Custom Endpoint',
                    'detail': 'Custom endpoint defined in your api.py',
                    'auth': False,
                })

    # Sort: features first, then custom, then shared
    source_order = {'feature': 0, 'custom': 1, 'shared': 2}
    endpoints.sort(key=lambda e: (source_order.get(e['source'], 1), e['name']))

    # Check if artist has an api.py
    artist_path = get_artist_path(artist_slug)
    has_custom_api = (artist_path / 'api.py').exists()

    return jsonify({
        'endpoints': endpoints,
        'has_custom_api': has_custom_api,
        'custom_api_prefix': f'/api/artists/{artist_slug}',
    })


@bp.route('/claude-reset', methods=['POST'])
def claude_reset():
    """Reset Claude session for the artist. Requires auth."""
    artist_slug = get_authenticated_artist()
    if not artist_slug:
        abort(401)

    _claude_sessions.pop(artist_slug, None)
    _save_claude_sessions(_claude_sessions)
    return jsonify({'ok': True, 'message': 'Session reset. Next message will start a fresh conversation.'})
