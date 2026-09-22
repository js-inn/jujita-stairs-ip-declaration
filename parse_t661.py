import xml.etree.ElementTree as ET

tree = ET.parse("t661_part7.xml")
root = tree.getroot()

ns = {
    "xsd": "http://www.w3.org/2001/XMLSchema",
    "ol": "http://www.cra-arc.gc.ca/enov/ol/interfaces/efile/partnership/olT661Parts7/1-0-0"
}

for elem in root.findall(".//xsd:complexType[@name='Part7DataType']//xsd:element", ns):
    print(f"Ref: {elem.attrib.get('ref')} | minOccurs: {elem.attrib.get('minOccurs', '1')}")
