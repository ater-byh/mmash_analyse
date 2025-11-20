import pandas as pd
import os

base_path = "/Volumes/T7/mmash_analysis/mmash_analyse/DataPaper"
all_users_info = []

# 1. Iterate through users 1 to 22
for i in range(1, 23):
    file_path = os.path.join(base_path, f"user_{i}", "user_info.csv")
    
    if os.path.exists(file_path):
        # Read CSV, using the first column as index to drop it later
        df = pd.read_csv(file_path, index_col=0)
        
        # Add User ID
        df['User_ID'] = i
        
        # Reorder columns to put User_ID first (Optional, for better look)
        cols = ['User_ID'] + [col for col in df.columns if col != 'User_ID']
        df = df[cols]
        
        all_users_info.append(df)

# 2. Merge data
if all_users_info:
    full_info_df = pd.concat(all_users_info, ignore_index=True)
else:
    print("No user_info files found.")
    exit()

# 3. Simple Cleaning
# Check for missing values (though unlikely in this dataset)
full_info_df.dropna(how='any', inplace=True)

# Standardize column names (remove potential whitespace)
full_info_df.columns = full_info_df.columns.str.strip()

# 4. Save merged file
output_path = os.path.join(base_path, "MMASH_UserInfo_Merged.csv")
full_info_df.to_csv(output_path, index=False)

print(f"--- Done ---")
print(full_info_df) # Print to console to verify
print(f"Saved to: {output_path}")