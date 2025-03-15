import pandas as pd

# Load the Excel file
xls = pd.ExcelFile("Payers.xlsx")

# List all sheet names
sheet_names = xls.sheet_names
print(sheet_names)

vyne_df = pd.read_excel("Payers.xlsx", sheet_name="Vyne")
availty_df = pd.read_excel("Payers.xlsx", sheet_name="Availity")
optul_dental_df = pd.read_excel("Payers.xlsx", sheet_name="Optum dental")
change_claims_df = pd.read_excel("Payers.xlsx", sheet_name="change-claims")
change_era_df = pd.read_excel("Payers.xlsx", sheet_name="change-ERA")
change_eft_df = pd.read_excel("Payers.xlsx", sheet_name="change-EFT")
DxC_df = pd.read_excel("Payers.xlsx", sheet_name="DxC")
Optum_all_df = pd.read_excel("Payers.xlsx", sheet_name="Optum-all")


# Extract Payer Groups
vyne_payer_groups = vyne_df['Payer Identification Information'].unique()
availty_payer_groups = availty_df['Payer Name'].unique()
optul_dental_payer_groups = optul_dental_df['Payer Name'].unique()
change_claims_payer_groups = change_claims_df['Payer'].unique()
change_era_payer_groups = change_era_df['Payer'].unique()
change_eft_payer_groups = change_eft_df['Payer'].unique()
Optum_all_payer_groups = Optum_all_df['Payer Name'].unique()

# Combine all payer groups
all_payer_groups = set(vyne_payer_groups).union(set(availty_payer_groups), set(optul_dental_payer_groups), 
                                                 set(change_claims_payer_groups), set(change_era_payer_groups),
                                                 set(change_eft_payer_groups), set(Optum_all_payer_groups))
print(all_payer_groups)