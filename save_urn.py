import os, webbrowser
from dotenv import load_dotenv, set_key

load_dotenv()
token = os.getenv("LINKEDIN_ACCESS_TOKEN", "")
url   = f"https://api.linkedin.com/v2/me?oauth2_access_token={token}"

print()
print("Opening your LinkedIn profile API in browser...")
print()
webbrowser.open(url)
print()
print("The browser will show JSON like:")
print('  {"id": "ABC123xyz", "firstName": {"localized": {"en_US": "John"}},...}')
print()
print('Copy the value of the "id" field (just the random string, e.g. ABC123xyz)')
print()

person_id = input("Paste your LinkedIn ID here: ").strip()
if person_id:
    urn = f"urn:li:person:{person_id}"
    set_key(".env", "LINKEDIN_PERSON_URN", urn)
    print()
    print(f"[DONE] Saved LINKEDIN_PERSON_URN = {urn}")
    print()
    print("All LinkedIn credentials are now configured!")
    print("Run: python run.py   to launch the app!")
else:
    print("[SKIP] No ID entered.")
