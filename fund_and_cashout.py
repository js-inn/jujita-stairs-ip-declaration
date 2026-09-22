import sqlite3
import hashlib
import json
from datetime import datetime, timezone
import uuid

DB_FILE = "corporate_ledger.db"

def execute_flow():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get latest block
    cursor.execute("SELECT block_index, previous_hash, nonce, hash FROM octopus_transactions ORDER BY block_index DESC LIMIT 1")
    latest = cursor.fetchone()

    # 1. Fund CARD-UID-ALPHA-99 from capital pool
    new_index = latest["block_index"] + 1
    prev_hash = latest["hash"]
    nonce = latest["nonce"] + 1
    timestamp = datetime.now(timezone.utc).isoformat()

    fund_content = {
        "index": new_index,
        "previous_hash": prev_hash,
        "timestamp": timestamp,
        "sender_card": "INITIAL-CAPITAL-POOL",
        "recipient_card": "CARD-UID-ALPHA-99",
        "amount": 100.00,
        "currency": "CAD",
        "nonce": nonce
    }
    fund_hash = hashlib.sha256(json.dumps(fund_content, sort_keys=True).encode("utf-8")).hexdigest()

    cursor.execute("""
        INSERT INTO octopus_transactions (
            block_index, previous_hash, timestamp, sender_card, 
            recipient_card, amount, currency, nonce, hash, 
            corporate_issuer, creator_uuid
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (new_index, prev_hash, timestamp, "INITIAL-CAPITAL-POOL", "CARD-UID-ALPHA-99", 100.00, "CAD", nonce, fund_hash, "10839477 Canada Inc.", "e4f1b2a7-6d3c-4902-8a5e-9f7b6c5d4e1a"))
    conn.commit()
    print(f"[SUCCESS] Funded CARD-UID-ALPHA-99 with $100.00 CAD (Block #{new_index})")

    # 2. Now request Canada Post Cash-Out ($50.00)
    cursor.execute("SELECT block_index, previous_hash, nonce, hash FROM octopus_transactions ORDER BY block_index DESC LIMIT 1")
    latest = cursor.fetchone()
    
    cashout_index = latest["block_index"] + 1
    cashout_prev = latest["hash"]
    cashout_nonce = latest["nonce"] + 1
    cashout_ts = datetime.now(timezone.utc).isoformat()
    voucher_uuid = str(uuid.uuid4())

    cashout_content = {
        "index": cashout_index,
        "previous_hash": cashout_prev,
        "timestamp": cashout_ts,
        "sender_card": "CARD-UID-ALPHA-99",
        "recipient_card": "POSTAL-NODE-YEG-CP-042",
        "amount": 50.00,
        "currency": "CAD",
        "nonce": cashout_nonce,
        "voucher_id": voucher_uuid
    }
    cashout_hash = hashlib.sha256(json.dumps(cashout_content, sort_keys=True).encode("utf-8")).hexdigest()

    cursor.execute("""
        INSERT INTO octopus_transactions (
            block_index, previous_hash, timestamp, sender_card, 
            recipient_card, amount, currency, nonce, hash, 
            corporate_issuer, creator_uuid
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (cashout_index, cashout_prev, cashout_ts, "CARD-UID-ALPHA-99", "POSTAL-NODE-YEG-CP-042", 50.00, "CAD", cashout_nonce, cashout_hash, "10839477 Canada Inc.", "e4f1b2a7-6d3c-4902-8a5e-9f7b6c5d4e1a"))
    conn.commit()
    conn.close()

    print(f"\n[SUCCESS] Canada Post Cash-Out Voucher Generated Successfully!")
    print(f"--------------------------------------------------")
    print(f"Corporate Issuer : 10839477 Canada Inc.")
    print(f"Postal Terminal  : POSTAL-NODE-YEG-CP-042")
    print(f"Source Card      : CARD-UID-ALPHA-99")
    print(f"Payout Amount    : $50.00 CAD")
    print(f"Voucher Reference: {voucher_uuid}")
    print(f"Ledger Block     : #{cashout_index}")
    print(f"Cryptographic Hash: {cashout_hash}")
    print(f"--------------------------------------------------")

if __name__ == "__main__":
    execute_flow()
