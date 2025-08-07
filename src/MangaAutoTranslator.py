import os
# from PIL import Image
from manga_ocr import MangaOcr
from transformers import pipeline
from evaluate import load

def ocr_extractor(img="", file_dir="", multi_file=False):
    """
    Extract Japanese Text using MangaOCR.
    
    Args:
        img (str): Path to the image file if only looking at one image.
        file_dir (str): Path to directory containing images to translate.
        multi_file (bool): If True, process all images in the directory.

    Returns:
        list: List of extracted Japanese text
    """

    image_extensions = (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp")
    if multi_file:
        files = [
            f for f in os.listdir(file_dir)
            if f.lower().endswith(image_extensions) and os.path.isfile(os.path.join(file_dir, f))
        ]
    else:
        files = [img]
    
    mocr = MangaOcr()
    jp_text_list = [mocr(os.path.join(file_dir, file)) for file in files]

    return jp_text_list


def get_translations(jp_text_list, translation_model="Helsinki-NLP/opus-mt-ja-en", concat_sent=False):
    """
    Translate extracted text to English
    
    Args:
        jp_text_list (list of strings): List of extracted Japanese text
        translation_model (str): Translation model to use.
        concat_sent (bool): Whether to concatenate all sentences before translation.
        
    Returns:
        list: list of translated English text
    """

    if not jp_text_list:
        return []
    translate_pipe = pipeline("translation", model=translation_model)

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
    for sent in input_references:
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
    if input_references is None:
        raise ValueError("Input references must be provided for evaluation.")

    tr_text_lists = [tr.split(" ") for tr in translated_text]

    formatted_references = reference_wrapper(input_references)
    
    bleu_metric = load("bleu")
    results = bleu_metric.compute(predictions=tr_text_lists, references=formatted_references)
    print(results)
    
    return results
    
    
def AutoTranslator(img="", file_dir="", translation_model="Helsinki-NLP/opus-mt-ja-en", input_references=None,
                   multi_file=False, concat_sent=False, eval_results=True):
    jp_text_list = ocr_extractor(img=img, file_dir=file_dir, multi_file=multi_file)
    translated_text_list = get_translations(jp_text_list, translation_model=translation_model, concat_sent=concat_sent)
    if eval_results:
        return jp_text_list, translated_text_list, eval_translations(translated_text_list, input_references)
    else:
        return jp_text_list, translated_text_list
