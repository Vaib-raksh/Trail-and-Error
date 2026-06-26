import gradio as gr
from aaharwise import chat
from database import add_user, add_meal
from datetime import datetime

# default user for now
USER_ID = 1

def ask_aaharwise(question):
    if not question.strip():
        return "Please ask me something about your nutrition!"
    response = chat(USER_ID, question)
    return response

def log_meal(food):
    if not food.strip():
        return "Please enter what you ate!"
    time = datetime.now().strftime("%Y-%m-%d %H:%M")
    add_meal(USER_ID, food, time)
    return f"✅ Logged: {food} at {time}"

with gr.Blocks(title="AaharWise") as app:
    gr.Markdown("# 🌿 AaharWise")
    gr.Markdown("*Your personal AI nutrition assistant*")
    
    with gr.Tab("Chat"):
        chatbox = gr.Textbox(label="Ask AaharWise", placeholder="How is my diet affecting my energy levels?")
        ask_btn = gr.Button("Ask", variant="primary")
        response = gr.Textbox(label="AaharWise says", interactive=False)
        ask_btn.click(fn=ask_aaharwise, inputs=chatbox, outputs=response)
    
    with gr.Tab("Log Meal"):
        meal_input = gr.Textbox(label="What did you eat?", placeholder="rice, dal, sabzi")
        log_btn = gr.Button("Log Meal", variant="primary")
        log_status = gr.Textbox(label="Status", interactive=False)
        log_btn.click(fn=log_meal, inputs=meal_input, outputs=log_status)

app.launch()