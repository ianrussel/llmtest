from llmtool.scripts.sample_app import run
if __name__ == '__main__':
    print('running')
    # Input text for summarization
    text = """
    Hugging blah blah blah Face has democratized AI by providing open-source resources and pre-trained models for a variety of NLP tasks. 
    Their transformers library has become a go-to resource for both researchers and developers looking to leverage state-of-the-art models. 
    From text classification to text generation, and from translation to summarization, Hugging Face offers a comprehensive suite of tools 
    that simplify the implementation of complex NLP tasks. Their Model Hub is a community-driven platform where users can share models and datasets, 
    fostering collaboration and innovation in the AI community.
    """
    result = run(text)

    print(result)
