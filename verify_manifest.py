import json
import hmac
import hashlib

SECRET_KEY = b"jujita_secret_root_key"
MANIFEST_FILE = "master_audit_manifest.json"

def verify_audit_manifest():
    print(f"\n[*] Loading audit manifest: {MANIFEST_FILE}...")
    try:
        with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"[!] Error: {MANIFEST_FILE} not found.")
        return

    audit_report = data.get("audit_report")
    claimed_anchor = data.get("cryptographic_proof", {}).get("root_state_anchor")
    
    if not audit_report or not claimed_anchor:
        print("[!] Error: Invalid manifest structure.")
        return

    # Re-compute HMAC-SHA256 over the exact sorted JSON payload
    json_payload = json.dumps(audit_report, sort_keys=True)
    computed_anchor = hmac.new(SECRET_KEY, json_payload.encode('utf-8'), hashlib.sha256).hexdigest()
    
    print(f"    Claimed Root Anchor:  {claimed_anchor}")
    print(f"    Computed Root Anchor: {computed_anchor}")
    
    if hmac.compare_digest(computed_anchor, claimed_anchor):
        print("\n[✔] VERIFICATION SUCCESSFUL: Master audit manifest integrity verified. Zero tampering detected.")
    else:
        print("\n[✘] VERIFICATION FAILED: Manifest payload has been altered or secret key mismatch!")

if __name__ == "__main__":
    verify_audit_manifest()
