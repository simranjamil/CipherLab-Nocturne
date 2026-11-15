"""CipherLab - Nocturne Triad edition (Blue Team, CT-486 Classical Cipher Challenge)."""

import hmac
import math
import random

import pandas as pd
import streamlit as st

import analysis
import hill
import playfair
import theme
from alphabet import STD_ALPHABET
from challenge import (
    METHODS,
    SAMPLE_PLAINTEXTS,
    answer_sheet_csv,
    build_challenge,
    parse_plaintexts,
    red_team_csv,
)
from config import ACTIVITY_LINE, CHALLENGE_PAIRS, CHALLENGE_WRONG, CIPHER_CODE, CIPHER_NAME, COURSE_LINE, REVEAL_CODE
from hybrid_cipher import check_keys, decrypt_hybrid, encrypt_hybrid, generate_keys

st.set_page_config(
    page_title=f"{CIPHER_NAME} | CipherLab",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded",
)
theme.inject_css()

PAGES = ["Dashboard", "Encryption Studio", "Challenge Generator", "Strength Analysis", "Algorithm Info"]
STAGES = [
    ("Vigenère", "Keyed 25-letter alphabet, repeating key"),
    ("Playfair + Mirror rule", "5×5 square, letter pairs, no filler"),
    ("Hill", "Matrix blocks mod 25, ciphertext stealing"),
]


# ----------------------------------------------------------------------------
# state
# ----------------------------------------------------------------------------

def init_state():
    ss = st.session_state
    if "k1" not in ss:
        ss.k1, ss.k2, ss.k3 = generate_keys(5)       # fresh random keys, nothing hard-coded
    ss.setdefault("revealed", False)
    ss.setdefault("show_keys", False)


def regen_keys():
    ss = st.session_state
    block = math.isqrt(int(ss.get("k3_len", 25)))
    ss.k1, ss.k2, ss.k3 = generate_keys(block)


def unlock():
    code = st.session_state.get("reveal_code_input", "")
    if hmac.compare_digest(code.encode(), REVEAL_CODE.encode()):
        st.session_state.revealed = True
        st.session_state.unlock_failed = False
    else:
        st.session_state.unlock_failed = True


def seal():
    st.session_state.revealed = False


def keys():
    ss = st.session_state
    return ss.k1, ss.k2, ss.k3


def require_keys():
    status = check_keys(*keys())
    if not status["ok"]:
        for err in status["errors"]:
            st.error(err)
        st.info("Open the Key Vault in the sidebar and fix the key, or press **Generate random keys**.")
        st.stop()
    return status


# ----------------------------------------------------------------------------
# sidebar
# ----------------------------------------------------------------------------

def sidebar():
    ss = st.session_state
    sealed = not ss.revealed
    with st.sidebar:
        theme.brand("CipherLab", f"{CIPHER_NAME}")
        page = st.radio("Navigation", PAGES, label_visibility="collapsed", key="page")
        theme.sep()

        with st.expander("🗝️  Key Vault"):
            st.checkbox("Show keys on screen", key="show_keys")
            kind = "default" if ss.show_keys else "password"
            names = ("Key 1", "Key 2", "Key 3") if sealed else ("Key 1 · Vigenère", "Key 2 · Playfair", "Key 3 · Hill")
            st.text_input(names[0], key="k1", type=kind)
            st.text_input(names[1], key="k2", type=kind)
            st.text_input(names[2], key="k3", type=kind)
            st.selectbox(
                "Generated key 3 length",
                [9, 16, 25],
                index=2,
                key="k3_len",
                format_func=lambda n: f"{n} letters",
            )
            st.button("Generate random keys", key="btn_regen", on_click=regen_keys)
            st.caption("Keys are random on every start. Store them safely - they are not saved anywhere.")

        status = check_keys(*keys())
        if status["ok"]:
            theme.chips([("✓ Keys valid", "ok")])
        else:
            theme.chips([("✗ Key problem", "bad")])
            for err in status["errors"]:
                st.caption(err)

        theme.sep()
        if ss.revealed:
            theme.chips([("🔓 Reveal Mode", "warn")])
            st.button("Seal again", key="btn_seal", on_click=seal)
        else:
            theme.chips([("🔒 Challenge Mode", "")])
            with st.expander("Unlock Reveal Mode"):
                st.text_input("Passcode", type="password", key="reveal_code_input")
                st.button("Unlock", key="btn_unlock", on_click=unlock)
                if ss.get("unlock_failed"):
                    st.error("Wrong passcode.")
            st.caption("Algorithm details stay hidden until the challenge is over.")
        theme.sep()
        st.caption(COURSE_LINE)
    return page


# ----------------------------------------------------------------------------
# pages
# ----------------------------------------------------------------------------

def page_dashboard():
    ss = st.session_state
    sealed = not ss.revealed
    theme.hero(
        ACTIVITY_LINE,
        CIPHER_NAME,
        "A three-layer classical cipher designed to be hard to read from the outside and fully "
        "reversible from the inside. Built for the CT-486 Classical Cipher Challenge.",
    )
    theme.stats([
        ("Layers", "3", "classical stages"),
        ("Alphabet", "25", "letters · I = J"),
        ("Challenge", f"{CHALLENGE_PAIRS}", f"pairs · {CHALLENGE_PAIRS - CHALLENGE_WRONG} correct + {CHALLENGE_WRONG} wrong"),
        ("Mode", "Sealed" if sealed else "Reveal", "algorithm hidden" if sealed else "details visible"),
    ])

    st.markdown("### Encryption pipeline")
    theme.pipeline(STAGES, sealed)
    if sealed:
        st.caption("Stage details are sealed while the challenge is running. Unlock Reveal Mode in the sidebar afterwards.")

    st.write("")
    left, right = st.columns([3, 2], gap="large")
    status = check_keys(*keys())
    with left:
        have_dataset = bool(ss.get("ch_result"))
        theme.checklist([
            (1, "Unique cipher name and description", "Dashboard", "Done", "ok"),
            (2, "Complete encryption technique and sequence", "Algorithm Info", "Reveal Mode" if sealed else "Visible", "" if sealed else "ok"),
            (3, "Key, alphabet mapping and special rules", "Key Vault · Algorithm Info", "Keys valid" if status["ok"] else "Fix keys", "ok" if status["ok"] else "bad"),
            (4, f"{CHALLENGE_PAIRS} challenge pairs ({CHALLENGE_PAIRS - CHALLENGE_WRONG} correct, {CHALLENGE_WRONG} wrong)", "Challenge Generator", "Generated" if have_dataset else "Not yet", "ok" if have_dataset else "warn"),
            (5, "Final explanation after the challenge", "Algorithm Info", "After challenge", ""),
        ])
    with right:
        st.markdown("#### System check")
        theme.chips([
            ("Key 1 ✓" if not any(e.startswith("Key 1") for e in status["errors"]) else "Key 1 ✗", "ok" if not any(e.startswith("Key 1") for e in status["errors"]) else "bad"),
            ("Key 2 ✓" if not any(e.startswith("Key 2") for e in status["errors"]) else "Key 2 ✗", "ok" if not any(e.startswith("Key 2") for e in status["errors"]) else "bad"),
            ("Key 3 ✓" if not any(e.startswith("Key 3") for e in status["errors"]) else "Key 3 ✗", "ok" if not any(e.startswith("Key 3") for e in status["errors"]) else "bad"),
        ])
        st.caption("Runs 300 random round-trips with your current keys.")
        if st.button("Run self-test", key="btn_selftest"):
            if not status["ok"]:
                st.error("Fix the keys first.")
            else:
                rng = random.Random()
                block = status["block"]
                failures = 0
                for _ in range(300):
                    n = rng.randint(block, 140)
                    text = "".join(rng.choice(STD_ALPHABET) for _ in range(n))
                    enc = encrypt_hybrid(text, *keys())
                    if decrypt_hybrid(enc["ciphertext"], *keys())["original"] != text or len(enc["ciphertext"]) != n:
                        failures += 1
                if failures:
                    st.error(f"{failures} of 300 round-trips failed.")
                else:
                    st.success("300 / 300 round-trips passed. Decryption needs only the ciphertext and the three keys.")


def page_studio():
    ss = st.session_state
    sealed = not ss.revealed
    theme.page_header("Cipher workbench", "Encryption Studio", "Encrypt and decrypt with the keys from your Key Vault.")
    require_keys()
    k1, k2, k3 = keys()

    tab_enc, tab_dec = st.tabs(["🔒  Encrypt", "🔓  Decrypt"])

    with tab_enc:
        left, right = st.columns(2, gap="large")
        with left:
            st.text_area(
                "Plaintext",
                key="studio_pt",
                height=190,
                placeholder="Type or paste a message. Spaces are removed and J is written as I.",
            )
            if st.button("Encrypt message", key="btn_enc"):
                try:
                    res = encrypt_hybrid(ss.studio_pt, k1, k2, k3)
                    back = decrypt_hybrid(res["ciphertext"], k1, k2, k3)["original"]
                    res["roundtrip"] = back == res["original"]
                    ss.last_enc = res
                except ValueError as exc:
                    ss.last_enc = None
                    st.error(str(exc))
        with right:
            res = ss.get("last_enc")
            if not res:
                theme.card("Ciphertext appears here", "Enter a plaintext on the left and press Encrypt.")
            else:
                theme.chips([
                    ("Encrypted ✓", "ok"),
                    (f"{len(res['ciphertext'])} letters", ""),
                    ("Round-trip verified ✓" if res["roundtrip"] else "Round-trip FAILED", "ok" if res["roundtrip"] else "bad"),
                ])
                for note in res["notes"]:
                    st.caption(f"Input note: {note}.")
                st.markdown("**Final ciphertext**")
                theme.cipher_blocks(res["ciphertext"])
                st.caption("Copy-ready (no spaces)")
                st.code(res["ciphertext"], language=None)
                st.download_button("Download ciphertext", res["ciphertext"], "ciphertext.txt", "text/plain", key="dl_ct")
                if not sealed:
                    with st.expander("Stage outputs", expanded=True):
                        st.caption("Stage 1 · Vigenère")
                        st.code(res["stage1"], language=None)
                        st.caption("Stage 2 · Playfair + Mirror rule")
                        st.code(res["stage2"], language=None)
                        st.caption("Stage 3 · Hill (= final ciphertext)")
                        st.code(res["ciphertext"], language=None)
                else:
                    st.caption("Stage outputs are hidden in Challenge Mode.")

    with tab_dec:
        left, right = st.columns(2, gap="large")
        with left:
            st.text_area("Ciphertext", key="studio_ct", height=190, placeholder="Paste the ciphertext here.")
            st.caption("No metadata needed: the ciphertext and the three keys are enough.")
            if st.button("Decrypt message", key="btn_dec"):
                try:
                    ss.last_dec = decrypt_hybrid(ss.studio_ct, k1, k2, k3)
                except ValueError as exc:
                    ss.last_dec = None
                    st.error(str(exc))
        with right:
            res = ss.get("last_dec")
            if not res:
                theme.card("Plaintext appears here", "Paste a ciphertext on the left and press Decrypt.")
            else:
                theme.chips([("Decrypted ✓", "ok"), (f"{len(res['original'])} letters", "")])
                st.markdown("**Recovered plaintext**")
                st.code(res["original"], language=None)
                st.caption("By design the recovered text has no spaces and J appears as I.")
                st.download_button("Download plaintext", res["original"], "plaintext.txt", "text/plain", key="dl_pt")
                if not sealed:
                    with st.expander("Stage outputs", expanded=True):
                        st.caption("After Hill⁻¹ (Stage 2 output)")
                        st.code(res["stage2"], language=None)
                        st.caption("After Playfair⁻¹ (Stage 1 output)")
                        st.code(res["stage1"], language=None)


def page_challenge():
    ss = st.session_state
    theme.page_header(
        "Blue Team deliverable 4",
        "Challenge Generator",
        f"Build the {CHALLENGE_PAIRS} plaintext–ciphertext pairs for the Red Team: "
        f"{CHALLENGE_PAIRS - CHALLENGE_WRONG} correct and {CHALLENGE_WRONG} intentionally wrong.",
    )
    status = require_keys()
    k1, k2, k3 = keys()

    st.markdown("### 1 · Plaintexts")
    ss.setdefault("ch_text", "\n".join(SAMPLE_PLAINTEXTS))
    st.text_area(
        f"One plaintext per line - exactly {CHALLENGE_PAIRS} lines",
        key="ch_text",
        height=270,
        help="Use your own sentences. 40-80 letters each. Do not hint at the cipher inside the text.",
    )
    st.caption("Spaces are removed and J is written as I - exactly what the Red Team will see.")

    st.markdown("### 2 · Wrong pairs")
    c1, c2, c3 = st.columns(3, gap="large")
    with c1:
        method_key = st.selectbox(
            "How to make a wrong pair",
            list(METHODS.keys()),
            format_func=lambda k: METHODS[k],
            key="ch_method",
        )
    with c2:
        seed = st.number_input("Random seed", min_value=0, max_value=10_000_000, value=2026, step=1, key="ch_seed")
    with c3:
        pick_mode = st.radio("Which pairs are wrong?", ["Random (from seed)", "I will choose"], key="ch_pick")
    manual = []
    if pick_mode == "I will choose":
        manual = st.multiselect(
            f"Choose exactly {CHALLENGE_WRONG} pairs", list(range(1, CHALLENGE_PAIRS + 1)), key="ch_manual"
        )
    st.caption("Wrong pairs are made with the real cipher, so they look exactly like correct pairs and have the same length.")

    if st.button("Generate challenge dataset", key="btn_challenge"):
        try:
            plains, warnings = parse_plaintexts(ss.ch_text, status["block"])
            if pick_mode == "I will choose":
                if len(manual) != CHALLENGE_WRONG:
                    raise ValueError(f"Choose exactly {CHALLENGE_WRONG} wrong pairs.")
                wrong = [n - 1 for n in manual]
            else:
                wrong = random.Random(int(seed) * 7919 + 1).sample(range(CHALLENGE_PAIRS), CHALLENGE_WRONG)
            ss.ch_result = build_challenge(plains, k1, k2, k3, wrong, method_key, int(seed))
            ss.ch_warnings = warnings
        except ValueError as exc:
            ss.ch_result = None
            st.error(str(exc))

    data = ss.get("ch_result")
    if not data:
        return

    st.divider()
    for warning in ss.get("ch_warnings", []):
        st.warning(warning)

    st.markdown("### 3 · Dataset for the Red Team")
    theme.pairs_table([(r["no"], r["plaintext"], r["shown"]) for r in data["rows"]])
    st.write("")
    st.download_button("Download Red Team dataset (CSV)", red_team_csv(data), "challenge_dataset.csv", "text/csv", key="dl_red")
    st.caption("Give the Red Team only this file. Never share the answer sheet, the keys or the algorithm.")

    st.markdown("### 4 · Private answer sheet")
    with st.expander("Show answer sheet (Blue Team only)"):
        st.warning("This table reveals which pairs are wrong. Do not show it on a shared screen.")
        sheet = pd.DataFrame([
            {
                "Pair": r["no"],
                "Status": "✅ correct" if r["valid"] else "❌ WRONG",
                "Ciphertext given": r["shown"],
                "Correct ciphertext": r["true"],
                "How made": "" if r["valid"] else r["how"],
            }
            for r in data["rows"]
        ])
        st.dataframe(sheet, hide_index=True)
        st.markdown("**Freeze fingerprint (SHA-256)**")
        st.code(data["fingerprint"], language=None)
        st.caption(
            "Write this down before you hand over the dataset. It is a hash of the cipher name, the keys and all "
            "ten pairs, so it proves later that nothing was changed."
        )
        st.download_button("Download answer sheet (CSV)", answer_sheet_csv(data), "answer_sheet_PRIVATE.csv", "text/csv", key="dl_ans")


def page_strength():
    ss = st.session_state
    sealed = not ss.revealed
    theme.page_header(
        "Blue Team evidence",
        "Strength Analysis",
        "Measure how the cipher behaves: letter statistics, change spreading, key size and speed.",
    )
    status = require_keys()
    k1, k2, k3 = keys()
    block = status["block"]

    tab_f, tab_a, tab_k, tab_p = st.tabs(["Letter frequency", "Change spreading", "Key space", "Performance"])

    with tab_f:
        st.text_area("Sample text (any English text, 100+ letters)", value=analysis.SAMPLE_TEXT, key="st_text", height=150)
        plain = analysis.letters_only(ss.st_text)
        if len(plain) < max(100, block):
            st.warning("Enter at least 100 letters.")
        else:
            cipher = encrypt_hybrid(plain, k1, k2, k3)["ciphertext"]
            df = pd.DataFrame(
                {"Plaintext": analysis.letter_frequency(plain), "Ciphertext": analysis.letter_frequency(cipher)},
                index=list(STD_ALPHABET),
            )
            st.markdown("##### Letter frequency (% of text)")
            st.bar_chart(df, color=["#8B5CF6", "#38BDF8"], stack=False)
            ic_p, ic_c = analysis.index_of_coincidence(plain), analysis.index_of_coincidence(cipher)
            m1, m2, m3 = st.columns(3)
            m1.metric("Index of coincidence · plaintext", f"{ic_p:.4f}")
            m2.metric("Index of coincidence · ciphertext", f"{ic_c:.4f}")
            m3.metric("Perfectly random text", "0.0400")
            st.caption(
                "English text has uneven letter counts (high value). A cipher that flattens them towards 0.040 "
                "gives frequency analysis nothing to work with."
            )

    with tab_a:
        st.markdown("Change **one** plaintext letter, encrypt again, and count how many ciphertext letters change.")
        trials = st.slider("Number of tests", 100, 1000, 300, step=100, key="av_trials")
        if st.button("Run test", key="btn_avalanche"):
            sample = analysis.letters_only(ss.get("st_text", analysis.SAMPLE_TEXT))[:60]
            counts = analysis.avalanche(sample, k1, k2, k3, trials=trials, seed=random.randrange(10**6))
            ss.av_result = (len(sample), counts)
        if ss.get("av_result"):
            length, counts = ss.av_result
            m1, m2, m3 = st.columns(3)
            m1.metric("Average letters changed", f"{sum(counts) / len(counts):.2f} of {length}")
            m2.metric("Smallest", min(counts))
            m3.metric("Largest", max(counts))
            hist = pd.Series(counts).value_counts().sort_index()
            hist_df = pd.DataFrame({"Tests": hist.values}, index=[str(i) for i in hist.index])
            st.markdown("##### Letters changed per test")
            st.bar_chart(hist_df, color="#8B5CF6")
            st.caption(
                f"An ideal cipher would change about {length * 24 / 25:.0f} of {length} letters. Classical ciphers spread "
                "changes much less - this number is an honest measure of that limit."
            )
            if not sealed and block % 2 == 0:
                st.info(
                    f"Block size {block} is even, so it lines up with the Playfair letter pairs and a change can only "
                    "reach one block. An odd key size (9 or 25 letters) mixes more."
                )

    with tab_k:
        parts, total = analysis.key_space(k1, k2, k3)
        if sealed:
            st.metric("Combined key space (random keys)", f"2^{analysis.bits(total):.0f}")
            st.caption("Stage-by-stage numbers are shown in Reveal Mode.")
        else:
            table = pd.DataFrame([
                {"Key": name, "Possible keys": analysis.sci(size), "Size": f"2^{analysis.bits(size):.1f}"}
                for name, size in parts
            ])
            st.dataframe(table, hide_index=True)
            st.metric("Combined key space", f"2^{analysis.bits(total):.0f}")
        st.caption(
            "These are brute-force sizes for truly random keys. A key made from a word or a phrase is guessed "
            "from a dictionary long before this number matters."
        )

    with tab_p:
        st.markdown("Speed compared with a single Shift cipher (shift 3). Each test is repeated 10 times; the median is shown.")
        if st.button("Run benchmark", key="btn_bench"):
            with st.spinner("Running benchmark..."):
                ss.perf = analysis.benchmark(k1, k2, k3)
        if ss.get("perf"):
            rows = ss.perf
            st.dataframe(pd.DataFrame(rows), hide_index=True)
            chart = pd.DataFrame(rows).set_index("Message Length")
            st.markdown("##### Encryption time (ms)")
            st.line_chart(chart[["Triad Encryption (ms)", "Shift Encryption (ms)"]], color=["#8B5CF6", "#38BDF8"])
            st.markdown("##### Decryption time (ms)")
            st.line_chart(chart[["Triad Decryption (ms)", "Shift Decryption (ms)"]], color=["#8B5CF6", "#38BDF8"])
            st.caption("Both are linear, O(n). The three-stage cipher costs more per letter because it does three passes.")


def page_algorithm():
    ss = st.session_state
    theme.page_header("Blue Team deliverables 2, 3 and 5", "Algorithm Info", "The complete cipher, explained.")
    if not ss.revealed:
        theme.lock_card(
            "Sealed during the challenge",
            "The algorithm, special rules and key matrices are hidden until the Red Team has finished. "
            "Unlock Reveal Mode in the sidebar for the final explanation.",
        )
        return

    k1, k2, k3 = keys()
    status = check_keys(k1, k2, k3)

    st.markdown("### Overview")
    st.write(
        f"**{CIPHER_NAME} ({CIPHER_CODE})** encrypts in three stages and decrypts them in reverse order. "
        "Ciphertext length always equals plaintext length, and no metadata is stored anywhere."
    )
    theme.pipeline(STAGES, sealed=False)

    st.markdown("### Alphabet mapping")
    st.write(
        "The working alphabet has **25 letters** (A-Z without J; J is written as I). Spaces are removed. "
        "Text letters are numbered by their position in the **keyed alphabet**: the unique letters of key 2, "
        "followed by the unused letters in normal order - this is the Playfair square read row by row. "
        "Key letters of stages 1 and 3 are numbered normally (A = 0 … Z = 24)."
    )

    st.markdown("### Stage 1 · Vigenère over the keyed alphabet")
    st.latex(r"C_i = \mathrm{alph}\big[(\mathrm{idx}(P_i) + k_{\,i \bmod L}) \bmod 25\big]")
    st.latex(r"P_i = \mathrm{alph}\big[(\mathrm{idx}(C_i) - k_{\,i \bmod L}) \bmod 25\big]")
    st.caption("Because the text is numbered by the keyed alphabet, the usual shortcut 'ciphertext minus plaintext = key' fails.")

    st.markdown("### Stage 2 · Playfair with the Mirror rule")
    st.markdown(
        "The text is cut into consecutive pairs. No filler letters are ever inserted.\n\n"
        "| Case | Encryption rule |\n|---|---|\n"
        "| Two different letters, same row | each letter → the letter to its right |\n"
        "| Two different letters, same column | each letter → the letter below |\n"
        "| Two different letters, rectangle | each letter → same row, the other letter's column |\n"
        "| **Mirror rule:** doubled letters (e.g. LL) | both → the letter to the right of L |\n"
        "| **Lone last letter** (odd length) | → the letter to its right |\n\n"
        "Standard Playfair never outputs a pair of identical letters, so the Mirror rule is always reversible and also removes "
        "that tell-tale property."
    )

    st.markdown("### Stage 3 · Hill modulo 25 with ciphertext stealing")
    st.latex(r"\mathbf{c} = K\,\mathbf{p} \bmod 25 \qquad \mathbf{p} = K^{-1}\,\mathbf{c} \bmod 25")
    st.markdown(
        "- Key 3 has m² letters (9, 16 or 25) and fills an m × m matrix K row by row.\n"
        "- K is accepted only if det(K) is **not a multiple of 5** (then K⁻¹ exists mod 25) and every row and column has "
        "at least two non-zero entries, so every letter really mixes with others.\n"
        "- If the length is not a multiple of m, **ciphertext stealing** replaces padding: the last m−r letters of the last full "
        "cipher block are joined with the r leftover letters into one extra block, which is encrypted and placed at the end. "
        "Decryption reverses this exactly."
    )

    st.markdown("### Special rules (summary)")
    st.markdown(
        "1. 25-letter keyed alphabet shared by all three stages, J written as I.\n"
        "2. Mirror rule for doubled letters and a lone last letter in Playfair (no filler, no metadata).\n"
        "3. Ciphertext stealing in Hill (no padding).\n"
        "4. Hill key must be invertible mod 25 and must mix (every row and column at least two non-zero entries).\n"
        "5. Plaintext uses A-Z only; spaces are removed."
    )

    st.markdown("### Why this order")
    st.write(
        "Playfair sits between Vigenère and Hill on purpose. Vigenère and Hill are both affine (linear plus a shift), and two "
        "affine layers next to each other collapse into one affine cipher that linear algebra solves from known plaintext. "
        "Playfair is not linear, so it keeps the two apart."
    )

    st.markdown("### Known limitations")
    st.markdown(
        "- **Hill is linear.** If an attacker knows the output of stages 1 and 2 for a known plaintext (for example by guessing keys 1 "
        "and 2), key 3 follows from simple linear algebra. All the strength rests on keys 1 and 2 being long and random.\n"
        "- **Guessable keys.** Words, names and course terms are tried first by any attacker.\n"
        "- **Limited spreading.** One changed letter changes only a few ciphertext letters (see Strength Analysis).\n"
        "- **Educational cipher.** Not suitable for protecting real data."
    )

    if status["ok"]:
        st.markdown("### Live key matrices")
        st.caption("Derived from the keys currently in the Key Vault - do not show this on a shared screen during the challenge.")
        c1, c2, c3 = st.columns(3, gap="large")
        M, inv = hill.validate_key(k3)
        with c1:
            st.markdown("**Playfair square (key 2)**")
            theme.matrix(playfair.generate_matrix(k2))
        with c2:
            st.markdown("**Hill matrix K (key 3)**")
            theme.matrix(M, dim=True)
        with c3:
            st.markdown("**Inverse K⁻¹ mod 25**")
            theme.matrix(inv, dim=True)

        st.markdown("### Worked example")
        example = "MEET ME AT THE LIBRARY AFTER LUNCH"
        res = encrypt_hybrid(example, k1, k2, k3)
        table = pd.DataFrame(
            [
                ("Plaintext (cleaned)", res["original"]),
                ("After Stage 1 · Vigenère", res["stage1"]),
                ("After Stage 2 · Playfair + Mirror", res["stage2"]),
                ("After Stage 3 · Hill = ciphertext", res["ciphertext"]),
            ],
            columns=["Step", "Text"],
        )
        st.dataframe(table, hide_index=True)
        text = "\n".join(f"{a}: {b}" for a, b in table.itertuples(index=False))
        st.download_button("Download worked example (TXT)", text, "worked_example.txt", "text/plain", key="dl_example")


# ----------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------

init_state()
current = sidebar()

if current == "Dashboard":
    page_dashboard()
elif current == "Encryption Studio":
    page_studio()
elif current == "Challenge Generator":
    page_challenge()
elif current == "Strength Analysis":
    page_strength()
else:
    page_algorithm()
