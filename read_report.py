import json

with open("sibling_audit_report.json", "r") as f:
    data = json.load(f)

print("Status:", data.get("status"))
findings = data.get("findings", [])
print(f"Cataloged items: {len(findings)}")
for entry in findings:
    print(f" - {entry.get('file')} ({entry.get('size_bytes')} bytes)")
