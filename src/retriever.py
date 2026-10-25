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

query = ('Tolong tuliskan format rumus VLOOKUP untuk mencari data nilai siswa berdasarkan panduan Excel di dalam buku ini!')

retriever = db.as_retriever(search_kwargs={"k": 3})

relevance_docs = retriever.invoke(query)

print(f'User query: {query}')
for i, doc in enumerate(relevance_docs, 1):
    print(f'Documents {i}:\n({doc.page_content}\n)')

# retriever = db.as_retriever(
#     search_type="similarity_score_threshold",
#     search_kwargs={
#         "k":5,
#         "score_threshold":0.3

#     }
# ) menembalikan chunks dengan cosine similarity 0.3

# Apa itu LAN?
# Apa itu topologi jaringan? Jelaskan dan sebutkan jenis nya.
# Bagaimana konsep dasar DNS itu bekerja?
# Bagaimana konsep dasar VLAN itu bekerja?
# Bagaimana cara melakukan perhitungan subnetting dalam jaringan?
# Apa yang dimaksud Problem Solving?
# Bagaimana cara kerja jaringan lokal?
# Bagaimana cara mengamankan jaringan lokal?
    
