"""Stage 3 - Hill cipher modulo 25 with ciphertext stealing (no padding).

* The key is m*m letters (9, 16 or 25) read row by row into an m x m matrix.
  Key letters are numbered A=0 ... Z=24 (no J).
* The matrix must be invertible modulo 25  <=>  its determinant is not a
  multiple of 5.  It must also mix: every row and column needs at least two
  non-zero entries, otherwise a letter would only depend on itself.
* Text letters are numbered by the keyed alphabet.
* If the length is not a multiple of m, the last short block is handled with
  ciphertext stealing, so no padding letters and no metadata are needed and
  the ciphertext has exactly the same length as the plaintext.
"""

import math
import random

from alphabet import MOD, STD_ALPHABET, STD_INDEX, clean_key, index_map

ALLOWED_SIZES = (3, 4, 5)           # block sizes -> key lengths 9, 16, 25


def key_lengths():
    return [m * m for m in ALLOWED_SIZES]


# ----- small integer linear algebra (m <= 5) --------------------------------

def _minor(M, i, j):
    return [row[:j] + row[j + 1:] for k, row in enumerate(M) if k != i]


def _det(M):
    n = len(M)
    if n == 1:
        return M[0][0]
    if n == 2:
        return M[0][0] * M[1][1] - M[0][1] * M[1][0]
    return sum((-1) ** j * M[0][j] * _det(_minor(M, 0, j)) for j in range(n))


def inverse_mod(M, mod=MOD):
    """Inverse matrix modulo `mod`; ValueError if it does not exist."""
    n = len(M)
    d = _det(M) % mod
    if math.gcd(d, mod) != 1:
        raise ValueError("is not usable (matrix not invertible) - generate a new key.")
    d_inv = pow(d, -1, mod)
    return [
        [(d_inv * (-1) ** (i + j) * _det(_minor(M, j, i))) % mod for j in range(n)]
        for i in range(n)
    ]


def _mix_ok(M):
    n = len(M)
    rows = all(sum(1 for v in row if v % MOD) >= 2 for row in M)
    cols = all(sum(1 for r in range(n) if M[r][c] % MOD) >= 2 for c in range(n))
    return rows and cols


# ----- key handling ----------------------------------------------------------

def key_to_matrix(key):
    key = clean_key(key)
    m = math.isqrt(len(key))
    if m * m != len(key) or m not in ALLOWED_SIZES:
        raise ValueError(f"needs exactly {', '.join(map(str, key_lengths()))} letters.")
    vals = [STD_INDEX[ch] for ch in key]
    return [vals[r * m:(r + 1) * m] for r in range(m)]


def validate_key(key):
    """Return (matrix, inverse) or raise ValueError."""
    M = key_to_matrix(key)
    inv = inverse_mod(M)
    if not _mix_ok(M):
        raise ValueError("is too simple (a row or column has fewer than 2 non-zero letters).")
    return M, inv


def random_key(m=4, rng=None):
    """Random valid key with m*m letters."""
    rng = rng or random.SystemRandom()
    while True:
        key = "".join(rng.choice(STD_ALPHABET) for _ in range(m * m))
        try:
            validate_key(key)
            return key
        except ValueError:
            continue


def group_size(m):
    """Number of invertible m x m matrices modulo 25."""
    gl_mod5 = 1
    for i in range(m):
        gl_mod5 *= 5 ** m - 5 ** i
    return 5 ** (m * m) * gl_mod5


# ----- encryption / decryption ----------------------------------------------

def _apply(M, block):
    m = len(M)
    return [sum(M[r][c] * block[c] for c in range(m)) % MOD for r in range(m)]


def encrypt_hill(text, key, alphabet):
    M, _ = validate_key(key)
    m = len(M)
    idx = index_map(alphabet)
    vals = [idx[ch] for ch in text]
    n = len(vals)
    if n < m:
        raise ValueError(f"needs at least {m} letters for this key size.")
    q, r = divmod(n, m)
    out = []
    for b in range(q):
        out += _apply(M, vals[b * m:(b + 1) * m])
    if r:
        last_block = out[(q - 1) * m:q * m]
        stolen = last_block[r:] + vals[q * m:]            # (m-r) + r = m values
        out = out[:(q - 1) * m] + last_block[:r] + _apply(M, stolen)
    return "".join(alphabet[v] for v in out)


def decrypt_hill(text, key, alphabet):
    _, inv = validate_key(key)
    m = len(inv)
    idx = index_map(alphabet)
    vals = [idx[ch] for ch in text]
    n = len(vals)
    if n < m:
        raise ValueError(f"needs at least {m} letters for this key size.")
    q, r = divmod(n, m)
    plain = []
    if r == 0:
        for b in range(q):
            plain += _apply(inv, vals[b * m:(b + 1) * m])
    else:
        head = vals[:(q - 1) * m]
        part = vals[(q - 1) * m:(q - 1) * m + r]
        tail_cipher = vals[(q - 1) * m + r:]
        w = _apply(inv, tail_cipher)                      # = last_block[r:] + short tail
        last_block = part + w[:m - r]
        short_tail = w[m - r:]
        for b in range(q - 1):
            plain += _apply(inv, head[b * m:(b + 1) * m])
        plain += _apply(inv, last_block)
        plain += short_tail
    return "".join(alphabet[v] for v in plain)
