import json
import unittest
from io import BytesIO

from fastapi.testclient import TestClient

from app.main import app


class AuditBackupTests(unittest.TestCase):
    def auth_headers(self, client: TestClient) -> dict:
        response = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
        token = response.json()["data"]["access_token"]
        return {"Authorization": f"Bearer {token}"}

    def test_protected_operation_writes_audit_log(self):
        client = TestClient(app)
        headers = self.auth_headers(client)

        response = client.post("/api/import/demo", headers=headers)
        self.assertEqual(response.status_code, 200)

        logs = client.get("/api/audit/logs", headers=headers)
        self.assertEqual(logs.status_code, 200)
        rows = logs.json()["data"]
        self.assertGreater(len(rows), 0)
        self.assertEqual(rows[0]["username"], "admin")
        self.assertIn(rows[0]["method"], {"POST", "GET"})

    def test_backup_export_requires_auth_and_returns_json(self):
        client = TestClient(app)

        unauthorized = client.get("/api/backup/export")
        self.assertEqual(unauthorized.status_code, 401)

        response = client.get("/api/backup/export", headers=self.auth_headers(client))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "application/json")
        payload = json.loads(response.content.decode("utf-8"))
        self.assertIn("raw_posts", payload)
        self.assertIn("cleaned_posts", payload)
        self.assertIn("sentiment_results", payload)

    def test_backup_restore_imports_json_backup(self):
        client = TestClient(app)
        headers = self.auth_headers(client)
        export_response = client.get("/api/backup/export", headers=headers)
        self.assertEqual(export_response.status_code, 200)

        restore_response = client.post(
            "/api/backup/restore",
            headers=headers,
            files={"file": ("backup.json", BytesIO(export_response.content), "application/json")},
            data={"replace": "true"},
        )

        self.assertEqual(restore_response.status_code, 200)
        self.assertIn("raw_posts", restore_response.json()["data"])

    def test_audit_logs_support_filters_and_pagination(self):
        client = TestClient(app)
        headers = self.auth_headers(client)
        client.post("/api/import/demo", headers=headers)

        response = client.get("/api/audit/logs?method=POST&path=/api/import&limit=5&offset=0", headers=headers)

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertIn("total", body["meta"])
        self.assertLessEqual(len(body["data"]), 5)
        self.assertTrue(all(row["method"] == "POST" for row in body["data"]))

    def test_import_logs_support_filters_and_pagination(self):
        client = TestClient(app)
        headers = self.auth_headers(client)
        client.post("/api/import/demo", headers=headers)

        response = client.get("/api/import/logs?task_type=import_demo&limit=5&offset=0", headers=headers)

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertIn("total", body["meta"])
        self.assertLessEqual(len(body["data"]), 5)
        self.assertTrue(all(row["task_type"] == "import_demo" for row in body["data"]))


if __name__ == "__main__":
    unittest.main()
