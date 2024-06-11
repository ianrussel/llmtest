from transformers import pipeline


def run(text: str) -> str:
    """
    Summarizes the given text using a pre-trained summarization model.

    This function performs the following steps:
    1. Initializes a summarization pipeline using a pre-trained model.
    2. Splits the input text into manageable chunks.
    3. Summarizes each chunk individually.
    4. Concatenates the summaries of all chunks into a final summary.

    Args:
        text (str): The input text to be summarized.

    Returns:
        str: The summarized text.
    """
    # summarizer = pipeline("summarization", model="")
    """ 
    we use sshleifer/distilbart-cnn-12-6 as it requires low resources as compared to facebook/bart-large-cnn, suitable for this test task
    """
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    chunks = split_text(text, max_length=512)

    # Summarize each chunk
    summaries = [
        summarizer(chunk, max_length=130, min_length=30, do_sample=False)[0][
            "summary_text"
        ]
        for chunk in chunks
    ]

    # Concatenate summaries
    final_summary = " ".join(summaries)

    return final_summary


def split_text(text, max_length=512):
    """
    Splits the given text into chunks of a specified maximum length.

    This function splits the input text into chunks, ensuring that each chunk
    does not exceed the specified maximum length. The splitting is done based
    on sentences, maintaining the integrity of sentences across chunks.

    Args:
        text (str): The input text to be split.
        max_length (int, optional): The maximum length of each chunk. Defaults to 512.

    Returns:
        list: A list of text chunks, each with a length up to max_length.
    """
    sentences = text.split(". ")
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sentence_length = len(sentence) + 1
        if current_length + sentence_length > max_length:
            chunks.append(". ".join(current_chunk))
            current_chunk = []
            current_length = 0
        current_chunk.append(sentence)
        current_length += sentence_length

    if current_chunk:
        chunks.append(". ".join(current_chunk))

    return chunks
