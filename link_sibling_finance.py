import json

with open("wipo_lineage_report.json", "r") as f:
    wipo_data = json.load(f)

with open("wire_ledger.json", "r") as f:
    wire_data = json.load(f)

# Create a bridge mapping financial flows to sibling lineage nodes
bridge_mapping = {
    "primary_entity": wipo_data.get("target_entity"),
    "lineage_source": wipo_data.get("source"),
    "linked_family_nodes": len(wipo_data.get("lineage_records", [])),
    "financial_ledger_id": wire_data.get("ledger_id"),
    "standard_alignment": wire_data.get("standard_alignment"),
    "status": "Bridge active - Family nodes bound to payment routing layer"
}

with open("sibling_financial_bridge.json", "w") as f:
    json.dump(bridge_mapping, f, indent=2)

print("[+] Successfully generated sibling-to-financial bridge manifest: sibling_financial_bridge.json")
