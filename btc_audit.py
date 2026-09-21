import urllib.request
import json

def check_bitcoin_address(address):
    url = f"https://mempool.space/api/address/{address}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'PydroidAuditTool'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            chain_stats = data.get('chain_stats', {})
            funded = chain_stats.get('funded_txo_sum', 0) / 1e8
            spent = chain_stats.get('spent_txo_sum', 0) / 1e8
            balance = funded - spent
            print(f"--- Bitcoin Address Audit ---")
            print(f"Address: {address}")
            print(f"Current Balance: {balance} BTC")
            return balance
    except Exception as e:
        print(f"[ERROR] Failed to query blockchain data: {e}")
        return None

if __name__ == "__main__":
    target_address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
    check_bitcoin_address(target_address)
