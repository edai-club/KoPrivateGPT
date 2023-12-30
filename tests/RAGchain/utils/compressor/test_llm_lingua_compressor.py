import pytest
from langchain.llms.openai import OpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.schema import StrOutputParser

from RAGchain.utils.compressor.llm_lingua import LLMLinguaCompressor


@pytest.fixture
def llm_lingua_compressor():
    compressor = LLMLinguaCompressor(model_name="TheBloke/Llama-2-7b-Chat-GPTQ", model_config={"revision": "main"})
    yield compressor


def test_llm_lingua_compressor(llm_lingua_compressor):
    prompt = PromptTemplate.from_template("Hello, I am a {role}.")
    runnable = prompt | llm_lingua_compressor | OpenAI() | StrOutputParser()
    answer = runnable.invoke({"role": "student"})
    assert answer.strip() == "Hello, I am a student."

    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", "As a helpful assistant, follow the instructions below."),
        ("user", "Hello, I am a {role}."),  # user input
    ])

    runnable = chat_prompt | llm_lingua_compressor | OpenAI() | StrOutputParser()
    answer = runnable.invoke({"role": "student"})
    assert bool(answer) is True

    for s in runnable.stream({"role": "student"}):
        print(s)
