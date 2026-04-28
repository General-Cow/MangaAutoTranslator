# MangaAutoTranslator

## Project Overview
MangaAutoTranslator is a Python-based Streamlit app meant to give English speakers who don't speak Japanese the ability to read and enjoy untranslated manga
It includes the entire pipeline necessary to go from untranslated manga pages to English language translations. 
Features include preprocessing, OCR, autotranslation and a reader.

## Features

- Preprocessing: Includes a preprocessing page for slicing text boxes for input into the OCR tool.
- OCR Extraction: Utilizes the MangaOCR library to extract Japanese Text from manga.
- Autotranslation: Translate extracted Japanese text into English using translation models, LLMs, and proprietary model APIs.
- Reader: Page for loading and viewing previously translated pages.

## Installation/Dependencies

This repository was built on Python version 3.12.6. The CUDA/PyTorch environment used was built on version 12.6.

A virtual environment is recommended and a requirements.txt file is provided with dependencies for this repository.

Install using the following command:

```python
pip install -r requirements.txt
```

## How to Use
To open this app open a terminal, navigate to the repository directory, and enter the following command

```python
streamlit run app.py
```

Will include description and instructions for each page. Currently WIP.

### Home Page
WIP

### Manual Slicer
WIP

### Manga AutoTranslator
WIP

### Manga Reader
WIP

## License
This project is licensed under the MIT License.

## Contact
For questions or contributions, please reach out via GitHub.
