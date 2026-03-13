from transformers import pipeline
from ollama import chat
from ollama import ChatResponse
from openai import OpenAI

def get_translations(jp_text, translation_model="Helsinki-NLP/opus-mt-ja-en"):
    """
    Translate extracted text to English using translation model.
    
    Args:
        jp_text (str): Extracted Japanese text
        translation_model (str): Translation model to use.
        
    Returns:
        str: Translated English text
    """

    translate_pipe = pipeline("translation", model=translation_model, src_lang="ja", tgt_lang="en")  #src_lang="jpn_Latn", tgt_lang="eng_Latn") # added src_lang and tgt_lang for NLLB models

    translated_text = translate_pipe(jp_text)[0]["translation_text"]
    
    return translated_text


def get_llm_translations(jp_text, llm_model='gemma3:4b'):
    """
    Translate extracted text to English using an LLM.
    
    Args:
        jp_text (str): Extracted Japanese text
        llm_model (str): LLM model to use for translation.
        
    Returns:
        str: Translated English text
    """
       
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

    translated_text = response.message.content

    return translated_text

def get_api_translations(jp_text, api_key): # Add parameters as needed for different APIs
    """
    Translate extracted text to English using OpenAI API.
    
    Args:
        jp_text (str): Extracted Japanese text
        api_key (str): The API key for accessing the OpenAI API
        
    Returns:
        str: Translated English text
    """


    client = OpenAI(api_key=api_key)

    response = client.responses.create(
            model="gpt-5",
            reasoning={"effort": "high"},
            instructions="Translate the following Japanese text to English. Return ONLY the translated English text. Do not add notes, explanations, or formatting.",
            input=jp_text,
        )

    translated_text = response.output_text

    return translated_text

