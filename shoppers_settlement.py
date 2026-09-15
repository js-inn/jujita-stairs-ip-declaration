import sqlite3
import hashlib
import hmac
import json
from datetime import datetime, timezone
import uuid

DB_FILE = "corporate_ledger.db"

def simulate_shoppers_settlement():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. Fetch latest block for chain continuity
    cursor.execute("""
        SELECT block_index, amount, currency, hash 
        FROM octopus_transactions 
        ORDER BY block_index DESC LIMIT 1
    """)
    latest = cursor.fetchone()

    if not latest:
        print("[ERROR] No existing ledger blocks found.")
        conn.close()
        return

    target_block = latest["block_index"]
    payout_amount = latest["amount"]
    
    # Precise downtown retail postal node identifier
    retail_node = "SHOPPERS-DRUG-MART-EDMONTON-CITY-CENTRE-10255-101-ST"

    new_index = target_block + 1
    prev_hash = latest["hash"]
    timestamp = datetime.now(timezone.utc).isoformat()
    settlement_id = str(uuid.uuid4()).upper()
    secret_key = b"10839477-CANADA-INC-SECURE-MASTER-KEY-2026"

    block_content = {
        "index": new_index,
        "previous_hash": prev_hash,
        "timestamp": timestamp,
        "sender_card": retail_node,
        "recipient_card": "DISBURSED-PHYSICAL-CASH-DRAWER",
        "amount": payout_amount,
        "currency": "CAD",
        "nonce": new_index * 15,
        "settlement_id": settlement_id,
        "location_address": "10255 101 St NW, Edmonton, AB T5J 0K3",
        "settlement_status": "RETAIL_COUNTER_CASH_DISBURSED",
        "issuer": "10839477 Canada Inc."
    }

    block_string = json.dumps(block_content, sort_keys=True).encode("utf-8")
    block_hash = hashlib.sha256(block_string).hexdigest()
    signature = hmac.new(secret_key, block_string, hashlib.sha256).hexdigest()

    # Commit localized settlement block
    cursor.execute("""
        INSERT INTO octopus_transactions (
            block_index, previous_hash, timestamp, sender_card, 
            recipient_card, amount, currency, nonce, hash, 
            corporate_issuer, creator_uuid
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        new_index, prev_hash, timestamp, retail_node, 
        "DISBURSED-PHYSICAL-CASH-DRAWER", payout_amount, "CAD", 
        new_index * 15, block_hash, "10839477 Canada Inc.", 
        "e4f1b2a7-6d3c-4902-8a5e-9f7b6c5d4e1a"
    ))
    conn.commit()
    conn.close()

    print(f"\n==================================================")
    print(f"      DOWNTOWN RETAIL COUNTER SETTLEMENT          ")
    print(f"==================================================")
    print(f" Settlement Block : #{new_index}")
    print(f" Outlet Location  : Shoppers Drug Mart (City Centre)")
    print(f" Address          : 10255 101 St NW, Edmonton, AB")
    print(f" Status           : CASH PHYSICALLY DISBURSED")
    print(f" Amount Settled   : ${payout_amount:.2f} CAD")
    print(f" Settlement ID    : {settlement_id}")
    print(f"--------------------------------------------------")
    print(f" HMAC Signature   : {signature[:32]}...")
    print(f" SHA-256 Hash     : {block_hash[:32]}...")
    print(f"==================================================\n")

if __name__ == "__main__":
    print("Simulating Downtown Core Retail Counter Settlement...")
    simulate_shoppers_settlement()
