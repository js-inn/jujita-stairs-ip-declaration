import xml.etree.ElementTree as ET

raw_xml_snippet = """<xsd:enumeration value="Sa"/>
<xsd:enumeration value="AB"/>
<xsd:enumeration value="ab"/>
<xsd:enumeration value="Ab"/>
<xsd:enumeration value="AL"/>
<xsd:enumeration value="al"/>
<xsd:enumeration value="Al"/>
<xsd:enumeration value="BC"/>
<xsd:enumeration value="bc"/>
<xsd:enumeration value="Bc"/>
<xsd:enumeration value="NT"/>
<xsd:enumeration value="nt"/>
<xsd:enumeration value="Nt"/>
<xsd:enumeration value="YT"/>
<xsd:enumeration value="yt"/>
<xsd:enumeration value="Yt"/>
<xsd:enumeration value="NL"/>
<xsd:enumeration value="nl"/>
<xsd:enumeration value="Nl"/>
<xsd:enumeration value="NF"/>
<xsd:enumeration value="nf"/>
<xsd:enumeration value="Nf"/>
<xsd:enumeration value="LB"/>
<xsd:enumeration value="lb"/>
<xsd:enumeration value="Lb"/>
<xsd:enumeration value="PQ"/>
<xsd:enumeration value="pq"/>
<xsd:enumeration value="Pq"/>
<xsd:enumeration value="QU"/>
<xsd:enumeration value="qu"/>
<xsd:enumeration value="Qu"/>
<xsd:enumeration value="NU"/>
<xsd:enumeration value="nu"/>
<xsd:enumeration value="Nu"/>
<xsd:enumeration value="NN"/>
<xsd:enumeration value="nn"/>
<xsd:enumeration value="Nn"/>
<xsd:enumeration value="US"/>
<xsd:enumeration value="us"/>
<xsd:enumeration value="Us"/>
<xsd:enumeration value="ZZ"/>
<xsd:enumeration value="zz"/>
<xsd:enumeration value="Zz"/>
</xsd:restriction>
</xsd:simpleType>
<xsd:simpleType name="stateType">
<xsd:restriction base="xsd:string">
<xsd:enumeration value="AL"/>
<xsd:enumeration value="al"/>
<xsd:enumeration value="NV"/>
<xsd:enumeration value="nv"/>
<xsd:enumeration value="AK"/>
<xsd:enumeration value="ak"/>
<xsd:enumeration value="NH"/>
<xsd:enumeration value="nh"/>
<xsd:enumeration value="AZ"/>
<xsd:enumeration value="az"/>
<xsd:enumeration value="NJ"/>
<xsd:enumeration value="nj"/>
<xsd:enumeration value="AR"/>
<xsd:enumeration value="ar"/>
<xsd:enumeration value="NM"/>
<xsd:enumeration value="nm"/>
<xsd:enumeration value="CA"/>
<xsd:enumeration value="ca"/>
<xsd:enumeration value="NY"/>
<xsd:enumeration value="ny"/>
<xsd:enumeration value="CO"/>
<xsd:enumeration value="co"/>
<xsd:enumeration value="NC"/>
<xsd:enumeration value="nc"/>
<xsd:enumeration value="CT"/>
<xsd:enumeration value="ct"/>
<xsd:enumeration value="ND"/>
<xsd:enumeration value="nd"/>
<xsd:enumeration value="DE"/>
<xsd:enumeration value="de"/>
<xsd:enumeration value="OH"/>
<xsd:enumeration value="oh"/>
<xsd:enumeration value="DC"/>
<xsd:enumeration value="dc"/>
<xsd:enumeration value="OK"/>
<xsd:enumeration value="ok"/>
<xsd:enumeration value="FL"/>
<xsd:enumeration value="fl"/>
<xsd:enumeration value="OR"/>
<xsd:enumeration value="or"/>
<xsd:enumeration value="GA"/>
<xsd:enumeration value="ga"/>
<xsd:enumeration value="PA"/>
<xsd:enumeration value="pa"/>
<xsd:enumeration value="HI"/>
<xsd:enumeration value="hi"/>
<xsd:enumeration value="RI"/>
<xsd:enumeration value="ri"/>
<xsd:enumeration value="ID"/>
<xsd:enumeration value="id"/>
<xsd:enumeration value="SC"/>
<xsd:enumeration value="sc"/>
<xsd:enumeration value="IL"/>
<xsd:enumeration value="il"/>
<xsd:enumeration value="SD"/>
<xsd:enumeration value="sd"/>
<xsd:enumeration value="IN"/>
<xsd:enumeration value="in"/>
<xsd:enumeration value="TN"/>
<xsd:enumeration value="tn"/>
<xsd:enumeration value="IA"/>
<xsd:enumeration value="ia"/>
<xsd:enumeration value="TX"/>
<xsd:enumeration value="tx"/>
<xsd:enumeration value="KS"/>
<xsd:enumeration value="ks"/>
<xsd:enumeration value="UT"/>
<xsd:enumeration value="ut"/>
<xsd:enumeration value="KY"/>
<xsd:enumeration value="ky"/>
<xsd:enumeration value="VT"/>
<xsd:enumeration value="vt"/>
<xsd:enumeration value="LA"/>
<xsd:enumeration value="la"/>
<xsd:enumeration value="VA"/>
<xsd:enumeration value="va"/>
<xsd:enumeration value="ME"/>
<xsd:enumeration value="me"/>
<xsd:enumeration value="WA"/>
<xsd:enumeration value="wa"/>
<xsd:enumeration value="MD"/>
<xsd:enumeration value="md"/>
<xsd:enumeration value="WV"/>
<xsd:enumeration value="wv"/>
<xsd:enumeration value="MA"/>
<xsd:enumeration value="ma"/>
<xsd:enumeration value="WI"/>
<xsd:enumeration value="wi"/>
<xsd:enumeration value="MI"/>
<xsd:enumeration value="mi"/>
<xsd:enumeration value="WY"/>
<xsd:enumeration value="wy"/>
<xsd:enumeration value="MN"/>
<xsd:enumeration value="mn"/>
<xsd:enumeration value="MS"/>
<xsd:enumeration value="ms"/>
<xsd:enumeration value="MO"/>
<xsd:enumeration value="mo"/>
<xsd:enumeration value="MT"/>
<xsd:enumeration value="mt"/>
<xsd:enumeration value="NE"/>
<xsd:enumeration value="ne"/>
<xsd:enumeration value="PR"/>
<xsd:enumeration value="pr"/>
<xsd:enumeration value="AS"/>
<xsd:enumeration value="as"/>
<xsd:enumeration value="FM"/>
<xsd:enumeration value="fm"/>
<xsd:enumeration value="GU"/>
<xsd:enumeration value="gu"/>
<xsd:enumeration value="MH"/>
<xsd:enumeration value="mh"/>
<xsd:enumeration value="MP"/>
<xsd:enumeration value="mp"/>
<xsd:enumeration value="PW"/>
<xsd:enumeration value="pw"/>
<xsd:enumeration value="VI"/>
<xsd:enumeration value="vi"/>
<xsd:enumeration value="ZZ"/>
<xsd:enumeration value="zz"/>
</xsd:restriction>
</xsd:simpleType>
<xsd:simpleType name="char22Type">
<xsd:restriction base="xsd:string">
<xsd:minLength value="1"/>
<xsd:maxLength value="22"/>
</xsd:restriction>
</xsd:simpleType>
<xsd:simpleType name="numeric3Type">
<xsd:restriction base="xsd:string">
<xsd:pattern value="\\d{3}"/>
</xsd:restriction>
</xsd:simpleType>
<xsd:simpleType name="phoneType">
<xsd:restriction base="xsd:string">
<xsd:pattern value="\\d{3}-\\d{4}"/>
</xsd:restriction>
</xsd:simpleType>
<xsd:simpleType name="int7Type">
<xsd:restriction base="xsd:string">
<xsd:pattern value="\\d{1,7}"/>
</xsd:restriction>
</xsd:simpleType>
<xsd:simpleType name="char60Type">
<xsd:restriction base="xsd:string">
<xsd:minLength value="1"/>
<xsd:maxLength value="60"/>
</xsd:restriction>
</xsd:simpleType>"""

xml_data = f"""<root xmlns:xsd="http://www.w3.org/2001/XMLSchema">
<xsd:simpleType name="provinceType">
<xsd:restriction base="xsd:string">
{raw_xml_snippet}
</root>"""

root = ET.fromstring(xml_data)
ns = {'xsd': 'http://www.w3.org/2001/XMLSchema'}

for simple_type in root.findall('xsd:simpleType', ns):
    type_name = simple_type.attrib.get('name')
    enums = [e.attrib['value'] for e in simple_type.findall('.//xsd:enumeration', ns)]
    pattern = simple_type.find('.//xsd:pattern', ns)

    print(f"Type: {type_name}")
    if enums:
        print(f" - Enumeration Count: {len(enums)}")
    if pattern is not None:
        print(f" - Pattern: {pattern.attrib['value']}")
