with open("verify_audit_suite.py", "r") as f:
    content = f.read()

if "questrade_income_claim_manifest.json" not in content:
    old_target = '"tdb_income_claim_manifest.json"'
    new_target = '"tdb_income_claim_manifest.json",\n    "questrade_income_claim_manifest.json"'
    content = content.replace(old_target, new_target)
    with open("verify_audit_suite.py", "w") as f:
        f.write(content)
    print("[+] Added questrade_income_claim_manifest.json to verification suite.")
