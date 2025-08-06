from langchain.document_loaders import PyPDFLoader
from langchain.docstore.document import Document
from langchain.text_splitter import TokenTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
import os
from dotenv import load_dotenv
from src.prompt import *

load_dotenv()
OPENAI_API_KEY = os.getenv("sk-1234qrstuvwxabcd1234qrstuvwxabcd1234qrst")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

def file_preocessing(file_path):
    loader = PyPDFLoader(file_path)
    data = loader.load()

    question_gen = ''

    for page in data:
        question_gen += page.page_content

    splitter_ques_gen = TokenTextSplitter(chunk_size=1000, chunk_overlap=200)

    chunk_ques_gen = splitter_ques_gen.split_text(question_gen)

    document_ques_gen = [Document(page_content=chunk) for chunk in chunk_ques_gen]

    splitter_ans_gen = TokenTextSplitter(chunk_size=1000, chunk_overlap=100)

    document_ans_gen = splitter_ans_gen.split_documents(document_ques_gen)
    return document_ques_gen, document_ans_gen


def llm_pipeline(file_path):
    document_ques_gen, document_ans_gen = file_preocessing(file_path)

    llm_ques_gen_pipeline = ChatOpenAI(
        model_name="text-davinci-003",
        temperature=0.3,
    )

    PROMPT_QUESTIONS = PromptTemplate(template = PromptTemplate, input_variables=["text"]    )

    REFINE_PROMPT_QUESTIONS = PromptTemplate(template=refine_template, input_variables=["text", "existing_answer"])
    ques_gen_chain = load_summarize_chain(llm=llm_ques_gen_pipeline, chain_type="refine",
                                            question_prompt=PROMPT_QUESTIONS,
                                            refine_prompt=REFINE_PROMPT_QUESTIONS)
    ques = ques_gen_chain.run(document_ques_gen)

    embeddings = OpenAIEmbeddings()

    vector_store = FAISS.from_documents(document_ans_gen, embeddings)
    llm_ans_gen = ChatOpenAI(temperature=0.1, model_name="gpt-3.5-turbo")

    ques_list = ques.split("\n")
    filtered_ques_list = [element for element in ques_list if element.endswith("?") or element.endswith(".")]

    answer_generation_chain = RetrievalQA.from_chain_type(
        llm=llm_ans_gen,
        chain_type="stuff",
        retriever=vector_store.as_retriever())
    
    return answer_generation_chain, filtered_ques_list

