__author__ = "Himanshu Sharma"
__copyright__ = "Copyright 2024, Personal"
__license__ = "GreymanAI ownership"
__version__ = "0.1"
__maintainer__ = "Himanshu Sharma"
__status__ = "Development"

import os, json

from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
load_dotenv()


def combine_results(sql_data, website_data, pdf_data):
    combined_data = sql_data + [website_data] + pdf_data
    return " ".join([str(item) for item in combined_data])


def process_text(username, combined_text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
    # api_key = os.environ["GOOGLE_API_KEY"]
    splits = text_splitter.split_text(combined_text)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(splits, embeddings)
    vector_store.save_local(username)
    return "Resources processed. You can now ask questions."


def get_context(username, user_input):
    api_key = os.environ["GOOGLE_API_KEY"]
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local(folder_path=username, embeddings=embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_input)
    top_docs = docs[:3]
    contexts = [doc.page_content for doc in top_docs if doc.page_content]
    combined_context = " ".join(contexts)

    return combined_context


def save_user_data(user_data):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'userid.json')
    with open(file_path, 'w') as file:
        json.dump(user_data, file)


def load_user_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'userid.json')
    with open('userId.json', 'r') as file:
        content = file.read()
        return json.loads(content)


if __name__ == '__main__':
    print(process_text('a',"hello this is me"))
    # print(get_context('z', "What is GreymanAI"))


