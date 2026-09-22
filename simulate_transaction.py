import json
import datetime
import uuid

timestamp = datetime.datetime.now().isoformat()

# 1. Simulate an Octopus 2.0 offline retail event
with open("octopus_ledger.json", "r") as f:
    octopus = json.load(f)

octopus["nodes_active"] += 1
octopus["cash_to_digital_events"].append({
    "event_id": f"octo-txn-{uuid.uuid4()}",
    "type": "Cash-to-Digital Retail Conversion",
    "amount_cad": 250.00,
    "location": "Postal Network Terminal - Edmonton Node",
    "timestamp": timestamp,
    "status": "anchored"
})

with open("octopus_ledger.json", "w") as f:
    json.dump(octopus, f, indent=2)

# 2. Simulate an ISO 20022 aligned wire transaction
with open("wire_ledger.json", "r") as f:
    wire = json.load(f)

wire["transactions"].append({
    "tx_id": f"wire-pacs008-{uuid.uuid4()}",
    "message_type": "pacs.008.001.10 (FI to FI Customer Credit Transfer)",
    "debtor": "10839477 Canada Inc.",
    "amount_cad": 15000.00,
    "timestamp": timestamp,
    "compliance_ref": "WIPO-PCT-CA2026-8841"
})

with open("wire_ledger.json", "w") as f:
    json.dump(wire, f, indent=2)

print("[+] Financial pipeline transaction simulation executed successfully.")
