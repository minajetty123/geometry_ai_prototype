"""
index_code.py
Scans your C# geometry source files, splits them into chunks,
embeds them, and stores them in a local ChromaDB vector store.
Run this once (and re-run whenever your source code changes).
"""

import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from config import SOURCE_CODE_DIR, CHROMA_DB_DIR, EMBED_MODEL, CHUNK_SIZE, CHUNK_OVERLAP


def index():
    if not os.path.exists(SOURCE_CODE_DIR):
        os.makedirs(SOURCE_CODE_DIR)
        print(f"Created '{SOURCE_CODE_DIR}' — add your .cs files there, then re-run.")
        return

    print(f"Loading C# files from '{SOURCE_CODE_DIR}' ...")
    loader = DirectoryLoader(
        SOURCE_CODE_DIR,
        glob="**/*.cs",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True,
    )
    docs = loader.load()
    if not docs:
        print("No .cs files found. Add your geometry source files and re-run.")
        return

    print(f"Loaded {len(docs)} file(s). Splitting into chunks ...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\nclass ", "\npublic ", "\nprivate ", "\n\n", "\n", " "],
    )
    chunks = splitter.split_documents(docs)
    print(f"Created {len(chunks)} chunks.")

    print("Embedding and storing in ChromaDB (first run may take a minute) ...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    Chroma.from_documents(
        chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DB_DIR,
        collection_name="geometry_code",
    )
    print(f"Done! Index saved to '{CHROMA_DB_DIR}'.")


if __name__ == "__main__":
    index()
