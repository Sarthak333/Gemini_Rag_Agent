from dotenv import load_dotenv
load_dotenv()

import os
from google import genai
import numpy as np

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

with open("Documents/Companypolicy.txt", "r") as f:
    content = f.read()

chunks = content.split("\n\n")

chunk_data = []
for chunk in chunks:
    result = client.models.embed_content(model="gemini-embedding-001", contents=chunk)
    embedding = result.embeddings[0].values
    chunk_data.append({"text": chunk, "embedding": embedding})

print("Knowledge base ready!\n")

# --- NEW PART: search ---
def find_best_chunk(question):
    question_embedding = client.models.embed_content(
        model="gemini-embedding-001",
        contents=question
    ).embeddings[0].values

    best_score = -1
    best_chunk = None

    for item in chunk_data:
        # Cosine similarity: measures how "close" two number-lists are
        score = np.dot(question_embedding, item["embedding"])
        if score > best_score:
            best_score = score
            best_chunk = item["text"]

    return best_chunk, best_score

question = input("Ask a question about the policy: ")
best_chunk, score = find_best_chunk(question)


final_prompt = f"""Answer the user's question using ONLY the information below.

Information:
{best_chunk}

Question: {question}

Answer:"""

response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents=final_prompt
)

print("\nAgent's answer:")
print(response.text)