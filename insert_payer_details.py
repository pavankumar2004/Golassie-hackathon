import psycopg2
import pandas as pd
from fuzzywuzzy import process

DATABASE_URL = "postgresql://postgres:golassie@db.cbgtocxhyfflpmaxbugd.supabase.co:5432/postgres"
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Read both Excel sheets
payer_group_df = pd.read_excel("payer_with_payer_group.xlsx")
availity_df = pd.read_excel("Payers.xlsx", sheet_name="Availity")

def get_payer_id(payer_name, payer_group_name, conn):
    cursor.execute("SELECT payer_group_id FROM payer_groups WHERE payer_group_name = %s", (payer_group_name,))
    payer_group_id = cursor.fetchone()

    if not payer_group_id:
        print(f"Error: Payer Group '{payer_group_name}' not found.")
        return None

    payer_group_id = payer_group_id[0]

    cursor.execute("SELECT payer_id, payer_name FROM payers WHERE payer_group_id = %s", (payer_group_id,))
    payer_records = cursor.fetchall()

    matched_payer = process.extractOne(payer_name, [record[1] for record in payer_records])

    if matched_payer and matched_payer[1] >= 80:
        matched_payer_name = matched_payer[0]
        payer_id = payer_records[[record[1] for record in payer_records].index(matched_payer_name)][0]
        return payer_id
    else:
        print(f"Error: No sufficient match found for payer '{payer_name}' in payer group '{payer_group_name}'.")
        return None

def find_best_match(payer_name, availity_df):
    exact_match = availity_df[availity_df['Payer Name'].str.lower() == payer_name.lower()]
    
    if not exact_match.empty:
        return exact_match.iloc[0]
    
    # If no exact match, try fuzzy matching
    payer_names = availity_df['Payer Name'].tolist()
    matched_name = process.extractOne(payer_name, payer_names, score_cutoff=90)
    
    if matched_name:
        return availity_df[availity_df['Payer Name'] == matched_name[0]].iloc[0]
    
    return None

def insert_payer_details(payer_name, payer_number, payer_group_name, conn, availity_df):
    payer_id = get_payer_id(payer_name, payer_group_name, conn)
    if payer_id is None:
        return None
    
    # Find best matching record in Availity sheet
    matched_record = find_best_match(payer_name, availity_df)
    
    tax_id = None
    short_name = None
    
    if matched_record is not None:
        tax_id = matched_record['Transaction Type (ID)']
        short_name = matched_record['Payer Short Name']
        print(f"Found match for '{payer_name}' -> '{matched_record['Payer Name']}'")
    else:
        print(f"No match found in Availity for '{payer_name}'")
    
    cursor.execute("""
        INSERT INTO payer_details (payer_id, payer_name, short_name, tax_id)
        VALUES (%s, %s, %s, %s) RETURNING payer_detail_id
    """, (payer_id, payer_name, short_name, tax_id))

    payer_detail_id = cursor.fetchone()[0]
    conn.commit()
    print(f"Payer Detail for '{payer_name}' inserted with payer_detail_id {payer_detail_id}.")
    return payer_detail_id

# Process each payer
for _, row in payer_group_df.iterrows():
    payer_name = row["Payer Name"]
    payer_number = row["Payer ID"]
    payer_group_name = row["Payer Group Name"]

    insert_payer_details(payer_name, payer_number, payer_group_name, conn, availity_df)

conn.commit()
cursor.close()
conn.close()
print("Database connection closed.")