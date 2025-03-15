import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the Excel file
xls = pd.ExcelFile("Payers.xlsx")

# Load payer names and IDs from different sheets
sheet_info = {
    "Vyne": ("Payer Identification Information", "Payer ID"),
    "Availity": ("Payer Name", "Payer ID"),
    "Optum dental": ("Payer Name", "Payer ID"),
    "change-claims": ("Payer", "ID\t"),
    "change-ERA": ("Payer", "ID\t"),
    "change-EFT": ("Payer", "ID\t"),
    "DxC": ("Name", "ID"),
    "Optum-all": ("Payer Name", "Payer ID")
}

# Store payer data (ID and Name)
payer_data = []

for sheet, (payer_col, payer_id_col) in sheet_info.items():
    df = pd.read_excel(xls, sheet_name=sheet)
    
    if payer_col in df and payer_id_col in df:  # Ensure both columns exist
        df = df[[payer_col, payer_id_col]].dropna()
        df.columns = ["Payer Name", "Payer ID"]  # Standardize column names
        payer_data.append(df)

# Combine all sheets into one DataFrame
all_payers_df = pd.concat(payer_data, ignore_index=True).drop_duplicates()

# Step 1: Extract first two words for clustering
def extract_first_two_words(text):
    words = text.split()[:2]  # Get first two words
    return " ".join(words)

all_payers_df["Payer Group Key"] = all_payers_df["Payer Name"].apply(extract_first_two_words)

# Step 2: Convert payer group names into numerical vectors using TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(all_payers_df["Payer Group Key"])

# Step 3: Apply DBSCAN clustering
dbscan = DBSCAN(eps=0.3, min_samples=2, metric="cosine")  # Adjust eps if needed
clusters = dbscan.fit_predict(X)

# Step 4: Find the shortest full payer name in each cluster to use as "Payer Group Name"
cluster_map = {}  # Cluster -> Shortest Full Payer Name
grouped_payers = {}

for payer_name, cluster in zip(all_payers_df["Payer Name"], clusters):
    if cluster == -1:
        continue  # Skip unclustered payers
    
    if cluster not in grouped_payers:
        grouped_payers[cluster] = []
    
    grouped_payers[cluster].append(payer_name)

# Find the shortest full payer name in each cluster
for cluster, names in grouped_payers.items():
    shortest_full_name = min(names, key=len)  # Find shortest full name in the cluster
    cluster_map[cluster] = shortest_full_name  # Assign shortest name as the payer group name

# Assign the "Payer Group Name" based on cluster
all_payers_df["Payer Group Name"] = all_payers_df["Payer Name"].apply(
    lambda x: cluster_map.get(clusters[list(all_payers_df["Payer Name"]).index(x)], x)
)

# Step 5: Save the results to an Excel file
all_payers_df = all_payers_df[["Payer ID", "Payer Group Name", "Payer Name"]]  # Keep only required columns
all_payers_df.to_excel("payer_with_payer_group.xlsx", index=False)

print("Payer groups and names saved to payer_clusters_with_correct_group_name.xlsx")
