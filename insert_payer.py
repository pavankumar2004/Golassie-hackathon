import psycopg2
import pandas as pd

# Database connection
DATABASE_URL = "postgresql://postgres:golassie@db.cbgtocxhyfflpmaxbugd.supabase.co:5432/postgres"
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Load the prepared DataFrame (payer_with_payer_group.xlsx)
all_payers_df = pd.read_excel("payer_with_payer_group.xlsx")

def insert_payer(payer_id, payer_group_name, payer_name, conn):
    # Fetch payer group ID for the given payer group name
    cursor.execute("SELECT payer_group_id FROM payer_groups WHERE payer_group_name = %s", (payer_group_name,))
    payer_group_id = cursor.fetchone()

    if payer_group_id:
        payer_group_id = payer_group_id[0]  # Extract payer group ID
    else:
        print(f"Error: Payer Group '{payer_group_name}' not found.")
        return

    # Check if a payer with the same name and payer group already exists
    cursor.execute("""
        SELECT payer_id, payer_name, payer_number 
        FROM payers 
        WHERE payer_group_id = %s AND payer_name = %s
    """, (payer_group_id, payer_name))
    
    existing_payers = cursor.fetchall()

    # If a payer with the same name exists but different payer number, do not insert
    for existing_payer in existing_payers:
        existing_payer_id, existing_payer_name, existing_payer_number = existing_payer
        if existing_payer_number != "NULL":  # Only skip if the payer number is different
            print(f"⚠️ Payer '{payer_name}' already exists with a different payer number. Skipping insertion.")
            return existing_payer_id

    # Insert the new payer only if it doesn't already exist
    cursor.execute("""
        INSERT INTO payers (payer_group_id, payer_name, payer_number) 
        VALUES (%s, %s, NULL) RETURNING payer_id
    """, (payer_group_id, payer_name))

    payer_id = cursor.fetchone()[0]  # Get the inserted payer_id
    conn.commit()
    print(f"✅ Payer '{payer_name}' inserted with payer_id {payer_id}.")
    return payer_id

# Iterate over the DataFrame and insert payers
for _, row in all_payers_df.iterrows():
    payer_id = row["Payer ID"]
    payer_group_name = row["Payer Group Name"]
    payer_name = row["Payer Name"]
    insert_payer(payer_id, payer_group_name, payer_name, conn)

# Commit any changes
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
print("✅ Database connection closed.")
