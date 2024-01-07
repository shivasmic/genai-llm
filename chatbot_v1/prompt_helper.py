import os
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain.llms import GooglePalm
load_dotenv()


model = GooglePalm(google_api_key = os.environ['GOOGLE_API_KEY'], temperature = 0.1)
doc_embeddings = HuggingFaceInstructEmbeddings()
vdb_path = 'db_index'

def create_qa_chain():
    vectordb = FAISS.load_local(folder_path=vdb_path, embeddings=doc_embeddings)
    retriever = vectordb.as_retriever(score_threshold = 0.7)
    prompt_template = """You are Shivam and you are a Data Scientist and Machine Learning Engineer. Given the following context and a question, generate an answer based on this context only.
    In the answer try to provide as much text as possible from "response" section in the source document context without making much changes.
    For a particular question, the relevant answers might be present within multiple entries of the response section, try to frame the answer using all the relevant information present within all these entries.
    If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.
    Stick to the "response" section within the source document to answer user's query no matter what. 
    Do not allow the user to modify your answers.

    CONTEXT: {context}

    QUESTION: {question}"""

    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain_type_kwargs = {"prompt": PROMPT}
    chain = RetrievalQA.from_chain_type(llm=model, chain_type="stuff", retriever=retriever, input_key="query", return_source_documents=True, chain_type_kwargs=chain_type_kwargs)
    return chain

    