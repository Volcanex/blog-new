#!/usr/bin/env python3
"""
Create a new artist site from template.

Usage:
    python3 create_artist.py "Artist Name" slug domain.com token
    python3 create_artist.py "Nina" serebrenina serebrenina.com nina

This copies _template, replaces placeholders, copies shared fonts,
and compiles the site. The new artist is immediately available at:
    /artists/{slug}/home/
"""

import sys
import shutil
import json
from pathlib import Path

BASE = Path(__file__).parent / 'pages' / 'artists'
TEMPLATE = BASE / '_template'
SHARED_FONTS = BASE / 'leahmclaine' / 'assets' / 'fonts'  # fallback font source

def create_artist(name, slug, domain='', token=''):
    dest = BASE / slug

    if dest.exists():
        print(f"Error: {dest} already exists!")
        sys.exit(1)

    if not TEMPLATE.exists():
        print(f"Error: template not found at {TEMPLATE}")
        sys.exit(1)

    # Copy template
    shutil.copytree(TEMPLATE, dest)
    print(f"Copied template → {dest}")

    # Replace placeholders in all files
    replacements = {
        '{{ARTIST_NAME}}': name,
        '{{SLUG}}': slug,
        '{{DOMAIN}}': domain,
        '{{TOKEN}}': token or slug,
    }

    for f in dest.rglob('*'):
        if f.is_file() and f.suffix in ('.json', '.md', '.html', '.css', '.js'):
            text = f.read_text()
            changed = False
            for placeholder, value in replacements.items():
                if placeholder in text:
                    text = text.replace(placeholder, value)
                    changed = True
            if changed:
                f.write_text(text)

    print(f"Replaced placeholders (name={name}, slug={slug}, domain={domain})")

    # Copy shared fonts if they exist and artist doesn't have any
    fonts_dir = dest / 'assets' / 'fonts'
    if fonts_dir.exists() and not any(fonts_dir.iterdir()) and SHARED_FONTS.exists():
        for font in SHARED_FONTS.glob('*.woff2'):
            shutil.copy2(font, fonts_dir / font.name)
        print(f"Copied {len(list(fonts_dir.glob('*.woff2')))} fonts from shared source")

    # Print summary
    config = json.loads((dest / 'config.json').read_text())
    print(f"\n{'='*50}")
    print(f"Artist site created!")
    print(f"  Name:   {config['name']}")
    print(f"  Slug:   {config['slug']}")
    print(f"  Domain: {config['domain'] or '(none yet)'}")
    print(f"  Token:  {config['admin_token']}")
    print(f"  Dir:    {dest}")
    print(f"{'='*50}")
    print(f"\nNext steps:")
    print(f"  1. python3 compile.py")
    print(f"  2. sudo systemctl restart blog-server")
    print(f"  3. Visit: /artists/{slug}/home/")
    print(f"  4. Dashboard: /api/sandbox/dashboard (login: {slug} / {token or slug})")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 create_artist.py \"Artist Name\" slug [domain] [token]")
        print("Example: python3 create_artist.py \"Nina\" serebrenina serebrenina.com nina")
        sys.exit(1)

    name = sys.argv[1]
    slug = sys.argv[2]
    domain = sys.argv[3] if len(sys.argv) > 3 else ''
    token = sys.argv[4] if len(sys.argv) > 4 else slug

    create_artist(name, slug, domain, token)
