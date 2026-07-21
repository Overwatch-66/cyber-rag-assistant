"""
Script d'ingestion des référentiels cybersécurité.
Charge les documents PDF, les découpe en segments et les indexe
dans une base vectorielle FAISS.

Usage : python ingest.py
"""

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

DOCUMENTS_DIR = "documents"
VECTORSTORE_DIR = "vectorstore"

def load_all_pdfs(directory: str):
    """Charge l'ensemble des fichiers PDF présents dans un répertoire."""
    all_docs = []
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            filepath = os.path.join(directory, filename)
            print(f"[+] Chargement : {filename}")
            loader = PyPDFLoader(filepath)
            docs = loader.load()
            for doc in docs:
                doc.metadata["source_document"] = filename
            all_docs.extend(docs)
    return all_docs

def split_documents(documents, chunk_size=1000, chunk_overlap=200):
    """Découpe les documents en segments avec chevauchement."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " "]
    )
    return splitter.split_documents(documents)

def create_vectorstore(chunks, output_dir):
    """Génère les embeddings et sauvegarde l'index FAISS."""
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(output_dir)
    return vectorstore

if __name__ == "__main__":
    print("=" * 50)
    print("  CyberRAG — Ingestion des documents")
    print("=" * 50)

    documents = load_all_pdfs(DOCUMENTS_DIR)
    print(f"\n[OK] {len(documents)} pages chargées.")

    chunks = split_documents(documents)
    print(f"[OK] {len(chunks)} segments créés.")

    print("[..] Création des embeddings en cours...")
    create_vectorstore(chunks, VECTORSTORE_DIR)
    print(f"[OK] Index sauvegardé dans /{VECTORSTORE_DIR}")

    print("\nIngestion terminée. Lancer l'application :")
    print("  streamlit run app.py")