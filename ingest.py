from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document
import fitz
import re
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import time

load_dotenv()

def clean_pdf(file_path):
    doc = fitz.open(file_path)
    teks_bersih = ""

    for page in doc:
        rect = page.rect
        clip_area = fitz.Rect(rect.x0, rect.y0 + (rect.height * 0.1), 
                              rect.x1, rect.y1 - (rect.height * 0.1))
        teks = page.get_text("text", clip=clip_area)
        teks = re.sub(r'(?<!\n)\n(?!\n)', ' ', teks)
        teks_bersih += teks + "\n\n"

    return teks_bersih

teks_dokumen_1 = clean_pdf("data/Dasar-Teknik-Jaringan-Komputer-dan-Telekomunikasi-BS-KLS-X.pdf")
teks_dokumen_2 = clean_pdf("data/Informatika-Kelas-X-SMK.pdf")
teks_dokumen_3 = clean_pdf("data/Modul Praktikum Jaringan Komputer.pdf")


def load_cleaned_documents():
    documents = [
        Document(page_content=teks_dokumen_1, metadata={"source": "data/Dasar-Teknik-Jaringan-Komputer-dan-Telekomunikasi-BS-KLS-X.pdf"}),
        Document(page_content=teks_dokumen_2, metadata={"source": "data/Informatika-Kelas-X-SMK.pdf"}),
        Document(page_content=teks_dokumen_3, metadata={"source": "data/Modul Praktikum Jaringan Komputer.pdf"})
    ]
    
    for i, doc in enumerate(documents):
        print(f'\nDocument {i+1}:')
        print(f'Source: {doc.metadata["source"]}')
        print(f'Content Length: {len(doc.page_content)} characters')
        print(f'Content Priview: {doc.page_content[:100]}...')    
        print(f'Metadata: {doc.metadata}')

    return documents

documents = load_cleaned_documents()

def chungking(documents, chunk_size=1000, chunk_overlap=150):
    print("Splitting documents into chunk")

    text_splitter = CharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks= text_splitter.split_documents(documents)

    if chunks:
        for i, c in enumerate(chunks[:5]):
            print(f'\nChunk {i+1}:')
            print(f"Source: {c.metadata['source']}")
            print(f"length: {len(c.page_content)} characters")
            print(f'Content: ')
            print("-"*50)

        if len(chunks)>5:
            print(f'\n... and {len(chunks)-5 } more chunks')
    
    return chunks

def create_db_vector(chunks, persist_directory="db/chroma/db"):
    print("Creating embedding and storing in chromaDB")
    
    embedding_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

    batch_size = 50
    vectorstore = None

    print("Creating vector store")
    for i in range(0, len(chunks), batch_size):
        batch_chunks = chunks[i:i+batch_size]
        print(f"Processing batch {i//batch_size+1}/{(len(chunks)//batch_size)+1}")
        
        if vectorstore is None:
            vectorstore = Chroma.from_documents(
                documents=batch_chunks,
                embedding=embedding_model,
                persist_directory=persist_directory,
                collection_metadata={"hnsw:space": "cosine"}
            )
        else:
            vectorstore.add_documents(batch_chunks)
        
        if i+batch_size < len(chunks):
            print("Waiting 60s for rate limit...")
            time.sleep(60)
    
    print(f"Vector store created and save to {persist_directory}")

    return vectorstore

def main():
    # baca dokumen
    document = load_cleaned_documents()

    # chunking
    chunks = chungking(document)

    # vector db
    vectorstore = create_db_vector(chunks)


if __name__ == "__main__":
    main()