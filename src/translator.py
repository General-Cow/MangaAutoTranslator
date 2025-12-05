from transformers import pipeline


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
    translate_pipe = pipeline("translation", model=translation_model,src_lang="ja", tgt_lang="en")  #src_lang="jpn_Latn", tgt_lang="eng_Latn") # added src_lang and tgt_lang for NLLB models

    if concat_sent:
        concatenated_text = "".join(jp_text_list)
        translated_text_list = [translate_pipe(concatenated_text)[0]["translation_text"]]
    else:
        translated_text_list = [translate_pipe(text)[0]["translation_text"] for text in jp_text_list]
    
    return translated_text_list


def get_llm_translations(jp_text_list, llm_model='gemma3:4b'):


    from ollama import chat
    from ollama import ChatResponse

    translated_text_list = []
    for jp_text in jp_text_list:

        print(jp_text_list)
        response: ChatResponse = chat(model=llm_model, messages=[
        {
            'role': 'system',
            'content': 'You are a helpful assistant that translates Japanese to English and only returns the translated text without any additions.',
        },
        {
            'role': 'user',
            'content': jp_text,
        },
        ])
        translated_text_list.append(response.message.content)

    return translated_text_list