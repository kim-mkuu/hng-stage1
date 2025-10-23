import hashlib

def calculate_properties(value):
    """Calculate all properties for a given string"""

    sha256_hash = hashlib.sha256(value.encode('utf-8')).hexdigest()

    length= len(value)

    is_palindrome = value.lower() == value.lower()[::-1]

    unique_characters = len(set(value))

    word_count = len(value.split())

    character_frequency_map = {}
    for char in value:
        character_frequency_map[char] = character_frequency_map.get(char, 0) + 1

    return {
        'sha256_hash': sha256_hash,
        'length': length,
        'is_palindrome': is_palindrome,
        'unique_characters': unique_characters,
        'word_count': word_count,
        'character_frequency_map': character_frequency_map
    }
