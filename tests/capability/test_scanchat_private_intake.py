import hashlib
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from scanchat_private_intake import convert, IntakeError

def fixture():
    files = {"manifest.json": json.dumps({"schema_version": "scanchat-archive/1.1"}).encode(),
             "conversation.json": json.dumps({"schema_version": "scanchat-conversation/1.1",
               "messages": [{"message_key": "m1", "role": "user", "text": "Czesc", "attachments": []}]}).encode()}
    return seal(files)

def seal(files):
    out = {k: v for k,v in files.items() if k != "checksums.sha256"}
    out["checksums.sha256"] = "".join(hashlib.sha256(value).hexdigest() + "  " + key + "\n" for key, value in out.items()).encode()
    return out

class TestPrivateIntake(unittest.TestCase):
    def test_valid(self):
        result = convert(fixture())
        self.assertEqual(result["conversation_count"], 1)
        self.assertEqual(result["archive_integrity"], "SHA256_MANIFEST_VERIFIED")
        self.assertEqual(result["global_completeness"], "NOT_PROVEN")
        self.assertFalse(result["ai_analysis_performed"])
    def test_tampering(self):
        files = fixture()
        files["conversation.json"] += b" "
        with self.assertRaisesRegex(IntakeError, "checksum mismatch"):
            convert(files)
    def test_unlisted_payload(self):
        files = fixture()
        files["not-covered.txt"] = b"payload"
        with self.assertRaisesRegex(IntakeError, "inventory mismatch"):
            convert(files)
    def test_duplicate_message(self):
        files = fixture()
        chat = json.loads(files["conversation.json"])
        chat["messages"] *= 2
        files["conversation.json"] = json.dumps(chat).encode()
        with self.assertRaisesRegex(IntakeError, "duplicate"):
            convert(seal(files))
    def test_missing_text(self):
        files = fixture()
        chat = json.loads(files["conversation.json"])
        del chat["messages"][0]["text"]
        files["conversation.json"] = json.dumps(chat).encode()
        with self.assertRaisesRegex(IntakeError, "invalid role"):
            convert(seal(files))
    def test_project_archive(self):
        files = fixture()
        files["manifest.json"] = json.dumps({"schema_version": "scanchat-project-archive/1.2"}).encode()
        files["chat-a/conversation.json"] = files.pop("conversation.json")
        files["chat-b/conversation.json"] = files["chat-a/conversation.json"]
        self.assertEqual(convert(seal(files))["conversation_count"], 2)
    def test_duplicate_json_fields(self):
        files = fixture()
        files["manifest.json"] = b'{"schema_version":"scanchat-archive/1.1","schema_version":"scanchat-archive/1.1"}'
        with self.assertRaisesRegex(IntakeError, "duplicate JSON key"):
            convert(seal(files))

if __name__ == "__main__":
    unittest.main()
