from flask import Blueprint, jsonify, request
import os

api = Blueprint('scrabble_tracker_api', __name__)

# Load dictionary into memory for fast lookups
DICTIONARY = set()
DICTIONARY_LOADED = False

def load_dictionary():
    """Load the Scrabble dictionary into memory"""
    global DICTIONARY, DICTIONARY_LOADED

    if DICTIONARY_LOADED:
        return

    dict_path = os.path.join(os.path.dirname(__file__), 'scrabble_dictionary.txt')

    try:
        with open(dict_path, 'r', encoding='utf-8') as f:
            # Load all words and normalize to lowercase
            DICTIONARY = set(line.strip().lower() for line in f if line.strip())

        DICTIONARY_LOADED = True
        print(f"Loaded {len(DICTIONARY)} words into Scrabble dictionary")
    except Exception as e:
        print(f"Error loading Scrabble dictionary: {e}")

# Load dictionary when module is imported
load_dictionary()

@api.route('/check-word')
def check_word():
    """Check if a word is valid in the Scrabble dictionary"""
    word = request.args.get('word', '').strip().lower()

    if not word:
        return jsonify({'error': 'No word provided'}), 400

    # Check if word is in dictionary
    is_valid = word in DICTIONARY

    return jsonify({
        'word': word.upper(),
        'valid': is_valid,
        'length': len(word)
    })

@api.route('/stats')
def get_stats():
    """Get dictionary statistics"""
    return jsonify({
        'total_words': len(DICTIONARY),
        'dictionary_loaded': DICTIONARY_LOADED
    })

@api.route('/search')
def search_words():
    """Search for words matching a pattern (useful for finding valid words)"""
    pattern = request.args.get('pattern', '').strip().lower()
    limit = int(request.args.get('limit', 50))

    if not pattern:
        return jsonify({'error': 'No pattern provided'}), 400

    # Simple pattern matching - words that start with pattern
    matching_words = [
        word for word in DICTIONARY
        if word.startswith(pattern)
    ][:limit]

    return jsonify({
        'pattern': pattern,
        'matches': sorted(matching_words),
        'count': len(matching_words),
        'showing': min(len(matching_words), limit)
    })
