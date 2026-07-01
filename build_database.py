from docx import Document
from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb

documents_folder = Path("documents")
chunk_size = 10

model = SentenceTransformer("all-MiniLM-L6-v2")

all_chunks = []

# Read all Word documents
for file_path in documents_folder.glob("*.docx"):

    if file_path.name.startswith("~$"):
        continue

    doc = Document(file_path)

    paragraphs = []

    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    for i in range(0, len(paragraphs), chunk_size):

        chunk_text = "\n".join(paragraphs[i:i + chunk_size])

        all_chunks.append({
            "source": file_path.name,
            "chunk": chunk_text
        })

    print(f"{file_path.name}: {len(paragraphs)} paragraphs")

print(f"\nTotal chunks: {len(all_chunks)}")

print("Creating embeddings...")

for chunk in all_chunks:
    chunk["embedding"] = model.encode(chunk["chunk"])

print("Embeddings complete.")

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="iras_tax_knowledge"
)

# Optional: remove old data before rebuilding
try:
    collection.delete(ids=collection.get()["ids"])
except:
    pass

ids = []
documents = []
metadatas = []
embeddings = []

for i, chunk in enumerate(all_chunks):

    ids.append(f"chunk_{i}")
    documents.append(chunk["chunk"])
    metadatas.append({"source": chunk["source"]})
    embeddings.append(chunk["embedding"].tolist())

collection.add(
    ids=ids,
    documents=documents,
    metadatas=metadatas,
    embeddings=embeddings
)

print(f"\nDatabase built successfully!")
print(f"Total chunks stored: {collection.count()}")