import argparse
import os
import sys
from datetime import datetime

def run_pipeline(generation_type='basic', skip_sampling=False, min_age_level=3, max_age_level=4, strata_type='both'):
    """
    Run the complete pipeline: sampling words and generating assessments
    
    Parameters:
    - generation_type: Type of assessment generator ('basic', 'freq_complex', or 'poly')
    - skip_sampling: Whether to skip the word sampling step
    - min_age_level: Minimum education level (1-6)
    - max_age_level: Maximum education level (1-6)
    - strata_type: Type of stratification ('3', '5', or 'both')
    
    Education levels:
    1: Early childhood
    2: Later childhood
    3: Elementary
    4: Middle school
    5: High school
    6: University
    """
    print(f"Starting vocabulary assessment pipeline using {generation_type} generator...")
    print(f"Age range: {min_age_level} to {max_age_level}")
    print(f"Strata type: {strata_type}")
    
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(project_root, 'src'))
    
    import sampling
    from freq_complex_voc import generate_assessments as freq_complex_generate
    from poly_voc import generate_assessments as poly_generate
    from vocabulary_item_creation3 import generate_assessments as basic_generate
    
    generators = {
        'basic': basic_generate,
        'freq_complex': freq_complex_generate,
        'poly': poly_generate
    }
    
    try:
        # Generate a single seed for the entire run
        seed = int(datetime.now().timestamp())
        print(f"Using seed: {seed} for this run")
        
        # Step 1: Run sampling to get stratified words
        if not skip_sampling:
            print("\n1. Generating stratified word samples...")
            
            if strata_type in ['5', 'both']:
                # Generate quintiles (5)
                print("\nProcessing quintiles (5)...")
                quintiles_result = sampling.process_and_save_words(
                    '5', 
                    min_age_level=min_age_level, 
                    max_age_level=max_age_level,
                    seed=seed
                )
                if quintiles_result[0]:  # Check first element of tuple
                    print("✓ Quintiles word sampling completed")
                else:
                    print("→ Skipping quintiles word sampling (using existing words)")
            
            if strata_type in ['3', 'both']:
                # Generate terciles (3)
                print("\nProcessing terciles (3)...")
                terciles_result = sampling.process_and_save_words(
                    '3', 
                    min_age_level=min_age_level, 
                    max_age_level=max_age_level,
                    seed=seed
                )
                if terciles_result[0]:  # Check first element of tuple
                    print("✓ Terciles word sampling completed")
                else:
                    print("→ Skipping terciles word sampling (using existing words)")
        else:
            print("\n→ Skipping word sampling step...")
        
        # Step 2: Generate assessments using specified generator
        print(f"\n2. Generating {generation_type} vocabulary assessments...")
        
        generator = generators[generation_type]
        
        if strata_type in ['5', 'both']:
            print("\nGenerating assessments for quintiles...")
            generator('5')
            print("✓ Quintiles assessment generation completed")
        
        if strata_type in ['3', 'both']:
            print("\nGenerating assessments for terciles...")
            generator('3')
            print("✓ Terciles assessment generation completed")
        
        print("\n✓ Pipeline completed successfully!")
        print("\nOutput files can be found in:")
        print(f"- Word lists: {os.path.join(project_root, 'output', 'stratified_words')}")
        print(f"- Assessments: {os.path.join(project_root, 'output', 'assessment_items')}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Generate vocabulary assessments')
    parser.add_argument('--type', 
                       choices=['basic', 'freq_complex', 'poly'],
                       default='basic',
                       help='Type of assessment to generate')
    parser.add_argument('--skip-sampling',
                       action='store_true',
                       help='Skip the word sampling step and use existing word lists')
    parser.add_argument('--min-age',
                       type=int,
                       choices=range(1, 7),
                       default=3,
                       help='Minimum education level (1: Early childhood, 2: Later childhood, '
                            '3: Elementary, 4: Middle school, 5: High school, 6: University)')
    parser.add_argument('--max-age',
                       type=int,
                       choices=range(1, 7),
                       default=4,
                       help='Maximum education level (1: Early childhood, 2: Later childhood, '
                            '3: Elementary, 4: Middle school, 5: High school, 6: University)')
    parser.add_argument('--strata',
                       choices=['3', '5', 'both'],
                       default='both',
                       help='Strata type (3: terciles, 5: quintiles, both: run both)')
    
    args = parser.parse_args()
    
    # Validate age range
    if args.min_age > args.max_age:
        parser.error("Minimum age level cannot be greater than maximum age level")
    
    run_pipeline(
        args.type, 
        args.skip_sampling,
        min_age_level=args.min_age,
        max_age_level=args.max_age,
        strata_type=args.strata
    )

if __name__ == "__main__":
    main()