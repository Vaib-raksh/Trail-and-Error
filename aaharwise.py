from groq import Groq 
from dotenv import load_dotenv
from database import get_meals 
import os 

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def build_system_prompt(user_id):
    meals = get_meals(user_id)

    if not meals:
        meal_history ="No meals logged yet."
    else:
        meal_history = "\n".join([f"- {m[0]} at {m[1]}" for m in meals])

    return f"""You are AaharWise, a personal AI nutrition assistant who analyses meal inputs and predicts how they will affect the user's health with a biological timeline.

    Here is the user's complete meal history:
    {meal_history}

    For each analysis:
    - Reference their actual meals specifically
    - Give a biological timeline of how those foods are affecting their body (30 mins, 2 hours, next morning etc.)
    - Be encouraging but honest about nutritional gaps
    - Keep it conversational, not clinical"""

def chat(user_id, question):
    system_prompt = build_system_prompt(user_id)

    response = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages =[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}

        ]
    )
    return response.choices[0].message.content

# testing the chat function 
if __name__ == "__main__":
    user_id = 1
    print("AaharWise is ready! Ask me anything about your nutrition.\n")
    
    while True:
        question = input("You: ")
        if question == "exit":
            break
        response = chat(user_id, question)
        print(f"AaharWise: {response}\n")