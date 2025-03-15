import pandas as pd
import psycopg2

DATABASE_URL = "postgresql://postgres:golassie@db.cbgtocxhyfflpmaxbugd.supabase.co:5432/postgres"

conn = psycopg2.connect(DATABASE_URL)
conn.autocommit = True  
cursor = conn.cursor()

df = pd.read_excel("payer_with_payer_group.xlsx")

payer_group_ids = {}  

for payer_group in df["Payer Group Name"].unique():
    print(f"Inserting {payer_group} into payer_groups table")
    cursor.execute("SELECT payer_group_id FROM payer_groups WHERE payer_group_name = %s", (payer_group,))
    result = cursor.fetchone()

    if result:
        payer_group_ids[payer_group] = result[0]  
    else:
        cursor.execute("INSERT INTO payer_groups (payer_group_name) VALUES (%s) RETURNING payer_group_id", (payer_group,))
        payer_group_id = cursor.fetchone()[0]  
        payer_group_ids[payer_group] = payer_group_id

print("✅ Payer Groups Inserted")

cursor.close()
conn.close()
print("✅ Database Connection Closed")
