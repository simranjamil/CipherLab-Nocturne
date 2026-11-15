"""The three-stage cipher: Vigenere -> Mirror-Playfair -> Hill.

No metadata is produced or needed: ciphertext + three keys are enough.
"""

import random
import secrets

import hill
import playfair
import vigenere
from alphabet import STD_ALPHABET, keyed_alphabet, prepare_text


def encrypt_hybrid(plaintext, key1, key2, key3):
    clean, notes = prepare_text(plaintext)
    alphabet = keyed_alphabet(playfair.validate_key(key2))
    stage1 = vigenere.encrypt_vigenere(clean, key1, alphabet)
    stage2 = playfair.encrypt_playfair(stage1, alphabet)
    stage3 = hill.encrypt_hill(stage2, key3, alphabet)
    return {
        "original": clean,
        "notes": notes,
        "stage1": stage1,
        "stage2": stage2,
        "ciphertext": stage3,
    }


def decrypt_hybrid(ciphertext, key1, key2, key3):
    clean, notes = prepare_text(ciphertext)
    alphabet = keyed_alphabet(playfair.validate_key(key2))
    stage2 = hill.decrypt_hill(clean, key3, alphabet)
    stage1 = playfair.decrypt_playfair(stage2, alphabet)
    plain = vigenere.decrypt_vigenere(stage1, key1, alphabet)
    return {
        "ciphertext": clean,
        "notes": notes,
        "stage2": stage2,
        "stage1": stage1,
        "original": plain,
    }


def check_keys(key1, key2, key3):
    """Validate all keys. Returns {'ok': bool, 'errors': [...], 'block': m or None}."""
    errors = []
    block = None
    for label, fn, key in (
        ("Key 1", vigenere.validate_key, key1),
        ("Key 2", playfair.validate_key, key2),
        ("Key 3", lambda k: hill.validate_key(k)[0], key3),
    ):
        try:
            result = fn(key)
            if label == "Key 3":
                block = len(result)
        except ValueError as exc:
            errors.append(f"{label} {exc}")
    return {"ok": not errors, "errors": errors, "block": block}


def generate_keys(hill_block=5):
    """Fresh random keys: (key1, key2, key3)."""
    rng = random.SystemRandom()
    key1 = "".join(secrets.choice(STD_ALPHABET) for _ in range(14))
    key2 = "".join(rng.sample(STD_ALPHABET, 14))
    key3 = hill.random_key(hill_block, rng)
    return key1, key2, key3
