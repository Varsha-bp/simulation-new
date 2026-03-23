import json
import unittest
from datetime import datetime, timezone


# ------------------------------------------------------------------
# IMPLEMENT: convertFromFormat1
# Format 1 uses an ISO 8601 timestamp string (e.g. "2021-05-21T00:00:00.000Z")
# The unified format requires milliseconds since epoch (integer).
# ------------------------------------------------------------------
def convertFromFormat1(jsonObject):
    # Copy the object so we don't mutate the original
    result = json.loads(json.dumps(jsonObject))

    # Convert ISO timestamp string → milliseconds since epoch
    iso_timestamp = result["timestamp"]
    # Parse the ISO string; replace 'Z' with '+00:00' for Python compatibility
    dt = datetime.fromisoformat(iso_timestamp.replace("Z", "+00:00"))
    result["timestamp"] = int(dt.timestamp() * 1000)

    return result


# ------------------------------------------------------------------
# IMPLEMENT: convertFromFormat2
# Format 2 already uses milliseconds since epoch (integer).
# No timestamp conversion needed — just return a clean copy.
# ------------------------------------------------------------------
def convertFromFormat2(jsonObject):
    # Timestamp is already in milliseconds since epoch; return a copy as-is
    result = json.loads(json.dumps(jsonObject))
    return result


# ------------------------------------------------------------------
# Unit Tests
# ------------------------------------------------------------------
class TestConversions(unittest.TestCase):

    def setUp(self):
        with open("data-1.json") as f:
            self.data1 = json.load(f)
        with open("data-2.json") as f:
            self.data2 = json.load(f)
        with open("data-result.json") as f:
            self.expected = json.load(f)

    def test_convertFromFormat1(self):
        result = convertFromFormat1(self.data1)
        self.assertEqual(result, self.expected,
                         "Format 1 conversion did not match expected result")

    def test_convertFromFormat2(self):
        result = convertFromFormat2(self.data2)
        self.assertEqual(result, self.expected,
                         "Format 2 conversion did not match expected result")

    def test_format1_timestamp_is_int(self):
        result = convertFromFormat1(self.data1)
        self.assertIsInstance(result["timestamp"], int,
                              "Timestamp should be an integer (ms since epoch)")

    def test_format2_timestamp_unchanged(self):
        result = convertFromFormat2(self.data2)
        self.assertEqual(result["timestamp"], self.data2["timestamp"],
                         "Format 2 timestamp should remain unchanged")

    def test_format1_does_not_mutate_input(self):
        original_ts = self.data1["timestamp"]
        convertFromFormat1(self.data1)
        self.assertEqual(self.data1["timestamp"], original_ts,
                         "convertFromFormat1 should not mutate the input object")

    def test_both_produce_same_output(self):
        result1 = convertFromFormat1(self.data1)
        result2 = convertFromFormat2(self.data2)
        self.assertEqual(result1, result2,
                         "Both converters should produce identical output")


if __name__ == "__main__":
    unittest.main(verbosity=2)
