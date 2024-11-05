#========================================================
# Part 1: Data Import and Age of Acquisition Processing
#========================================================

#--------------------------------------------------------
# Step 1: Import Data
#--------------------------------------------------------

import pandas as pd
import numpy as np
import datetime
import os
import csv

# Add error handling and debugging for CSV reading
try:
    # Get the project root directory (one level up from src)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Construct the full path to the CSV file
    csv_path = os.path.join(project_root, "data", "predictions_imputed_aoa.csv")
    print(f"Looking for file at: {csv_path}")
    
    df = pd.read_csv(csv_path, sep=';', on_bad_lines='skip')
    print(f"Successfully loaded {len(df)} rows of data")
except Exception as e:
    # If that fails, try to read with a different delimiter or quoting
    try:
        df = pd.read_csv(csv_path, 
                        sep=';',
                        on_bad_lines='skip',
                        quoting=csv.QUOTE_NONE)
        print(f"Successfully loaded {len(df)} rows of data with modified quoting")
    except Exception as e:
        print(f"Error reading CSV: {str(e)}")
        print("Please ensure the file exists in the following location:")
        print(f"  {os.path.abspath(csv_path)}")
        raise

# Check if the column exists before trying to access it
if 'age_band' in df.columns:
    print(df['age_band'].value_counts())
else:
    print("Note: 'age_band' column not found in the dataset")
    print("\nAvailable columns:")
    print(df.columns.tolist())

#--------------------------------------------------------
# Step 2: Data Preparation and Merging
#--------------------------------------------------------

# Rename the existing '_merge' variable to avoid conflicts with the upcoming merge
if '_merge' in df.columns:
    df.rename(columns={'_merge': '_mergeold'}, inplace=True)

# Construct the full path to the Stata file
stata_path = os.path.join(project_root, "data", "emotion.dta")
print(f"Looking for Stata file at: {stata_path}")

# Merge the current dataset with 'emotion.dta' based on the variable 'word' using a one-to-one merge
df_emotion = pd.read_stata(stata_path)
df = df.merge(df_emotion, on='word', how='left')

#--------------------------------------------------------
# Step 3: Data Filtering Based on Emotion and Complexity
#--------------------------------------------------------

# Drop words where the emotion mean (EMO_vmeany) is less than 3.5
df = df[df['EMO_vmeany'] >= 3.5]

# Keep observations where the Age of Acquisition mean (aoamean) is not missing
df = df[df['aoamean'].notna()]

# For noun analysis: Keep observations where word complexity (complexity_awl) is not missing
df = df[df['complexity_awl'].notna()]

#--------------------------------------------------------
# Step 4: Creating and Labeling AoA Quantiles
#--------------------------------------------------------

# Create six quantiles for the Age of Acquisition mean (aoamean)
df['quantile_aoamean'] = pd.qcut(df['aoamean'], q=6, labels=False) + 1  # Labels from 1 to 6

# Define labels for each quantile to represent developmental stages
quantile_labels = {
    1: "Early childhood",
    2: "Later childhood",
    3: "Elementary",
    4: "Middle school",
    5: "High school",
    6: "University"
}

# Assign the labels to the quantile variable
df['quantile_aoamean_label'] = df['quantile_aoamean'].map(quantile_labels)

#--------------------------------------------------------
# Step 5: Selecting Specific AoA Quantiles
#--------------------------------------------------------

# Keep words up to the 'High school' quantile (quantiles less than 5)
df = df[df['quantile_aoamean'] < 5]

# Drop words in the 'Early childhood' and 'Later childhood' quantiles
df = df[~df['quantile_aoamean'].isin([1, 2])]

# At this point, the dataset contains words learned between elementary and middle school ages.

#========================================================
# Part 2: Stratified Sampling
#========================================================

# Define output directory (add this before Step 6)
OUTPUT_DIR = os.path.join(project_root, "output")

#--------------------------------------------------------
# Step 6: Creating Strata Variables with Groups of 5 and 3
#--------------------------------------------------------

#--- Word Length Strata ---#

# Calculate the length of each word
df['length2'] = df['word'].str.len()

# Create 5 strata based on word length (complexity)
df['complex_strata5'] = pd.cut(df['length2'], bins=5, labels=range(1, 6))

# Create 3 strata based on word length (complexity)
df['complex_strata3'] = pd.cut(df['length2'], bins=3, labels=range(1, 4))

#--- Frequency Strata ---#

# Create 5 strata based on word frequency
df['frequency_strata5'] = pd.cut(df['frequency_awl'], bins=5, labels=range(1, 6))

# Create 3 strata based on word frequency
df['frequency_strata3'] = pd.cut(df['frequency_awl'], bins=3, labels=range(1, 4))

#--- Polysemy Strata ---#

# Create 5 strata based on word polysemy
df['polysemy_strata5'] = pd.cut(df['polysemy_awl'], bins=5, labels=range(1, 6))

# Create 3 strata based on word polysemy
df['polysemy_strata3'] = pd.cut(df['polysemy_awl'], bins=3, labels=range(1, 4))

#--------------------------------------------------------
# Step 7: Creating Combined Strata Identifiers
#--------------------------------------------------------

#--- For Groups of 5 ---#

# Convert numeric strata variables to strings
df['complex_strata5_str'] = df['complex_strata5'].astype(str)
df['frequency_strata5_str'] = df['frequency_strata5'].astype(str)
df['polysemy_strata5_str'] = df['polysemy_strata5'].astype(str)

# Concatenate the string versions to create a combined strata identifier
df['strata5'] = df['complex_strata5_str'] + df['frequency_strata5_str'] + df['polysemy_strata5_str']

# Drop the intermediate string variables
df.drop(columns=['complex_strata5_str', 'frequency_strata5_str', 'polysemy_strata5_str'], inplace=True)

#--- For Groups of 3 ---#

# Convert numeric strata variables to strings
df['complex_strata3_str'] = df['complex_strata3'].astype(str)
df['frequency_strata3_str'] = df['frequency_strata3'].astype(str)
df['polysemy_strata3_str'] = df['polysemy_strata3'].astype(str)

# Concatenate the string versions to create a combined strata identifier
df['strata3'] = df['complex_strata3_str'] + df['frequency_strata3_str'] + df['polysemy_strata3_str']

# Drop the intermediate string variables
df.drop(columns=['complex_strata3_str', 'frequency_strata3_str', 'polysemy_strata3_str'], inplace=True)

#--------------------------------------------------------
# Step 8: Listing the Number of Words in Each Stratum
#--------------------------------------------------------

#--- For Groups of 5 ---#
print("Strata5 Value Counts:")
print(df['strata5'].value_counts())

#--- For Groups of 3 ---#
print("\nStrata3 Value Counts:")
print(df['strata3'].value_counts())

#--------------------------------------------------------
# Step 9: Selecting One Word from Each Stratum
#--------------------------------------------------------

#--- For Groups of 5 ---#

# Set seed for reproducibility
np.random.seed(123456)

# Create a random sorting variable
df['rand_order5'] = np.random.rand(len(df))

# Sort by strata and random order
df = df.sort_values(by=['strata5', 'rand_order5'])

# Tag the first occurrence of each unique stratum
df['target5'] = df.duplicated(subset='strata5', keep='first').apply(lambda x: 0 if x else 1)

#--- For Groups of 3 ---#

# Set a different seed for reproducibility
np.random.seed(123456)

# Create a random sorting variable
df['rand_order3'] = np.random.rand(len(df))

# Sort by strata and random order
df = df.sort_values(by=['strata3', 'rand_order3'])

# Tag the first occurrence of each unique stratum
df['target3'] = df.duplicated(subset='strata3', keep='first').apply(lambda x: 0 if x else 1)

#--------------------------------------------------------
# Step 10: Exporting the Selected Words with Date and Time (No Slashes)
#--------------------------------------------------------

def process_and_save_words(strata_type='5'):
    """Process and save stratified words."""
    global df  # Access the main dataframe
    
    # Create output directories if they don't exist
    output_dirs = {
        'strata5': os.path.join(OUTPUT_DIR, 'stratified_words', 'quintiles'),
        'strata3': os.path.join(OUTPUT_DIR, 'stratified_words', 'terciles')
    }

    for dir_path in output_dirs.values():
        os.makedirs(dir_path, exist_ok=True)

    # Export the selected words based on strata_type
    if strata_type == '5':
        # Create df_target5 with a clean copy
        df_target = df[df['target5'] == 1].copy()
        df_target = df_target.rename(columns={'word': 'Target_Word'})
        
        date_time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"stratified_words_quintiles_{date_time}.csv"
        filepath = os.path.join(output_dirs['strata5'], filename)
    else:
        # Create df_target3 with a clean copy
        df_target = df[df['target3'] == 1].copy()
        df_target = df_target.rename(columns={'word': 'Target_Word'})
        
        date_time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"stratified_words_terciles_{date_time}.csv"
        filepath = os.path.join(output_dirs['strata3'], filename)

    # Export the selected words and their features
    df_target[['Target_Word', 'frequency_awl', 'complexity_awl', 'proximity_awl', 
               'diversity_awl', 'polysemy_awl', 
               f'strata{strata_type}']].to_csv(filepath, index=False)
    
    print(f"Exported {'quintile' if strata_type=='5' else 'tercile'} stratified words to: {filepath}")
    return filepath

if __name__ == "__main__":
    # Process both quintiles and terciles
    process_and_save_words('5')
    process_and_save_words('3')