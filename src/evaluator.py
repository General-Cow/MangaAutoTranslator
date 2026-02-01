from evaluate import load

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
    
    return results