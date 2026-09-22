import sqlite3
import hashlib
import json
from datetime import datetime, timezone

DB_FILE = "corporate_ledger.db"
CREATOR_UUID = "e4f1b2a7-6d3c-4902-8a5e-9f7b6c5d4e1a"

def record_trace_block():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get latest block metadata
    cursor.execute("SELECT block_index, hash, nonce FROM octopus_transactions ORDER BY block_index DESC LIMIT 1")
    latest = cursor.fetchone()

    new_index = latest["block_index"] + 1
    prev_hash = latest["hash"]
    nonce = latest["nonce"] + 1
    timestamp = datetime.now(timezone.utc).isoformat()

    block_content = {
        "index": new_index,
        "previous_hash": prev_hash,
        "timestamp": timestamp,
        "sender_card": "SWIFT-ISO-NETWORK",
        "recipient_card": "CORPORATE-TREASURY-RESERVE",
        "amount": 360.00,
        "currency": "CAD",
        "nonce": nonce,
        "action": "SWIFT_TRACE_INVESTIGATION_CAMT_029",
        "issuer": "10839477 Canada Inc."
    }

    block_string = json.dumps(block_content, sort_keys=True).encode("utf-8")
    block_hash = hashlib.sha256(block_string).hexdigest()

    cursor.execute("""
        INSERT INTO octopus_transactions (
            block_index, previous_hash, timestamp, sender_card, 
            recipient_card, amount, currency, nonce, hash, 
            corporate_issuer, creator_uuid
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        new_index, prev_hash, timestamp, "SWIFT-ISO-NETWORK", 
        "CORPORATE-TREASURY-RESERVE", 360.00, "CAD", nonce, block_hash, 
        "10839477 Canada Inc.", CREATOR_UUID
    ))
    conn.commit()
    conn.close()
    print(f"\n[SUCCESS] Block #{new_index} executed: SWIFT Trace Investigation (camt.029) logged for $360.00 CAD!\n")

if __name__ == "__main__":
    record_trace_block()
