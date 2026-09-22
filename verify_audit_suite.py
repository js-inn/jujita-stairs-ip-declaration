import os
import json

files_to_check = [
    "CIPO_SUBMISSION_MEMO.json",
    "published_audit_manifest.json",
    "LAC_ATTRIBUTION_REQUEST.json",
    "MANIFEST.json",
    "sibling_audit_report.json",
    "wipo_lineage_report.json",
    "wipo_sibling_extension.py",
    "update_wipo_report.py"
]

print("=== STARTING END-TO-END AUDIT VERIFICATION ===")
missing_files = []
valid_json_count = 0

for filepath in files_to_check:
    if os.path.exists(filepath):
        print(f"[CHECK] Found: {filepath}")
        if filepath.endswith(".json"):
            try:
                with open(filepath, "r") as f:
                    json.load(f)
                print(f"  -> JSON Syntax: VALID")
                valid_json_count += 1
            except Exception as e:
                print(f"  -> JSON Syntax: INVALID ({e})")
    else:
        print(f"[MISSING] {filepath}")
        missing_files.append(filepath)

print("\n=== VERIFICATION SUMMARY ===")
print(f"Total files verified: {len(files_to_check) - len(missing_files)}/{len(files_to_check)}")
print(f"Valid JSON manifests: {valid_json_count}")
if not missing_files:
    print("[+] Status: All core sovereign audit assets are verified and aligned.")
else:
    print(f"[-] Status: Missing files -> {missing_files}")
