import chromadb
from sentence_transformers import SentenceTransformer

# load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# create chromadb
client = chromadb.Client()
collection = client.create_collection("nutrition")

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

# convert to embeddings and store
embeddings = model.encode(nutrition_facts).tolist()

collection.add(
    documents=nutrition_facts,
    embeddings=embeddings,
    ids=[f"fact_{i}" for i in range(len(nutrition_facts))]
)

print("Knowledge base created!")

# test search
query = "how does rice affect my energy?"
query_embedding = model.encode([query]).tolist()

results = collection.query(
    query_embeddings=query_embedding,
    n_results=2
)

print("\nMost relevant facts for your query:")
for doc in results['documents'][0]:
    print(f"→ {doc}")