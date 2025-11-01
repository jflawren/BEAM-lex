# ROAR Vocabulary Assessment Generator

> An AI-powered tool for generating stratified vocabulary assessments using AI.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/badge/poetry-package-blueviolet)](https://python-poetry.org/)

## Overview

ROAR Vocabulary Assessment Generator is a sophisticated tool designed to create high-quality vocabulary assessments by leveraging AI technology. The system:

- 📊 Uses word stratification data (frequency, complexity, polysemy) from the database
- 🤖 Generates context-rich vocabulary assessment items using AI
- 📝 Produces standardized, ready-to-use assessment materials
- 📈 Automatically performs correlation analysis between lexical dimensions

## Key Features

### Word Stratification
- **Multi-level Classification**
  - Quintile (5-level) stratification for fine-grained assessment
  - Tercile (3-level) stratification for broader grouping
  
### Assessment Type
- **Basic Assessment**: Traditional vocabulary testing format with AI-generated context-rich items

## Usage

### Age Levels
1. Early childhood
2. Later childhood
3. Elementary
4. Middle school
5. High school
6. University

### Command Structure

```bash
python src/main.py --min-age [MIN] --max-age [MAX]
```
Note: This command will work if you've activated the Python environment and all project dependencies are installed. If you prefer to use the Poetry environment—especially to avoid installing dependencies manually—add poetry run at the beginning, right before python.
For example: 
```bash
poetry run python src/main.py --min-age [MIN] --max-age [MAX]
```

### Common Age Range Commands

#### Adjacent Age Groups
```bash
# Early Childhood to Later Childhood (Ages 1-2)
poetry run python src/main.py --min-age 1 --max-age 2 --strata 3

# Later Childhood to Elementary (Ages 2-3)
poetry run python src/main.py --min-age 2 --max-age 3 --strata 3

# Elementary to Middle School (Ages 3-4)
poetry run python src/main.py --min-age 3 --max-age 4 --strata 3

# Middle School to High School (Ages 4-5)
poetry run python src/main.py --min-age 4 --max-age 5 --strata 3

# High School to University (Ages 5-6)
poetry run python src/main.py --min-age 5 --max-age 6 --strata 3
```

#### Broader Ranges
```bash
# Early Childhood to Elementary (Ages 1-3)
poetry run python src/main.py --min-age 1 --max-age 3 --strata 3

# Elementary to High School (Ages 3-5)
poetry run python src/main.py --min-age 3 --max-age 5 --strata 3

# Middle School to University (Ages 4-6)
poetry run python src/main.py --min-age 4 --max-age 6 --strata 3
```

### Additional Options
- `--skip-sampling`: Use existing word lists instead of generating new ones (skips correlation analysis)
```bash
poetry run python src/main.py --min-age 1 --max-age 2 --skip-sampling
```
- `--custom-words`: Generate assessments for specific words
  - Accepts comma-separated words or text file path
  - Always uses quintile (5-level) stratification

Note: When using custom words:
- Age level options (--min-age, --max-age) are ignored
- Strata type is always set to quintiles
- Only generates one assessment (no terciles/quintiles option)

### Example Usage
Using comma-separated words
```bash
poetry run python src/main.py --custom-words "apple,banana,orange,eat"
```
Using a text file (one word per line)
```bash
poetry run python src/main.py --custom-words "words.txt"
```

### Strata Selection
- `--strata`: Choose stratification type
  - `3`: Terciles only (3-level stratification)
  - `5`: Quintiles only (5-level stratification)
  - `both`: Generate both types (default)

```bash
poetry run python src/main.py --min-age 3 --max-age 4 --strata 3
```


## Installation

1. Ensure you have Python 3.10+ installed
2. Install Poetry if you haven't already:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
3. Clone this repository
4. Install dependencies:
   ```bash
   poetry install
   ```

## Configuration
- Ensure your AI API key is properly set up
- Check configuration files are in place (see `.gitignore` for required files)

### API Key (config.py)
Create a git-ignored file at `src/config.py` that contains your OpenAI API key:

```python
# src/config.py
api_key = "YOUR_OPENAI_API_KEY"
```

This project loads the key with `from config import api_key`. Do not commit this file; it is intentionally excluded from version control for security.

## File Structure and Storage

### Database
- **Main dataset**: `data/predictions_imputed_quantileaoa.csv`
  - Contains 407,513 words with linguistic metrics
  - Used for word stratification and custom word lookup
  - Required for all operations
  - Information about the dataset and sample data used can be found [here](URL_TO_BE_ADDED)  

### Output Locations

**Note:** All output directories are created automatically when needed. You don't need to create them manually.

#### Word Lists
- **Regular stratified words**: `output/stratified_words/`
  - `quintiles/` - 5-level stratified word files
  - `terciles/` - 3-level stratified word files
  - Files named: `stratified_words_seed{seed}_age_{min}-{max}_{timestamp}.csv`

#### Custom Words
- **Custom word files**: `output/stratified_words/`
  - Files named: `custom_words_seed{seed}_{timestamp}.csv`
  - Created when using `--custom-words` option

#### Assessment Items
- **Generated assessments**: `output/assessment_items/`
  - Files named: `assessment_items_seed{seed}_age{range}_{timestamp}.csv`
  - Contains: Target Word, Stem, Correct_Response, Response_B, Response_C, Response_D, metrics

### Custom Words Input

#### Comma-Separated Words
```bash
poetry run python src/main.py --custom-words "apple,banana,orange,eat"
```

#### Text File (One word per line)
Create a text file (e.g., `words.txt`):
```
apple
banana
orange
eat
```
Then use:
```bash
poetry run python src/main.py --custom-words "words.txt"
```

#### File Requirements
- **Text files**: Must contain one word per line
- **Word matching**: Case-insensitive (converted to lowercase for matching)
- **Dataset lookup**: Words must exist in the main dataset
- **Output**: Custom words are saved to `output/stratified_words/custom_words_*.csv`

### Example File Structure
```
roar_voc/
├── data/
│   └── predictions_imputed_quantileaoa.csv    # Main word database
├── output/
│   ├── stratified_words/
│   │   ├── quintiles/                         # 5-level word files
│   │   ├── terciles/                          # 3-level word files
│   │   └── custom_words_*.csv                 # Custom word files
│   ├── assessment_items/
│   │   └── assessment_items_*.csv             # Generated assessments
│   └── correlations/
│       └── correlations_*.csv/.png            # Correlation analysis outputs
├── src/
│   └── main.py                               # Main script
└── words.txt                                 # Example custom words file
```

## Age of Acquisition Distribution

| Quantile (AoA Mean) |   Mean   |   Min    |   Max    |    N    |
|:-------------------|:--------:|:--------:|:--------:|:-------:|
| 1                  | 6.22068  | 1.58000  | 7.94000  | 5,192   |
| 2                  | 8.91688  | 7.94815  | 9.76000  | 5,132   |
| 3                  | 10.49940 | 9.77000  | 11.17000 | 5,177   |
| 4                  | 11.84753 | 11.17542 | 12.50000 | 5,167   |
| 5                  | 13.24037 | 12.52000 | 14.00000 | 5,230   |
| 6                  | 15.34878 | 14.03796 | 21.00000 | 5,069   |
|-------------------|----------|----------|----------|---------|
| Total             | 11.00142 | 1.58000  | 21.00000 | 30,967  |
