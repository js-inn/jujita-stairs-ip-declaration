import json
import sqlite3
import os

JSON_FILE = "octopus_ledger.json"
DB_FILE = "corporate_ledger.db"

def migrate_ledger():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS octopus_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            block_index INTEGER UNIQUE NOT NULL,
            previous_hash TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            sender_card TEXT NOT NULL,
            recipient_card TEXT NOT NULL,
            amount REAL NOT NULL,
            currency TEXT NOT NULL,
            nonce INTEGER UNIQUE NOT NULL,
            hash TEXT UNIQUE NOT NULL,
            corporate_issuer TEXT NOT NULL,
            creator_uuid TEXT NOT NULL
        )
    """)
    conn.commit()
    print(f"[INFO] SQLite database initialized: {DB_FILE}")

    if not os.path.exists(JSON_FILE):
        print(f"[WARNING] {JSON_FILE} not found. Starting with an empty SQLite database table.")
        conn.close()
        return

    with open(JSON_FILE, "r", encoding="utf-8") as f:
        try:
            chain_data = json.load(f)
        except json.JSONDecodeError:
            print("[ERROR] Failed to parse JSON ledger.")
            conn.close()
            return

    imported_count = 0
    for block in chain_data:
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO octopus_transactions (
                    block_index, previous_hash, timestamp, sender_card, 
                    recipient_card, amount, currency, nonce, hash, 
                    corporate_issuer, creator_uuid
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                block["index"],
                block["previous_hash"],
                block["timestamp"],
                block["sender_card"],
                block["recipient_card"],
                block["amount"],
                block["currency"],
                block["nonce"],
                block["hash"],
                block["corporate_issuer"],
                block["creator_uuid"]
            ))
            if cursor.rowcount > 0:
                imported_count += 1
        except sqlite3.Error as e:
            print(f"[ERROR] Database insertion failed at block {block.get('index')}: {e}")

    conn.commit()
    conn.close()
    print(f"[SUCCESS] Migrated {imported_count} blocks from JSON to SQLite database.")

if __name__ == "__main__":
    migrate_ledger()
