import os
import tempfile
import unittest

from app import app
from models import db, Task


class TaskApiTests(unittest.TestCase):
    def setUp(self):
        self.path = tempfile.mktemp(suffix=".db")
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + self.path
        self.client = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_create_and_list(self):
        response = self.client.post("/api/tasks", json={"title": "Write tests", "description": "API coverage"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.client.get("/api/tasks").json[0]["title"], "Write tests")

    def test_reject_empty_title(self):
        self.assertEqual(self.client.post("/api/tasks", json={"title": ""}).status_code, 400)

    def test_update_status(self):
        created = self.client.post("/api/tasks", json={"title": "Ship feature"}).json
        response = self.client.patch(f"/api/tasks/{created['id']}", json={"status": "done"})
        self.assertEqual(response.json["status"], "done")

    def test_delete(self):
        created = self.client.post("/api/tasks", json={"title": "Remove me"}).json
        self.client.delete(f"/api/tasks/{created['id']}")
        with app.app_context():
            self.assertIsNone(db.session.get(Task, created["id"]))


if __name__ == "__main__":
    unittest.main()
