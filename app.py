from flask import Flask, jsonify, render_template, request
from models import db, User, Project, Task

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///taskflow.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()
    if not User.query.first():
        db.session.add_all([User(name="Bharath", email="bharath@example.com")])
        db.session.commit()

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/api/tasks")
def list_tasks():
    status = request.args.get("status")
    query = Task.query
    if status:
        query = query.filter_by(status=status)
    tasks = query.order_by(Task.id.desc()).all()
    return jsonify([t.to_dict() for t in tasks])

@app.post("/api/tasks")
def create_task():
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    if not title:
        return jsonify({"error": "title is required"}), 400
    task = Task(title=title, description=str(data.get("description", "")).strip(),
                status=data.get("status", "todo"), project_id=data.get("project_id"))
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

@app.patch("/api/tasks/<int:task_id>")
def update_task(task_id):
    task = db.get_or_404(Task, task_id)
    data = request.get_json(silent=True) or {}
    for field in ("title", "description", "status"):
        if field in data:
            value = str(data[field]).strip()
            if field == "title" and not value:
                return jsonify({"error": "title cannot be empty"}), 400
            setattr(task, field, value)
    db.session.commit()
    return jsonify(task.to_dict())

@app.delete("/api/tasks/<int:task_id>")
def delete_task(task_id):
    task = db.get_or_404(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"deleted": task_id})

if __name__ == "__main__":
    app.run(debug=True)
