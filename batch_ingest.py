import os
import sqlite3
import xml.etree.ElementTree as ET

DB_NAME = "tax_audit_log.db"
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS tax_audit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        schema_name TEXT,
        element_ref TEXT,
        min_occurs TEXT,
        max_occurs TEXT
    )
''')

xml_files = [f for f in os.listdir(".") if f.endswith(".xml")]
print(f"Found schema files: {xml_files}")

for filename in xml_files:
    schema_name = filename.split(".")[0].upper()
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
        for elem in root.iter():
            tag = elem.tag.split("}")[-1]
            if tag == "element":
                name = elem.attrib.get("name") or elem.attrib.get("ref")
                min_occ = elem.attrib.get("minOccurs", "1")
                max_occ = elem.attrib.get("maxOccurs", "1")
                if name:
                    cursor.execute(
                        "INSERT INTO tax_audit_log (schema_name, element_ref, min_occurs, max_occurs) VALUES (?, ?, ?, ?)",
                        (schema_name, name, min_occ, max_occ)
                    )
    except Exception as e:
        print(f"Error parsing {filename}: {e}")

conn.commit()
conn.close()
print("Batch schema ingestion into tax_audit_log.db complete!")
