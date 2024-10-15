# Import necessary libraries
import openai  # For interacting with OpenAI's API
import pandas as pd  # For data manipulation
import os  # For file path operations
import time  # For adding delays between API calls

from config import api_key  # Import your API key securely

# Set your OpenAI API key
openai.api_key = api_key

# Define the path for the CSV file containing new words
script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory where the script is located
new_words_path = os.path.join(script_dir, 'new_words.csv')  # Path to the new words file

# Load the new words into a DataFrame
try:
    new_words_df = pd.read_csv(new_words_path)
except FileNotFoundError as e:
    print(f"Error: {e}")
    exit()

# Extract the list of target words from the DataFrame
if 'Target_Word' in new_words_df.columns:
    new_target_words = new_words_df['Target_Word'].dropna().tolist()
elif 'Word' in new_words_df.columns:
    new_target_words = new_words_df['Word'].dropna().tolist()
else:
    print("Error: 'Target_Word' or 'Word' column not found in new_words.csv")
    exit()

# Function to generate a new assessment item for a given word
def generate_assessment_item(word):
    """
    Generates a multiple-choice vocabulary item for the given word using OpenAI's GPT-4 model.
    """
    # Instructions for the model, including example items
    instructions = (
        "You are a multiple-choice vocabulary test designer. For every Target_Word I give you, please write one multiple-choice item for that word. "
        "First, list the Target_Word you are using. Many words will have multiple meanings. You will try to design the item for the most common meaning of the word. "
        "Then, create a Stem. A Stem is a sentence that uses the Target_Word in an example sentence where the Target_Word is capitalized in that sentence. "
        "Then, create the Correct_Response. This is a synonym for the Target_Word that could replace it in the Stem. "
        "Create three other responses (Response_B, Response_C, Response_D) that should not be synonyms but should be able to fit grammatically in the Stem. "
        "In total you will create: Target_Word, Stem, Correct_Response, Response_B, Response_C, Response_D."
        "\n\nHere are some examples of good items:\n"
        "Target_Word: cockeyed\n"
        "Stem: The artist created a COCKEYED portrait that left the audience both puzzled and intrigued.\n"
        "Correct_Response: bizarre\n"
        "Response_B: beautiful\n"
        "Response_C: conventional\n"
        "Response_D: realistic\n"
        "\n"
        "Target_Word: heckle\n"
        "Stem: During the comedian's performance, some audience members began to HECKLE him, disrupting the show.\n"
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
        "Target_Word: cock\n"
        "Stem: The rooster began to COCK its head curiously at the noise coming from the barn.\n"
        "Correct_Response: tilt\n"
        "Response_B: hide\n"
        "Response_C: boast\n"
        "Response_D: perch\n"
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
    )

    # Construct the prompt for the API call
    prompt = f"{instructions}\n\nTarget_Word: {word}"

    try:
        # Make the API call to OpenAI's GPT-4 model
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # Use the GPT-4 model
            messages=[
                {"role": "system", "content": "You are an expert at creating vocabulary assessment items."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,  # Maximum tokens allowed in the response
            timeout=15  # Timeout in seconds for the API call
        )
        # Return the assistant's response text
        return response.choices[0].message['content'].strip()
    except openai.error.OpenAIError as e:
        print(f"Error generating assessment item for '{word}': {e}")
        return None
    except Exception as e:
        print(f"Unexpected error generating assessment item for '{word}': {e}")
        return None

# Generate new assessment items for each target word
new_items = []  # List to hold the generated items

for word in new_target_words:
    print(f"Generating item for word: {word}")
    item = generate_assessment_item(word)
    if item:
        # Clean up the generated text if necessary
        item = item.replace('**', '')  # Remove any asterisks (e.g., markdown bold formatting)
        new_items.append({
            "Target Word": word,
            "Generated Item": item
        })
    time.sleep(1)  # Add a delay to prevent hitting API rate limits

# Process the generated items to extract structured data
formatted_items = []  # List to hold the formatted assessment items

for item in new_items:
    # Split the generated item into lines
    lines = item['Generated Item'].split('\n')
    # Initialize variables to hold the components
    target_word = ''
    stem = ''
    correct_response = ''
    response_b = ''
    response_c = ''
    response_d = ''
    # Process each line to extract the components
    for line in lines:
        if line.strip() == "":
            continue  # Skip empty lines
        line = line.strip()
        if line.startswith('Target_Word:'):
            target_word = line.split('Target_Word:')[1].strip()
        elif line.startswith('Stem:'):
            stem = line.split('Stem:')[1].strip()
        elif line.startswith('Correct_Response:'):
            correct_response = line.split('Correct_Response:')[1].strip()
        elif line.startswith('Response_B:'):
            response_b = line.split('Response_B:')[1].strip()
        elif line.startswith('Response_C:'):
            response_c = line.split('Response_C:')[1].strip()
        elif line.startswith('Response_D:'):
            response_d = line.split('Response_D:')[1].strip()
    # Check if all components have been collected
    if target_word and stem and correct_response and response_b and response_c and response_d:
        formatted_items.append([target_word, stem, correct_response, response_b, response_c, response_d])
    else:
        print(f"Incomplete item for word: {item['Target Word']}")
        print("Generated content:")
        print(item['Generated Item'])

# Create a DataFrame from the formatted items
formatted_items_df = pd.DataFrame(
    formatted_items,
    columns=['Target Word', 'Stem', 'Correct_Response', 'Response_B', 'Response_C', 'Response_D']
)

# Define the path for the output CSV file
new_items_path = os.path.join(script_dir, 'new_assessment_items.csv')

# Save the new assessment items to a CSV file
try:
    formatted_items_df.to_csv(new_items_path, index=False, encoding='utf-8')
    print(f"New assessment items saved to: {new_items_path}")
except Exception as e:
    print(f"Error saving file: {e}")
