import json
import datetime
import os

LEDGER_FILE = "wire_ledger.json"

def process_wire_update():
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    date_str = timestamp[:10].replace("-", "")

    # Load existing ledger or initialize
    if os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE, "r") as f:
            try:
                ledger = json.load(f)
            except json.JSONDecodeError:
                ledger = []
    else:
        ledger = []

    # Calculate next sequence number for reference ID
    next_seq = len(ledger) + 1
    ref_id = f"WIRE-{date_str}-{next_seq:03d}"
    
    wire_entry = {
        "timestamp": timestamp,
        "entity": "10839477 Canada Inc.",
        "status": "PROCESSED",
        "message_type": "camt.053",
        "reference_id": ref_id
    }

    ledger.append(wire_entry)

    with open(LEDGER_FILE, "w") as f:
        json.dump(ledger, f, indent=4)

    print(f"Updated {LEDGER_FILE} with entry {ref_id} at {timestamp}")

if __name__ == "__main__":
    process_wire_update()
