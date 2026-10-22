import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

def load_document(docs_path="data"):
    print(f"Loading documents from{docs_path}...")

    if not os.path.exists(docs_path):
        raise FileNotFoundError(f'The directory {docs_path} does not exists. Please create it and add your company files.')

    loader = DirectoryLoader(path=docs_path, glob="*.pdf", loader_cls=PyPDFLoader)

    documents = loader.load()

    if len(documents) == 0:
        raise FileNotFoundError(f'No documents found in {docs_path}. Please add your company documents')
    
    for i, doc in enumerate(documents):
        print(f'\nDocument {i+1}:')
        print(f'Source: {doc.metadata["source"]}')
        print(f'Content Length: {len(doc.page_content)} characters')
        print(f'Content Priview: {doc.page_content[:100]}...')    
        print(f'Metadata: {doc.metadata}')

    return documents

def main():
    pass


if __name__ == "__main__":
    main()