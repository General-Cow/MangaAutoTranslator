import os
from PIL import Image
from manga_ocr import MangaOcr
import easyocr
from transformers import pipeline
from datasets import load_metric

def ocr_extractor(img="", file_dir=""):
    """
    Extract Japanese Text using MangaOCR.
    
    Args:
        img (str): Path to the image file if only looking at one image.
        file_dir (str): Path to directory containing images to translate.
    
    Returns:
        list: List of extracted Japanese text
    """

    if multi_file:
        files = os.listdir(file_dir)
    else:
        files = [img]
    
    mocr = MangaOcr()
    jp_text_list = [mocr(file_dir+file) for file in files]

    return jp_text_list


def get_translations(jp_text_list, translation_model="Helsinki-NLP/opus-mt-ja-en", multi_file=False, concat_sent=False):
    """
    Translate extracted text to English
    
    Args:
        jp_text_list (list of strings): List of extracted Japanese text
        translation_model (str): Translation model to use.
        multi_file (bool): Whether to process multiple files.
        concat_sent (bool): Whether to concatenate all sentences before translation.
        
    Returns:
        list: list of translated English text
    """
    
    translate_pipe = pipeline("translation", model=translation_model)
    translated_text_list = []
    if concat_sent:
        concatenated_text = "".join(jp_text_list)
        translated_text_list = [translate_pipe(concatenated_text)[0]["translation_text"]]
    else:
        translated_text_list = [translate_pipe(text)[0]["translation_text"] for text in jp_text_list]
    
    return translated_text_list


def reference_wrapper(input_references):
    """
    Formats the reference list for BLEU evaluation.
    
    Input should have the following form:
    
    [
    [sent_1 entry_1, sent1 entry2],
    [sent2 entry1....],
    .
    .
    .
    [sent_n entry1, .....]
    ]

    Args:
        input_references(list of list of str): Outer list is different sentences. Inner list are different acceptable translations of the sentence.

    Returns:
        list: Formatted reference list for BLEU metric.
    """
    
    formatted_references = []
    for sent in references:
        if len(sent) > 1:
            multi_entry_list = [entry.split(" ") for entry in sent]
            formatted_references.append(multi_entry_list)
        else:
            formatted_references.append([sent[0].split(" ")])

    return formatted_references


def eval_translations(translated_text, input_references):
    """
    Evaluates translations using the BLEU metric.
    
    Args:
        translated_text (list of str): Translated text sentences.
        input_references (list of list of str): Reference sentences for evaluation.
        
    Returns:
        dict: BLEU score and other evaluation results
    """
    
    tr_text_lists = [tr.split(" ") for tr in translated_text]

    formatted_references = reference_wrapper(input_references)
    
    bleu_metric = load_metric("bleu")
    results = bleu_metric.compute(predictions=tr_text_lists, references=formatted_references)

    return results
    
    
def AutoTranslator(input_references, img="", file_dir="", translation_model="Helsinki-NLP/opus-mt-ja-en", multi_file=False, concat_sent=False, eval_results=True):
    jp_text_list = ocr_extractor(img=img, file_dir=file_dir)
    translated_text_list = get_translations(jp_text_list, translation_model=translation_model, multi_file=multi_file, concat_sent=concat_sent)
    if eval_results:
        return jp_text_list, translated_text_list, eval_translations(translated_text_list, input_references)
    else:
        return jp_text_list, translated_text_list