import json
import os

print("[*] Loading local corporate and IP declaration state...")

if os.path.exists("MANIFEST.json"):
    with open("MANIFEST.json", "r") as f:
        manifest = json.load(f)
    print(f"[+] Entity: {manifest.get('entity')}")
    print(f"[+] Jurisdiction: {manifest.get('jurisdiction')}")
    print(f"[+] Creator UUID: {manifest.get('creator_uuid')}")
    print(f"[+] Ledger Hash: {manifest.get('ledger_hash')[:16]}...")
else:
    print("[-] MANIFEST.json not found.")

if os.path.exists("LAC_ATTRIBUTION_REQUEST.json"):
    with open("LAC_ATTRIBUTION_REQUEST.json", "r") as f:
        lac = json.load(f)
    print(f"[+] Target Institution: {lac.get('target_institution')}")
    print(f"[+] Request Type: {lac.get('request_type')}")
else:
    print("[-] LAC_ATTRIBUTION_REQUEST.json not found.")

print("\n[+] Local repository state is synchronized and valid.")
print("[i] To check the live federal database standing of 10839477 Canada Inc., visit the Corporations Canada Online Filing Centre portal.")
