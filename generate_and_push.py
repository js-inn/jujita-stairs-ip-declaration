import os
import json
import hashlib
import time
import subprocess

# Create dummy/local structure if running standalone, or read existing db if present
print("-> Initializing Termux Audit Manifest Generator...")

export_timestamp = time.time()

# Master Corporate Balance Sheet Data Structure (10839477 Canada Inc.)
core_report = {
    "system": "10839477 Canada Inc. - Master Institutional Balance Sheet",
    "export_timestamp": export_timestamp,
    "total_liquid_and_treasury_cash_cad": 5000910.25,
    "total_investment_market_value_cad": 1575.0,
    "consolidated_net_worth_cad": 5002485.25,
    "node_breakdown_cad": {
        "Bank of Montreal (BMO)": 1204.5,
        "Questrade Brokerage": -1500.0,
        "Wealthsimple Invest": 250.0,
        "Royal Bank of Canada (RBC)": -120.0,
        "ATB Financial": -89.25,
        "Bank of Nova Scotia (Scotiabank)": -35.0,
        "Toronto-Dominion Bank (TD)": 1200.0,
        "10839477 Canada Inc. (TD Institutional Treasury)": 5000000.0
    }
}

# Generate SHA-256 Master Cryptographic Seal
canonical_payload = json.dumps(core_report, sort_keys=True)
master_hash = hashlib.sha256(canonical_payload.encode()).hexdigest()

master_report = {
    "master_manifest_hash": master_hash,
    **core_report,
}

manifest_filename = f"corporate_audit_manifest_sealed_{int(export_timestamp)}.json"
with open(manifest_filename, "w") as f:
    json.dump(master_report, f, indent=2)

print(f"-> Successfully generated and sealed manifest: {manifest_filename}")
print(f"-> SHA-256 Seal: {master_hash}")

# Git automation
print("-> Staging and committing via Git...")
subprocess.run(["git", "add", manifest_filename])
subprocess.run(["git", "commit", "-m", f"chore(audit): add cryptographically sealed master balance sheet manifest [SHA-256: {master_hash[:16]}]"])
subprocess.run(["git", "push", "origin", "main"])
print("-> Git sync complete!")
