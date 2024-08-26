from transformers import pipeline
#from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
def hf_summary(text) -> str:

    model = "facebook/bart-large-cnn"

    summarizer = pipeline("summarization", model=model)
    summary = summarizer(text, max_length=50, min_length=2, do_sample=False)
    summarized = summary[0]["summary_text"]
    return summarized


def create_Q(summarized) -> str:

    model_name = "google/flan-t5-large"
    instruct = "Create a question based on the text"
    questioncreator = pipeline("text2text-generation", model=model_name)
    question = questioncreator(summarized + instruct)
    return question

def openAI_qa(text, openai_key=None) -> str:
    if openai_key is None:
        openai_key = os.getenv("OPENAI_API_KEY")
    assert openai_key is not None, "OpenAI API key not found."

    client = OpenAI(api_key=openai_key)
    model = "gpt-3.5-turbo-0125"

    completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful tutor for high school."},
            {
                "role": "user",
                "content": text + "Create a multiple choice question with for potential answers"
            }
        ],
        model=model,
    )

    qa = completion.choices[0].message.content
    return qa

