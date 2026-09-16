import sqlite3
import hashlib
import hmac
import json
from datetime import datetime, timezone
import uuid

DB_FILE = "corporate_ledger.db"

def simulate_settlement():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. Fetch the latest pending cash-out block (e.g., Block #8)
    cursor.execute("""
        SELECT block_index, recipient_card, amount, currency, hash 
        FROM octopus_transactions 
        ORDER BY block_index DESC LIMIT 1
    """)
    latest = cursor.fetchone()

    if not latest or "CANADA-POST" not in latest["recipient_card"]:
        print("[ERROR] No pending postal redemption block found to settle.")
        conn.close()
        return

    target_block = latest["block_index"]
    payout_amount = latest["amount"]
    outlet_node = latest["recipient_card"]

    # 2. Prepare the new Settlement Block (Chain continuity)
    new_index = target_block + 1
    prev_hash = latest["hash"]
    timestamp = datetime.now(timezone.utc).isoformat()
    settlement_id = str(uuid.uuid4()).upper()
    secret_key = b"10839477-CANADA-INC-SECURE-MASTER-KEY-2026"

    block_content = {
        "index": new_index,
        "previous_hash": prev_hash,
        "timestamp": timestamp,
        "sender_card": outlet_node,
        "recipient_card": "DISBURSED-PHYSICAL-CASH-DRAWER",
        "amount": payout_amount,
        "currency": "CAD",
        "nonce": new_index * 10,
        "settlement_id": settlement_id,
        "settlement_status": "COMPLETED_CASH_DISBURSED",
        "issuer": "10839477 Canada Inc."
    }

    block_string = json.dumps(block_content, sort_keys=True).encode("utf-8")
    block_hash = hashlib.sha256(block_string).hexdigest()
    signature = hmac.new(secret_key, block_string, hashlib.sha256).hexdigest()

    # 3. Commit Settlement Block to SQLite Ledger
    cursor.execute("""
        INSERT INTO octopus_transactions (
            block_index, previous_hash, timestamp, sender_card, 
            recipient_card, amount, currency, nonce, hash, 
            corporate_issuer, creator_uuid
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        new_index, prev_hash, timestamp, outlet_node, 
        "DISBURSED-PHYSICAL-CASH-DRAWER", payout_amount, "CAD", 
        new_index * 10, block_hash, "10839477 Canada Inc.", 
        "e4f1b2a7-6d3c-4902-8a5e-9f7b6c5d4e1a"
    ))
    conn.commit()
    conn.close()

    print(f"\n==================================================")
    print(f"      COUNTER SETTLEMENT SUCCESSFUL               ")
    print(f"==================================================")
    print(f" Settlement Block : #{new_index}")
    print(f" Source Node      : {outlet_node}")
    print(f" Status           : CASH PHYSICALLY DISBURSED")
    print(f" Amount Settled   : ${payout_amount:.2f} CAD")
    print(f" Settlement ID    : {settlement_id}")
    print(f"--------------------------------------------------")
    print(f" HMAC Signature   : {signature[:32]}...")
    print(f" SHA-256 Hash     : {block_hash[:32]}...")
    print(f"==================================================\n")

if __name__ == "__main__":
    print("Simulating Canada Post Over-the-Counter Settlement...")
    simulate_settlement()
