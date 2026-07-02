from groq import Groq
from dotenv import load_dotenv
from database import get_meals
import os
import chromadb
from sentence_transformers import SentenceTransformer

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# load embedding model and knowledge base
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
chroma_client = chromadb.Client()
collection = chroma_client.create_collection("nutrition")

# nutrition knowledge base
nutrition_facts = [
    "Rice is a high carbohydrate food that provides quick energy. It has a high glycemic index.",
    "Dal is rich in plant-based protein and fiber. It helps in muscle repair and keeps you full longer.",
    "Bananas are rich in potassium and natural sugars. They provide instant energy and help muscle recovery.",
    "Milk is an excellent source of calcium and protein. It supports bone health and muscle growth.",
    "Sabzi (vegetables) provide essential vitamins, minerals and fiber. They support immunity and digestion.",
    "High carb meals cause blood sugar to spike within 30 minutes then drop causing energy crashes.",
    "Protein takes 3-4 hours to digest and provides sustained energy without blood sugar spikes.",
    "Eating fiber with carbs slows down sugar absorption and prevents energy crashes.",
]

embeddings = embedding_model.encode(nutrition_facts).tolist()
collection.add(
    documents=nutrition_facts,
    embeddings=embeddings,
    ids=[f"fact_{i}" for i in range(len(nutrition_facts))]
)

def retrieve_nutrition_facts(question, n=2):
    query_embedding = embedding_model.encode([question]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n
    )
    return results['documents'][0]

def build_system_prompt(user_id, question):
    # get personal meal history
    meals = get_meals(user_id)
    if not meals:
        meal_history = "No meals logged yet."
    else:
        meal_history = "\n".join([f"- {m[0]} at {m[1]}" for m in meals])

    # retrieve relevant nutrition science
    relevant_facts = retrieve_nutrition_facts(question)
    nutrition_context = "\n".join([f"- {fact}" for fact in relevant_facts])

    return f"""You are AaharWise, a personal AI nutrition assistant who analyses meal inputs and predicts how they will affect the user's health with a biological timeline.

User's meal history:
{meal_history}

Relevant nutrition science:
{nutrition_context}

Use both the user's personal data AND the nutrition science to give specific, accurate answers.
Give a biological timeline of how foods are affecting their body.
Be encouraging but honest. Keep it conversational."""

def chat(user_id, question):
    system_prompt = build_system_prompt(user_id, question)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    user_id = 1
    print("AaharWise RAG is ready!\n")

    while True:
        question = input("You: ")
        if question == "exit":
            break
        response = chat(user_id, question)
        print(f"AaharWise: {response}\n")