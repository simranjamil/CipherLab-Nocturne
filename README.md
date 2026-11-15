# CipherLab · Nocturne Triad (Blue Team edition)

Three-layer classical cipher for the CT-486 Classical Cipher Challenge, with a dark navy/purple Streamlit app.

**Pipeline:** Plaintext → Vigenère → Playfair (Mirror rule) → Hill → Ciphertext
Ciphertext length = plaintext length. No metadata. Decryption needs only the ciphertext and three keys.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Run the tests:

```bash
python tests/test_cipher.py        # cipher maths (11 tests)
python apptest_all_pages.py        # every page of the app
```

## Files

| File | Purpose |
|---|---|
| `app.py` | Streamlit app: Dashboard, Encryption Studio, Challenge Generator, Strength Analysis, Algorithm Info |
| `theme.py` | Navy/purple CSS and HTML components |
| `config.py` | Cipher name, course line, Reveal passcode |
| `alphabet.py` | 25-letter keyed alphabet, input cleaning |
| `vigenere.py` · `playfair.py` · `hill.py` | The three stages |
| `hybrid_cipher.py` | Combines the stages, key validation, random key generator |
| `challenge.py` | Builds the 10 pairs (7 correct, 3 wrong), CSV export, SHA-256 fingerprint |
| `analysis.py` | Letter frequency, index of coincidence, change-spreading test, key space, benchmark |
| `.streamlit/config.toml` | Dark theme colours |

## Challenge Mode and Reveal Mode

* The app starts in **Challenge Mode**: stage names, stage outputs, the Algorithm Info page and per-stage key sizes are hidden.
* Unlock **Reveal Mode** in the sidebar with the passcode in `config.py` (default `reveal-after-challenge`; override with the `CIPHERLAB_REVEAL_CODE` environment variable). Use it for the final explanation (Deliverable 5).
* This is a screen-level gate only. The source code contains the algorithm, so **keep the repository private until the challenge is over**.

## Keys

* Random keys are generated on every start; nothing is hard-coded. Copy them out of the Key Vault and store them safely - they are not saved anywhere.
* Key 1 (Vigenère): at least 10 letters. Key 2 (Playfair): at least 10 different letters. Key 3 (Hill): 9, 16 or 25 letters forming an invertible matrix.
* Use random keys, never words or course terms.
* An odd Hill size (9 or 25 letters) spreads a one-letter change further than 16, because 16 lines up with Playfair's letter pairs. Default is 25.

## Special rules (for Deliverable 3)

1. 25-letter keyed alphabet (A-Z without J, J written as I) shared by all stages; spaces and common punctuation are removed.
2. Mirror rule in Playfair: doubled letters both move one step right; a lone last letter moves one step right. No filler.
3. Ciphertext stealing in Hill: no padding.
4. Hill key must be invertible mod 25 (determinant not a multiple of 5) and must mix (every row and column has at least two non-zero entries).

## Known limitations

Hill is linear: if the output of stages 1 and 2 is known (for instance by guessing keys 1 and 2), key 3 follows from linear algebra. Security depends on keys 1 and 2 being long and random. This is an educational classical cipher, not for real data.
