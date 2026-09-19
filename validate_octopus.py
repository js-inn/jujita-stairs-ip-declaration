import json
import hashlib
import os

CHAIN_FILE = "octopus_ledger.json"

def validate_chain():
    if not os.path.exists(CHAIN_FILE):
        print(f"[ERROR] Ledger file {CHAIN_FILE} not found.")
        return False

    with open(CHAIN_FILE, "r", encoding="utf-8") as f:
        chain = json.load(f)

    if not chain:
        print("[WARNING] Ledger chain is empty.")
        return True

    print(f"Auditing chain length: {len(chain)} blocks...")

    for i, block in enumerate(chain):
        if i == 0:
            if block["index"] != 0:
                print(f"[FAIL] Invalid genesis index: {block['index']}")
                return False
            if block["previous_hash"] != "0" * 64:
                print(f"[FAIL] Genesis previous_hash is corrupted.")
                return False
        else:
            prev_block = chain[i - 1]
            if block["previous_hash"] != prev_block["hash"]:
                print(f"[FAIL] Broken link at block index {i}! Previous hash mismatch.")
                return False
            
            if block["nonce"] != prev_block["nonce"] + 1:
                print(f"[FAIL] Nonce sequence failure at block index {i}.")
                return False

        stored_hash = block["hash"]
        block_content = {
            "index": block["index"],
            "previous_hash": block["previous_hash"],
            "timestamp": block["timestamp"],
            "sender_card": block["sender_card"],
            "recipient_card": block["recipient_card"],
            "amount": block["amount"],
            "currency": block["currency"],
            "nonce": block["nonce"]
        }
        
        computed_string = json.dumps(block_content, sort_keys=True).encode("utf-8")
        computed_hash = hashlib.sha256(computed_string).hexdigest()

        if computed_hash != stored_hash:
            print(f"[FAIL] Hash mismatch at block index {i}! Ledger has been altered.")
            return False

    print("[SUCCESS] Chain validation passed. Ledger immutability and cryptographic integrity verified.")
    return True

if __name__ == "__main__":
    validate_chain()
