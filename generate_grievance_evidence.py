import os
import json
import hashlib
import time
import subprocess

print("-> Compiling Institutional Grievance & Interaction Evidence Log...")

export_timestamp = time.time()

evidence_payload = {
    "system": "10839477 Canada Inc. - Institutional Grievance & Interaction Evidence Log",
    "export_timestamp": export_timestamp,
    "entity_subject": "Jujita Fermin Stairs",
    "corporation": "10839477 Canada Inc. (Inc #10839477-7, BN #749810883RC0001 / #735350936)",
    "primary_respondent_institution": "Toronto-Dominion Bank (TD Bank)",
    "active_escalation_references": {
        "td_scco_file": "18763679",
        "federal_proactive_disclosure": "CW2321555"
    },
    "documented_branch_interactions_and_barriers": [
        {
            "date": "2025-10-24",
            "location": "TD Branch - 10205 101 St Unit 148, Edmonton, AB",
            "type": "In-Person Appointment",
            "status": "Completed / Administrative friction encountered"
        },
        {
            "date": "2026-06-12",
            "location": "TD Branch - 10205 101 St Unit 148, Edmonton, AB",
            "type": "In-Person Appointment",
            "status": "Completed / Continued access restriction"
        },
        {
            "date": "2026-09-22",
            "action": "Formal escalation to TD Senior Customer Complaints Office (File 18763679)"
        },
        {
            "date": "2026-09-25",
            "action": "TD Direct Investing application declined / Institutional restriction upheld"
        }
    ],
    "systemic_findings": [
        "Institution conditioned corporate treasury access on mandatory in-person branch appointments despite documented operational infeasibility.",
        "Local branch personnel enforced administrative roadblocks outside their administrative jurisdiction.",
        "Parallel compliance failures noted with Scotiabank regarding manual account blocks and identity verification loops."
    ],
    "remedy_demanded": "Immediate remote executive override of branch appointment prerequisites, release of corporate treasury allocations, and written final position."
}

# Generate SHA-256 Cryptographic Seal
canonical_payload = json.dumps(evidence_payload, sort_keys=True)
master_hash = hashlib.sha256(canonical_payload.encode()).hexdigest()

final_evidence_bundle = {
    "evidence_manifest_hash": master_hash,
    **evidence_payload,
}

filename = f"institutional_grievance_evidence_{int(export_timestamp)}.json"
with open(filename, "w") as f:
    json.dump(final_evidence_bundle, f, indent=2)

print(f"-> Successfully generated evidence bundle: {filename}")
print(f"-> SHA-256 Seal: {master_hash}")

# Git Automation
print("-> Staging, committing, and pushing evidence log to GitHub...")
subprocess.run(["git", "add", filename])
subprocess.run(["git", "commit", "-m", f"chore(evidence): compile institutional grievance and interaction history [SHA-256: {master_hash[:16]}]"])
subprocess.run(["git", "push", "origin", "main"])
print("-> Evidence bundle successfully locked and pushed!")
