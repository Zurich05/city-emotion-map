import unittest
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


class UsersRbacTests(unittest.TestCase):
    def admin_headers(self, client: TestClient) -> dict:
        login = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
        self.assertEqual(login.status_code, 200)
        return {"Authorization": f"Bearer {login.json()['data']['access_token']}"}

    def test_admin_can_create_user_and_user_can_login(self):
        client = TestClient(app)
        headers = self.admin_headers(client)
        username = f"analyst_{uuid4().hex[:8]}"

        created = client.post(
            "/api/users",
            headers=headers,
            json={"username": username, "password": "safePass123", "role": "analyst"},
        )

        self.assertEqual(created.status_code, 200)
        self.assertEqual(created.json()["data"]["username"], username)
        self.assertEqual(created.json()["data"]["role"], "analyst")

        login = client.post("/api/auth/login", json={"username": username, "password": "safePass123"})
        self.assertEqual(login.status_code, 200)

    def test_non_admin_cannot_create_user(self):
        client = TestClient(app)
        admin_headers = self.admin_headers(client)
        viewer_username = f"viewer_{uuid4().hex[:8]}"
        blocked_username = f"blocked_{uuid4().hex[:8]}"
        client.post(
            "/api/users",
            headers=admin_headers,
            json={"username": viewer_username, "password": "safePass123", "role": "viewer"},
        )
        viewer_login = client.post("/api/auth/login", json={"username": viewer_username, "password": "safePass123"})
        viewer_headers = {"Authorization": f"Bearer {viewer_login.json()['data']['access_token']}"}

        denied = client.post(
            "/api/users",
            headers=viewer_headers,
            json={"username": blocked_username, "password": "safePass123", "role": "viewer"},
        )

        self.assertEqual(denied.status_code, 403)


if __name__ == "__main__":
    unittest.main()
