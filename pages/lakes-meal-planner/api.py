"""
Lakes Meal Planner API — shared bubble board for food + activity ideas.
"""

from flask import Blueprint, jsonify, request
from shared.database import get_db
from datetime import datetime, timedelta
import uuid
import os
import json
import re
import urllib.request
import urllib.error


def _clean_name(s):
    """Strip whitespace, leading/trailing punctuation, cap length. Preserves casing."""
    s = (s or '').strip()
    s = re.sub(r'^[^\w]+', '', s)
    s = re.sub(r'[^\w]+$', '', s)
    return s[:24].strip()


def _name_key(s):
    """Comparison key — case-insensitive, punctuation-insensitive."""
    return _clean_name(s).lower()


def _dedupe_voters(names):
    """Keep first-seen casing of each unique person."""
    seen = {}
    out = []
    for n in names:
        cleaned = _clean_name(n)
        if not cleaned:
            continue
        key = cleaned.lower()
        if key in seen:
            continue
        seen[key] = cleaned
        out.append(cleaned)
    return out

bp = Blueprint('lakes_meal_planner', __name__, url_prefix='/api/lakes-meal-planner')

PAGE = 'lakes-meal-planner'
COLLECTION = 'ideas'

VALID_KINDS = ('food', 'activity')


def _migrate(item):
    if 'ups' not in item:
        v = item.get('votes', 0)
        item['ups'] = max(v, 0)
        item['downs'] = max(-v, 0)
    item.setdefault('downs', 0)
    item.setdefault('who_ups', [])
    item.setdefault('who_downs', [])
    # clean + dedupe by case-insensitive name key; if a person is in both lists,
    # keep them in whichever list they last appeared (downs wins to be safe).
    ups = _dedupe_voters(item['who_ups'])
    downs = _dedupe_voters(item['who_downs'])
    down_keys = {n.lower() for n in downs}
    ups = [n for n in ups if n.lower() not in down_keys]
    item['who_ups'] = ups
    item['who_downs'] = downs
    item['ups'] = len(ups)
    item['downs'] = len(downs)
    if item.get('created_by'):
        item['created_by'] = _clean_name(item['created_by'])
    item['votes'] = item['ups'] - item['downs']
    return item


EVENTS_COLLECTION = 'events'
EVENTS_KEEP = 40


def _push_event(evt):
    db = get_db()
    events = db.get_page_data(PAGE, EVENTS_COLLECTION, []) or []
    events.append(evt)
    if len(events) > EVENTS_KEEP:
        events = events[-EVENTS_KEEP:]
    db.set_page_data(PAGE, EVENTS_COLLECTION, events)


def _load():
    db = get_db()
    raw = db.get_page_data(PAGE, COLLECTION, []) or []
    before = json.dumps(raw, sort_keys=True)
    items = [_migrate(i) for i in raw]
    after = json.dumps(items, sort_keys=True)
    if before != after:
        db.set_page_data(PAGE, COLLECTION, items)
    return items


def _save(items):
    db = get_db()
    db.set_page_data(PAGE, COLLECTION, items)


@bp.route('/ideas', methods=['GET'])
def list_ideas():
    return jsonify({'ideas': _load()})


@bp.route('/ideas', methods=['POST'])
def add_idea():
    data = request.get_json(silent=True) or {}
    text = (data.get('text') or '').strip()
    kind = data.get('kind', 'food')
    name = _clean_name(data.get('name')) or 'someone'

    if not text:
        return jsonify({'error': 'text required'}), 400
    if len(text) > 80:
        return jsonify({'error': 'too long (80 char max)'}), 400
    if kind not in VALID_KINDS:
        return jsonify({'error': 'kind must be food or activity'}), 400

    idea = {
        'id': uuid.uuid4().hex[:10],
        'text': text,
        'kind': kind,
        'ups': 0,
        'downs': 0,
        'who_ups': [],
        'who_downs': [],
        'votes': 0,
        'created': datetime.utcnow().isoformat() + 'Z',
        'created_by': name,
    }

    items = _load()
    items.append(idea)
    _save(items)
    return jsonify(idea), 201


@bp.route('/ideas/<idea_id>/vote', methods=['POST'])
def vote(idea_id):
    data = request.get_json(silent=True) or {}
    delta = data.get('delta', 1)
    name = _clean_name(data.get('name')) or 'someone'
    key = name.lower()
    if delta not in (1, -1):
        return jsonify({'error': 'delta must be 1 or -1'}), 400

    items = _load()
    for item in items:
        if item['id'] == idea_id:
            ups = item.setdefault('who_ups', [])
            downs = item.setdefault('who_downs', [])
            in_ups   = next((n for n in ups   if n.lower() == key), None)
            in_downs = next((n for n in downs if n.lower() == key), None)
            if delta == 1:
                if in_ups:
                    ups.remove(in_ups)  # toggle off
                else:
                    if in_downs: downs.remove(in_downs)
                    ups.append(name)
            else:
                if in_downs:
                    downs.remove(in_downs)
                else:
                    if in_ups: ups.remove(in_ups)
                    downs.append(name)
            item['who_ups'] = _dedupe_voters(ups)
            item['who_downs'] = _dedupe_voters(downs)
            item['ups'] = len(item['who_ups'])
            item['downs'] = len(item['who_downs'])
            item['votes'] = item['ups'] - item['downs']
            _save(items)
            _push_event({
                'id': uuid.uuid4().hex[:8],
                'idea_id': idea_id,
                'name': name,
                'delta': delta,
                'text': item['text'],
                'kind': item['kind'],
                'ts': datetime.utcnow().isoformat() + 'Z',
            })
            return jsonify(item)
    return jsonify({'error': 'not found'}), 404


@bp.route('/events', methods=['GET'])
def list_events():
    db = get_db()
    since = request.args.get('since', '')
    events = db.get_page_data(PAGE, EVENTS_COLLECTION, []) or []
    if since:
        events = [e for e in events if e.get('ts', '') > since]
    return jsonify({'events': events[-EVENTS_KEEP:]})


@bp.route('/ideas/<idea_id>/kind', methods=['POST'])
def switch_kind(idea_id):
    data = request.get_json(silent=True) or {}
    kind = data.get('kind')
    if kind not in VALID_KINDS:
        return jsonify({'error': 'kind must be food or activity'}), 400
    items = _load()
    for item in items:
        if item['id'] == idea_id:
            item['kind'] = kind
            _save(items)
            return jsonify(item)
    return jsonify({'error': 'not found'}), 404


PLAN_COLLECTION = 'plan'
GROUP_SIZE = 10
OPENROUTER_MODEL = 'anthropic/claude-haiku-4.5'
SYNTH_MIN_INTERVAL = timedelta(seconds=20)


def _call_openrouter(prompt):
    key = os.environ.get('OPENROUTER_API_KEY')
    if not key:
        raise RuntimeError('OPENROUTER_API_KEY not set on server')
    req = urllib.request.Request(
        'https://openrouter.ai/api/v1/chat/completions',
        data=json.dumps({
            'model': OPENROUTER_MODEL,
            'messages': [{'role': 'user', 'content': prompt}],
            'response_format': {'type': 'json_object'},
            'temperature': 0.4,
        }).encode('utf-8'),
        headers={
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://gabrielpenman.com/lakes-meal-planner',
            'X-Title': 'Lakes Meal Planner',
        },
    )
    with urllib.request.urlopen(req, timeout=45) as resp:
        body = json.loads(resp.read().decode('utf-8'))
    text = body['choices'][0]['message']['content'].strip()
    # strip markdown fences if the model wrapped its JSON
    if text.startswith('```'):
        text = text.split('\n', 1)[1] if '\n' in text else text
        if text.endswith('```'):
            text = text.rsplit('```', 1)[0]
        text = text.strip()
        if text.lower().startswith('json'):
            text = text[4:].lstrip()
    # find first { ... last } in case there's still preamble
    if not text.startswith('{'):
        start = text.find('{'); end = text.rfind('}')
        if start >= 0 and end > start:
            text = text[start:end+1]
    return json.loads(text)


def _build_prompt(ideas):
    food = [i for i in ideas if i['kind'] == 'food']
    activity = [i for i in ideas if i['kind'] == 'activity']
    food.sort(key=lambda i: i['votes'], reverse=True)
    activity.sort(key=lambda i: i['votes'], reverse=True)

    def fmt(items):
        return '\n'.join(f'- {i["text"]} ({i["votes"]} votes)' for i in items) or '(none yet)'

    return f"""You are planning a 2-day weekend trip at the Lake District for {GROUP_SIZE} people.

Use ONLY the group's voted ideas below. Do NOT invent meals or activities that aren't on these lists — the group wants to see their own ideas, not your suggestions. Higher-vote items take priority.

Slot the food ideas across Day 1 and Day 2 (breakfast, lunch, dinner). If there aren't enough food ideas for all 6 slots, LEAVE THE EXTRA SLOTS EMPTY (use null) rather than inventing meals. Same rule for activities — only use what's been voted on.

Then generate a consolidated shopping list for {GROUP_SIZE} people based on whatever meals you've slotted, grouped by aisle.

FOOD IDEAS (by votes):
{fmt(food)}

ACTIVITY IDEAS (by votes):
{fmt(activity)}

Respond with VALID JSON ONLY — no markdown fences, no commentary. Use this exact shape:
{{
  "days": [
    {{
      "label": "Day 1",
      "meals": {{"breakfast": "..." or null, "lunch": "..." or null, "dinner": "..." or null}},
      "activities": ["..."]
    }},
    {{
      "label": "Day 2",
      "meals": {{"breakfast": "..." or null, "lunch": "..." or null, "dinner": "..." or null}},
      "activities": ["..."]
    }}
  ],
  "shopping_list": [
    {{"section": "Produce", "items": ["2kg potatoes", "..."]}}
  ],
  "notes": "one-sentence summary for the group chat"
}}"""


@bp.route('/plan', methods=['GET'])
def get_plan():
    db = get_db()
    plan = db.get_page_data(PAGE, PLAN_COLLECTION, None)
    return jsonify(plan or {'plan': None})


@bp.route('/plan/synthesise', methods=['POST'])
def synthesise():
    db = get_db()
    existing = db.get_page_data(PAGE, PLAN_COLLECTION, None) or {}

    last = existing.get('generated_at')
    force = (request.get_json(silent=True) or {}).get('force')
    if last and not force:
        try:
            last_dt = datetime.fromisoformat(last.rstrip('Z'))
            if datetime.utcnow() - last_dt < SYNTH_MIN_INTERVAL:
                return jsonify(existing)
        except Exception:
            pass

    ideas = _load()
    if not ideas:
        return jsonify({'error': 'no ideas yet — add some on the entry page'}), 400

    try:
        plan = _call_openrouter(_build_prompt(ideas))
    except urllib.error.HTTPError as e:
        return jsonify({'error': f'openrouter http {e.code}', 'detail': e.read().decode('utf-8', 'replace')[:400]}), 502
    except Exception as e:
        return jsonify({'error': str(e)}), 502

    record = {
        'plan': plan,
        'generated_at': datetime.utcnow().isoformat() + 'Z',
        'idea_count': len(ideas),
        'group_size': GROUP_SIZE,
        'model': OPENROUTER_MODEL,
    }
    db.set_page_data(PAGE, PLAN_COLLECTION, record)
    return jsonify(record)


@bp.route('/ideas/<idea_id>', methods=['DELETE'])
def remove(idea_id):
    items = _load()
    new_items = [i for i in items if i['id'] != idea_id]
    if len(new_items) == len(items):
        return jsonify({'error': 'not found'}), 404
    _save(new_items)
    return jsonify({'ok': True})
