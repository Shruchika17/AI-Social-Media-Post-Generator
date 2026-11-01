# -*- coding: utf-8 -*-
"""
LinkedIn Token & Person URN Fetcher (with OpenID + profile scopes)
"""

import os
import sys
import json
import urllib.parse
import webbrowser
import requests
from dotenv import load_dotenv, set_key

load_dotenv()

CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID", "789vphsmjbyieg")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET", "WPL_AP1.vNlRPfCQT4AYbRut.D5zKoQ==")
REDIRECT_URI = "http://localhost:8080/callback"
SCOPE = "openid profile email w_member_social"
ENV_FILE = ".env"


def build_auth_url():
    params = urllib.parse.urlencode({
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "state": "linkedin_auth_complete",
    })
    return f"https://www.linkedin.com/oauth/v2/authorization?{params}"


def exchange_code(code: str) -> dict:
    r = requests.post(
        "https://www.linkedin.com/oauth/v2/accessToken",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )
    return r.json()


def get_user_profile(token: str) -> dict:
    r = requests.get(
        "https://api.linkedin.com/v2/userinfo",
        headers={"Authorization": f"Bearer {token}"},
        timeout=15,
    )
    return r.json()


def main():
    print("=" * 65)
    print("  LinkedIn Token & Author URN Generator")
    print("=" * 65)
    print()
    print("STEP 1: Open this link in your browser:")
    print()
    auth_url = build_auth_url()
    print(auth_url)
    print()
    print("Opening browser automatically...")
    webbrowser.open(auth_url)
    print()
    print("STEP 2: Click 'Allow' on LinkedIn.")
    print("STEP 3: When localhost fails to connect, COPY the full address bar URL.")
    print("        It starts with: http://localhost:8080/callback?code=AQ...")
    print()

    raw = input("Paste the callback URL here: ").strip()
    if not raw:
        print("[ERROR] No URL pasted.")
        sys.exit(1)

    # Extract code
    code = None
    if "code=" in raw:
        try:
            parsed = urllib.parse.urlparse(raw)
            params = urllib.parse.parse_qs(parsed.query)
            code = params["code"][0]
        except Exception:
            pass

    if not code:
        code = raw

    print(f"\n[OK] Exchanging code: {code[:15]}...")
    token_data = exchange_code(code)

    if "access_token" not in token_data:
        print(f"[ERROR] Token exchange failed: {token_data}")
        sys.exit(1)

    access_token = token_data["access_token"]
    print("[OK] Access token retrieved!")

    print("\nFetching exact account Author ID via userinfo...")
    profile = get_user_profile(access_token)
    sub = profile.get("sub", "")
    name = profile.get("name", "LinkedIn Member")
    email = profile.get("email", "")

    if not sub:
        print(f"[ERROR] Could not read userinfo: {profile}")
        sys.exit(1)

    author_urn = f"urn:li:person:{sub}"

    # Save both directly into .env
    set_key(ENV_FILE, "LINKEDIN_ACCESS_TOKEN", access_token)
    set_key(ENV_FILE, "LINKEDIN_PERSON_URN", author_urn)

    print()
    print("=" * 65)
    print("🎉 SUCCESS! LinkedIn Fully Configured!")
    print(f"  Account Name : {name}")
    print(f"  Email        : {email}")
    print(f"  Author URN   : {author_urn}")
    print("=" * 65)
    print()
    print("Saved to .env file! Now you can post directly to LinkedIn.")


if __name__ == "__main__":
    main()
