"""Smoke-test every page of the app with Streamlit's AppTest (no browser needed).

Run from the project folder:  python apptest_all_pages.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from streamlit.testing.v1 import AppTest

from config import REVEAL_CODE


def fresh():
    at = AppTest.from_file("app.py", default_timeout=60)
    at.run()
    assert not at.exception, at.exception
    return at


def go(at, page):
    at.sidebar.radio(key="page").set_value(page).run()
    assert not at.exception, f"{page}: {at.exception}"


def main():
    at = fresh()
    print("PASS  dashboard loads (sealed)")

    # self-test button on dashboard
    at.button(key="btn_selftest").click().run()
    assert not at.exception and any("300 / 300" in s.value for s in at.success), "self-test did not pass"
    print("PASS  dashboard self-test")

    # studio: encrypt + decrypt
    go(at, "Encryption Studio")
    at.text_area(key="studio_pt").set_value("Just meet me at the library before noon, please").run()
    at.button(key="btn_enc").click().run()
    assert not at.exception, at.exception
    res = at.session_state["last_enc"]
    assert res["roundtrip"] and len(res["ciphertext"]) == len(res["original"])
    at.text_area(key="studio_ct").set_value(res["ciphertext"]).run()
    at.button(key="btn_dec").click().run()
    assert at.session_state["last_dec"]["original"] == res["original"]
    print("PASS  studio encrypt/decrypt")

    # studio: bad input is reported, not crashed
    go(at, "Encryption Studio")
    at.text_area(key="studio_pt").set_value("hello 123").run()
    at.button(key="btn_enc").click().run()
    assert not at.exception and at.error, "bad input should show an error"
    print("PASS  studio validation")

    # challenge generator
    go(at, "Challenge Generator")
    at.button(key="btn_challenge").click().run()
    assert not at.exception, at.exception
    data = at.session_state["ch_result"]
    assert len(data["rows"]) == 10 and sum(not r["valid"] for r in data["rows"]) == 3
    print("PASS  challenge generator (7 correct + 3 wrong)")

    # strength analysis
    go(at, "Strength Analysis")
    at.button(key="btn_avalanche").click().run()
    assert not at.exception, at.exception
    at.button(key="btn_bench").click().run()
    assert not at.exception, at.exception
    print("PASS  strength analysis (frequency, change spreading, benchmark)")

    # algorithm page: sealed, then unlock
    go(at, "Algorithm Info")
    assert not at.session_state["revealed"]
    at.text_input(key="reveal_code_input").set_value("wrong").run()
    at.button(key="btn_unlock").click().run()
    assert not at.session_state["revealed"]
    at.text_input(key="reveal_code_input").set_value(REVEAL_CODE).run()
    at.button(key="btn_unlock").click().run()
    assert at.session_state["revealed"], "correct passcode should unlock"
    go(at, "Algorithm Info")
    print("PASS  sealed -> reveal gate and algorithm page")

    # every page again in reveal mode
    for page in ("Dashboard", "Encryption Studio", "Challenge Generator", "Strength Analysis", "Algorithm Info"):
        go(at, page)
    print("PASS  all pages in Reveal Mode")

    # invalid key blocks pages with a friendly message
    at.text_input(key="k3").set_value("AAAAAAAAA").run()
    go(at, "Encryption Studio")
    assert at.error, "invalid key should show an error"
    print("PASS  invalid key handled")
    print("\nAll app checks passed")


if __name__ == "__main__":
    main()
