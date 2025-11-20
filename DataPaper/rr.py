import pandas as pd
import os

base_path = "/Volumes/T7/mmash_analysis/mmash_analyse/DataPaper"
all_rr_data = []

# 1. Iterate through users 1 to 22
for i in range(1, 23):
    file_path = os.path.join(base_path, f"user_{i}", "RR.csv")
    
    if os.path.exists(file_path):
        # Read CSV (Handle index_col=0 to remove the raw index)
        df = pd.read_csv(file_path, index_col=0)
        
        # Add User ID
        df['User_ID'] = i
        
        # 2. Physiological Cleaning (Artifact Removal)
        # Keep only realistic intervals: 0.3s (200 BPM) to 1.5s (40 BPM)
        # This removes noise and sensor errors.
        df = df[(df['ibi_s'] > 0.3) & (df['ibi_s'] < 1.5)]
        
        # 3. Add BPM column (Optional but recommended)
        # Calculates instantaneous Heart Rate
        df['HR_BPM'] = 60 / df['ibi_s']
        
        # Note: We are keeping 'day' (1, 2) and 'time' (HH:MM:SS) as is.
        
        all_rr_data.append(df)
        print(f"User {i} processed.")

# 4. Merge all users
if all_rr_data:
    full_rr_df = pd.concat(all_rr_data, ignore_index=True)
else:
    print("No RR files found.")
    exit()

# 5. Save to CSV
output_path = os.path.join(base_path, "MMASH_RR_Merged_Cleaned.csv")
full_rr_df.to_csv(output_path, index=False)

print(f"--- Done ---")
print(f"Total rows: {len(full_rr_df)}")
print(f"Saved to: {output_path}")