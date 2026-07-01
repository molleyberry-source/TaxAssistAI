from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer
import chromadb
import os

load_dotenv()

openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

model = SentenceTransformer("all-MiniLM-L6-v2")

chroma_client = chromadb.PersistentClient(path="chroma_db")

collection = chroma_client.get_or_create_collection(
    name="iras_tax_knowledge"
)


def ask_taxassist(question):
    question_embedding = model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=3
    )

    context = ""

    for doc in results["documents"][0]:
        context += doc + "\n\n"

    prompt = f"""
You are TaxAssist AI, an assistant for Singapore Individual Income Tax.

Answer the user's question using only the IRAS context below.
If the answer is not found in the context, say that the information is not available in the retrieved IRAS documents.

Rules:
- Provide the direct answer first.
- Include only information that is directly relevant to the user's question.
- Do not include unrelated tax reliefs, deductions, rebates, or other topics.
- If additional information is helpful, keep it brief and directly related.
- If the answer cannot be found in the retrieved IRAS context, say that the information is not available in the retrieved IRAS documents.

Question:
{question}

IRAS Context:
{context}

Answer:
"""

    response = openai_client.responses.create(
        model="gpt-5-nano",
        input=prompt
    )

    return response.output_text


if __name__ == "__main__":
    test_question = "What happens if I do not pay my income tax by the due date?"

    answer = ask_taxassist(test_question)

    print("\nQuestion:")
    print(test_question)

    print("\nTaxAssist AI Answer:")
    print(answer)