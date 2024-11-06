# ROAR Vocabulary Assessment Generator

> An AI-powered tool for generating stratified vocabulary assessments using AI.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/badge/poetry-package-blueviolet)](https://python-poetry.org/)

## Overview

ROAR Vocabulary Assessment Generator is a sophisticated tool designed to create high-quality vocabulary assessments by leveraging AI technology. The system:

- 📊 Stratifies words using multiple dimensions (frequency, complexity, polysemy)
- 🤖 Generates context-rich assessment items using AI
- 📝 Produces standardized, ready-to-use assessment materials

## Key Features

### Word Stratification
- **Multi-level Classification**
  - Quintile (5-level) stratification for fine-grained assessment
  - Tercile (3-level) stratification for broader grouping
  
### Assessment Types
- **Basic Assessment** (`basic`): Traditional vocabulary testing format
- **Frequency-Complexity** (`freq_complex`): Advanced items incorporating word usage patterns
- **Polysemy Assessment** (`poly`): Items targeting multiple-word meanings and context

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
python src/main.py --min-age [MIN] --max-age [MAX] --type [TYPE]
```

### Common Age Range Commands

#### Adjacent Age Groups
```bash
# Early Childhood to Later Childhood (Ages 1-2)
python src/main.py --min-age 1 --max-age 2 --type basic

# Later Childhood to Elementary (Ages 2-3)
python src/main.py --min-age 2 --max-age 3 --type basic

# Elementary to Middle School (Ages 3-4)
python src/main.py --min-age 3 --max-age 4 --type basic

# Middle School to High School (Ages 4-5)
python src/main.py --min-age 4 --max-age 5 --type basic

# High School to University (Ages 5-6)
python src/main.py --min-age 5 --max-age 6 --type basic
```

#### Broader Ranges
```bash
# Early Childhood to Elementary (Ages 1-3)
python src/main.py --min-age 1 --max-age 3 --type basic

# Elementary to High School (Ages 3-5)
python src/main.py --min-age 3 --max-age 5 --type basic

# Middle School to University (Ages 4-6)
python src/main.py --min-age 4 --max-age 6 --type basic
```

### Assessment Types
Replace `--type basic` with:
- `--type freq_complex` for frequency-complexity assessments
- `--type poly` for polysemy assessments

### Additional Options
- `--skip-sampling`: Use existing word lists instead of generating new ones
```bash
python src/main.py --min-age 1 --max-age 2 --type basic --skip-sampling
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
- Ensure your OpenAI API key is properly set up
- Check configuration files are in place (see `.gitignore` for required files)