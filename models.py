from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    tasks = db.relationship("Task", backref="assignee", lazy=True)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    tasks = db.relationship("Task", backref="project", lazy=True, cascade="all, delete-orphan")


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default="")
    status = db.Column(db.String(30), nullable=False, default="todo")
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=True)
    assignee_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    def to_dict(self):
        return {"id": self.id, "title": self.title, "description": self.description,
                "status": self.status, "project_id": self.project_id, "assignee_id": self.assignee_id}
