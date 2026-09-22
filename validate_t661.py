import sqlite3
import xml.etree.ElementTree as ET

def validate_t661_xml(xml_path, db_path="tax_audit_log.db"):
    # 1. Load expected schema fields from database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT field_name, min_occurs, max_occurs FROM t661_schema_fields")
    schema_rules = {row[0]: {"min": int(row[1]), "max": int(row[2])} for row in cursor.fetchall()}
    conn.close()

    if not schema_rules:
        print("Error: No schema rules found in database. Run parse_t661.py first.")
        return False

    # 2. Parse the target XML file
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except Exception as e:
        print(f"Error parsing XML file: {e}")
        return False

    # Strip namespaces for consistent tag matching
    for elem in root.iter():
        if '}' in elem.tag:
            elem.tag = elem.tag.split('}', 1)[1]

    # 3. Count occurrences of each field in the XML document
    element_counts = {}
    for elem in root.iter():
        tag = elem.tag
        element_counts[tag] = element_counts.get(tag, 0) + 1

    # 4. Validate against database constraints
    errors = []
    for field_name, rules in schema_rules.items():
        count = element_counts.get(field_name, 0)
        
        if count < rules["min"]:
            errors.append(f"Missing required field '{field_name}': found {count}, expected minimum {rules['min']}")
        elif count > rules["max"]:
            errors.append(f"Field '{field_name}' exceeds maximum occurrence: found {count}, expected maximum {rules['max']}")

    if errors:
        print("Validation Failed:")
        for err in errors:
            print(f"  ❌ {err}")
        return False
    else:
        print(f"Validation Successful: '{xml_path}' complies with all T661 Part 7 database schema rules.")
        return True

if __name__ == "__main__":
    validate_t661_xml("cra_submission.xml")
