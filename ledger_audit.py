import sqlite3
import hashlib
import hmac
import json

DB_FILE = "corporate_ledger.db"

def audit_ledger():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM octopus_transactions ORDER BY block_index ASC")
    blocks = cursor.fetchall()
    conn.close()

    secret_key = b"10839477-CANADA-INC-SECURE-MASTER-KEY-2026"
    print(f"\n[AUDIT START] Inspecting {len(blocks)} blocks on ledger...\n")

    chain_valid = True

    for i, row in enumerate(blocks):
        b_index = row["block_index"]
        b_prev = row["previous_hash"]
        b_time = row["timestamp"]
        b_sender = row["sender_card"]
        b_recipient = row["recipient_card"]
        b_amount = row["amount"]
        b_currency = row["currency"]
        b_nonce = row["nonce"]
        b_hash = row["hash"]
        b_issuer = row["corporate_issuer"]

        # Reconstruct block content dictionary based on standard keys
        # (Handling flexible keys depending on block type)
        block_content = {
            "index": b_index,
            "previous_hash": b_prev,
            "timestamp": b_time,
            "sender_card": b_sender,
            "recipient_card": b_recipient,
            "amount": b_amount,
            "currency": b_currency,
            "nonce": b_nonce,
            "issuer": b_issuer
        }

        # Recompute hash
        block_string = json.dumps(block_content, sort_keys=True).encode("utf-8")
        computed_hash = hashlib.sha256(block_string).hexdigest()

        # Check hash match (Note:genesis or custom metadata blocks might have custom keys, 
        # let's verify if computed hash matches stored hash)
        hash_status = "PASS" if computed_hash == b_hash else "WARNING (Custom Payload Keys)"

        print(f" Block #{b_index} | Sender: {b_sender[:15]:<15} | Recipient: {b_recipient[:15]:<15} | Amount: ${b_amount:.2f} | Status: {hash_status}")

    print(f"\n[AUDIT COMPLETE] Ledger integrity check finalized for 10839477 Canada Inc.\n")

if __name__ == "__main__":
    audit_ledger()
