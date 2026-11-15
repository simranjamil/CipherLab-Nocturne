
# CipherLab · Nocturne Triad (Blue Team Edition)

Three-layer classical cipher for the CT-486 Classical Cipher Challenge, with a dark navy/purple Streamlit app.

**Pipeline:** Plaintext → Vigenère → Playfair (Mirror rule) → Hill → Ciphertext

Ciphertext length = plaintext length. No metadata. Decryption needs only the ciphertext and three keys.

## Run

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd CipherLab-Nocturne
```

### 2. Create and activate a virtual environment

Windows:

```powershell
python -m venv venv
.\venv\Scripts\Activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Reveal Mode passcode

Create a `.env` file in the project root directory (the same directory as `app.py`).

Add your private passcode:

```env
CIPHERLAB_REVEAL_CODE=your-private-passcode
```

**Important:**
- Never upload your `.env` file to GitHub.
- The `.env` file is excluded through `.gitignore`.
- Never hardcode the actual passcode in `config.py`.
- A `.env.example` file may be provided with a placeholder value for reference.

### 5. Start the application

```bash
streamlit run app.py
```

## Run the Tests

Cipher mathematics (11 tests):

```bash
python tests/test_cipher.py
```

Test every page of the app:

```bash
python apptest_all_pages.py
```

## Files

| File | Purpose |
|---|---|
| `app.py` | Streamlit app: Dashboard, Encryption Studio, Challenge Generator, Strength Analysis, Algorithm Info |
| `theme.py` | Navy/purple CSS and HTML components |
| `config.py` | Cipher name, course line, and environment-based Reveal Mode passcode |
| `.env` | Stores the private Reveal Mode passcode locally; never commit this file |
| `.env.example` | Example environment configuration with a placeholder passcode |
| `.gitignore` | Excludes private files, environment secrets, and generated files |
| `alphabet.py` | 25-letter keyed alphabet, input cleaning |
| `vigenere.py` · `playfair.py` · `hill.py` | The three cipher stages |
| `hybrid_cipher.py` | Combines the stages, key validation, random key generator |
| `challenge.py` | Builds the 10 pairs (7 correct, 3 wrong), CSV export, SHA-256 fingerprint |
| `analysis.py` | Letter frequency, index of coincidence, change-spreading test, key space, benchmark |
| `.streamlit/config.toml` | Dark theme colours |
| `requirements.txt` | Python dependencies |

## Challenge Mode and Reveal Mode

- The app starts in **Challenge Mode**: stage names, stage outputs, the Algorithm Info page and per-stage key sizes are hidden.
- Unlock **Reveal Mode** in the sidebar using the passcode configured through the `CIPHERLAB_REVEAL_CODE` environment variable.
- For local development, create a `.env` file using `.env.example` as a reference.
- Use Reveal Mode for the final explanation (Deliverable 5).
- The Reveal Mode passcode is not hardcoded in `config.py`.
- The screen-level gate only controls what is displayed in the app. The source code still contains the algorithm, so **keep the repository private until the challenge is over**.

## Keys

- Random keys are generated on every start; nothing is hard-coded. Copy them out of the Key Vault and store them safely — they are not saved anywhere.
- Key 1 (Vigenère): at least 10 letters.
- Key 2 (Playfair): at least 10 different letters.
- Key 3 (Hill): 9, 16 or 25 letters forming an invertible matrix.
- Use random keys, never words or course terms.
- An odd Hill size (9 or 25 letters) spreads a one-letter change further than 16, because 16 lines up with Playfair's letter pairs. Default is 25.

## Special Rules (for Deliverable 3)

1. **25-letter keyed alphabet:** A-Z without J, with J written as I, shared by all stages; spaces and common punctuation are removed.
2. **Mirror rule in Playfair:** Doubled letters both move one step right; a lone last letter moves one step right. No filler.
3. **Ciphertext stealing in Hill:** No padding.
4. **Hill key requirements:** The key must be invertible mod 25 (determinant not a multiple of 5) and must mix (every row and column has at least two non-zero entries).

## Security and Privacy

- The Reveal Mode passcode is stored in an environment variable, not hardcoded in the source code.
- Local `.env` files are excluded from Git tracking through `.gitignore`.
- Never commit private passcodes, answer sheets, or other sensitive files.
- If the passcode was previously committed, changing `.gitignore` alone does not remove it from Git history. Change the exposed passcode as well.
- Keep the repository private until the challenge is over.

## Known Limitations

Hill is linear: if the output of stages 1 and 2 is known (for instance by guessing keys 1 and 2), key 3 follows from linear algebra. Security depends on keys 1 and 2 being long and random.

This is an educational classical cipher, not for real data.
