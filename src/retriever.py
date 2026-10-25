from sqlalchemy.orm import persistence
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

persistence_directory = ("./db/chroma/db")

embed_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

db = Chroma(
    persist_directory=persistence_directory,
    embedding_function=embed_model,
    collection_metadata={"hnsw:space": "cosine"}
)

query = ('Jelaskan prinsip kerja layanan DHCP dengan jelas dan lengkap.')

retriever = db.as_retriever(search_kwargs={"k": 4})

# Apa itu LAN?
# Apa itu topologi jaringan? Jelaskan dan sebutkan jenis nya.
# Bagaimana konsep dasar DNS itu bekerja?
# Bagaimana konsep dasar VLAN itu bekerja?
# Bagaimana cara melakukan perhitungan subnetting dalam jaringan?
# Apa yang dimaksud Problem Solving?
# Bagaimana cara kerja jaringan lokal?
# Bagaimana cara mengamankan jaringan lokal?
    
