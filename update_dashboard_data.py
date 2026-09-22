import json
import os

def inject_dashboard_data():
    bundle_filename = "gvt_verified_audit_bundle.json"
    html_filename = "index.html"
    
    if not os.path.exists(bundle_filename):
        print(f"[!] Error: {bundle_filename} not found.")
        return
        
    if not os.path.exists(html_filename):
        print(f"[!] Error: {html_filename} not found.")
        return
        
    with open(bundle_filename, "r", encoding="utf-8") as f:
        bundle_data = json.load(f)
        
    hierarchy = bundle_data["data"]["corporate_hierarchy"]
    
    # Build HTML snippet for the corporate hierarchy table/cards
    rows_html = ""
    for node in hierarchy:
        rows_html += f"""
        <tr>
            <td><code>{node['node_id']}</code></td>
            <td><strong>{node['entity_name']}</strong></td>
            <td>{node['business_number']}</td>
            <td><span class="badge">{node['status']}</span></td>
            <td>{node['associated_contracts']}</td>
        </tr>
        """
        
    with open(html_filename, "r", encoding="utf-8") as f:
        html_content = f.read()
        
    # Check if a placeholder exists or insert into a designated container
    placeholder = "<!-- GVT_CORPORATE_HIERARCHY_TARGET -->"
    
    if placeholder in html_content:
        updated_html = html_content.replace(placeholder, rows_html)
        with open(html_filename, "w", encoding="utf-8") as f:
            f.write(updated_html)
        print("[SUCCESS] Corporate hierarchy dynamically injected into index.html")
    else:
        # If placeholder doesn't exist, let's append a section before </body>
        section_html = f"""
        <section class="gvt-card" style="margin-top: 20px; padding: 20px; background: var(--card); border: 1px solid var(--border); border-radius: 8px;">
            <h3 style="color: var(--heading);">Sovereign Corporate Hierarchy & Entity Mapping</h3>
            <p style="color: var(--text); font-size: 13px;">Authenticated via GVT Framework | Primary BN: 749810883RC0001</p>
            <div style="overflow-x: auto;">
                <table style="width: 100%; border-collapse: collapse; margin-top: 10px; color: var(--text); text-align: left;">
                    <thead>
                        <tr style="border-bottom: 1px solid var(--border);">
                            <th style="padding: 8px;">Node ID</th>
                            <th style="padding: 8px;">Entity Name</th>
                            <th style="padding: 8px;">Business Number</th>
                            <th style="padding: 8px;">Status</th>
                            <th style="padding: 8px;">Contracts</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows_html}
                    </tbody>
                </table>
            </div>
        </section>
        </body>
        """
        if "</body>" in html_content:
            updated_html = html_content.replace("</body>", section_html)
            with open(html_filename, "w", encoding="utf-8") as f:
                f.write(updated_html)
            print("[SUCCESS] Appended corporate hierarchy section to index.html")
        else:
            print("[!] Could not find </body> tag in index.html")

if __name__ == "__main__":
    inject_dashboard_data()
