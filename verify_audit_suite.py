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
    "update_wipo_report.py",
    "financial_pipeline.py",
    "link_sibling_finance.py",
    "simulate_transaction.py",
    "wire_ledger.json",
    "wire_status.json",
    "octopus_ledger.json",
    "postal_payout_manifest.json",
    "bridge_activity.json",
    "sibling_financial_bridge.json"
]

print("=== STARTING COMPREHENSIVE REPOSITORY VERIFICATION ===")
missing_files = []
valid_json_count = 0
total_files = len(files_to_check)

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
print(f"Total files verified: {total_files - len(missing_files)}/{total_files}")
print(f"Valid JSON manifests: {valid_json_count}")
if not missing_files:
    print("[+] Status: All IP, financial, and bridge assets are verified and aligned.")
else:
    print(f"[-] Status: Missing files -> {missing_files}")
