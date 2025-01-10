import os
from PIL import Image
from manga_ocr import MangaOcr
from transformers import pipeline
import evaluate

## Need to move to OOP style to manage variables.


def ocr_extractor(img="", file_dir="", multi_file=False):
    """
    Extract Japanese Text using MangaOCR.
    
    Args:
        img (str): Path to the image file if only looking at one image.
        file_dir (str): Path to directory containing images to translate.
    
    Returns:
        list: List of extracted Japanese text
    """
    print(multi_file) # This is error source. this variable is of course not updating. Either move to OOP or arg_parser.
    if multi_file:
        files = os.listdir(file_dir)
        print(files)
    else:
        files = [img]
    
    mocr = MangaOcr()
    # currently getting error on this saying permission denied when I run with AutoTranslator
    #jp_text_list = [mocr(file_dir+file) for file in files]

    file_list = [file_dir + file for file in files]
    try:
        jp_text_list = [mocr(file) for file in file_list]
    except:
        print(files)
        print(file_list)

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
    
    #tr_text_lists = [tr.split(" ") for tr in translated_text]

    formatted_references = reference_wrapper(input_references)
    
    bleu = evaluate.load("bleu")
    # results = bleu.compute(predictions=tr_text_lists, references=formatted_references)
    results = bleu.compute(predictions=translated_text, references=formatted_references)    
    print(results)
    
    return results
    
    
def AutoTranslator(img="", file_dir="", translation_model="Helsinki-NLP/opus-mt-ja-en", input_references=[], multi_file=False, concat_sent=False, eval_results=True):
    #jp_text_list = ocr_extractor(img=img, file_dir=file_dir)
    jp_text_list = ocr_extractor(img, file_dir)
    translated_text_list = get_translations(jp_text_list, translation_model=translation_model, multi_file=multi_file, concat_sent=concat_sent)
    if eval_results:
        return jp_text_list, translated_text_list, eval_translations(translated_text_list, input_references)
    else:
        return jp_text_list, translated_text_list
 
 
# Moving to script model
# def parse_args():
    # # General settings
    # parser = argparse.ArgumentParser(description="MangaAutoTranslator")
    # parser.add_argument("--img", type=str, default="", help="Single input image filename")
    # parser.add_argument("--file_dir", type=str, default="", help="File Directory containing multiple images to be translated")
    # parser.add_argument("--translation_model", type=str, default="", help="File Directory containing multiple images to be translated")
    
    # # Flags
    # parser.add_argument("--autogen_prompt", action="store_true", help="Whether to use autogen prompt feature")
    # parser.add_argument("--no_autogen_prompt", action="store_false", dest="autogen_prompt", help="Don't use autogen prompt feature")
    # parser.set_defaults(autogen_prompt=True)
    
    # parser.add_argument("--predownloaded", action="store_true", help="Model is predownloaded")
    # parser.add_argument("--not_predownloaded", action="store_false", dest="predownloaded", help="Model is not predownloaded")
    # parser.set_defaults(predownloadedt=True)
    
    # parser.add_argument("--full_auto", action="store_false", help="Full auto toggle")
    # parser.add_argument("--full_auto_on", action="store_true", dest="full_auto", help="Full auto toggle")
    # parser.set_defaults(full_auto=False)

    # return parser.parse_args()
    

# if __name__ == "__main__":
    # args = parse_args()
    
    # generate_graphic_mods(
                    # filepath=args.filepath,
                    # save_folder=args.save_folder,
                    # style=args.style,
                    # num_inference_steps=args.num_inference_steps,
                    # max_length=args.max_length,
                    # autogen_prompt=args.autogen_prompt,
                    # predownloaded=args.predownloaded,
                    # full_auto=args.full_auto
                    # )

    # # # Example call in the command line using different values from preset
    # # # python AutogenGraphicsMods.py --filepath './images/' --save_folder './out/' --style ghibli etc etc
