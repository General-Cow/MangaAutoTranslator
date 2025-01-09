# MangaAutoTranslator

## Project Overview
MangaAutoTranslator is a Python-based script designed to automate the the process of extracting and translation of Japanese test from manga. It does so by utilizing Optical Character Recognition and machine translation pipelines to translate from Japanese to English.

## Features

- OCR Extraction: Utilizes the MangaOCR library to extract Japanese Text from manga.
- Translation: Translate extracted Japanese text into English using Hugging Face's transformer pipeline and preferred translation model.
- Evaluation: Assess translation quality using the BLEU metric based on input reference translations.

## Installation/Dependencies
Ensure the following Python libraries are installed:

- `Pillow`
- `manga_ocr`
- `transformers`
- `datasets`

Install them using pip:


`pip install Pillow manga_ocr transformers datasets`

## Function Descriptions
- `ocr_extractor`: Extracts Japanese text from a single image or batch of images.
- `get_translations`: Translates extracted text to English using a specified model.
- `reference_wrapper`: Formats reference text for BLEU evaluation.
- `eval_translations`: Evaluates translations using BLEU score.
- `AutoTranslator`: Combines all steps into a single, streamlined function.

##Configuration Options
- `multi_file`: Set to True to process multiple images in a directory.
- `concat_sent`: Concatenate all sentences into one string before translation.
- `translation_model`: Choose a Hugging Face translation model (default: `Helsinki-NLP/opus-mt-ja-en`).

## Example References Format
For BLEU evaluation, the input references should follow this format:
```
[
    ["This is a sentence.", "Alternate translation of this sentence."],
    ["Another sentence.", "Alternate of another."]
]
```

## How to Use

This script allows for as individual functions or a simple complete process with the AutoTranslator function.

### 1. Extract Japanese Texts
The `ocr_extractor` function extracts Japanese Text from an image or directory of images.

```
from MangaAutoTranslator import ocr_extractor

jp_text_list = ocr_extractor(img="path/to/image.png", file_dir="path/to/image_directory")`
```

### 2. Translate Text
The `get_translations` function translates extracted Japanese text into English using input translation model. Sentences can be concatenated if desired.

```
from MangaAutoTranslator import get_translations

translated_text_list = get_translations(jp_text_list, translation_model="Helsinki-NLP/opus-mt-ja-en", concat_sent=False)
```

### 3. Evaluate Translations
The `eval_translations` function evaluates the quality of the translation with the BLEU metric. This requires reference translations to score against.

```
from MangaAutoTranslator import eval_translations

bleu_results = eval_translations(translated_text_list, input_references)
```

### 4. Full Workflow
The `AutoTranslator` function runs the full workflow in one line. Can choose whether or not to 

```
from MangaAutoTranslator import AutoTranslator

jp_text, en_text, eval_results = AutoTranslator(
    img="path/to/image.png", 
    file_dir="path/to/image_directory",
    input_references=reference_text
    multi_file=True, 
    concat_sent=False, 
    eval_results=True
)
```

## Future Work
- Try different OCR methods and better automation for finding text in images to eliminate need to crop word bubbles.
   - Text position tracking/Overlay translations
- Improve translation quality
   - Incorporate context aware models
   - Fine-tuning of translation models to improve performance
- Create UI

- Consider other evaluation methods

## License
This project is licensed under the MIT License.

## Contact
For questions or contributions, please reach out via GitHub.
