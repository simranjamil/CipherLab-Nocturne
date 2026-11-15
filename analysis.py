"""Strength-analysis helpers: letter counts, avalanche, key space, timing."""

import math
import random
import re
import statistics
import time

import hill
from alphabet import STD_ALPHABET
from hybrid_cipher import decrypt_hybrid, encrypt_hybrid

SAMPLE_TEXT = (
    "The morning train arrived a few minutes late and the platform filled quickly with "
    "students, workers and travellers carrying heavy bags. A gentle rain had started during "
    "the night, so the streets were quiet and the air smelled of wet stone. Inside the old "
    "station a small cafe was already open, and the owner greeted each customer by name while "
    "preparing tea and fresh bread. Outside, the clock above the entrance struck eight, and "
    "the crowd slowly moved toward the city centre."
)


def letters_only(text):
    """Keep A-Z only, upper-case, J written as I."""
    return re.sub(r"[^A-Za-z]", "", str(text)).upper().replace("J", "I")


def letter_frequency(text):
    """Percentage of each of the 25 letters, in alphabet order."""
    total = len(text) or 1
    return [100.0 * text.count(ch) / total for ch in STD_ALPHABET]


def index_of_coincidence(text):
    n = len(text)
    if n < 2:
        return 0.0
    return sum(text.count(ch) * (text.count(ch) - 1) for ch in STD_ALPHABET) / (n * (n - 1))


def avalanche(plaintext, k1, k2, k3, trials=500, seed=1):
    """Change one plaintext letter at random; count changed ciphertext letters."""
    rng = random.Random(seed)
    base = encrypt_hybrid(plaintext, k1, k2, k3)["ciphertext"]
    counts = []
    for _ in range(trials):
        pos = rng.randrange(len(plaintext))
        alt = rng.choice([c for c in STD_ALPHABET if c != plaintext[pos]])
        changed = plaintext[:pos] + alt + plaintext[pos + 1:]
        ct = encrypt_hybrid(changed, k1, k2, k3)["ciphertext"]
        counts.append(sum(a != b for a, b in zip(base, ct)))
    return counts


def sci(n):
    """Format a big integer as 'a.b x 10^e'."""
    if n < 10 ** 6:
        return f"{n:,}"
    exp = len(str(n)) - 1
    return f"{n / 10 ** exp:.2f} x 10^{exp}"


def key_space(k1, k2, k3):
    """Brute-force sizes for RANDOM keys of the given shapes."""
    k1 = "".join(k1.split())
    k2_distinct = len(set("".join(k2.split()).upper().replace("J", "I")))
    m = int(math.isqrt(len("".join(k3.split()))))
    parts = [
        ("Key 1", 25 ** len(k1)),
        ("Key 2", math.perm(25, min(k2_distinct, 25))),
        ("Key 3", hill.group_size(m)),
    ]
    total = 1
    for _, size in parts:
        total *= size
    return parts, total


def bits(n):
    return math.log2(n)


# ----- timing ----------------------------------------------------------------

def shift_encrypt(message, shift=3):
    return "".join(chr((ord(c) - 65 + shift) % 26 + 65) for c in message)


def shift_decrypt(message, shift=3):
    return "".join(chr((ord(c) - 65 - shift) % 26 + 65) for c in message)


def benchmark(k1, k2, k3, lengths=(100, 500, 1000, 5000, 10000), reps=10):
    rows = []
    for n in lengths:
        plain = (STD_ALPHABET * (n // 25 + 1))[:n]
        he, hd, se, sd = [], [], [], []
        for _ in range(reps):
            t = time.perf_counter()
            enc = encrypt_hybrid(plain, k1, k2, k3)["ciphertext"]
            he.append((time.perf_counter() - t) * 1000)
            t = time.perf_counter()
            decrypt_hybrid(enc, k1, k2, k3)
            hd.append((time.perf_counter() - t) * 1000)
            t = time.perf_counter()
            sc = shift_encrypt(plain)
            se.append((time.perf_counter() - t) * 1000)
            t = time.perf_counter()
            shift_decrypt(sc)
            sd.append((time.perf_counter() - t) * 1000)
        rows.append({
            "Message Length": n,
            "Triad Encryption (ms)": round(statistics.median(he), 4),
            "Shift Encryption (ms)": round(statistics.median(se), 4),
            "Triad Decryption (ms)": round(statistics.median(hd), 4),
            "Shift Decryption (ms)": round(statistics.median(sd), 4),
        })
    return rows
