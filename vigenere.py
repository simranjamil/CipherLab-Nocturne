"""Stage 1 - Vigenere over the keyed 25-letter alphabet (mod 25)."""

from alphabet import MOD, STD_INDEX, clean_key, index_map

MIN_KEY_LEN = 10


def validate_key(key):
    key = clean_key(key)
    if len(key) < MIN_KEY_LEN:
        raise ValueError(f"needs at least {MIN_KEY_LEN} letters.")
    return key


def _shifts(key):
    return [STD_INDEX[ch] for ch in key]


def encrypt_vigenere(text, key, alphabet):
    key = validate_key(key)
    idx = index_map(alphabet)
    shifts = _shifts(key)
    return "".join(
        alphabet[(idx[ch] + shifts[i % len(shifts)]) % MOD]
        for i, ch in enumerate(text)
    )


def decrypt_vigenere(text, key, alphabet):
    key = validate_key(key)
    idx = index_map(alphabet)
    shifts = _shifts(key)
    return "".join(
        alphabet[(idx[ch] - shifts[i % len(shifts)]) % MOD]
        for i, ch in enumerate(text)
    )
