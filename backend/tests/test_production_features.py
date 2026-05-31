import unittest

from fastapi.testclient import TestClient

from app.main import app


class ProductionFeatureTests(unittest.TestCase):
    def test_task_endpoints_require_auth_and_accept_login_token(self):
        client = TestClient(app)

        unauthorized = client.post("/api/clean/run")
        self.assertEqual(unauthorized.status_code, 401)

        login = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
        self.assertEqual(login.status_code, 200)
        token = login.json()["data"]["access_token"]

        authorized = client.post("/api/clean/run", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(authorized.status_code, 200)

    def test_report_exports_pdf_and_docx(self):
        client = TestClient(app)
        login = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
        token = login.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        pdf = client.get("/api/report/export?format=pdf", headers=headers)
        self.assertEqual(pdf.status_code, 200)
        self.assertEqual(pdf.headers["content-type"], "application/pdf")
        self.assertTrue(pdf.content.startswith(b"%PDF"))

        docx = client.get("/api/report/export?format=docx", headers=headers)
        self.assertEqual(docx.status_code, 200)
        self.assertIn("application/vnd.openxmlformats-officedocument.wordprocessingml.document", docx.headers["content-type"])
        self.assertTrue(docx.content.startswith(b"PK"))


if __name__ == "__main__":
    unittest.main()
