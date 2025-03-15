import psycopg2
import pandas as pd
from fuzzywuzzy import process

# Database connection
DATABASE_URL = "postgresql://postgres:golassie@db.cbgtocxhyfflpmaxbugd.supabase.co:5432/postgres"
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Load the prepared DataFrame (payer_with_payer_group.xlsx)
all_payers_df = pd.read_excel("payer_with_payer_group.xlsx")

# Function to get payer_id from the payer table based on matching payer_name and payer_group
def get_payer_id(payer_name, payer_group_name, conn):
    # First, fetch the payer group ID based on the payer group name
    cursor.execute("SELECT payer_group_id FROM payer_groups WHERE payer_group_name = %s", (payer_group_name,))
    payer_group_id = cursor.fetchone()

    if not payer_group_id:
        print(f"Error: Payer Group '{payer_group_name}' not found.")
        return None

    payer_group_id = payer_group_id[0]

    # Fuzzy matching logic to find the closest match in the payer table
    cursor.execute("SELECT payer_id, payer_name FROM payers WHERE payer_group_id = %s", (payer_group_id,))
    payer_records = cursor.fetchall()

    # Fuzzy matching to get the best match for payer_name
    matched_payer = process.extractOne(payer_name, [record[1] for record in payer_records])

    if matched_payer and matched_payer[1] >= 80:  # Confidence threshold of 80 for fuzzy match
        # Find the payer_id for the best matched payer
        matched_payer_name = matched_payer[0]
        payer_id = payer_records[[record[1] for record in payer_records].index(matched_payer_name)][0]
        return payer_id
    else:
        print(f"Error: No sufficient match found for payer '{payer_name}' in payer group '{payer_group_name}'.")
        return None

def insert_payer_details(payer_name, payer_number, tax_id, payer_group_name, conn):
    # Get the payer_id by matching the payer_name and payer_group_name
    payer_id = get_payer_id(payer_name, payer_group_name, conn)
    if payer_id is None:
        return None  # Skip insertion if payer_id was not found
    cursor.execute("""
        INSERT INTO payer_details (payer_id, payer_name, payer_number, tax_id)
        VALUES (%s, %s, %s, %s) RETURNING payer_detail_id
    """, (payer_id, payer_name, payer_number, tax_id))

    payer_detail_id = cursor.fetchone()[0]  # Get the inserted payer_detail_id
    conn.commit()  # Commit the transaction
    print(f"✅ Payer Detail for '{payer_name}' inserted with payer_detail_id {payer_detail_id}.")
    return payer_detail_id

# Iterate over the DataFrame and insert payer details
for _, row in all_payers_df.iterrows():
    payer_name = row["Payer Name"]
    payer_number = row["Payer ID"]  
    tax_id = row.get("Tax ID", None)  # Assuming Tax ID might be optional in the file
    payer_group_name = row["Payer Group Name"]

    insert_payer_details(payer_name, payer_number, tax_id, payer_group_name, conn)

# Commit any changes
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
print("✅ Database connection closed.")
