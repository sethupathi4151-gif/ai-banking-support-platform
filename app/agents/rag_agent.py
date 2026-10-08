import os
import shutil
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()


KNOWLEDGE_DIR = Path("data/knowledge_base")
CHROMA_DIR = "data/.chroma"


embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
)


def build_vectorstore():

    documents = []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    for file_path in KNOWLEDGE_DIR.glob("*.txt"):

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            text = file.read()

        chunks = splitter.create_documents(
            [text],
            metadatas=[
                {
                    "source": file_path.name
                }
            ]
        )

        documents.extend(chunks)

    if not documents:
        raise RuntimeError(
            "No knowledge base documents found."
        )

    if os.path.exists(CHROMA_DIR):
        shutil.rmtree(CHROMA_DIR)

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )

    return vectorstore


def search_knowledge(
    query: str,
    k: int = 3
):

    vectorstore = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )

    results = vectorstore.similarity_search(
        query,
        k=k
    )

    return [
        document.page_content
        for document in results
    ]