"""Alphabet rules shared by all three stages.

Working alphabet = 25 letters (A-Z without J, because I and J share a cell in
the Playfair square).  Every stage works modulo 25.

* Text letters are numbered by their position in the KEYED alphabet
  (the Playfair square read row by row).
* Key letters (stage 1 and stage 3 keys) are numbered in the STANDARD order
  A=0 ... I=8, K=9 ... Z=24, so the key checks do not depend on the Playfair key.
"""

STD_ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
MOD = 25
STD_INDEX = {ch: i for i, ch in enumerate(STD_ALPHABET)}
PUNCTUATION = set(".,;:!?'\"()-–—‘’“”")   # stripped from messages


def clean_key(key):
    """Upper-case, strip spaces, J -> I. Raises ValueError for non-letters."""
    key = "".join(str(key).split()).upper()
    if not key:
        raise ValueError("is empty.")
    if not (key.isascii() and key.isalpha()):
        raise ValueError("may contain English letters A-Z only.")
    return key.replace("J", "I")


def prepare_text(text):
    """Normalise plaintext/ciphertext.

    Returns (clean_text, notes).  Spaces and line breaks are removed and J is
    written as I.  Digits, punctuation and non-English letters are rejected.
    """
    raw = str(text)
    stripped = "".join(raw.split())
    removed_spaces = len(raw) - len(stripped)
    no_punct = "".join(ch for ch in stripped if ch not in PUNCTUATION)
    removed_punct = len(stripped) - len(no_punct)
    stripped = no_punct
    if not stripped:
        raise ValueError("Enter a message first.")
    if not (stripped.isascii() and stripped.isalpha()):
        raise ValueError(
            "Use English letters A-Z only. Spaces and common punctuation are removed, "
            "but digits and other symbols are not allowed."
        )
    upper = stripped.upper()
    notes = []
    if removed_spaces:
        notes.append(f"{removed_spaces} space/line-break character(s) removed")
    if removed_punct:
        notes.append(f"{removed_punct} punctuation mark(s) removed")
    j_count = upper.count("J")
    if j_count:
        notes.append(f"{j_count} letter J written as I")
    return upper.replace("J", "I"), notes


def keyed_alphabet(playfair_key):
    """25-letter alphabet: unique key letters first, then the unused letters."""
    key = clean_key(playfair_key)
    seen = []
    for ch in key + STD_ALPHABET:
        if ch not in seen:
            seen.append(ch)
    return "".join(seen)


def index_map(alphabet):
    return {ch: i for i, ch in enumerate(alphabet)}
