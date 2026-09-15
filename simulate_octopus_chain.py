import json
import hashlib
from datetime import datetime, timezone
import os

CHAIN_FILE = "octopus_ledger.json"

class OfflineTransactionBlock:
    def __init__(self, index, previous_hash, sender_card, recipient_card, amount, currency, nonce):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.sender_card = sender_card
        self.recipient_card = recipient_card
        self.amount = amount
        self.currency = currency
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_content = {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "sender_card": self.sender_card,
            "recipient_card": self.recipient_card,
            "amount": self.amount,
            "currency": self.currency,
            "nonce": self.nonce
        }
        block_string = json.dumps(block_content, sort_keys=True).encode("utf-8")
        return hashlib.sha256(block_string).hexdigest()

class OfflineLedgerChain:
    def __init__(self, storage_file=CHAIN_FILE):
        self.storage_file = storage_file
        self.chain = self.load_chain()

    def load_chain(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def create_genesis_block(self, postal_terminal_id):
        if len(self.chain) == 0:
            genesis_block = OfflineTransactionBlock(
                index=0,
                previous_hash="0" * 64,
                sender_card=f"POSTAL-NODE-{postal_terminal_id}",
                recipient_card="INITIAL-CAPITAL-POOL",
                amount=100.00,
                currency="CAD",
                nonce=1
            )
            self.chain.append(self.__block_to_dict(genesis_block))
            self.save_chain()
            print("[INFO] Genesis block initialized via postal node anchor.")

    def add_transaction(self, sender_card, recipient_card, amount, currency):
        last_entry = self.chain[-1]
        new_index = last_entry["index"] + 1
        previous_hash = last_entry["hash"]
        new_nonce = last_entry["nonce"] + 1

        new_block = OfflineTransactionBlock(
            index=new_index,
            previous_hash=previous_hash,
            sender_card=sender_card,
            recipient_card=recipient_card,
            amount=amount,
            currency=currency,
            nonce=new_nonce
        )

        self.chain.append(self.__block_to_dict(new_block))
        self.save_chain()
        print(f"[SUCCESS] Offline P2P transfer chained. Hash: {new_block.hash[:16]}... (Nonce: {new_nonce})")

    def __block_to_dict(self, block):
        return {
            "index": block.index,
            "previous_hash": block.previous_hash,
            "timestamp": block.timestamp,
            "sender_card": block.sender_card,
            "recipient_card": block.recipient_card,
            "amount": block.amount,
            "currency": block.currency,
            "nonce": block.nonce,
            "hash": block.hash,
            "corporate_issuer": "10839477 Canada Inc.",
            "creator_uuid": "e4f1b2a7-6d3c-4902-8a5e-9f7b6c5d4e1a"
        }

    def save_chain(self):
        with open(self.storage_file, "w", encoding="utf-8") as f:
            json.dump(self.chain, f, indent=4)

if __name__ == "__main__":
    print("Initializing Octopus 2.0 Offline Secure Element Simulator...")
    ledger = OfflineLedgerChain()
    
    if len(ledger.chain) == 0:
        ledger.create_genesis_block(postal_terminal_id="YEG-CP-042")

    ledger.add_transaction(
        sender_card="CARD-UID-ALPHA-99",
        recipient_card="CARD-UID-BETA-44",
        amount=15.50,
        currency="CAD"
    )
