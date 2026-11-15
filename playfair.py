"""Stage 2 - Playfair with the Mirror rule (no filler letters, no metadata).

Standard Playfair inserts filler letters, which is why the old CipherLab had to
carry "filler positions" around.  Here the text is simply cut into consecutive
pairs and every case has a reversible rule:

    two different letters, same row     -> letter to the right of each
    two different letters, same column  -> letter below each
    two different letters, rectangle    -> swap the columns
    Mirror rule: doubled pair (LL)      -> both become the letter right of L
    lone last letter (odd length)       -> letter to its right

Ciphertext length always equals plaintext length.
"""

from alphabet import clean_key, keyed_alphabet

MIN_DISTINCT = 10


def validate_key(key):
    key = clean_key(key)
    if len(set(key)) < MIN_DISTINCT:
        raise ValueError(f"needs at least {MIN_DISTINCT} different letters.")
    return key


def generate_matrix(key):
    """5x5 matrix (list of rows) for display."""
    alphabet = keyed_alphabet(validate_key(key))
    return [list(alphabet[i:i + 5]) for i in range(0, 25, 5)]


def _crypt(text, alphabet, sign):
    pos = {ch: divmod(i, 5) for i, ch in enumerate(alphabet)}

    def at(r, c):
        return alphabet[(r % 5) * 5 + (c % 5)]

    out = []
    i = 0
    while i < len(text):
        a = text[i]
        ra, ca = pos[a]
        if i + 1 == len(text):                       # lone last letter
            out.append(at(ra, ca + sign))
            break
        b = text[i + 1]
        rb, cb = pos[b]
        if a == b:                                   # Mirror rule
            out.append(at(ra, ca + sign) * 2)
        elif ra == rb:                               # same row
            out.append(at(ra, ca + sign) + at(rb, cb + sign))
        elif ca == cb:                               # same column
            out.append(at(ra + sign, ca) + at(rb + sign, cb))
        else:                                        # rectangle (self-inverse)
            out.append(at(ra, cb) + at(rb, ca))
        i += 2
    return "".join(out)


def encrypt_playfair(text, alphabet):
    return _crypt(text, alphabet, +1)


def decrypt_playfair(text, alphabet):
    return _crypt(text, alphabet, -1)
