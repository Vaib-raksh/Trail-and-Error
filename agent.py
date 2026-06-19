from groq import Groq

client = Groq(api_key="paste-your-key-here")

conversation = []

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