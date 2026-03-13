from transformers import pipeline
from ollama import chat
from ollama import ChatResponse
from openai import OpenAI

def get_translations(jp_text_list, translation_model="Helsinki-NLP/opus-mt-ja-en", concat_sent=False):
    """
    Translate extracted text to English using translation model.
    
    Args:
        jp_text_list (list of strings): List of extracted Japanese text
        translation_model (str): Translation model to use.
        concat_sent (bool): Whether to concatenate all sentences before translation.
        
    Returns:
        list: list of translated English text
    """

    if not jp_text_list:
        return []
    
    translate_pipe = pipeline("translation", model=translation_model, src_lang="ja", tgt_lang="en")  #src_lang="jpn_Latn", tgt_lang="eng_Latn") # added src_lang and tgt_lang for NLLB models

    if concat_sent:
        concatenated_text = "".join(jp_text_list)
        translated_text_list = [translate_pipe(concatenated_text)[0]["translation_text"]]
    else:
        translated_text_list = [translate_pipe(text)[0]["translation_text"] for text in jp_text_list]
    
    return translated_text_list


def get_llm_translations(jp_text_list, llm_model='gemma3:4b'):
    """
    Translate extracted text to English using an LLM.
    
    Args:
        jp_text_list (list of strings): List of extracted Japanese text
        llm_model (str): LLM model to use for translation.
        
    Returns:
        list: list of translated English text
    """
    translated_text_list = []
    for jp_text in jp_text_list:
        response: ChatResponse = chat(model=llm_model, messages=[
            {
                'role': 'system',
                'content': (
                    'Translate the following Japanese text to English. '
                    'Return ONLY the translated English text. '
                    'Do not add notes, explanations, or formatting.'
                            ),
            },
            {
                'role': 'user',
                'content': jp_text,
            },
        ])

        translated_text_list.append(response.message.content)

    return translated_text_list

def get_api_translations(jp_text_list, api_key): # Add parameters as needed for different APIs
    """
    Translate extracted text to English using OpenAI API.
    
    Args:
        jp_text_list (list of strings): List of extracted Japanese text
        api_key (str): The API key for accessing the OpenAI API
        
    Returns:
        list: list of translated English text
    """

    translated_text_list = []
    client = OpenAI(api_key=api_key)

    for jp_text in jp_text_list:
        response = client.responses.create(
                model="gpt-5",
                reasoning={"effort": "high"},
                instructions="Translate the following Japanese text to English. Return ONLY the translated English text. Do not add notes, explanations, or formatting.",
                input=jp_text,
            )

        translated_text_list.append(response.output_text)

    return translated_text_list

