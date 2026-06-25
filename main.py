from fastapi import FastAPI
from database import add_user, add_meal, get_meals

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AaharWise API is running"}

@app.post("/user")
def create_user(name: str, age: int):
    user_id = add_user(name, age)
    return {"user_id": user_id, "message": f"User {name} created"}

@app.post("/meal")
def log_meal(user_id: int, food: str, time: str):
    add_meal(user_id, food, time)
    return {"message": "Meal logged successfully"}

@app.get("/meals/{user_id}")
def fetch_meals(user_id: int):
    meals = get_meals(user_id)
    return {"meals": [{"food": m[0], "time": m[1], "user": m[2]} for m in meals]}