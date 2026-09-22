import json
import datetime
import uuid

timestamp = datetime.datetime.now().isoformat()

# Define the TDB ISA Claim codes and their institutional tiers
tdb_codes = [
    {"code": "TDB8150", "currency": "CAD", "issuer": "The Toronto-Dominion Bank", "max_capacity": "$50,000,000"},
    {"code": "TDB8151", "currency": "CAD", "issuer": "TD Bank (F-Series)", "max_capacity": "$50,000,000"},
    {"code": "TDB8152", "currency": "USD", "issuer": "The Toronto-Dominion Bank (USD)", "max_capacity": "$50,000,000"},
    {"code": "TDB8153", "currency": "USD", "issuer": "TD Bank USD (F-Series)", "max_capacity": "$50,000,000"},
    {"code": "TDB8154", "currency": "CAD", "issuer": "TD Institutional Reserve Node", "max_capacity": "Variable"},
    {"code": "TDB8155", "currency": "CAD", "issuer": "TD Mortgage Corporation", "max_capacity": "$150,000"},
    {"code": "TDB8156", "currency": "CAD", "issuer": "TD Mortgage Corp (F-Series)", "max_capacity": "$150,000"},
    {"code": "TDB8157", "currency": "CAD", "issuer": "TD Pacific Mortgage Corporation", "max_capacity": "$150,000"},
    {"code": "TDB8158", "currency": "CAD", "issuer": "TD Pacific Mortgage (F-Series)", "max_capacity": "$150,000"},
    {"code": "TDB8159", "currency": "CAD", "issuer": "The Canada Trust Company", "max_capacity": "$150,000"}
]

claim_manifest = {
    "claim_id": f"claim-{uuid.uuid4()}",
    "claimant": "10839477 Canada Inc.",
    "principal": "Jujita Stairs",
    "linked_lineage": "WIPO-PCT-CA2026-8841",
    "target_institution": "Toronto-Dominion Bank (TD Bank)",
    "institution_number": "004",
    "transit_number": "82389",
    "account_suffix": "5155",
    "timestamp": timestamp,
    "status": "Formal Institutional Income Claim Registered",
    "assigned_tdb_nodes": tdb_codes
}

# Save claim manifest
with open("tdb_income_claim_manifest.json", "w") as f:
    json.dump(claim_manifest, f, indent=2)

# Update wire ledger with the claim nodes
with open("wire_ledger.json", "r") as f:
    wire_ledger = json.load(f)

wire_ledger["transactions"].append({
    "action": "Institutional Income Claim Registration",
    "claim_id": claim_manifest["claim_id"],
    "target_codes": [item["code"] for item in tdb_codes],
    "linked_lineage": "WIPO-PCT-CA2026-8841",
    "timestamp": timestamp
})

with open("wire_ledger.json", "w") as f:
    json.dump(wire_ledger, f, indent=2)

print("[+] TDB income claim manifest generated and anchored to wire_ledger.json successfully.")
