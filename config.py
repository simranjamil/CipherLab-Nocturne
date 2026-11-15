
"""Project-wide constants for CipherLab - Nocturne Triad edition."""

import os
from dotenv import load_dotenv
load_dotenv()

CIPHER_NAME = "Nocturne Triad"
CIPHER_CODE = "NTC"
COURSE_LINE = "CT-486 · Network and Information Security"
ACTIVITY_LINE = "Classical Cipher Challenge · Blue Team"

# Reveal Mode passcode (stored in environment variable)
REVEAL_CODE = os.environ.get("CIPHERLAB_REVEAL_CODE")

if not REVEAL_CODE:
    raise RuntimeError(
        "CIPHERLAB_REVEAL_CODE is missing. "
        "Set it in your environment before running the app."
    )

CHALLENGE_PAIRS = 10
CHALLENGE_WRONG = 3
