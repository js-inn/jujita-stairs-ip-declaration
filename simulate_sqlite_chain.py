import sqlite3
import hashlib
import json
from datetime import datetime, timezone
import os

DB_FILE = "corporate_ledger.db"

class SQLiteLedgerEngine:
    def __init__(self, db_file=DB_FILE):
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.conn.row_factory = sqlite3.Row

    def get_latest_block(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT block_index, previous_hash, nonce, hash 
            FROM octopus_transactions 
            ORDER BY block_index DESC LIMIT 1
        """)
        return cursor.fetchone()

    def add_transaction(self, sender_card, recipient_card, amount, currency="CAD"):
        latest = self.get_latest_block()
        if not latest:
            print("[ERROR] Ledger is empty.")
            return

        new_index = latest["block_index"] + 1
        previous_hash = latest["hash"]
        new_nonce = latest["nonce"] + 1
        timestamp = datetime.now(timezone.utc).isoformat()

        block_content = {
            "index": new_index,
            "previous_hash": previous_hash,
            "timestamp": timestamp,
            "sender_card": sender_card,
            "recipient_card": recipient_card,
            "amount": amount,
            "currency": currency,
            "nonce": new_nonce
        }

        block_string = json.dumps(block_content, sort_keys=True).encode("utf-8")
        new_hash = hashlib.sha256(block_string).hexdigest()

        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO octopus_transactions (
                    block_index, previous_hash, timestamp, sender_card, 
                    recipient_card, amount, currency, nonce, hash, 
                    corporate_issuer, creator_uuid
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                new_index, previous_hash, timestamp, sender_card, 
                recipient_card, amount, currency, new_nonce, new_hash, 
                "10839477 Canada Inc.", "e4f1b2a7-6d3c-4902-8a5e-9f7b6c5d4e1a"
            ))
            self.conn.commit()
            print(f"[SUCCESS] Block #{new_index} committed to SQLite. Hash: {new_hash[:16]}... (Nonce: {new_nonce})")
        except sqlite3.Error as e:
            print(f"[ERROR] Failed to commit transaction: {e}")
            self.conn.rollback()

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    print("Initializing Direct SQLite Transaction Engine...")
    engine = SQLiteLedgerEngine()
    engine.add_transaction(
        sender_card="CARD-UID-ALPHA-99",
        recipient_card="CARD-UID-GAMMA-77",
        amount=25.00,
        currency="CAD"
    )
    engine.close()
