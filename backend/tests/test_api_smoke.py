import unittest

from fastapi.testclient import TestClient

from app.main import app


class ApiSmokeTests(unittest.TestCase):
    def auth_headers(self, client: TestClient) -> dict:
        response = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
        token = response.json()["data"]["access_token"]
        return {"Authorization": f"Bearer {token}"}

    def test_demo_import_and_logs(self):
        client = TestClient(app)
        headers = self.auth_headers(client)

        imported = client.post("/api/import/demo", headers=headers)
        self.assertEqual(imported.status_code, 200)
        self.assertGreaterEqual(imported.json()["data"]["success_count"], 80)

        logs = client.get("/api/import/logs", headers=headers)
        self.assertEqual(logs.status_code, 200)
        self.assertGreater(len(logs.json()["data"]), 0)
        self.assertIn("task_type", logs.json()["data"][0])

    def test_demo_closed_loop(self):
        client = TestClient(app)
        headers = self.auth_headers(client)

        crawl = client.post("/api/crawl/start", json={"platform": "mock", "keyword": "地铁", "limit": 12}, headers=headers)
        self.assertEqual(crawl.status_code, 200)
        self.assertGreater(crawl.json()["data"]["success_count"], 0)

        clean = client.post("/api/clean/run", headers=headers)
        self.assertEqual(clean.status_code, 200)

        sentiment = client.post("/api/sentiment/run", headers=headers)
        self.assertEqual(sentiment.status_code, 200)

        emotions = client.get("/api/emotions")
        self.assertEqual(emotions.status_code, 200)
        self.assertGreater(len(emotions.json()["data"]), 0)

        overview = client.get("/api/statistics/overview")
        self.assertEqual(overview.status_code, 200)
        self.assertGreater(overview.json()["data"]["total_count"], 0)

        hotspots = client.get("/api/hotspots")
        self.assertEqual(hotspots.status_code, 200)
        self.assertGreater(len(hotspots.json()["data"]), 0)

        report = client.get("/api/report")
        self.assertEqual(report.status_code, 200)
        self.assertIn("summary", report.json()["data"])


if __name__ == "__main__":
    unittest.main()
