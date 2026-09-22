import json

print("=== CIPO SUBMISSION MEMO ===")
try:
    with open("CIPO_SUBMISSION_MEMO.json", "r") as f:
        memo = json.load(f)
    print(json.dumps(memo, indent=2))
except Exception as e:
    print("Error reading memo:", e)

print("\n=== PUBLISHED AUDIT MANIFEST (Snippet) ===")
try:
    with open("published_audit_manifest.json", "r") as f:
        manifest = json.load(f)
    # Print top-level keys and a summary
    print("Manifest Keys:", list(manifest.keys()) if isinstance(manifest, dict) else "List format")
    print(json.dumps(manifest, indent=2)[:1000] + "\n... [truncated for brevity]")
except Exception as e:
    print("Error reading manifest:", e)
