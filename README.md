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
- **Basic Assessment**: Traditional vocabulary testing format
- **Frequency-Complexity**: Advanced items incorporating word usage patterns
- **Polysemy Assessment**: Items targeting multiple-word meanings and context

## Quick Start

### Prerequisites
- Python 3.10 or higher
- Poetry package manager
- AI API

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/jflawren/roar-voc.git
   cd roar-voc
   ```
   Or

   - Fetch and checkout update/josh if you have the repo.. to use this updated branch

3. Install dependencies:
   ```bash
   poetry install
   ```

4. Configure your environment:
   ```bash
   Create config.py in src/ and add your API key
   ```
5. Prepare data
   - Create directory named data in root directory and add data files
     
## Usage

### Command Line Interface

```bash
# Generate basic assessment
python src/main.py

# Use existing word lists
python src/main.py --skip-sampling

# Generate specific assessment type
python src/main.py --type basic|freq_complex|poly
```

## Output

Generated files are organized in:
- `output/stratified_words/`: Processed word lists
- `output/assessment_items/`: Final assessment items

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
