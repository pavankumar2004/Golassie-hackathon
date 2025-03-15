import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the Excel file
xls = pd.ExcelFile("Payers.xlsx")


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

payer_data = []


for sheet, (payer_col, payer_id_col) in sheet_info.items():
    df = pd.read_excel(xls, sheet_name=sheet)
    
    if payer_col in df and payer_id_col in df:  
        df = df[[payer_col, payer_id_col]].dropna()
        df.columns = ["Payer Name", "Payer ID"]  
        payer_data.append(df)

all_payers_df = pd.concat(payer_data, ignore_index=True).drop_duplicates()

def extract_first_two_words(text):
    words = text.split()[:2]  
    return " ".join(words)

all_payers_df["Payer Group Key"] = all_payers_df["Payer Name"].apply(extract_first_two_words)


vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(all_payers_df["Payer Group Key"])


dbscan = DBSCAN(eps=0.3, min_samples=2, metric="cosine")  # Adjust eps as necessary
clusters = dbscan.fit_predict(X)


all_payers_df['Cluster'] = clusters
all_payers_df = all_payers_df[all_payers_df['Cluster'] != -1]


grouped_payers = all_payers_df.groupby('Cluster')['Payer Name'].apply(list).to_dict()

cluster_map = {}
for cluster, names in grouped_payers.items():
    shortest_full_name = min(names, key=len)  # Find the shortest full name in the cluster
    cluster_map[cluster] = shortest_full_name  


all_payers_df['Payer Group Name'] = all_payers_df['Cluster'].map(cluster_map)

all_payers_df = all_payers_df[["Payer ID", "Payer Group Name", "Payer Name"]] 
all_payers_df.to_excel("payer_with_payer_group.xlsx", index=False)

print("Payer groups and names saved to payer_with_payer_group.xlsx")
