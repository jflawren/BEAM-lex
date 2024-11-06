# ROAR Vocabulary Assessment Generator

> An AI-powered tool for generating stratified vocabulary assessments using OpenAI's GPT models.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/badge/poetry-package-blueviolet)](https://python-poetry.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-green)](https://openai.com/)

## Overview

ROAR Vocabulary Assessment Generator is a sophisticated tool designed to create high-quality vocabulary assessments by leveraging AI technology. The system:

- 📊 Stratifies words using multiple dimensions (frequency, complexity, polysemy)
- 🤖 Generates context-rich assessment items using GPT models
- 📝 Produces standardized, ready-to-use assessment materials

## Key Features

### Word Stratification
- **Multi-level Classification**
  - Quintile (5-level) stratification for fine-grained assessment
  - Tercile (3-level) stratification for broader grouping
  
### Assessment Types
- **Basic Assessment**: Traditional vocabulary testing format
- **Frequency-Complexity**: Advanced items incorporating word usage patterns
- **Polysemy Assessment**: Items targeting multiple word meanings and context

## Quick Start

### Prerequisites
- Python 3.10 or higher
- Poetry package manager
- OpenAI API key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/roar-voc.git
   cd roar-voc
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Configure your environment:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

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

### Configuration Options

Customize your assessment generation in `config/settings.py`:
```python
WORD_COUNT = 50  # Number of words per assessment
DIFFICULTY_LEVELS = 5  # Number of stratification levels
MODEL_VERSION = "gpt-4"  # OpenAI model selection
```

## Project Structure

```
roar-voc/
├── src/
│   ├── main.py              # Application entry point
│   ├── sampling.py          # Word stratification engine
│   ├── generators/
│   │   ├── basic.py        # Basic assessment generator
│   │   ├── freq_complex.py # Frequency-complexity generator
│   │   └── poly.py         # Polysemy assessment generator
│   └── utils/
├── data/
│   ├── raw/                # Source word lists and metrics
│   └── output/             # Generated assessments
└── config/
    ├── settings.py         # Application configuration
    └── prompts.py         # GPT prompt templates
```

## Output

Generated files are organized in:
- `output/stratified_words/`: Processed word lists
- `output/assessment_items/`: Final assessment items
- `output/metrics/`: Generation statistics and quality metrics

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors

- **[Your Name]** - *Initial work* - [GitHub Profile]

## Acknowledgments

- OpenAI for providing the GPT API
- Contributors and maintainers
- [Other acknowledgments]

---

For detailed documentation, visit our [Wiki](wiki-link).
Report issues on our [Issue Tracker](issues-link).
