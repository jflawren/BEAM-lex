import os
import sys
import time
from datetime import datetime

def run_pipeline():
    """Run the complete pipeline: sampling words and generating assessments"""
    print("Starting vocabulary assessment pipeline...")
    
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(project_root, 'src'))
    
    import sampling
    from freq_complex_voc import generate_assessments
    
    try:
        # Step 1: Run sampling to get stratified words for both types
        print("\n1. Generating stratified word samples...")
        
        # Generate quintiles (5)
        print("\nProcessing quintiles (5)...")
        sampling.process_and_save_words('5')
        print("✓ Quintiles word sampling completed")
        
        # Generate terciles (3)
        print("\nProcessing terciles (3)...")
        sampling.process_and_save_words('3')
        print("✓ Terciles word sampling completed")
        
        # Step 2: Generate assessments for both types
        print("\n2. Generating vocabulary assessments...")
        
        print("\nGenerating assessments for quintiles...")
        generate_assessments('5')
        print("✓ Quintiles assessment generation completed")
        
        print("\nGenerating assessments for terciles...")
        generate_assessments('3')
        print("✓ Terciles assessment generation completed")
        
        print("\n✓ Pipeline completed successfully!")
        print("\nOutput files can be found in:")
        print(f"- Word lists: {os.path.join(project_root, 'output', 'stratified_words')}")
        print(f"- Assessments: {os.path.join(project_root, 'output', 'assessment_items')}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline()