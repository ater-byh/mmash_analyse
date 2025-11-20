import pandas as pd
import os

# Base directory path
base_path = "/Volumes/T7/mmash_analysis/mmash_analyse/DataPaper"
all_data = []

# 1. Iterate through users 1 to 22
for i in range(1, 23):
    file_path = os.path.join(base_path, f"user_{i}", "Activity.csv")
    
    if os.path.exists(file_path):
        # Read CSV (index_col=0 removes the raw index column from the file)
        df = pd.read_csv(file_path, index_col=0)
        
        # Add User ID
        df['User_ID'] = i
        all_data.append(df)

# 2. Merge data
if all_data:
    full_df = pd.concat(all_data, ignore_index=True)
else:
    print("No files found.")
    exit()

# 3. Data Cleaning
# Drop rows where 'End' time is missing (e.g., the last row in your snippet)
full_df.dropna(subset=['End'], inplace=True)

# Optional: Remove Activity 0 (Unknown/Not Worn) if strict cleaning is needed
# full_df = full_df[full_df['Activity'] != 0]

# 4. Save merged file
output_path = os.path.join(base_path, "MMASH_Activity_Merged.csv")
full_df.to_csv(output_path, index=False)

print(f"Processing complete. Total rows: {len(full_df)}")
print(f"Saved to: {output_path}")