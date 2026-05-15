#!/usr/bin/env python3
"""Post a tweet via CloakBrowser — bypass datacenter shadow-block.

Why a real browser:
    X.com generates `x-client-transaction-id` via JavaScript at request time.
    httpx-based POSTs from datacenter IPs return 200 OK + tweet_results: {} (empty),
    silently dropping the tweet. Real browser auto-generates the header.

Usage:
    DISPLAY=:99 TWEET_TEXT="hello world" python3 x_post_via_browser.py
"""
import json
import os
import time

from cloakbrowser import launch_persistent_context

PROFILE = os.environ.get("X_PROFILE", "/home/agent/.cloakbrowser/x-profile")
TWEET_TEXT = os.environ.get("TWEET_TEXT", "")
STATUS = "/tmp/x_post_status.json"

assert TWEET_TEXT, "Set TWEET_TEXT env"


def write_status(state, msg=""):
    with open(STATUS, "w") as f:
        json.dump({"state": state, "msg": msg, "ts": time.time()}, f)


def main():
    write_status("launching")
    context = launch_persistent_context(
        user_data_dir=PROFILE,
        headless=False,
        humanize=True,
        backend="patchright",
        args=["--no-sandbox", "--disable-blink-features=AutomationControlled"],
        viewport={"width": 1280, "height": 800},
        locale="en-US",
        timezone_id="Asia/Jakarta",
    )
    page = context.new_page()

    # Direct compose URL
    page.goto("https://x.com/compose/post", wait_until="domcontentloaded", timeout=30000)
    time.sleep(7)

    # Type into contenteditable div (NOT <textarea>)
    write_status("typing")
    ta = page.locator('[data-testid="tweetTextarea_0"]').first
    ta.wait_for(timeout=15000)
    ta.click()
    page.keyboard.type(TWEET_TEXT, delay=60)  # human-like delay
    time.sleep(2)

    # Click Post button
    write_status("posting")
    btn = page.locator('[data-testid="tweetButton"]').first
    btn.wait_for(timeout=10000)
    btn.click()
    time.sleep(5)

    # Success indicator: redirect to /home
    if "/home" in page.url:
        write_status("POSTED", page.url)
    else:
        write_status("UNCERTAIN", page.url)

    time.sleep(3)
    context.close()


if __name__ == "__main__":
    main()
