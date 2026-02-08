# Lowercase Text Formatter

You know that meme about guys that type in all lowercase? Well this Python application does just that. It has a GUI for formatting text to lowercase while intelligently preserving capitalization for proper nouns, the pronoun "I", and other contextually appropriate elements. Works in two modes: an advanced NLP mode powered by spaCy for enhanced entity recognition, or a basic mode using regular expressions for simpler processing. Built using CustomTkinter for a cool interface

## Features

- Converts text to lowercase while maintaining capitalization for proper nouns, entities, and specific words like "I"
- Dual Processing Modes:
  - NLP Mode: Utilizes spaCy for accurate part-of-speech tagging and entity detection (requires spaCy installation)
  - Basic Mode: Falls back to rule-based processing with regular expressions if spaCy is unavailable
- Retains leading whitespace and line structures from the input text
- Displays word and character counts for the formatted output
- Allows easy copying of the processed text to the clipboard

## Requirements

- Python 3.8 or higher
- Required libraries:
  - `customtkinter`: For the GUI framework
  - `re`: Standard library for regular expressions (included in Python)
- Optional libraries:
  - `spacy`: For NLP mode. Install the English model with `python -m spacy download en_core_web_sm`
- No additional internet access or API keys are required

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/lowercase-text-formatter.git
   cd lowercase-text-formatter
   ```

2. Install the required dependencies:
   ```
   pip install customtkinter
   ```

3. (Optional) For NLP mode, install spaCy and the language model:
   ```
   pip install spacy
   python -m spacy download en_core_web_sm
   ```

## Usage

Run the application:
```
   lowercase text formatter.py
```

The status indicator in the header will show "NLP ACTIVE" if spaCy is available, or "BASIC MODE" otherwise

## Limitations

- NLP mode requires additional installation and may increase processing time for large texts
- Basic mode may not handle complex entity recognition as accurately as NLP mode
- The application is designed for English text; support for other languages would require spaCy model adjustments

## Acknowledgments

- Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for the GUI
- Powered by [spaCy](https://spacy.io/) for natural language processing (optional)
