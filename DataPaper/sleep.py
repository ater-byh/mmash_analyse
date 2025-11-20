import pandas as pd
import os

base_path = "/Volumes/T7/mmash_analysis/mmash_analyse/DataPaper"
all_sleep_data = []

# 1. Iterate through users 1 to 22
for i in range(1, 23):
    file_path = os.path.join(base_path, f"user_{i}", "sleep.csv")
    
    if os.path.exists(file_path):
        # Read CSV, remove raw index
        df = pd.read_csv(file_path, index_col=0)
        
        # Add User ID
        df['User_ID'] = i
        
        # 2. Rename Columns for easier coding & analysis
        # Using standard sleep metrics abbreviations
        df.rename(columns={
            'In Bed Date': 'In_Bed_Day',
            'In Bed Time': 'In_Bed_Time',
            'Out Bed Date': 'Out_Bed_Day',
            'Out Bed Time': 'Out_Bed_Time',
            'Onset Date': 'Onset_Day',
            'Onset Time': 'Onset_Time',
            'Total Minutes in Bed': 'TIB_min',       # Time In Bed
            'Total Sleep Time (TST)': 'TST_min',     # Total Sleep Time
            'Wake After Sleep Onset (WASO)': 'WASO_min',
            'Number of Awakenings': 'Num_Awakenings',
            'Average Awakening Length': 'Avg_Awake_Len_sec',
            'Movement Index': 'Mov_Index',
            'Fragmentation Index': 'Frag_Index',
            'Sleep Fragmentation Index': 'Sleep_Frag_Index'
        }, inplace=True)
        
        all_sleep_data.append(df)

# 3. Merge data
if all_sleep_data:
    full_sleep_df = pd.concat(all_sleep_data, ignore_index=True)
else:
    print("No sleep files found.")
    exit()

# 4. Data Cleaning
# Round floating point numbers to 2 decimal places for readability
cols_to_round = ['Efficiency', 'Avg_Awake_Len_sec', 'Mov_Index', 'Frag_Index', 'Sleep_Frag_Index']
full_sleep_df[cols_to_round] = full_sleep_df[cols_to_round].round(2)

# Reorder columns: Put User_ID first
cols = ['User_ID'] + [col for col in full_sleep_df.columns if col != 'User_ID']
full_sleep_df = full_sleep_df[cols]

# 5. Save
output_path = os.path.join(base_path, "MMASH_Sleep_Merged.csv")
full_sleep_df.to_csv(output_path, index=False)

print(f"--- Done ---")
print(f"Total sleep records: {len(full_sleep_df)}")
print(full_sleep_df.head())
print(f"Saved to: {output_path}")