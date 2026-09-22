import sqlite3
import hashlib
import json
from datetime import datetime, timezone
import uuid

DB_FILE = "corporate_ledger.db"

def issue_virtual_card(card_holder_name, initial_fund_amount=100.00):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    unique_suffix = str(uuid.uuid4())[:8].upper()
    virtual_card_uid = f"VCARD-{card_holder_name.upper().replace(' ', '-')}-{unique_suffix}"

    cursor.execute("SELECT block_index, previous_hash, nonce, hash FROM octopus_transactions ORDER BY block_index DESC LIMIT 1")
    latest = cursor.fetchone()

    new_index = latest["block_index"] + 1
    prev_hash = latest["hash"]
    nonce = latest["nonce"] + 1
    timestamp = datetime.now(timezone.utc).isoformat()

    block_content = {
        "index": new_index,
        "previous_hash": prev_hash,
        "timestamp": timestamp,
        "sender_card": "INITIAL-CAPITAL-POOL",
        "recipient_card": virtual_card_uid,
        "amount": initial_fund_amount,
        "currency": "CAD",
        "nonce": nonce,
        "card_type": "VIRTUAL",
        "issuer_entity": "10839477 Canada Inc."
    }

    block_string = json.dumps(block_content, sort_keys=True).encode("utf-8")
    new_hash = hashlib.sha256(block_string).hexdigest()

    try:
        cursor.execute("""
            INSERT INTO octopus_transactions (
                block_index, previous_hash, timestamp, sender_card, 
                recipient_card, amount, currency, nonce, hash, 
                corporate_issuer, creator_uuid
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            new_index, prev_hash, timestamp, "INITIAL-CAPITAL-POOL", 
            virtual_card_uid, initial_fund_amount, "CAD", nonce, new_hash, 
            "10839477 Canada Inc.", "e4f1b2a7-6d3c-4902-8a5e-9f7b6c5d4e1a"
        ))
        conn.commit()
        
        print(f"\n[SUCCESS] Virtual Card Issued and Funded!")
        print(f"--------------------------------------------------")
        print(f"Corporate Issuer : 10839477 Canada Inc.")
        print(f"Card Holder      : {card_holder_name}")
        print(f"Virtual Card UID : {virtual_card_uid}")
        print(f"Initial Balance  : ${initial_fund_amount:.2f} CAD")
        print(f"Ledger Block     : #{new_index}")
        print(f"Cryptographic Hash: {new_hash[:16]}...")
        print(f"--------------------------------------------------")
    except sqlite3.Error as e:
        print(f"[ERROR] Failed to issue virtual card: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("Initializing Virtual Card Issuer...")
    issue_virtual_card(card_holder_name="Jujita Stairs", initial_fund_amount=100.00)
