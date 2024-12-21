import pandas as pd
import os
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from vocabulary_item_creation3 import get_latest_word_file, setup_output_directory

def analyze_correlations(strata_type, generation_type):
    """Analyze correlations between word metrics and assessment items."""
    # Get latest files
    word_file = get_latest_word_file(strata_type)
    
    # Extract seed and age from word file name
    filename = os.path.basename(word_file)
    seed_str = filename.split('seed')[1].split('_age')[0]
    age_range = filename.split('_age_')[1].split('_')[0]
    
    # Setup output directory for correlations
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    corr_dir = os.path.join(base_dir, 'output', 'correlations')
    os.makedirs(corr_dir, exist_ok=True)
    
    # Load files
    words_df = pd.read_csv(word_file)
    
    # Define metrics to analyze
    metrics = ['frequency_awl', 'complexity_awl', 'proximity_awl', 
              'diversity_awl', 'polysemy_awl']
    
    # Calculate correlations
    corr_matrix = words_df[metrics].corr()
    
    # Create heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, 
                annot=True,  # Show correlation values
                cmap='coolwarm',  # Color scheme
                vmin=-1, vmax=1,  # Correlation range
                center=0,  # Center the colormap at 0
                fmt='.2f')  # Format correlation values to 2 decimal places
    
    plt.title(f'Metric Correlations for {generation_type}\n(Strata {strata_type}, Age {age_range})')
    
    # Save correlation matrix and plot
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_filename = f'correlations_{generation_type}_strata{strata_type}_seed{seed_str}_age{age_range}_{timestamp}'
    
    csv_file = os.path.join(corr_dir, f'{base_filename}.csv')
    plot_file = os.path.join(corr_dir, f'{base_filename}.png')
    
    # Save both CSV and plot
    corr_matrix.to_csv(csv_file)
    plt.savefig(plot_file, bbox_inches='tight', dpi=300)
    plt.close()
    
    print(f"\nCorrelation Analysis (Age {age_range}, Seed {seed_str}):")
    print(f"Number of items analyzed: {len(words_df)}")
    print(f"Correlation matrix saved to: {csv_file}")
    print(f"Correlation plot saved to: {plot_file}")
    
    # Print correlation summary
    print("\nStrong correlations (|r| > 0.5):")
    for i in range(len(metrics)):
        for j in range(i+1, len(metrics)):
            corr = corr_matrix.iloc[i, j]
            if abs(corr) > 0.5:
                print(f"{metrics[i]} - {metrics[j]}: {corr:.2f}")
    
    return corr_matrix
