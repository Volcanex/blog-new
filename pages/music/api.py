"""
Music API — parses SoundCloud's public RSS feed for Gabriel Penman's tracks.
No client_id scraping needed; feeds.soundcloud.com is publicly accessible
and not subject to Cloudflare bot protection.

Routes:
  GET /api/music/tracks   → { tracks: [{title, duration_ms, artwork_url, stream_url}] }
"""

import re
import time
import requests
import xml.etree.ElementTree as ET
from flask import Blueprint, jsonify

bp = Blueprint('music', __name__, url_prefix='/api/music')

RSS_URL   = 'https://feeds.soundcloud.com/users/soundcloud:users:202265942/sounds.rss'
CACHE_TTL = 3600  # 1 hour

_cache = {'tracks': None, 'ts': 0}

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (X11; Linux x86_64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    )
}

ITUNES_NS = 'http://www.itunes.com/dtds/podcast-1.0.dtd'


def _duration_to_ms(s):
    """Convert HH:MM:SS or MM:SS string to milliseconds."""
    try:
        parts = [int(p) for p in s.strip().split(':')]
        if len(parts) == 3:
            h, m, sec = parts
        elif len(parts) == 2:
            h, m, sec = 0, parts[0], parts[1]
        else:
            return 0
        return ((h * 3600) + (m * 60) + sec) * 1000
    except Exception:
        return 0


def _fetch_tracks():
    r = requests.get(RSS_URL, headers=HEADERS, timeout=15)
    r.raise_for_status()

    root = ET.fromstring(r.text)
    tracks = []

    for item in root.findall('.//item'):
        title = item.findtext('title', '').strip()
        enc   = item.find('enclosure')
        dur_s = item.findtext(f'{{{ITUNES_NS}}}duration', '')
        img   = item.find(f'{{{ITUNES_NS}}}image')

        stream_url  = enc.get('url') if enc is not None else None
        artwork_url = img.get('href') if img is not None else None

        if not stream_url:
            continue

        # Downscale artwork from t3000x3000 → t500x500 for faster loads
        if artwork_url:
            artwork_url = re.sub(r'-t\d+x\d+\.', '-t500x500.', artwork_url)

        tracks.append({
            'title':       title,
            'duration_ms': _duration_to_ms(dur_s),
            'artwork_url': artwork_url,
            'stream_url':  stream_url,
        })

    return tracks


def get_tracks():
    now = time.time()
    if _cache['tracks'] is not None and now - _cache['ts'] < CACHE_TTL:
        return _cache['tracks']
    tracks = _fetch_tracks()
    _cache['tracks'] = tracks
    _cache['ts'] = now
    return tracks


@bp.route('/tracks')
def tracks_route():
    try:
        return jsonify({'tracks': get_tracks()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
