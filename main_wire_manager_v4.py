import json
import os

def generate_html_dashboard():
    # Detect JSON path
    json_path = 'wire_status.json'
    if not os.path.exists(json_path) and os.path.exists('/sdcard/Download/wire_status.json'):
        json_path = '/sdcard/Download/wire_status.json'

    wires = []
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r') as f:
                wires = json.load(f)
        except Exception:
            wires = []

    total_wires = len(wires)
    available_cnt = 0
    in_transit_cnt = 0
    rejected_cnt = 0

    table_rows = ""
    for w in wires:
        st = str(w.get("iso_status", "")).strip().upper()
        
        # Categorize for top summary cards
        if "ACCC" in st or "ACSC" in st or "AVAILABLE" in st:
            available_cnt += 1
            badge = '<span style="background-color:#d4edda;color:#155724;padding:4px 8px;border-radius:4px;font-weight:bold;">ACCC (Available)</span>'
        elif "ACSP" in st or "TRANSIT" in st:
            in_transit_cnt += 1
            badge = '<span style="background-color:#fff3cd;color:#856404;padding:4px 8px;border-radius:4px;font-weight:bold;">ACSP (In Transit)</span>'
        elif "RJCT" in st or "REJECTED" in st:
            rejected_cnt += 1
            badge = '<span style="background-color:#f8d7da;color:#721c24;padding:4px 8px;border-radius:4px;font-weight:bold;">RJCT (REJECTED)</span>'
        else:
            badge = f'<span>{st}</span>'

        tx_id = w.get("transaction_id", "N/A")
        amount = f'{w.get("amount", "0.00")} {w.get("currency", "CAD")}'
        uetr = w.get("uetr", "N/A")
        bic = w.get("sender_bic", "N/A") if w.get("sender_bic") else "N/A"

        table_rows += f"""
        <tr>
            <td style="padding:12px;border-bottom:1px solid #ddd;">{tx_id}</td>
            <td style="padding:12px;border-bottom:1px solid #ddd;">{badge}</td>
            <td style="padding:12px;border-bottom:1px solid #ddd;">{amount}</td>
            <td style="padding:12px;border-bottom:1px solid #ddd;font-family:monospace;">{uetr}</td>
            <td style="padding:12px;border-bottom:1px solid #ddd;">{bic}</td>
        </tr>
        """

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>ISO 20022 Wire Monitoring Dashboard</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 20px; background: #f4f6f9; }}
        .header {{ background: #1a2530; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        .cards {{ display: flex; gap: 15px; margin-bottom: 20px; }}
        .card {{ flex: 1; background: white; padding: 15px; border-radius: 8px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
        .card h3 {{ margin: 0; color: #6c757d; font-size: 14px; }}
        .card p {{ margin: 10px 0 0; font-size: 28px; font-weight: bold; color: #212529; }}
        .card.rejected p {{ color: #dc3545; }}
        table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
        th {{ background: #e9ecef; text-align: left; padding: 12px; color: #495057; }}
    </style>
</head>
<body>
    <div class="header">
        <h2>ISO 20022 Wire Monitoring Dashboard</h2>
    </div>
    <div class="cards">
        <div class="card"><h3>Total Wires</h3><p>{total_wires}</p></div>
        <div class="card"><h3>Available</h3><p>{available_cnt}</p></div>
        <div class="card"><h3>In Transit</h3><p>{in_transit_cnt}</p></div>
        <div class="card rejected"><h3>Rejected Alerts</h3><p>{rejected_cnt}</p></div>
    </div>
    <table>
        <thead>
            <tr>
                <th>Tx ID</th>
                <th>ISO Status</th>
                <th>Amount</th>
                <th>SWIFT UETR UUID</th>
                <th>Sender BIC</th>
            </tr>
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>
</body>
</html>"""

    with open("wire_dashboard.html", "w") as f:
        f.write(html_content)
    print(f"[Success] Dashboard generated. Total: {total_wires} | Rejected: {rejected_cnt}")

if __name__ == "__main__":
    generate_html_dashboard()
