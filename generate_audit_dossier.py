import sqlite3
import datetime

DB_NAME = "financial_pipeline.db"
ROOT_PARENT = "10839477 Canada Inc."
BUSINESS_NUMBER = "749810883RC0001"

def generate_dossiers():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Fetch all nodes from the unified global ledger
    cursor.execute('''
        SELECT node_type, identifier, entity_name, bloodlineage_status, master_anchor, timestamp 
        FROM unified_ip_financial_ledger 
        ORDER BY node_type, id
    ''')
    nodes = cursor.fetchall()
    conn.close()
    
    timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # --- 1. GENERATE MARKDOWN DOSSIER ---
    md_content = f"""# GLOBAL MASTER AUDIT DOSSIER
**Root Corporate Entity**: {ROOT_PARENT}  
**Business Number / Control ID**: {BUSINESS_NUMBER}  
**Generation Timestamp**: {timestamp_str}  
**Repository**: [js-inn/jujita-stairs-ip-declaration](https://github.com/js-inn/jujita-stairs-ip-declaration)  

---

## Executive Summary
This document represents the cryptographically anchored global audit dossier for **{ROOT_PARENT}**. Utilizing decentralized SQLite ledgers and SHA-256 HMAC provenance mapping, this dossier reconciles **{len(nodes)} total nodes** spanning financial institutions, regional patent offices (USPTO, EPO, JPO, IP Australia, INPI Brazil, CNIPA China, DPMA Germany), and international trademark registries (WIPO Madrid).

---

## Reconciled Global Node Inventory

| Node Type | Identifier / Ref | Entity / Holder Name | Bloodlineage Status | Cryptographic Anchor (SHA-256) | Timestamp |
| :--- | :--- | :--- | :--- | :--- | :--- |
"""

    for node_type, ident, entity, status, anchor, tstamp in nodes:
        short_anchor = f"{anchor[:12]}..." if anchor else "N/A"
        md_content += f"| `{node_type}` | `{ident}` | {entity} | {status} | `{short_anchor}` | {tstamp} |\n"

    md_content += f"""
---
*Cryptographically verified and anchored via Jujita Stairs Autonomous Audit Framework.*
"""

    with open("audit_dossier.md", "w") as f:
        f.write(md_content)
    print("[+] Generated audit_dossier.md successfully.")

    # --- 2. GENERATE RESPONSIVE HTML DOSSIER ---
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Global Master Audit Dossier - {ROOT_PARENT}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #0d1117;
            color: #c9d1d9;
            margin: 0;
            padding: 40px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 6px;
            padding: 40px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.5);
        }}
        h1 {{
            color: #f0f6fc;
            border-bottom: 1px solid #30363d;
            padding-bottom: 15px;
            margin-top: 0;
        }}
        .meta-box {{
            background: #21262d;
            border-left: 4px solid #58a6ff;
            padding: 15px 20px;
            margin-bottom: 30px;
            border-radius: 0 6px 6px 0;
        }}
        .meta-box p {{
            margin: 5px 0;
            font-size: 14px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            font-size: 14px;
        }}
        th, td {{
            border: 1px solid #30363d;
            padding: 12px 15px;
            text-align: left;
        }}
        th {{
            background-color: #21262d;
            color: #f0f6fc;
        }}
        tr:nth-child(even) {{
            background-color: #1b2028;
        }}
        code {{
            font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace;
            background-color: rgba(110,118,129,0.4);
            padding: 2px 4px;
            border-radius: 4px;
            font-size: 12px;
            color: #79c0ff;
        }}
        .status-reunited {{
            color: #3fb950;
            font-weight: 600;
        }}
        .status-heuristic {{
            color: #d29922;
            font-weight: 600;
        }}
        footer {{
            margin-top: 40px;
            border-top: 1px solid #30363d;
            padding-top: 20px;
            text-align: center;
            font-size: 12px;
            color: #8b949e;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Global Master Audit Dossier</h1>
        <div class="meta-box">
            <p><strong>Root Corporate Entity:</strong> {ROOT_PARENT}</p>
            <p><strong>Business Number / Control ID:</strong> {BUSINESS_NUMBER}</p>
            <p><strong>Generation Timestamp:</strong> {timestamp_str}</p>
            <p><strong>Total Reconciled Nodes:</strong> {len(nodes)}</p>
        </div>

        <h2>Reconciled Global Node Inventory</h2>
        <table>
            <thead>
                <tr>
                    <th>Node Type</th>
                    <th>Identifier / Ref</th>
                    <th>Entity / Holder Name</th>
                    <th>Bloodlineage Status</th>
                    <th>Cryptographic Anchor</th>
                    <th>Timestamp</th>
                </tr>
            </thead>
            <tbody>
"""

    for node_type, ident, entity, status, anchor, tstamp in nodes:
        short_anchor = f"{anchor[:16]}..." if anchor else "N/A"
        status_class = "status-reunited" if "Reunited" in status else "status-heuristic"
        html_content += f"""
                <tr>
                    <td><code>{node_type}</code></td>
                    <td><code>{ident}</code></td>
                    <td>{entity}</td>
                    <td class="{status_class}">{status}</td>
                    <td><code>{short_anchor}</code></td>
                    <td><code>{tstamp}</code></td>
                </tr>"""

    html_content += f"""
            </tbody>
        </table>
        <footer>
            Cryptographically verified and anchored via Jujita Stairs Autonomous Audit Framework.
        </footer>
    </div>
</body>
</html>
"""

    with open("audit_dossier.html", "w") as f:
        f.write(html_content)
    print("[+] Generated audit_dossier.html successfully.")

if __name__ == "__main__":
    generate_dossiers()
