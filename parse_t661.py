import sqlite3
import xml.etree.ElementTree as ET

def parse_and_log_xsd(xsd_path, db_path="tax_audit_log.db"):
    tree = ET.parse(xsd_path)
    root = tree.getroot()

    # Strip namespaces
    for elem in root.iter():
        if '}' in elem.tag:
            elem.tag = elem.tag.split('}', 1)[1]

    fields = []
    for seq in root.findall(".//complexType//sequence"):
        for child in seq:
            ref = child.get('ref', '').split(':')[-1]
            fields.append({
                "field_name": ref,
                "min_occurs": child.get('minOccurs', '1'),
                "max_occurs": child.get('maxOccurs', '1')
            })

    # Connect to database and store schema metadata
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS t661_schema_fields (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            field_name TEXT UNIQUE,
            min_occurs TEXT,
            max_occurs TEXT
        )
    """)

    for f in fields:
        cursor.execute("""
            INSERT OR REPLACE INTO t661_schema_fields (field_name, min_occurs, max_occurs)
            VALUES (?, ?, ?)
        """, (f["field_name"], f["min_occurs"], f["max_occurs"]))

    conn.commit()
    conn.close()
    print(f"Successfully parsed and logged {len(fields)} T661 Part 7 fields into {db_path}.")

if __name__ == "__main__":
    parse_and_log_xsd("t661_part7.xsd")
