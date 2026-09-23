import sqlite3

DB_NAME = "financial_pipeline.db"

def run_cross_domain_analysis():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    print(f"\n=======================================================================")
    print(f"[*] CROSS-DOMAIN HYBRID ANALYSIS: STRUCTURAL LINEAGE & INFLUENCE")
    print(f"=======================================================================\n")
    
    # Fetch Corporate Hierarchies
    cursor.execute("SELECT parent_entity, child_entity, relationship_type, jurisdiction FROM corporate_hierarchy")
    structural_nodes = cursor.fetchall()
    
    # Fetch Leader-Follower Networks
    cursor.execute("SELECT leader_entity, follower_entity, influence_mechanism, domain FROM leader_follower_network")
    influence_nodes = cursor.fetchall()
    
    # Get unique entities involved in structural lineage
    entities = set()
    for p, c, _, _ in structural_nodes:
        entities.add(p)
        entities.add(c)
        
    for entity in sorted(entities):
        print(f"-----------------------------------------------------------------------")
        print(f" [Entity Dossier] {entity}")
        print(f"-----------------------------------------------------------------------")
        
        # 1. Structural Lineage (Parent-Child)
        has_structural = False
        print(f"  📂 Structural Lineage (Parent-Child):")
        for p, c, r, j in structural_nodes:
            if c == entity:
                print(f"     └── Legal Parent: {p} [{r}, Jurisdiction: {j}]")
                has_structural = True
            elif p == entity:
                print(f"     ├── Legal Subsidiary/Child: {c} [{r}, Jurisdiction: {j}]")
                has_structural = True
        if not has_structural:
            print(f"     └── [Independent / Root Entity or Sovereign Shell]")
            
        # 2. Ecosystem Gravity (Leader-Follower)
        has_influence = False
        print(f"  ⚡ Ecosystem Gravity (Leader-Follower):")
        for lead, foll, mech, dom in influence_nodes:
            # Match if entity name appears in leader or is part of follower string
            if entity.lower() in lead.lower():
                print(f"     ├── [As Leader] Drives '{foll}'")
                print(f"     │   Mechanism: {mech} ({dom})")
                has_influence = True
            elif entity.lower() in foll.lower():
                print(f"     ├── [As Follower/Ecosystem] Aligned with '{lead}'")
                print(f"     │   Mechanism: {mech} ({dom})")
                has_influence = True
        if not has_influence:
            print(f"     └── [Localized / Non-Networked Entity]")
        print()

    conn.close()

if __name__ == "__main__":
    run_cross_domain_analysis()
