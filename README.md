# TaskFlow — Team Task Management Web App

A full-stack task tracking application built with Flask, SQLite, SQLAlchemy, HTML, CSS and JavaScript.

## Features
- RESTful CRUD endpoints for tasks
- User, project and task OOP models
- Status filtering and inline status updates
- SQLite persistence through SQLAlchemy
- Input validation and API error handling
- Automated tests for core CRUD flows

## Run
```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
```
Open `http://127.0.0.1:5000`.

## Test
```bash
python -m unittest discover -s tests
```
