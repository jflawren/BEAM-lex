#========================================================
# Part 1: Data Import and Age of Acquisition Processing
#========================================================

import pandas as pd
import numpy as np
import datetime
import os
import csv
from better_profanity import profanity

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define output directory
OUTPUT_DIR = os.path.join(project_root, "output")

try:
    # Construct the full path to the CSV file
    csv_path = os.path.join(project_root, "data", "predictions_imputed_quantileaoa.csv")
    print(f"Looking for file at: {csv_path}")
    
    # First attempt with comma separator
    df = pd.read_csv(csv_path, 
                    encoding='utf-8',
                    engine='python',
                    sep=',',
                    on_bad_lines='warn')
    print(f"Successfully loaded {len(df)} rows of data")
    
    # Print first few column names for debugging
    # print("\nFirst few column names:")
    # print(df.columns.tolist())
    
except Exception as e:
    print(f"Error reading CSV: {str(e)}")
    raise

#--------------------------------------------------------
# Step 2: Data Preparation
#--------------------------------------------------------

# Global variable to track if distribution has been shown
distribution_shown = False

def filter_by_age_range(df, min_level, max_level):
    """Filter dataframe by age/education level range."""
    global distribution_shown
    
    if not (1 <= min_level <= 6 and 1 <= max_level <= 6):
        raise ValueError("Education levels must be between 1 and 6")
    if min_level > max_level:
        raise ValueError("Minimum level cannot be greater than maximum level")
    
    df_filtered = df.copy()
    
    # Create quantiles if they don't exist
    if 'quantile_aoamean' not in df_filtered.columns:
        df_filtered['quantile_aoamean'] = pd.qcut(df_filtered['aoamean'], 
                                                q=6, labels=False) + 1
    
    # Print education level distributions only once
    if not distribution_shown:
        education_levels = {
            1: "Early childhood",
            2: "Later childhood",
            3: "Elementary",
            4: "Middle school",
            5: "High school",
            6: "University"
        }
        
        print("\nEducation Level Distribution:")
        print("-----------------------------")
        level_counts = df_filtered['quantile_aoamean'].value_counts().sort_index()
        for level, count in level_counts.items():
            print(f"Level {level} ({education_levels[level]}): {count:,} words")
        
        distribution_shown = True  # Set flag to True after printing
    
    # Filter by age range
    df_filtered = df_filtered[
        (df_filtered['quantile_aoamean'] >= min_level) & 
        (df_filtered['quantile_aoamean'] <= max_level)
    ]
    
    print(f"\nRetained {len(df_filtered):,} words for levels {min_level}-{max_level}")
    
    return df_filtered

#--------------------------------------------------------
# Step 3: Create Strata
#--------------------------------------------------------

def create_strata_combinations(df, strata_type='3'):
    """Create strata combinations based on complexity, frequency, and polysemy."""
    n_levels = 5 if strata_type == '5' else 3
    
    # Create individual strata
    df[f'complex_strata{strata_type}'] = pd.qcut(df['complexity_awl'], 
                                                q=n_levels, 
                                                labels=range(n_levels))
    
    df[f'frequency_strata{strata_type}'] = pd.qcut(df['frequency_awl'], 
                                                  q=n_levels, 
                                                  labels=range(n_levels))
    
    df[f'polysemy_strata{strata_type}'] = pd.qcut(df['polysemy_awl'], 
                                                 q=n_levels, 
                                                 labels=range(n_levels))
    
    # Create combined strata identifier
    df[f'strata{strata_type}'] = (df[f'complex_strata{strata_type}'].astype(str) + 
                                 df[f'frequency_strata{strata_type}'].astype(str) + 
                                 df[f'polysemy_strata{strata_type}'].astype(str))
    
    print(f"\nNumber of unique strata combinations: {df[f'strata{strata_type}'].nunique()}")
    print(f"Expected combinations: {n_levels**3}")
    
    return df

#--------------------------------------------------------
# Step 4: Sample Words
#--------------------------------------------------------

def sample_from_strata(df, strata_type='3', seed=None):
    """Sample one word from each stratum."""
    if seed is not None:
        np.random.seed(seed)  # Set the random seed if provided
    
    sampled_words = []
    strata_col = f'strata{strata_type}'
    
    # Get all possible combinations
    n_levels = 5 if strata_type == '5' else 3
    all_combinations = [f"{i}{j}{k}" 
                       for i in range(n_levels) 
                       for j in range(n_levels) 
                       for k in range(n_levels)]
    
    # Initialize profanity filter
    profanity.load_censor_words()
    
    # Sample from each stratum
    for stratum in all_combinations:
        stratum_words = df[df[strata_col] == stratum]
        # Filter out profane words
        clean_words = stratum_words[~stratum_words['word'].apply(profanity.contains_profanity)]
        if len(clean_words) > 0:
            sampled = clean_words.sample(n=1)
            sampled_words.append(sampled)
        elif len(stratum_words) > 0:
            print(f"Warning: Stratum {stratum} only contains potentially inappropriate words")
    
    if sampled_words:
        result = pd.concat(sampled_words)
        print(f"\nTotal words sampled: {len(result)}")
        print(f"Unique strata represented: {result[strata_col].nunique()}")
        return result
    return pd.DataFrame()

#--------------------------------------------------------
# Step 5: Process and Save
#--------------------------------------------------------

def process_and_save_words(strata_type='5', min_age_level=3, max_age_level=4, seed=None):
    """Process and save stratified words."""
    # Filter by age range
    df_aged = filter_by_age_range(df.copy(), min_age_level, max_age_level)
    
    # Create strata
    df_aged = create_strata_combinations(df_aged, strata_type)
    
    # Sample words
    df_target = sample_from_strata(df_aged, strata_type, seed=seed)
    
    if len(df_target) == 0:
        print("No words sampled!")
        return None
    
    # Create output directories
    output_dir = os.path.join(OUTPUT_DIR, 'stratified_words', 
                             'quintiles' if strata_type == '5' else 'terciles')
    os.makedirs(output_dir, exist_ok=True)
    
    # Save results with age range in filename
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'stratified_words_seed{seed}_age_{min_age_level}-{max_age_level}_{timestamp}.csv'
    filepath = os.path.join(output_dir, filename)
    
    df_target['Target_Word'] = df_target['word']
    columns_to_export = ['Target_Word', 'frequency_awl', 'complexity_awl', 
                        'proximity_awl', 'diversity_awl', 'polysemy_awl', 
                        f'strata{strata_type}']
    
    df_target[columns_to_export].to_csv(filepath, index=False)
    print(f"\nExported words to: {filepath}")
    
    return filepath

if __name__ == "__main__":
    # Process both quintiles and terciles
    process_and_save_words('5')
    process_and_save_words('3')