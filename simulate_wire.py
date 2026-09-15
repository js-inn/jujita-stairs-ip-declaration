import json
from datetime import datetime, timezone
import os

LEDGER_FILE = "wire_ledger.json"

def create_wire_record(reference_id, amount, currency, sender_corp, recipient, message_type):
    record = {
        "schema_version": "1.0",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "corporate_issuer": sender_corp,
        "message_metadata": {
            "message_type": message_type,
            "reference_id": reference_id,
            "routing_state": "LOCAL_SIMULATION_PENDING"
        },
        "transaction_details": {
            "amount": amount,
            "currency": currency,
            "recipient": recipient
        },
        "cryptographic_anchor": {
            "creator_uuid": "e4f1b2a7-6d3c-4902-8a5e-9f7b6c5d4e1a",
            "anchor_uuid": "3d9f8a21-c5e7-4b6a-9128-f0d3e2a1b9c7"
        }
    }
    return record

def save_to_ledger(record):
    ledger = []
    if os.path.exists(LEDGER_FILE):
        try:
            with open(LEDGER_FILE, "r", encoding="utf-8") as f:
                ledger = json.load(f)
        except json.JSONDecodeError:
            ledger = []
            
    ledger.append(record)
    
    with open(LEDGER_FILE, "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=4)
    print(f"[SUCCESS] Wire payload logged to {LEDGER_FILE}")

if __name__ == "__main__":
    print("Initializing local financial messaging simulator...")
    sample_record = create_wire_record(
        reference_id="WIRE-REF-2026-001",
        amount=1000.00,
        currency="CAD",
        sender_corp="10839477 Canada Inc.",
        recipient="External Corporate Beneficiary",
        message_type="pacs.002.001.12"
    )
    save_to_ledger(sample_record)
