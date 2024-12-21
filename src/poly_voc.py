# Import necessary libraries
import openai
import pandas as pd
import os
import time
import glob
from datetime import datetime

from config import api_key

# Set your OpenAI API key
openai.api_key = api_key

def generate_assessment_item(word):
    """
    Generates a multiple-choice vocabulary item for the given word using OpenAI's GPT-4 model.
    """
    instructions = (
        "You are a multiple-choice vocabulary test designer. For every Target_Word I give you, please write one multiple-choice item for that word. "
        "First, list the Target_Word you are using. Many words will have multiple meanings. If a word has multiple meanings, design the test to see if the student knows the secondary meaning. "
        "Then, create a Stem. A Stem is a sentence that uses the Target_Word in an example sentence where the Target_Word is capitalized in that sentence. "
        "Then, create the Correct_Response. This is a synonym for the Target_Word that could replace it in the Stem. "
        "Next, create an incorrect response that is related to the most common meaning of the target word (Response_B)."
        "Finally, create three other responses (Response_C, Response_D) that should not be synonyms but should be able to fit grammatically in the Stem. "
        "In total you will create: Target_Word, Stem, Correct_Response, Response_B, Response_C, Response_D."
        "\n\nHere are some examples of good items:\n"
        "Target_Word: chair\n"
        "Stem: He was the CHAIR of the meeting.\n"
        "Correct_Response: leader\n"
        "Response_B: stool\n"
        "Response_C: listener\n"
        "Response_D: table\n"
    )

    prompt = f"{instructions}\n\nTarget_Word: {word}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert at creating vocabulary assessment items."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            timeout=15
        )
        return response.choices[0].message['content'].strip()
    except openai.error.OpenAIError as e:
        print(f"Error generating assessment item for '{word}': {e}")
        return None
    except Exception as e:
        print(f"Unexpected error generating assessment item for '{word}': {e}")
        return None

def get_latest_word_file(strata_type):
    """Get the most recent word file for the specified strata type."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    word_dir = os.path.join(base_dir, 'output', 'stratified_words', 
                           'quintiles' if strata_type == '5' else 'terciles')
    
    files = glob.glob(os.path.join(word_dir, f"stratified_words_*.csv"))
    if not files:
        raise FileNotFoundError(f"No word files found in {word_dir}")
    
    return max(files, key=os.path.getmtime)

def setup_output_directory():
    """Create and return the path for assessment items output."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir,'output', 'assessment_items')
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

def generate_assessments(strata_type, seed=None):
    """Generate assessment items for the specified strata type."""
    try:
        # Get the latest word file
        word_file = get_latest_word_file(strata_type)
        strata_name = 'quintiles' if strata_type == '5' else 'terciles'
        print(f"Using {strata_name} word file: {word_file}")
        
        # Extract seed and age range from the word file name
        filename = os.path.basename(word_file)
        seed_str = filename.split('seed')[1].split('_age')[0]
        age_range = filename.split('_age_')[1].split('_')[0]
        
        # Load the words with all metrics
        words_df = pd.read_csv(word_file)
        if 'Target_Word' in words_df.columns:
            new_target_words = words_df['Target_Word'].dropna().tolist()
        elif 'Word' in words_df.columns:
            new_target_words = words_df['Word'].dropna().tolist()
            # Rename 'Word' to 'Target_Word' for consistency
            words_df = words_df.rename(columns={'Word': 'Target_Word'})
        else:
            raise ValueError(f"Error: 'Target_Word' or 'Word' column not found in the {strata_name} file")

        # Setup output directory
        output_dir = setup_output_directory()
        
        # Generate items
        new_items = []
        for word in new_target_words:
            print(f"Generating item for word: {word}")
            item = generate_assessment_item(word)
            if item:
                item = item.replace('**', '')
                new_items.append({
                    "Target Word": word,
                    "Generated Item": item
                })
            time.sleep(1)

        # Process items and merge with metrics
        formatted_items_df = process_and_format_items(new_items)
        
        # Add age range
        formatted_items_df['age_range'] = age_range
        
        # Merge with the original words_df to include all metrics
        merged_df = pd.merge(
            formatted_items_df,
            words_df,
            how='left',
            left_on='Target Word',
            right_on='Target_Word'
        )
        # Drop duplicate Target_Word column if it exists
        if 'Target_Word' in merged_df.columns:
            merged_df = merged_df.drop(columns='Target_Word')

        strata_col = f'strata{strata_type}'
        if strata_col in merged_df.columns:
            merged_df[strata_col] = merged_df[strata_col].astype(str).str.zfill(3)

        # Save to CSV with seed before age in filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = os.path.join(output_dir, 
                               f'poly_assessment_items_seed{seed_str}_age{age_range}_{timestamp}.csv')
        
        merged_df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Assessment items with metrics saved to: {output_file}")
        return output_file

    except Exception as e:
        print(f"Error generating {strata_name} assessments: {str(e)}")
        raise
