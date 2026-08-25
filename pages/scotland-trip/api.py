"""
Scotland trip API — nodes, comments, kit. Open writes, no auth.
"""

from flask import Blueprint, jsonify, request
from shared.database import get_db
from datetime import datetime
import uuid

bp = Blueprint('scotland_trip', __name__, url_prefix='/api/scotland-trip')

PAGE = 'scotland-trip'

DEFAULT_NODES = [
    {"id": "n1",  "order": 0,  "name": "Milngavie",            "type": "start",    "lat": 55.9424, "lng": -4.3148, "description": "Start of the West Highland Way. Train from Glasgow Queen St (20 min).", "cost_gbp": 0,  "url": ""},
    {"id": "n2",  "order": 1,  "name": "Drymen",               "type": "resupply", "lat": 56.0728, "lng": -4.4543, "description": "Small village with a Co-op. Easy resupply before Loch Lomond.",          "cost_gbp": 0,  "url": ""},
    {"id": "n3",  "order": 2,  "name": "Balmaha",              "type": "campsite", "lat": 56.0866, "lng": -4.5378, "description": "Campsite on Loch Lomond shores. Midge hell in summer — bring a net.",    "cost_gbp": 12, "url": ""},
    {"id": "n4",  "order": 3,  "name": "Rowardennan",          "type": "campsite", "lat": 56.1487, "lng": -4.5969, "description": "Forestry campsite. Basic facilities. Start of the rough loch-side path.", "cost_gbp": 8,  "url": ""},
    {"id": "n5",  "order": 4,  "name": "Inverarnan",           "type": "hostel",   "lat": 56.3128, "lng": -4.7180, "description": "The Drovers Inn — ancient, atmospheric, slightly chaotic pub hostel.",    "cost_gbp": 22, "url": ""},
    {"id": "n6",  "order": 5,  "name": "Crianlarich",          "type": "hostel",   "lat": 56.3894, "lng": -4.6159, "description": "SYHA hostel. Good resupply point. Village has a Co-op.",                 "cost_gbp": 25, "url": ""},
    {"id": "n7",  "order": 6,  "name": "Tyndrum",              "type": "campsite", "lat": 56.4336, "lng": -4.7221, "description": "By The Way campsite. Good facilities, hot showers. Real Food Cafe nearby.", "cost_gbp": 14, "url": ""},
    {"id": "n8",  "order": 7,  "name": "Bridge of Orchy",      "type": "hostel",   "lat": 56.5075, "lng": -4.7663, "description": "Bridge of Orchy Hotel bunkhouse. Last shelter before Rannoch Moor.",     "cost_gbp": 28, "url": ""},
    {"id": "n9",  "order": 8,  "name": "Rannoch Moor (wild)",  "type": "wild",     "lat": 56.5800, "lng": -4.8200, "description": "Wild camp on the moor. Utterly exposed, utterly beautiful. Check weather.", "cost_gbp": 0,  "url": ""},
    {"id": "n10", "order": 9,  "name": "Kingshouse Hotel",     "type": "hostel",   "lat": 56.6065, "lng": -4.8622, "description": "Kingshouse bunkhouse. Gateway to the Devil's Staircase.",                "cost_gbp": 32, "url": ""},
    {"id": "n11", "order": 10, "name": "Kinlochleven",         "type": "hostel",   "lat": 56.7134, "lng": -4.9503, "description": "Blackwater Hostel. Laundry available. Local pub and Co-op.",             "cost_gbp": 20, "url": ""},
    {"id": "n12", "order": 11, "name": "Fort William",         "type": "end",      "lat": 56.8198, "lng": -5.1052, "description": "End of the WHW. Celebrations at the Grog & Gruel. Train back to Glasgow.", "cost_gbp": 0,  "url": ""},
]

DEFAULT_KIT = [
    {"id": "k1",  "category": "Shelter",      "name": "Tent",                        "weight_g": 1800, "packed": False, "notes": ""},
    {"id": "k2",  "category": "Shelter",      "name": "Sleeping bag (3 season)",     "weight_g": 800,  "packed": False, "notes": ""},
    {"id": "k3",  "category": "Shelter",      "name": "Sleeping mat",                "weight_g": 400,  "packed": False, "notes": ""},
    {"id": "k4",  "category": "Navigation",   "name": "OS Maps app (offline)",       "weight_g": 0,    "packed": False, "notes": ""},
    {"id": "k5",  "category": "Navigation",   "name": "Compass",                     "weight_g": 30,   "packed": False, "notes": ""},
    {"id": "k6",  "category": "Clothing",     "name": "Waterproof jacket",           "weight_g": 400,  "packed": False, "notes": ""},
    {"id": "k7",  "category": "Clothing",     "name": "Waterproof trousers",         "weight_g": 300,  "packed": False, "notes": ""},
    {"id": "k8",  "category": "Clothing",     "name": "Merino base layer ×2",        "weight_g": 400,  "packed": False, "notes": ""},
    {"id": "k9",  "category": "Clothing",     "name": "Mid layer fleece",            "weight_g": 350,  "packed": False, "notes": ""},
    {"id": "k10", "category": "Clothing",     "name": "Hiking boots",                "weight_g": 900,  "packed": False, "notes": ""},
    {"id": "k11", "category": "Clothing",     "name": "Gaiters",                     "weight_g": 200,  "packed": False, "notes": "Essential — boggy sections"},
    {"id": "k12", "category": "Food & Water", "name": "Backpacking stove + fuel",    "weight_g": 350,  "packed": False, "notes": ""},
    {"id": "k13", "category": "Food & Water", "name": "Cooking pot",                 "weight_g": 200,  "packed": False, "notes": ""},
    {"id": "k14", "category": "Food & Water", "name": "Water filter (Sawyer Squeeze)", "weight_g": 90, "packed": False, "notes": "Scottish water clean but use it anyway"},
    {"id": "k15", "category": "First Aid",    "name": "First aid kit",               "weight_g": 200,  "packed": False, "notes": ""},
    {"id": "k16", "category": "First Aid",    "name": "Blister kit (Compeed)",       "weight_g": 50,   "packed": False, "notes": "Bring more than you think"},
    {"id": "k17", "category": "Safety",       "name": "Midge head net",              "weight_g": 40,   "packed": False, "notes": "Non-negotiable June–August"},
    {"id": "k18", "category": "Safety",       "name": "Smidge repellent",            "weight_g": 75,   "packed": False, "notes": "Smidge > DEET for Scottish midges"},
    {"id": "k19", "category": "Safety",       "name": "Emergency bivvy bag",         "weight_g": 130,  "packed": False, "notes": ""},
    {"id": "k20", "category": "Electronics",  "name": "Headtorch + batteries",       "weight_g": 80,   "packed": False, "notes": ""},
    {"id": "k21", "category": "Electronics",  "name": "Power bank (20 000 mAh)",     "weight_g": 440,  "packed": False, "notes": ""},
]


def _nodes():
    db = get_db()
    data = db.get_page_data(PAGE, 'nodes', None)
    if data is None:
        db.set_page_data(PAGE, 'nodes', DEFAULT_NODES)
        return list(DEFAULT_NODES)
    return data


def _comments():
    db = get_db()
    return db.get_page_data(PAGE, 'comments', [])


def _kit():
    db = get_db()
    data = db.get_page_data(PAGE, 'kit', None)
    if data is None:
        db.set_page_data(PAGE, 'kit', DEFAULT_KIT)
        return list(DEFAULT_KIT)
    return data


def _save_nodes(nodes):
    get_db().set_page_data(PAGE, 'nodes', nodes)


def _save_comments(comments):
    get_db().set_page_data(PAGE, 'comments', comments)


def _save_kit(kit):
    get_db().set_page_data(PAGE, 'kit', kit)


@bp.route('/data')
def get_data():
    return jsonify({
        'nodes': sorted(_nodes(), key=lambda n: n.get('order', 0)),
        'comments': _comments(),
        'kit': _kit(),
    })


@bp.route('/nodes', methods=['POST'])
def add_node():
    data = request.get_json() or {}
    required = ['name', 'lat', 'lng']
    for f in required:
        if f not in data:
            return jsonify({'error': f'Missing field: {f}'}), 400

    nodes = _nodes()
    max_order = max((n.get('order', 0) for n in nodes), default=-1)
    node = {
        'id': 'n' + uuid.uuid4().hex[:8],
        'order': data.get('order', max_order + 1),
        'name': str(data['name'])[:80],
        'type': data.get('type', 'wild'),
        'lat': float(data['lat']),
        'lng': float(data['lng']),
        'description': str(data.get('description', ''))[:400],
        'cost_gbp': float(data.get('cost_gbp', 0)),
        'url': str(data.get('url', ''))[:200],
    }
    nodes.append(node)
    nodes.sort(key=lambda n: n.get('order', 0))
    _save_nodes(nodes)
    return jsonify({'node': node, 'nodes': nodes}), 201


@bp.route('/nodes/<node_id>', methods=['PUT'])
def update_node(node_id):
    data = request.get_json() or {}
    nodes = _nodes()
    node = next((n for n in nodes if n['id'] == node_id), None)
    if not node:
        return jsonify({'error': 'Node not found'}), 404

    for field in ['name', 'type', 'lat', 'lng', 'description', 'cost_gbp', 'url', 'order']:
        if field in data:
            if field in ('lat', 'lng', 'cost_gbp'):
                node[field] = float(data[field])
            elif field == 'order':
                node[field] = int(data[field])
            else:
                node[field] = str(data[field])[:400]

    nodes.sort(key=lambda n: n.get('order', 0))
    _save_nodes(nodes)
    return jsonify({'node': node, 'nodes': nodes})


@bp.route('/nodes/<node_id>', methods=['DELETE'])
def delete_node(node_id):
    nodes = _nodes()
    before = len(nodes)
    nodes = [n for n in nodes if n['id'] != node_id]
    if len(nodes) == before:
        return jsonify({'error': 'Node not found'}), 404
    _save_nodes(nodes)
    return jsonify({'deleted': node_id, 'nodes': nodes})


@bp.route('/comments', methods=['POST'])
def add_comment():
    data = request.get_json() or {}
    body = str(data.get('body', '')).strip()
    if not body:
        return jsonify({'error': 'body required'}), 400

    comment = {
        'id': 'c' + uuid.uuid4().hex[:8],
        'author': str(data.get('author', 'Anonymous'))[:40],
        'body': body[:1000],
        'node_id': data.get('node_id') or None,
        'created_at': datetime.utcnow().isoformat() + 'Z',
    }
    comments = _comments()
    comments.append(comment)
    _save_comments(comments)
    return jsonify({'comment': comment, 'comments': comments}), 201


@bp.route('/comments/<comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    comments = _comments()
    before = len(comments)
    comments = [c for c in comments if c['id'] != comment_id]
    if len(comments) == before:
        return jsonify({'error': 'Comment not found'}), 404
    _save_comments(comments)
    return jsonify({'deleted': comment_id})


@bp.route('/kit', methods=['POST'])
def add_kit_item():
    data = request.get_json() or {}
    if not data.get('name'):
        return jsonify({'error': 'name required'}), 400

    item = {
        'id': 'k' + uuid.uuid4().hex[:8],
        'category': str(data.get('category', 'Other'))[:40],
        'name': str(data['name'])[:80],
        'weight_g': int(data.get('weight_g', 0)),
        'packed': bool(data.get('packed', False)),
        'notes': str(data.get('notes', ''))[:200],
    }
    kit = _kit()
    kit.append(item)
    _save_kit(kit)
    return jsonify({'item': item, 'kit': kit}), 201


@bp.route('/kit/<kit_id>', methods=['PUT'])
def update_kit_item(kit_id):
    data = request.get_json() or {}
    kit = _kit()
    item = next((k for k in kit if k['id'] == kit_id), None)
    if not item:
        return jsonify({'error': 'Kit item not found'}), 404

    for field in ['name', 'category', 'notes']:
        if field in data:
            item[field] = str(data[field])[:200]
    if 'weight_g' in data:
        item['weight_g'] = int(data['weight_g'])
    if 'packed' in data:
        item['packed'] = bool(data['packed'])

    _save_kit(kit)
    return jsonify({'item': item, 'kit': kit})


@bp.route('/kit/<kit_id>', methods=['DELETE'])
def delete_kit_item(kit_id):
    kit = _kit()
    before = len(kit)
    kit = [k for k in kit if k['id'] != kit_id]
    if len(kit) == before:
        return jsonify({'error': 'Kit item not found'}), 404
    _save_kit(kit)
    return jsonify({'deleted': kit_id})


@bp.route('/seed', methods=['POST'])
def seed():
    """Reset to default data. Useful for AI sessions starting fresh."""
    get_db().set_page_data(PAGE, 'nodes', DEFAULT_NODES)
    get_db().set_page_data(PAGE, 'kit', DEFAULT_KIT)
    return jsonify({'seeded': True, 'nodes': len(DEFAULT_NODES), 'kit': len(DEFAULT_KIT)})
