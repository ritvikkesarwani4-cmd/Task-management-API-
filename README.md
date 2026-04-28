# Task Management API

A simple backend API to manage users and tasks with authentication.

## Features
- User signup & login
- Password hashing (bcrypt)
- Add tasks
- View tasks
- Mark task as completed

## Tech Stack
- FastAPI
- MySQL
- Python

## Project Structure
- main.py → API logic
- requirements.txt → dependencies

## Setup Instructions

1. Clone repo
git clone https://github.com/your-username/task-management-api.git

2. Go to folder
cd task-management-api

3. Create virtual environment
python -m venv venv

4. Activate venv
venv\Scripts\activate   (Windows)

5. Install dependencies
pip install -r requirements.txt

6. Run server
uvicorn main:app --reload

7. Open docs
http://127.0.0.1:8000/docs

## Database Setup

Create MySQL database:
- database name: taskbot

Tables:

User table:
- id (int, primary key, auto increment)
- username (varchar)
- password (varchar)

Tasks table:
- id (int, primary key)
- user_id (int)
- title (text)
- status (varchar)
- created_at (timestamp)
- complete_at (timestamp)

## API Endpoints

POST /signup  
POST /login  
POST /addtask  
GET /tasks/{user_id}  
PUT /tasks/{task_id}/complete  

## Future Improvements
- Add JWT authentication
- Add frontend UI
- Add task editing & delete