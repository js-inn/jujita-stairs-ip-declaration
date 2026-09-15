import json
from datetime import datetime, timezone
import os

CAMT_LOG_FILE = "camt053_statements.json"

def create_camt053_statement(statement_id, opening_balance, closing_balance, currency, entries):
    statement = {
        "schema_version": "camt.053.001.10",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "corporate_holder": "10839477 Canada Inc.",
        "statement_metadata": {
            "statement_id": statement_id,
            "electronic_sequence_number": 1,
            "creation_date_time": datetime.now(timezone.utc).isoformat()
        },
        "balance_summary": {
            "opening_balance": {"amount": opening_balance, "currency": currency, "type": "OPBD"},
            "closing_balance": {"amount": closing_balance, "currency": currency, "type": "CLBD"}
        },
        "statement_entries": entries,
        "cryptographic_anchor": {
            "creator_uuid": "e4f1b2a7-6d3c-4902-8a5e-9f7b6c5d4e1a",
            "anchor_uuid": "3d9f8a21-c5e7-4b6a-9128-f0d3e2a1b9c7"
        }
    }
    return statement

def log_statement(statement):
    statements = []
    if os.path.exists(CAMT_LOG_FILE):
        try:
            with open(CAMT_LOG_FILE, "r", encoding="utf-8") as f:
                statements = json.load(f)
        except json.JSONDecodeError:
            statements = []
            
    statements.append(statement)
    
    with open(CAMT_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(statements, f, indent=4)
    print(f"[SUCCESS] camt.053 statement payload logged to {CAMT_LOG_FILE}")

if __name__ == "__main__":
    print("Parsing sample ISO 20022 camt.053 structure...")
    sample_entries = [
        {
            "entry_reference": "ENT-2026-09-001",
            "amount": 5000.00,
            "currency": "CAD",
            "credit_debit_indicator": "CRDT",
            "status": "BOOK",
            "bank_transaction_code": "DTCT-ICDT",
            "remittance_information": "Initial corporate capitalization and liquidity anchor"
        }
    ]
    
    camt_payload = create_camt053_statement(
        statement_id="BMO-CAMT053-20260915-001",
        opening_balance=0.00,
        closing_balance=5000.00,
        currency="CAD",
        entries=sample_entries
    )
    log_statement(camt_payload)
