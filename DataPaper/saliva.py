import pandas as pd
import os

base_path = "/Volumes/T7/mmash_analysis/mmash_analyse/DataPaper"
all_saliva_data = []

# 1. Iterate through users 1 to 22
for i in range(1, 23):
    file_path = os.path.join(base_path, f"user_{i}", "saliva.csv")
    
    # Check if file exists (User_21 will be skipped here automatically)
    if os.path.exists(file_path):
        # Read CSV, removing the raw index column
        df = pd.read_csv(file_path, index_col=0)
        
        # Add User ID
        df['User_ID'] = i
        
        # 2. Rename Columns for consistency
        # "SAMPLES" -> "Sample_Time"
        # "Cortisol NORM" -> "Cortisol_Norm"
        # "Melatonin NORM" -> "Melatonin_Norm"
        df.rename(columns={
            'SAMPLES': 'Sample_Time',
            'Cortisol NORM': 'Cortisol_Norm',
            'Melatonin NORM': 'Melatonin_Norm'
        }, inplace=True)
        
        # 3. Standardize Sample Labels (Optional)
        # Ensure consistency (e.g., lowercase)
        df['Sample_Time'] = df['Sample_Time'].str.lower().str.strip()
        
        # Reorder columns: Put User_ID first
        cols = ['User_ID'] + [col for col in df.columns if col != 'User_ID']
        df = df[cols]
        
        all_saliva_data.append(df)
    else:
        print(f"Notice: No saliva data for User_{i} (Expected for User_21).")

# 4. Merge data
if all_saliva_data:
    full_saliva_df = pd.concat(all_saliva_data, ignore_index=True)
else:
    print("No saliva files found.")
    exit()

# 5. Save
output_path = os.path.join(base_path, "MMASH_Saliva_Merged.csv")
full_saliva_df.to_csv(output_path, index=False)

print(f"--- Done ---")
print(f"Total records: {len(full_saliva_df)}")
# Show a sample to confirm scientific notation is handled correctly
print(full_saliva_df.head())
print(f"Saved to: {output_path}")