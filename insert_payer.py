import psycopg2
import pandas as pd
from fuzzywuzzy import fuzz, process

DATABASE_URL = "postgresql://postgres:golassie@db.cbgtocxhyfflpmaxbugd.supabase.co:5432/postgres"
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

all_payers_df = pd.read_excel("payer_with_payer_group.xlsx")

cursor.execute("SELECT payer_id, payer_name FROM payers")
existing_payers = cursor.fetchall()
existing_payer_dict = {payer_name: payer_id for payer_id, payer_name in existing_payers}

def find_best_match(new_payer_name):
    if not existing_payer_dict:
        return None, 0  
    best_match, score = process.extractOne(new_payer_name, existing_payer_dict.keys(), scorer=fuzz.token_sort_ratio)
    return (existing_payer_dict[best_match], score) if score >= 85 else (None, score)

def insert_payer(payer_group_name, payer_name, payer_number, conn):
    print(f"\nProcessing Payer: {payer_name}, Group: {payer_group_name}, Number: {payer_number}")

    cursor.execute("SELECT payer_group_id FROM payer_groups WHERE payer_group_name = %s", (payer_group_name,))
    payer_group_id = cursor.fetchone()

    if not payer_group_id:
        print(f"Error: Payer Group '{payer_group_name}' not found. Skipping...")
        return None
    payer_group_id = payer_group_id[0]

    cursor.execute("SELECT payer_id FROM payers WHERE payer_id = %s", (payer_number,))
    existing_payer = cursor.fetchone()

    if existing_payer:
        print(f"ℹ️ Payer '{payer_name}' already exists with payer_id '{payer_number}'. Skipping...")
        return payer_number

    matched_payer_id, similarity_score = find_best_match(payer_name)

    if matched_payer_id:
        print(f"Similar Payer Found: '{payer_name}' matches existing payer_id '{matched_payer_id}' with {similarity_score}% similarity. Using existing payer_id.")
        return matched_payer_id  

    cursor.execute(
        """
        INSERT INTO payers (payer_id, payer_group_id, payer_name) 
        VALUES (%s, %s, %s)
        """,
        (payer_number, payer_group_id, payer_name)
    )
    conn.commit()
    print(f" Payer '{payer_name}' inserted successfully with payer_id {payer_number}.")
    
    existing_payer_dict[payer_name] = payer_number
    return payer_number

for index, row in all_payers_df.iterrows():
    payer_group_name = row.get("Payer Group Name", "").strip()
    payer_name = row.get("Payer Name", "").strip()
    payer_number = str(row["Payer ID"]).strip() if pd.notna(row["Payer ID"]) else None

    if payer_group_name and payer_name and payer_number:
        insert_payer(payer_group_name, payer_name, payer_number, conn)
    else:
        print(f"Skipping row {index}: Missing required data.")

conn.commit()
cursor.close()
conn.close()
print("Database update completed. Connection closed.")
