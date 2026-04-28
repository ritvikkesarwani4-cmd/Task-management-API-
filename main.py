from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from passlib.context import CryptContext

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ----------- DB FUNCTION -----------

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="rootsql",
        database="taskbot"
    )

# ----------- MODELS -----------

class User(BaseModel):
    username: str
    password: str

class Task(BaseModel):
    user_id: int
    title: str

# ----------- SIGNUP -----------

@app.post("/signup")
def signup(user: User):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT id FROM user WHERE username=%s", (user.username,))
    if cursor.fetchone():
        cursor.close()
        db.close()
        return {"message": "Username already exists"}

    hashed = pwd_context.hash(user.password)

    cursor.execute(
        "INSERT INTO user (username, password) VALUES (%s, %s)",
        (user.username, hashed)
    )
    db.commit()

    cursor.close()
    db.close()

    return {"message": "User created"}

# ----------- LOGIN -----------

@app.post("/login")
def login(user: User):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT id, password FROM user WHERE username=%s", (user.username,))
    row = cursor.fetchone()

    cursor.close()
    db.close()

    if row and pwd_context.verify(user.password, row[1]):
        return {
            "message": "Login successful",
            "user_id": row[0]
        }

    return {"message": "Invalid credentials"}

# ----------- ADD TASK -----------

@app.post("/addtask")
def add_task(task: Task):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO tasks (user_id, title, status) VALUES (%s, %s, %s)",
        (task.user_id, task.title, "pending")
    )
    db.commit()

    cursor.close()
    db.close()

    return {"message": "Task added"}

# ----------- GET TASKS -----------

@app.get("/tasks/{user_id}")
def get_tasks(user_id: int):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT id, title, status, created_at, complete_at FROM tasks WHERE user_id=%s",
        (user_id,)
    )
    rows = cursor.fetchall()

    tasks = []
    for t in rows:
        tasks.append({
            "task_id": t[0],
            "title": t[1],
            "status": t[2],
            "created_at": t[3],
            "complete_at": t[4]
        })

    cursor.close()
    db.close()

    if not tasks:
        return {"message": "No tasks found"}

    return {"tasks": tasks}

# ----------- COMPLETE TASK -----------

@app.put("/tasks/{task_id}/complete")
def complete_task(task_id: int):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "UPDATE tasks SET status=%s, complete_at=CURRENT_TIMESTAMP WHERE id=%s",
        ("done", task_id)
    )

    if cursor.rowcount == 0:
        cursor.close()
        db.close()
        return {"message": "Task not found"}

    db.commit()

    cursor.execute(
        "SELECT complete_at FROM tasks WHERE id=%s",
        (task_id,)
    )
    completed_at = cursor.fetchone()[0]

    cursor.close()
    db.close()

    return {
        "message": "Task completed",
        "completed_at": completed_at
    }