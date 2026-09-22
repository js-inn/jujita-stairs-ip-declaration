with open("verify_audit_suite.py", "r") as f:
    content = f.read()

# Add tdb_income_claim_manifest.json to files_to_check if not already present
if "tdb_income_claim_manifest.json" not in content:
    old_target = '"sibling_financial_bridge.json"'
    new_target = '"sibling_financial_bridge.json",\n    "tdb_income_claim_manifest.json",\n    "tdbank_lineage_bridge.json"'
    content = content.replace(old_target, new_target)
    with open("verify_audit_suite.py", "w") as f:
        f.write(content)
    print("[+] Updated verify_audit_suite.py with new claim manifests.")
else:
    print("[*] Verification suite already includes claim manifests.")
