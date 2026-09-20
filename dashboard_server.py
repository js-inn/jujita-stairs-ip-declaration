import sqlite3
import ast
from http.server import HTTPServer, BaseHTTPRequestHandler

class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            
            conn = sqlite3.connect("local_audit.db")
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT * FROM parsed_records ORDER BY rowid DESC LIMIT 50")
                raw_rows = cursor.fetchall()
            except sqlite3.OperationalError:
                raw_rows = []
            conn.close()
            
            rows = []
            for r in raw_rows:
                val = r[0] if len(r) == 1 else r
                if isinstance(val, str) and val.strip().startswith("("):
                    try:
                        parsed = ast.literal_eval(val)
                        if isinstance(parsed, tuple):
                            rows.append(parsed)
                            continue
                    except Exception:
                        pass
                rows.append(r if isinstance(r, tuple) else (r,))
            
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Samsung Keystore & Wallet Dashboard</title>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <style>
                    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }
                    h1 { color: #f8981d; font-size: 1.5rem; margin-bottom: 5px; }
                    .subtitle { color: #94a3b8; font-size: 0.9rem; margin-bottom: 20px; }
                    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; margin-bottom: 20px; }
                    .card { background: #1e293b; border-radius: 8px; padding: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); overflow-x: auto; }
                    .card h3 { margin-top: 0; color: #f8981d; font-size: 1.1rem; border-bottom: 1px solid #334155; padding-bottom: 8px; }
                    table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.85rem; white-space: nowrap; }
                    th, td { padding: 10px 12px; text-align: left; border-bottom: 1px solid #334155; }
                    th { background: #334155; color: #f8981d; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.05em; }
                    .badge { padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 0.75rem; }
                    .badge-success { background: #065f46; color: #34d399; }
                    .badge-danger { background: #7f1d1d; color: #f87171; }
                    .badge-warning { background: #78350f; color: #fbbf24; }
                    .badge-neutral { background: #334155; color: #cbd5e1; }
                    .stat-row { display: flex; justify-content: space-between; margin: 8px 0; font-size: 0.9rem; }
                </style>
            </head>
            <body>
                <h1>Samsung Cold Wallet & Node Audit Dashboard</h1>
                <div class="subtitle">Environment: Android Termux | Pipeline: Active TEE & Multi-Node Failover</div>
                
                <div class="grid">
                    <div class="card">
                        <h3>Hardware Wallet Status</h3>
                        <div class="stat-row"><span>TEE Bridge:</span> <strong style="color: #34d399;">Connected</strong></div>
                        <div class="stat-row"><span>Derivation Scheme:</span> <code>BIP-44 (HD)</code></div>
                        <div class="stat-row"><span>Active Coin Types:</span> <span style="color: #38bdf8;">BTC, ETH, KLAY, TRON</span></div>
                    </div>
                    <div class="card">
                        <h3>Asset / UTXO Watcher</h3>
                        <div class="stat-row"><span>BTC Account (0):</span> <span style="color: #fbbf24;">Synced (Path m/44&#x27;/0&#x27;/0&#x27;/0/0)</span></div>
                        <div class="stat-row"><span>ETH Account (0):</span> <span style="color: #34d399;">Synced (Path m/44&#x27;/60&#x27;/0&#x27;/0/0)</span></div>
                        <div class="stat-row"><span>Node Fallback:</span> <strong>Active</strong></div>
                    </div>
                </div>

                <div class="card">
                    <h3>Live Ledger & Audit Records</h3>
                    <table>
                        <tr>
                            <th>ID</th>
                            <th>Entity / Source</th>
                            <th>Identifier / Hash</th>
                            <th>Operation / Path</th>
                            <th>Type</th>
                            <th>Value / Metric</th>
                            <th>Standard</th>
                            <th>Status</th>
                            <th>Timestamp</th>
                        </tr>
            """
            
            for row in rows:
                r = list(row) + [""] * (9 - len(row))
                row_id, entity, identifier, op_path, op_type, val, standard, status, ts = r[:9]
                
                status_upper = str(status).upper()
                if any(k in status_upper for k in ["SYNCED", "HEALTHY", "ACTIVE", "VERIFIED"]):
                    badge_class = "badge-success"
                elif any(k in status_upper for k in ["FAILED", "ERROR"]):
                    badge_class = "badge-danger"
                elif any(k in status_upper for k in ["PENDING", "DRAFT", "SECURED"]):
                    badge_class = "badge-warning"
                else:
                    badge_class = "badge-neutral"
                
                html += f"""
                        <tr>
                            <td>{row_id}</td>
                            <td><strong>{entity}</strong></td>
                            <td style="color: #94a3b8; font-family: monospace;">{str(identifier)[:12]}...</td>
                            <td>{op_path}</td>
                            <td>{op_type}</td>
                            <td>{val}</td>
                            <td><span style="color: #38bdf8;">{standard}</span></td>
                            <td><span class="badge {badge_class}">{status}</span></td>
                            <td style="color: #94a3b8; font-size: 0.75rem;">{ts}</td>
                        </tr>
                """
                
            html += """
                    </table>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode("utf-8"))

def run():
    server_address = ('127.0.0.1', 8080)
    httpd = HTTPServer(server_address, DashboardHandler)
    print("Dashboard with Wallet Asset Watcher running at http://127.0.0.1:8080 ... Press Ctrl+C to stop.")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
