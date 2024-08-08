import openai
import pandas as pd
import os
import time

from config import api_key

# Load your API key from an environment variable or secret management service
openai.api_key = api_key = api_key

# Define relative paths for the CSV files
script_dir = os.path.dirname(os.path.abspath(__file__))
existing_items_path = os.path.join(script_dir, 'training_items.csv')
new_words_path = os.path.join(script_dir, 'new_words.csv')

try:
    existing_items = pd.read_csv(existing_items_path)
    new_words_df = pd.read_csv(new_words_path)
except FileNotFoundError as e:
    print(f"Error: {e}")
    exit()

new_target_words = new_words_df['Target_Word'].tolist()  # Assuming the column name is 'Word'


# Function to generate new assessment items
def generate_assessment_item(word):
    instructions = (
        "You are a multiple-choice vocabulary test designer. For every Target_Word in the new_words.csv file I give you, please write three different multiple-choice items for that word. "
        "First, list the Target_Word you are using. Then, create a Stem. A Stem is a sentence that uses the target word in an example sentence where the Target_Word is capitalized in that sentence. "
        "Then, create the Correct_Response. This is a synonym for the target word that could replace it in the Stem. "
        "Create three other responses (Response_B, Response_C, Response_D) that should not be synonyms but should be able to fit grammatically in the Stem. "
        "In total you will create: Target_Word, Stem, Correct_Response, Response_B, Response_C, Response_D."
    )

    prompt = f"{instructions}\n\nTarget_Word: {word}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # Use the GPT-4o model
            messages=[
                {"role": "system", "content": "You are an expert at creating vocabulary assessment items."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            timeout=15  # Set a timeout for the API call
        )
        return response.choices[0].message['content'].strip()
    except openai.error.OpenAIError as e:
        print(f"Error generating assessment item for '{word}': {e}")
        return None
    except Exception as e:
        print(f"Unexpected error generating assessment item for '{word}': {e}")
        return None


# Generate new items
new_items = []
for word in new_target_words:
    print(f"Generating item for word: {word}")
    item = generate_assessment_item(word)
    if item:
        item = item.replace('**', '')  # replace '**' with nothing
        new_items.append({
            "Target Word": word,
            "Generated Item": item
        })
    time.sleep(1)  # Add delay to prevent hitting rate limits

# Convert new items to DataFrame and split the response into columns
formatted_items = []
for item in new_items:
    lines = item['Generated Item'].split('\n')
    for line in lines:
        if line.strip() == "":
            continue
        if 'Target_Word:' in line:
            target_word = line.split('Target_Word:')[1].strip()
        elif 'Stem:' in line:
            stem = line.split('Stem:')[1].strip()
        elif 'Correct_Response:' in line:
            correct_response = line.split('Correct_Response:')[1].strip()
        elif 'Response_B:' in line:
            response_b = line.split('Response_B:')[1].strip()
        elif 'Response_C:' in line:
            response_c = line.split('Response_C:')[1].strip()
        elif 'Response_D:' in line:
            response_d = line.split('Response_D:')[1].strip()
            formatted_items.append([target_word, stem, correct_response, response_b, response_c, response_d])

formatted_items_df = pd.DataFrame(formatted_items,
                                  columns=['Target Word', 'Stem', 'Correct_Response', 'Response_B', 'Response_C',
                                           'Response_D'])

# Example of annotating existing items (This part is based on your need)
# Adding a 'Status' column to indicate if the item is 'Good' or 'Problematic'
existing_items['Status'] = 'Good'  # or 'Problematic' based on your manual review or criteria
existing_items['Issue'] = ''  # Add specific issues if any

# Define relative paths for the output CSV files
annotated_items_path = os.path.join(script_dir, 'annotated_training_items.csv')
new_items_path = os.path.join(script_dir, 'new_assessment_items.csv')

try:
    existing_items.to_csv(annotated_items_path, index=False, encoding='utf-8')
    formatted_items_df.to_csv(new_items_path, index=False, sep=',', encoding='utf-8')
    print(f"Annotated existing items saved to: {annotated_items_path}")
    print(f"New assessment items saved to: {new_items_path}")
except Exception as e:
    print(f"Error saving files: {e}")
