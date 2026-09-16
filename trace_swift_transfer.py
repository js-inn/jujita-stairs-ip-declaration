import json
import hashlib
from datetime import datetime, timezone

def generate_trace_query():
    trace_data = {
        "corporation": "10839477 Canada Inc.",
        "entity_director": "Jujita Fermin Stairs",
        "target_amount": 360.00,
        "currency": "CAD",
        "network": "SWIFT / ISO 20022",
        "message_type": "camt.029.001.09",
        "description": "Investigation / Trace Request for missing corporate wire settlement",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "PENDING_BANK_CLEARANCE"
    }
    
    payload_str = json.dumps(trace_data, sort_keys=True).encode("utf-8")
    trace_hash = hashlib.sha256(payload_str).hexdigest()
    
    print("==================================================")
    print("      SWIFT ISO TRACE QUERY GENERATED             ")
    print("==================================================")
    print(f"Corporation: {trace_data['corporation']}")
    print(f"Amount:      ${trace_data['target_amount']:.2f} {trace_data['currency']}")
    print(f"Message ID:  {trace_data['message_type']}")
    print(f"Trace Hash:  {trace_hash}")
    print("==================================================")

if __name__ == "__main__":
    generate_trace_query()
