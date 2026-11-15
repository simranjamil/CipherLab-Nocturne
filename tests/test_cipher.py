"""Cipher tests.  Run from the project folder:

    python tests/test_cipher.py        (plain Python)
    python -m pytest tests             (if pytest is installed)
"""

import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import hill
import playfair
from alphabet import MOD, STD_ALPHABET, keyed_alphabet
from challenge import build_challenge
from hybrid_cipher import check_keys, decrypt_hybrid, encrypt_hybrid, generate_keys


def rand_text(rng, n):
    return "".join(rng.choice(STD_ALPHABET) for _ in range(n))


def test_playfair_matches_textbook_vector():
    # Classic worked example (key PLAYFAIR EXAMPLE) - only pairs of two different letters,
    # so the Mirror rule is not involved and standard Playfair must be reproduced.
    alphabet = keyed_alphabet("PLAYFAIREXAMPLE")
    assert playfair.encrypt_playfair("HIDETHEGOLDINTHE", alphabet) == "BMODZBXDNABEKUDM"
    assert playfair.decrypt_playfair("BMODZBXDNABEKUDM", alphabet) == "HIDETHEGOLDINTHE"


def test_mirror_rule_and_lone_letter():
    alphabet = keyed_alphabet("PLAYFAIREXAMPLE")      # row 0 = P L A Y F
    assert playfair.encrypt_playfair("LL", alphabet) == "AA"      # L -> A (right neighbour)
    assert playfair.encrypt_playfair("F", alphabet) == "P"        # wraps around the row
    assert playfair.decrypt_playfair("AA", alphabet) == "LL"


def test_hill_inverse_is_identity():
    rng = random.Random(1)
    for m in hill.ALLOWED_SIZES:
        for _ in range(25):
            key = hill.random_key(m, rng)
            M, inv = hill.validate_key(key)
            for i in range(m):
                for j in range(m):
                    got = sum(M[i][k] * inv[k][j] for k in range(m)) % MOD
                    assert got == (1 if i == j else 0)


def test_hill_rejects_bad_keys():
    for bad in ("AAAAAAAAA", "ABCDEFGHI" * 2, "ABCDEFGH"):
        try:
            hill.validate_key(bad)
        except ValueError:
            continue
        raise AssertionError(f"{bad!r} should have been rejected")
    # identity matrix: invertible but does not mix
    try:
        hill.validate_key("BAAABAAAB")
    except ValueError:
        pass
    else:
        raise AssertionError("identity key should have been rejected")


def test_hill_group_size_matches_brute_force_ratio():
    # fraction of random 3x3 keys that are invertible should be close to the formula
    rng = random.Random(3)
    ok = 0
    trials = 4000
    for _ in range(trials):
        key = "".join(rng.choice(STD_ALPHABET) for _ in range(9))
        try:
            hill.inverse_mod(hill.key_to_matrix(key))
            ok += 1
        except ValueError:
            pass
    expected = hill.group_size(3) / 25 ** 9
    assert abs(ok / trials - expected) < 0.03


def test_roundtrip_many_random_cases():
    rng = random.Random(7)
    for _ in range(3000):
        m = rng.choice(hill.ALLOWED_SIZES)
        k1 = rand_text(rng, rng.randint(10, 20))
        k2 = "".join(rng.sample(STD_ALPHABET, rng.randint(10, 20)))
        k3 = hill.random_key(m, rng)
        n = rng.randint(m, 150)
        pt = rand_text(rng, n)
        if rng.random() < 0.3:                                   # force doubled letters
            pt = "".join(c * rng.choice([1, 2, 3]) for c in pt)[:max(n, m)]
        enc = encrypt_hybrid(pt, k1, k2, k3)
        assert len(enc["ciphertext"]) == len(pt)                 # length preserved
        assert decrypt_hybrid(enc["ciphertext"], k1, k2, k3)["original"] == pt


def test_every_tail_length_for_every_block_size():
    rng = random.Random(11)
    for m in hill.ALLOWED_SIZES:
        k1, k2, k3 = generate_keys(m)
        for n in range(m, 6 * m + 1):                            # all remainders, several blocks
            pt = rand_text(rng, n)
            enc = encrypt_hybrid(pt, k1, k2, k3)
            assert decrypt_hybrid(enc["ciphertext"], k1, k2, k3)["original"] == pt


def test_j_is_written_as_i_and_spaces_removed():
    k1, k2, k3 = generate_keys(3)
    enc = encrypt_hybrid("Just a quick jam session", k1, k2, k3)
    assert enc["original"] == "IUSTAQUICKIAMSESSION"
    assert len(enc["notes"]) == 2


def test_punctuation_is_stripped_but_digits_rejected():
    k1, k2, k3 = generate_keys(3)
    enc = encrypt_hybrid("Meet me, at the library!", k1, k2, k3)
    assert enc["original"] == "MEETMEATTHELIBRARY"
    assert any("punctuation" in n for n in enc["notes"])


def test_input_validation():
    k1, k2, k3 = generate_keys(3)
    for bad in ("", "HELLO123", "HÉLLO", "a+b"):
        try:
            encrypt_hybrid(bad, k1, k2, k3)
        except ValueError:
            continue
        raise AssertionError(f"{bad!r} should be rejected")
    assert not check_keys("SHORT", k2, k3)["ok"]
    assert not check_keys(k1, "AAAAAAAAAAAA", k3)["ok"]
    assert check_keys(k1, k2, k3)["ok"]


def test_challenge_builder():
    rng = random.Random(5)
    plains = [rand_text(rng, 60) for _ in range(10)]
    k1, k2, k3 = generate_keys(4)
    for method in ("plaintext", "key"):
        data = build_challenge(plains, k1, k2, k3, wrong=[1, 4, 8], method=method, seed=9)
        assert len(data["rows"]) == 10
        assert sum(1 for r in data["rows"] if not r["valid"]) == 3
        for i, row in enumerate(data["rows"]):
            true_ct = encrypt_hybrid(row["plaintext"], k1, k2, k3)["ciphertext"]
            if row["valid"]:
                assert row["shown"] == true_ct
            else:
                assert row["shown"] != true_ct
                assert len(row["shown"]) == len(true_ct)         # no length tell
        assert len(data["fingerprint"]) == 64


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_")]
    for name, fn in tests:
        fn()
        print(f"PASS  {name}")
    print(f"\n{len(tests)} tests passed")
