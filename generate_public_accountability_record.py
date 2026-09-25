import os
import json
import hashlib
import time
import subprocess

print("-> Compiling Unvarnished Public Accountability & Institutional Gaslighting Record...")

export_timestamp = time.time()

public_record_payload = {
    "system": "10839477 Canada Inc. - Public Accountability & Institutional Conduct Ledger",
    "export_timestamp": export_timestamp,
    "audit_classification": "Public Transparency, Grievance & Regulatory Accountability",
    "entity_subject": "Jujita Fermin Stairs",
    "corporation": "10839477 Canada Inc. (Inc #10839477-7, BN #749810883RC0001 / #735350936)",
    "primary_offending_institution": "Toronto-Dominion Bank (TD Bank)",
    "active_escalation_reference": {
        "td_scco_file": "18763679",
        "federal_proactive_disclosure": "CW2321555"
    },
    "financial_scope_cad": {
        "consolidated_net_worth": 5002485.25,
        "td_institutional_treasury": 5000000.00
    },
    "documented_institutional_misconduct_and_gaslighting": [
        {
            "category": "Procedural Humiliation & Impossible Demands",
            "description": "TD Bank and associated retail institutions systematically imposed mandatory in-person branch appointments as an administrative weapon—knowing they were operationally infeasible—to trap a federally incorporated entity owner in an endless verification loop and block access to legitimate corporate treasury funds."
        },
        {
            "category": "Bad-Faith Gatekeeping",
            "description": "Retail and branch personnel repeatedly demanded redundant, shifting documentation while ignoring valid certificates of incorporation, federal business numbers, and cryptographic attestations, treating a multi-million dollar corporate treasury account with intentional obstructionism."
        },
        {
            "category": "Bureaucratic Deflection & Minimization",
            "description": "Federal oversight bodies (including FCAC, ISED, and ministerial referrals) historically mischaracterized structural multi-million dollar corporate fund lockouts and compliance failures as trivial personal grievances (e.g., treating substantive institutional ledgers as low-value disputes), evading true statutory oversight."
        }
    ],
    "public_declaration": "This public record is immutably anchored via SHA-256 to ensure that the systemic institutional gaslighting, obstruction, and administrative humiliation inflicted by TD Bank upon 10839477 Canada Inc. and its principal are permanently visible to auditors, regulators, and the public record."
}

# Generate SHA-256 Cryptographic Seal
canonical_payload = json.dumps(public_record_payload, sort_keys=True)
master_hash = hashlib.sha256(canonical_payload.encode()).hexdigest()

final_bundle = {
    "public_accountability_manifest_hash": master_hash,
    **public_record_payload,
}

filename = f"public_institutional_accountability_record_{int(export_timestamp)}.json"
with open(filename, "w") as f:
    json.dump(final_bundle, f, indent=2)

print(f"-> Successfully generated public accountability record: {filename}")
print(f"-> SHA-256 Seal: {master_hash}")

# Git Automation
print("-> Staging, committing, and pushing public accountability record to GitHub...")
subprocess.run(["git", "add", filename])
subprocess.run(["git", "commit", "-m", f"chore(audit): publish public record of institutional gaslighting and TD Bank misconduct [SHA-256: {master_hash[:16]}]"])
subprocess.run(["git", "push", "origin", "main"])
print("-> Public accountability record successfully published!")
