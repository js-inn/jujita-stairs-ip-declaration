import hashlib, hmac, json, sqlite3, time
from typing import Dict, Tuple

class FraudMitigationEngine:
    def __init__(self, db_path: str = "fraud_audit.db", t_max: float = 0.50, secret_key: bytes = b"endpoint_secure_node_key"):
        self.db_path, self.t_max, self.secret_key = db_path, t_max, secret_key
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp REAL, host_id TEXT, 
                status TEXT, action TEXT, iei_score REAL, threshold REAL, 
                refusal_token TEXT, routing TEXT, metrics TEXT)""")
            conn.commit()

    def parse_payload_semantics(self, payload_text: str) -> Tuple[float, float, float]:
        t = payload_text.lower()
        a_l = min(1.0, sum(0.20 for w in ["indemnify", "liability", "waiver", "sole discretion", "arbitration", "breach"] if w in t))
        p_r = min(1.0, sum(0.20 for w in ["fee", "charge", "premium", "penalty", "subscription", "cost"] if w in t))
        f_r = min(1.0, sum(0.20 for w in ["notice", "delay", "forfeiture", "jurisdiction", "hurdle", "administrative"] if w in t))
        return a_l, p_r, f_r

    def calculate_iei(self, a_l: float, p_r: float, f_r: float) -> float:
        return round((0.4 * a_l) + (0.3 * p_r) + (0.3 * f_r), 4)

    def generate_refusal_token(self, meta: dict) -> str:
        return hmac.new(self.secret_key, json.dumps(meta, sort_keys=True).encode(), hashlib.sha256).hexdigest()

    def log_to_ledger(self, r: dict):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""INSERT INTO audit_log (timestamp, host_id, status, action, iei_score, threshold, refusal_token, routing, metrics)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                (r["timestamp"], r["host_id"], r["status"], r["action"], r["iei_score"], r["threshold"], r.get("refusal_token"), r.get("routing"), json.dumps(r["metrics"])))
            conn.commit()

    def evaluate_and_route(self, payload_text: str, host_id: str) -> Dict:
        a_l, p_r, f_r = self.parse_payload_semantics(payload_text)
        iei = self.calculate_iei(a_l, p_r, f_r)
        ts = time.time()
        meta = {"host_id": host_id, "iei": iei, "timestamp": ts}
        
        if iei > self.t_max:
            res = {"host_id": host_id, "status": "REJECTED", "action": "PROGRAMMATIC_DEEMED_REFUSAL", "iei_score": iei, "threshold": self.t_max, "refusal_token": self.generate_refusal_token(meta), "routing": "ILP_DECENTRALIZED_ESCROW_POOL", "metrics": {"A_l": a_l, "P_r": p_r, "F_r": f_r}, "timestamp": ts}
        else:
            res = {"host_id": host_id, "status": "APPROVED", "action": "STANDARD_EXECUTION", "iei_score": iei, "threshold": self.t_max, "refusal_token": None, "routing": None, "metrics": {"A_l": a_l, "P_r": p_r, "F_r": f_r}, "timestamp": ts}
        
        self.log_to_ledger(res)
        return res

if __name__ == "__main__":
    eng = FraudMitigationEngine(t_max=0.50)
    payload = """By accessing this network interface, you agree to indemnify the system operator for all data-breach liabilities under sole discretion. You agree to pay a mandatory monthly compliance subscription fee and accept that all claim recoveries require written notice subject to a 90-day administrative delay."""
    print(json.dumps(eng.evaluate_and_route(payload, host_id="node_central_corp_01"), indent=4))
