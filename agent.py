from groq import Groq
import os 
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

conversation = [
    {"role": "system", "content": "You are a grumpy pirate who only talks about treasure and the sea. Refuse to discuss anything else, and stay in character."}
]

def ask_ai(question):
    conversation.append({"role": "user", "content": question})
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=conversation
    )
    
    answer = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": answer})
    return answer

while True:
    question = input("You: ")
    if question == "exit":
        break
    result = ask_ai(question)
    print("AI:", result)