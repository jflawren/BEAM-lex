import openai
import pandas as pd
import os

from config import api_key


# Load your API key from an environment variable or secret management service
openai.api_key = api_key=api_key


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

new_target_words = new_words_df['Word'].tolist()  # Assuming the column name is 'Word'

# Function to generate new assessment items
def generate_assessment_item(word):
    prompt = f"Generate a vocabulary assessment item for the word '{word}'. Provide the following:\n\n" \
             f"1. A sentence using the word in context.\n" \
             f"2. Four response options (one correct and three incorrect) for the word's meaning.\n" \
             f"Format:\n" \
             f"Target Word: {word}\n" \
             f"Stem: \n" \
             f"Response_A: \n" \
             f"Response_B: \n" \
             f"Response_C: \n" \
             f"Response_D: \n"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # Use the GPT-4o model
            messages=[
                {"role": "system", "content": "You are an expert at creating vocabulary assessment items."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )
        return response.choices[0].message['content'].strip()
    except openai.error.OpenAIError as e:
        print(f"Error generating assessment item for '{word}': {e}")
        return None

# Generate new items
new_items = []
for word in new_target_words:
    item = generate_assessment_item(word)
    if item:
        new_items.append({
            "Target Word": word,
            "Generated Item": item
        })

# Convert new items to DataFrame
new_items_df = pd.DataFrame(new_items)

# Example of annotating existing items (This part is based on your need)
# Adding a 'Status' column to indicate if the item is 'Good' or 'Problematic'
existing_items['Status'] = 'Good'  # or 'Problematic' based on your manual review or criteria
existing_items['Issue'] = ''  # Add specific issues if any

# Define relative paths for the output CSV files
annotated_items_path = os.path.join(script_dir, 'annotated_training_items.csv')
new_items_path = os.path.join(script_dir, 'new_assessment_items.csv')

try:
    existing_items.to_csv(annotated_items_path, index=False)
    new_items_df.to_csv(new_items_path, index=False)
    print(f"Annotated existing items saved to: {annotated_items_path}")
    print(f"New assessment items saved to: {new_items_path}")
except Exception as e:
    print(f"Error saving files: {e}")
