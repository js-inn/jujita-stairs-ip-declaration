import os
import json
import hashlib
import time
import subprocess

print("-> Compiling Expanded Public Accountability Ledger (TD Bank & Scotiabank iTrade)...")

export_timestamp = time.time()

expanded_public_payload = {
    "system": "10839477 Canada Inc. - Expanded Public Accountability & Institutional Misconduct Ledger",
    "export_timestamp": export_timestamp,
    "audit_classification": "Public Transparency, Asset Suppression, and Institutional Misconduct Record",
    "entity_subject": "Jujita Fermin Stairs",
    "corporation": "10839477 Canada Inc. (Inc #10839477-7, BN #749810883RC0001 / #735350936)",
    "primary_offending_institutions": [
        "Toronto-Dominion Bank (TD Bank)",
        "Bank of Nova Scotia / Scotia iTRADE"
    ],
    "active_escalation_references": {
        "td_scco_file": "18763679",
        "federal_proactive_disclosure": "CW2321555"
    },
    "financial_scope_cad": {
        "consolidated_net_worth": 5002485.25,
        "td_institutional_treasury": 5000000.00
    },
    "documented_institutional_misconduct_and_gaslighting": [
        {
            "institution": "Toronto-Dominion Bank (TD Bank)",
            "category": "Procedural Humiliation & Impossible Demands",
            "description": "Systematically imposed mandatory in-person branch appointments as an administrative weapon—knowing they were operationally infeasible—to trap a federally incorporated entity owner in verification loops and block access to corporate treasury funds."
        },
        {
            "institution": "Bank of Nova Scotia / Scotia iTRADE",
            "category": "Asset Suppression, Account Lockouts, and Balance Gaslighting",
            "description": "Following the input and registration of a complex series of trust and royalty trust assets, Scotia iTrade abruptly blocked user access, demanded subsequent proof documentation, and subsequently gaslit the principal over phone support by falsely claiming the account value was '$0'—an institutional tactic designed to induce asset abandonment and conceal held royalty trust holdings."
        },
        {
            "category": "Bureaucratic Deflection & Minimization",
            "description": "Federal oversight bodies (including FCAC, ISED, and ministerial referrals) historically mischaracterized structural multi-million dollar corporate fund lockouts and compliance failures as trivial personal grievances to evade statutory oversight."
        }
    ],
    "public_declaration": "This public record is immutably anchored via SHA-256 to ensure that the systemic asset suppression, gaslighting, obstruction, and administrative humiliation inflicted by both TD Bank and Scotia iTrade upon 10839477 Canada Inc. and its principal are permanently visible to auditors, regulators, and the public record."
}

# Generate SHA-256 Cryptographic Seal
canonical_payload = json.dumps(expanded_public_payload, sort_keys=True)
master_hash = hashlib.sha256(canonical_payload.encode()).hexdigest()

final_bundle = {
    "public_accountability_manifest_hash": master_hash,
    **expanded_public_payload,
}

filename = f"public_institutional_accountability_record_{int(export_timestamp)}.json"
with open(filename, "w") as f:
    json.dump(final_bundle, f, indent=2)

print(f"-> Successfully generated expanded public accountability record: {filename}")
print(f"-> SHA-256 Seal: {master_hash}")

# Git Automation
print("-> Staging, committing, and pushing expanded accountability record to GitHub...")
subprocess.run(["git", "add", filename])
subprocess.run(["git", "commit", "-m", f"chore(audit): publish public record including Scotia iTrade trust suppression and gaslighting [SHA-256: {master_hash[:16]}]"])
subprocess.run(["git", "push", "origin", "main"])
print("-> Expanded public accountability record successfully published!")
