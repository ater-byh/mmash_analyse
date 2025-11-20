import pandas as pd
import os

base_path = "/Volumes/T7/mmash_analysis/mmash_analyse/DataPaper"
all_quest_data = []

# 1. Iterate and Read
for i in range(1, 23):
    file_path = os.path.join(base_path, f"user_{i}", "questionnaire.csv")
    
    if os.path.exists(file_path):
        # Read CSV, drop the raw index column
        df = pd.read_csv(file_path, index_col=0)
        
        # Add User ID
        df['User_ID'] = i
        
        # Reorder: Put User_ID at the front
        cols = ['User_ID'] + [col for col in df.columns if col != 'User_ID']
        df = df[cols]
        
        all_quest_data.append(df)

# 2. Merge
if all_quest_data:
    full_df = pd.concat(all_quest_data, ignore_index=True)
else:
    print("No questionnaire files found.")
    exit()

# 3. Rename columns for clarity
full_df.rename(columns={'Pittsburgh': 'PSQI'}, inplace=True)

# 4. Apply Categorization Logic (Based on your provided definitions)

# --- MEQ (Chronotype) ---
# <= 41: Evening, >= 59: Morning, 42-58: Intermediate
def classify_meq(score):
    if score <= 41: return 'Evening'
    elif score >= 59: return 'Morning'
    else: return 'Intermediate'

full_df['MEQ_Type'] = full_df['MEQ'].apply(classify_meq)

# --- STAI (Anxiety) ---
# < 31: Low, 31-49: Average, >= 50: High
def classify_stai(score):
    if score < 31: return 'Low'
    elif score <= 49: return 'Average'
    else: return 'High'

full_df['STAI1_Label'] = full_df['STAI1'].apply(classify_stai) # State Anxiety
full_df['STAI2_Label'] = full_df['STAI2'].apply(classify_stai) # Trait Anxiety

# --- PSQI (Sleep Quality) ---
# < 6: Good, >= 6: Poor
full_df['Sleep_Quality'] = full_df['PSQI'].apply(lambda x: 'Good' if x < 6 else 'Poor')

# 5. Save
output_path = os.path.join(base_path, "MMASH_Questionnaire_Merged.csv")
full_df.to_csv(output_path, index=False)

print(f"--- Done ---")
print(f"Total users processed: {len(full_df)}")
print("Preview of added labels:")
print(full_df[['User_ID', 'MEQ', 'MEQ_Type', 'STAI1', 'STAI1_Label', 'PSQI', 'Sleep_Quality']].head())
print(f"Saved to: {output_path}")