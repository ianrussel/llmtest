from transformers import pipeline


def run(text: str) -> str:
    # Load the summarization pipeline
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    # # Generate the summary
    # summary = summarizer(text, max_length=5000, min_length=30, do_sample=False)

    # # return the summary
    # return summary[0]['summary_text']
    # Split the text into chunks
    # BART typically handles up to 1024 tokens
    chunks = split_text(text, max_length=1024)

    # Summarize each chunk
    summaries = [summarizer(chunk, max_length=130, min_length=30, do_sample=False)[
        0]['summary_text'] for chunk in chunks]

    # Concatenate summaries
    final_summary = ' '.join(summaries)

    return final_summary


def split_text(text, max_length=1000):
    """Split the text into chunks of max_length."""
    # Split by sentences to avoid cutting in the middle of a sentence
    sentences = text.split('. ')
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sentence_length = len(sentence) + 1  # +1 to account for the '.'
        if current_length + sentence_length > max_length:
            chunks.append('. '.join(current_chunk))
            current_chunk = []
            current_length = 0
        current_chunk.append(sentence)
        current_length += sentence_length

    if current_chunk:
        chunks.append('. '.join(current_chunk))

    return chunks
