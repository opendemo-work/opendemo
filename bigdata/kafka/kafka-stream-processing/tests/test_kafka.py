import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "code"))

from producer import create_event


class TestProducer(unittest.TestCase):
    def test_create_event_structure(self):
        event = create_event(1)
        self.assertIn("user_id", event)
        self.assertIn("event_type", event)
        self.assertIn("page", event)
        self.assertIn("timestamp", event)
        self.assertIn("value", event)
        self.assertEqual(event["user_id"], "user_0001")

    def test_create_event_value_range(self):
        event = create_event(42)
        self.assertGreaterEqual(event["value"], 0)
        self.assertLessEqual(event["value"], 100)

    def test_create_event_is_json_serializable(self):
        event = create_event(1)
        try:
            json.dumps(event)
        except Exception as e:
            self.fail(f"event 无法序列化为 JSON: {e}")


class TestConsumer(unittest.TestCase):
    def test_deserialization(self):
        payload = json.dumps({"event_type": "click", "user_id": "user_0001"}).encode("utf-8")
        decoded = json.loads(payload.decode("utf-8"))
        self.assertEqual(decoded["event_type"], "click")


if __name__ == "__main__":
    unittest.main()
