import openai
import pandas as pd
import os
import time
import glob
from datetime import datetime
from openai import OpenAI
from config import api_key

# Set your OpenAI API key
client = OpenAI(api_key=api_key)

def generate_assessment_item(word):
    """
    Generates a multiple-choice vocabulary item for the given word using OpenAI's GPT-4 model.
    """
    instructions = (
        "You are a multiple-choice vocabulary test designer. For every Target_Word I give you, please write one multiple-choice item for that word. "
        "First, list the Target_Word you are using. Many words will have multiple meanings. You will try to design the item for the most common meaning of the word. "
        "Then, create a Stem. A Stem is a sentence that uses the Target_Word in an example sentence where the Target_Word is capitalized in that sentence. "
        "Then, create the Correct_Response. This is a synonym for the Target_Word that could replace it in the Stem. "
        "Create three other responses (Response_B, Response_C, Response_D) that should not be synonyms but should be able to fit grammatically in the Stem. "
        "In total you will create: Target_Word, Stem, Correct_Response, Response_B, Response_C, Response_D."

        "Keep sentence structures as simple as possible to express the intended meaning. "
        "A number of simple sentences are often more accessible than a single more complex sentence."
        "Avoid use of negatives and constructions utilizing not in the questions’ stems and options as they can cause confusion"
        "When a fictional context is necessary (e.g., for a mathematics word problem), use a simple context that will be familiar"
        "to as wide a range of students as possible. A school-based context will often be more accessible to ELLs than a home-based context."
        "\n\nGOOD EXAMPLES:\n"
        "Target_Word: cockeyed\n"
        "Stem: The artist created a COCKEYED portrait that left the audience both puzzled and intrigued.\n"
        "Correct_Response: bizarre\n"
        "Response_B: beautiful\n"
        "Response_C: conventional\n"
        "Response_D: realistic\n"
        "\n"
        "Target_Word: heckle\n"
        "Stem: During the performance, some audience members began to HECKLE him, disrupting the show.\n"
        "Correct_Response: taunt\n"
        "Response_B: applaud\n"
        "Response_C: ignore\n"
        "Response_D: praise\n"
        "\n"
        "Target_Word: predictor\n"
        "Stem: The scientist emphasized that the gene could be a critical PREDICTOR of the disease.\n"
        "Correct_Response: sign\n"
        "Response_B: cause\n"
        "Response_C: treatment\n"
        "Response_D: factor\n"
        "\n"
        "Target_Word: fairlead\n"
        "Stem: To reduce the wear on the lines, we passed the ropes through the FAIRLEAD before securing them.\n"
        "Correct_Response: guide\n"
        "Response_B: knot\n"
        "Response_C: sail\n"
        "Response_D: harpoon\n"
        "\n"
        "Target_Word: quibble\n"
        "Stem: The lawyer's tendency to QUIBBLE over insignificant points annoyed the judge and the jury.\n"
        "Correct_Response: nitpick\n"
        "Response_B: accept\n"
        "Response_C: applaud\n"
        "Response_D: abandon\n"
        "\n"
        "Target_Word: contour\n"
        "Stem: The hiker's map showed every CONTOUR of the mountain terrain, making it easy to plan his route.\n"
        "Correct_Response: outline\n"
        "Response_B: peak\n"
        "Response_C: forest\n"
        "Response_D: rock\n"
        "BAD EXAMPLES with explanation:"
        "\n"
        "Target_Word: ozone\n"
        "Stem: The scientists measured the levels of OZONE in the atmosphere to study pollution effects.\n"
        "Correct_Response: layer\n"
        "Response_B: particle\n"
        "Response_C: sunlight\n"
        "Response_D: cloud\n"
        "Comment: Layer is not a synonym for ozone. The correct response should be a word that is a synonym for ozone.\n"
        "\n"
        "Target_Word: microfilm\n"
        "Stem: The librarian explained that the old newspapers were stored on MICROFILM to preserve them for future research.\n"
        "Correct_Response: film\n"
        "Response_B: paper\n"
        "Response_C: shelf\n"
        "Response_D: scan\n"
        "Comment: The correct answer and the target should not share morphemes.\n"
    )

    prompt = f"{instructions}\n\nTarget_Word: {word}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert at creating vocabulary assessment items."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            timeout=15
        )
        return response.choices[0].message.content.strip()
    except openai.APIError as e:
        print(f"Error generating assessment item for '{word}': {e}")
        return None
    except Exception as e:
        print(f"Unexpected error generating assessment item for '{word}': {e}")
        return None

def get_latest_word_file(strata_type, use_custom_words=False):
    """Get the most recently created word file."""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_dir = os.path.join(project_root, 'output', 'stratified_words')
    
    # For normal commands, look in the appropriate strata directory
    strata_dir = 'quintiles' if strata_type == '5' else 'terciles'
    strata_path = os.path.join(base_dir, strata_dir)
    
    # Look for stratified word files
    files = glob.glob(os.path.join(strata_path, 'stratified_words_*.csv'))
    if files:
        return max(files, key=os.path.getmtime)
    
    # If no stratified files found, try custom words directory
    if use_custom_words:
        custom_files = glob.glob(os.path.join(base_dir, 'custom_words_*.csv'))
        if custom_files:
            return max(custom_files, key=os.path.getmtime)
    
    raise FileNotFoundError(f"No word files found in {strata_path} or custom words directory")

def setup_output_directory():
    """Create and return the path for assessment items output."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, 'output', 'assessment_items')
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def process_and_format_items(new_items):
    """Process and format the generated items into a DataFrame."""
    formatted_items = []
    for item in new_items:
        lines = item['Generated Item'].split('\n')
        components = {
            'target_word': '',
            'stem': '',
            'correct_response': '',
            'response_b': '',
            'response_c': '',
            'response_d': ''
        }
        
        for line in lines:
            if line.strip() == "":
                continue
            line = line.strip()
            if line.startswith('Target_Word:'):
                components['target_word'] = line.split('Target_Word:')[1].strip()
            elif line.startswith('Stem:'):
                components['stem'] = line.split('Stem:')[1].strip()
            elif line.startswith('Correct_Response:'):
                components['correct_response'] = line.split('Correct_Response:')[1].strip()
            elif line.startswith('Response_B:'):
                components['response_b'] = line.split('Response_B:')[1].strip()
            elif line.startswith('Response_C:'):
                components['response_c'] = line.split('Response_C:')[1].strip()
            elif line.startswith('Response_D:'):
                components['response_d'] = line.split('Response_D:')[1].strip()
        
        if all(components.values()):
            formatted_items.append([
                components['target_word'],
                components['stem'],
                components['correct_response'],
                components['response_b'],
                components['response_c'],
                components['response_d']
            ])
        else:
            print(f"Incomplete item for word: {item['Target Word']}")
            # print("Generated content:")
            # print(item['Generated Item'])

    return pd.DataFrame(
        formatted_items,
        columns=['Target Word', 'Stem', 'Correct_Response', 'Response_B', 'Response_C', 'Response_D']
    )

def generate_assessments(strata_type, seed=None, use_custom_words=False):
    """Generate vocabulary assessments."""
    strata_name = 'quintiles' if strata_type == '5' else 'terciles'
    
    try:
        # Get the latest word file
        word_file = get_latest_word_file(strata_type, use_custom_words)
        print(f"Using {strata_name} word file: {word_file}")
        
        # Extract seed and check if custom words
        filename = os.path.basename(word_file)
        is_custom = 'custom_words' in filename
        seed_str = filename.split('seed')[1].split('_')[0]
        
        # Get age range only for non-custom files
        age_range = ''
        if not is_custom:
            age_range = filename.split('_age_')[1].split('_')[0]
        
        # Load the words with all metrics
        words_df = pd.read_csv(word_file)
        
        # Setup output directory
        output_dir = setup_output_directory()
        
        # Generate items and build complete records
        complete_items = []
        for index, row in words_df.iterrows():
            word = row['Target_Word']
            
            print(f"Generating item for word: {word}")
            item = generate_assessment_item(word)
                
            if item:
                item = item.replace('**', '')
                # Process the generated item
                lines = item.split('\n')
                components = {
                    'target_word': '',
                    'stem': '',
                    'correct_response': '',
                    'response_b': '',
                    'response_c': '',
                    'response_d': ''
                }
                
                for line in lines:
                    if line.strip() == "":
                        continue
                    line = line.strip()
                    if line.startswith('Target_Word:'):
                        components['target_word'] = line.split('Target_Word:')[1].strip()
                    elif line.startswith('Stem:'):
                        components['stem'] = line.split('Stem:')[1].strip()
                    elif line.startswith('Correct_Response:'):
                        components['correct_response'] = line.split('Correct_Response:')[1].strip()
                    elif line.startswith('Response_B:'):
                        components['response_b'] = line.split('Response_B:')[1].strip()
                    elif line.startswith('Response_C:'):
                        components['response_c'] = line.split('Response_C:')[1].strip()
                    elif line.startswith('Response_D:'):
                        components['response_d'] = line.split('Response_D:')[1].strip()
                
                if all(components.values()):
                    # Build complete record with all data from the original row
                    complete_record = {
                        'Target Word': word,
                        'Stem': components['stem'],
                        'Correct_Response': components['correct_response'],
                        'Response_B': components['response_b'],
                        'Response_C': components['response_c'],
                        'Response_D': components['response_d'],
                        'age_range': age_range
                    }
                    
                    # Add all metrics from the original row
                    for col in words_df.columns:
                        if col != 'Target_Word':  # Avoid duplicate column
                            complete_record[col] = row[col]
                    
                    complete_items.append(complete_record)
                else:
                    print(f"Incomplete item for word: {word}")
            
            time.sleep(1)

        # Create DataFrame from complete records
        merged_df = pd.DataFrame(complete_items)
        
        # Handle strata column
        strata_col = f'strata{strata_type}'
        if strata_col in merged_df.columns:
            merged_df[strata_col] = merged_df[strata_col].astype(str).str.zfill(3)

        # Save to CSV with seed before age in filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = os.path.join(output_dir, 
                               f'assessment_items_seed{seed_str}_age{age_range}_{timestamp}.csv')
        
        merged_df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Assessment items with metrics saved to: {output_file}")
        return output_file

    except Exception as e:
        print(f"Error generating {strata_name} assessments: {str(e)}")
        raise