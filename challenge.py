"""Challenge dataset builder: 10 plaintext-ciphertext pairs (7 correct, 3 wrong)."""

import csv
import hashlib
import io
import json
import random

from alphabet import STD_ALPHABET, prepare_text
from config import CHALLENGE_PAIRS, CHALLENGE_WRONG, CIPHER_NAME
from hybrid_cipher import encrypt_hybrid

METHODS = {
    "plaintext": "Altered plaintext (2-3 letters changed, then encrypted)",
    "key": "One letter of key 1 changed during encryption",
}

# Neutral sample sentences (no J, no hints about the cipher).  Replace with your own.
SAMPLE_PLAINTEXTS = [
    "THE LIBRARY OPENS EARLY ON FRIDAY MORNING FOR THE FINAL YEAR STUDENTS",
    "A SMALL RIVER RUNS BEHIND THE OLD STATION AND FEEDS THE NORTHERN FIELDS",
    "PLEASE BRING YOUR LAPTOP AND CHARGER TO THE LAB BEFORE NOON TOMORROW",
    "THE COMMITTEE REVIEWED EVERY PROPOSAL CAREFULLY AND ANNOUNCED THREE WINNERS",
    "HEAVY RAIN DELAYED THE EVENING TRAIN BY ALMOST FORTY MINUTES YESTERDAY",
    "OUR TEAM MEETS EVERY WEDNESDAY TO DISCUSS PROGRESS AND PLAN THE NEXT STEPS",
    "THE OLD LIGHTHOUSE STILL GUIDES SMALL BOATS ACROSS THE QUIET HARBOUR AT NIGHT",
    "EVERY STUDENT MUST SUBMIT THE REPORT BEFORE THE DEADLINE TO AVOID PENALTIES",
    "A WARM BREEZE CARRIED THE SMELL OF FRESH BREAD THROUGH THE SLEEPING STREETS",
    "THE FINAL RESULTS WILL BE PUBLISHED ON THE NOTICE BOARD NEXT MONDAY AFTERNOON",
]


def parse_plaintexts(raw_text, block):
    """Turn the text box into 10 cleaned plaintexts. Returns (list, warnings)."""
    lines = [ln for ln in str(raw_text).splitlines() if ln.strip()]
    if len(lines) != CHALLENGE_PAIRS:
        raise ValueError(
            f"Enter exactly {CHALLENGE_PAIRS} plaintexts, one per line "
            f"(you entered {len(lines)})."
        )
    cleaned, warnings = [], []
    for i, line in enumerate(lines, 1):
        try:
            text, notes = prepare_text(line)
        except ValueError as exc:
            raise ValueError(f"Line {i}: {exc}")
        if len(text) < max(block, 20):
            raise ValueError(f"Line {i}: only {len(text)} letters - use at least {max(block, 20)}.")
        if not 40 <= len(text) <= 80:
            warnings.append(f"Line {i}: {len(text)} letters (40-80 recommended).")
        for note in notes:
            if "J" in note:
                warnings.append(f"Line {i}: {note}.")
        cleaned.append(text)
    if len(set(cleaned)) != len(cleaned):
        warnings.append("Two plaintexts are identical - the Red Team would see the structure.")
    return cleaned, warnings


def _alter_plaintext(text, rng):
    chars = list(text)
    for pos in rng.sample(range(len(chars)), min(rng.choice([2, 3]), len(chars))):
        chars[pos] = rng.choice([c for c in STD_ALPHABET if c != chars[pos]])
    return "".join(chars)


def _tweak_key(key, rng):
    key = "".join(key.split()).upper().replace("J", "I")
    pos = rng.randrange(len(key))
    new = rng.choice([c for c in STD_ALPHABET if c != key[pos]])
    return key[:pos] + new + key[pos + 1:]


def build_challenge(plaintexts, key1, key2, key3, wrong, method="plaintext", seed=2026):
    """plaintexts: cleaned strings. wrong: 0-based indices of the wrong pairs."""
    wrong = sorted(set(wrong))
    if len(wrong) != CHALLENGE_WRONG:
        raise ValueError(f"Choose exactly {CHALLENGE_WRONG} wrong pairs.")
    rng = random.Random(seed)
    rows = []
    for i, text in enumerate(plaintexts):
        true_ct = encrypt_hybrid(text, key1, key2, key3)["ciphertext"]
        shown, how = true_ct, "correct"
        if i in wrong:
            for _ in range(50):                                  # make sure it really differs
                if method == "key":
                    shown = encrypt_hybrid(text, _tweak_key(key1, rng), key2, key3)["ciphertext"]
                    how = METHODS["key"]
                else:
                    shown = encrypt_hybrid(_alter_plaintext(text, rng), key1, key2, key3)["ciphertext"]
                    how = METHODS["plaintext"]
                if shown != true_ct:
                    break
        rows.append({
            "no": i + 1,
            "plaintext": text,
            "shown": shown,
            "valid": i not in wrong,
            "true": true_ct,
            "how": how,
        })
    payload = {
        "cipher": CIPHER_NAME,
        "keys": ["".join(k.split()).upper().replace("J", "I") for k in (key1, key2, key3)],
        "pairs": [[r["plaintext"], r["shown"]] for r in rows],
    }
    fingerprint = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    return {
        "rows": rows,
        "fingerprint": fingerprint,
        "method": method,
        "seed": seed,
        "wrong": [i + 1 for i in wrong],
    }


def red_team_csv(data):
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["Pair", "Plaintext", "Ciphertext"])
    for r in data["rows"]:
        writer.writerow([r["no"], r["plaintext"], r["shown"]])
    return buf.getvalue()


def answer_sheet_csv(data):
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["Pair", "Valid", "Plaintext", "Ciphertext given to Red Team",
                     "Correct ciphertext", "How the wrong pair was made"])
    for r in data["rows"]:
        writer.writerow([r["no"], "YES" if r["valid"] else "NO", r["plaintext"],
                         r["shown"], r["true"], "" if r["valid"] else r["how"]])
    writer.writerow([])
    writer.writerow(["SHA-256 fingerprint", data["fingerprint"]])
    return buf.getvalue()
