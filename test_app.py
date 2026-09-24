"""
Self-verification test suite for Linux Command Simulator
"""

import unittest
from app import app
from data.commands_data import CHAPTERS, get_summary_stats

class TestLinuxSimulator(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_chapter_and_command_count(self):
        """Verify exactly 26 chapters and 260 curated commands exist."""
        self.assertEqual(len(CHAPTERS), 26, "Should have exactly 26 chapters")
        for ch in CHAPTERS:
            self.assertEqual(len(ch["commands"]), 10, f"Chapter {ch['chapter_id']} should have 10 commands")
        
        stats = get_summary_stats()
        self.assertEqual(stats["total_commands"], 260)
        self.assertEqual(stats["total_chapters"], 26)

    def test_index_route(self):
        """Verify index route renders HTML successfully."""
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Linux Command Simulator", response.data)
        self.assertIn(b"RHCSA 9", response.data)

    def test_curriculum_api(self):
        """Verify /api/curriculum returns all chapters."""
        response = self.app.get("/api/curriculum")
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data["status"], "success")
        self.assertEqual(len(json_data["data"]), 26)

    def test_all_chapter_endpoints(self):
        """Verify each of the 26 chapter endpoints returns valid data."""
        for cid in range(1, 27):
            response = self.app.get(f"/api/chapters/{cid}")
            self.assertEqual(response.status_code, 200, f"Chapter {cid} failed to load")
            data = response.get_json()["data"]
            self.assertEqual(data["chapter_id"], cid)
            self.assertEqual(len(data["commands"]), 10)

    def test_search_api(self):
        """Verify search finds relevant commands."""
        response = self.app.get("/api/search?q=systemctl")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreater(data["count"], 0)

    def test_simulation_engine(self):
        """Verify simulation execution of commands."""
        test_commands = [
            "hostnamectl status",
            "pwd",
            "echo 'hello linux'",
            "systemctl status sshd",
            "nonexistentcommand12345"
        ]
        for cmd in test_commands:
            response = self.app.post("/api/simulate", json={"command": cmd})
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data["status"], "success")
            self.assertIn("result", data)

if __name__ == "__main__":
    unittest.main()
