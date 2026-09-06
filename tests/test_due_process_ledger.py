from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from dikwp_verityweave.due_process import REQUIRED_CORRECTION_RECEIPTS, add_correction_receipt, get_appeal, open_appeal
from dikwp_verityweave.ledger import append_event, verify_ledger


class DueProcessAndLedgerTests(unittest.TestCase):
    def test_five_receipts_close_correction(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "appeals.json"
            appeal = open_appeal(store, "decision-1", "creator", "The context was omitted")
            self.assertTrue(appeal["consequential_use_blocked"])
            for receipt in sorted(REQUIRED_CORRECTION_RECEIPTS):
                current = add_correction_receipt(store, appeal["appeal_id"], receipt, "recorded evidence")
            self.assertEqual(current["status"], "CORRECTION_CLOSED")
            self.assertFalse(current["consequential_use_blocked"])
            self.assertEqual(get_appeal(store, appeal["appeal_id"])["missing_receipts"], [])

    def test_partial_correction_remains_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "appeals.json"
            appeal = open_appeal(store, "decision-2", "user", "Wrong attribution")
            current = add_correction_receipt(store, appeal["appeal_id"], "CORRECT_ORIGINAL_RECORD", "corrected")
            self.assertEqual(current["status"], "CORRECTION_IN_PROGRESS")
            self.assertTrue(current["consequential_use_blocked"])

    def test_unknown_receipt_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "appeals.json"
            appeal = open_appeal(store, "decision-3", "user", "error")
            with self.assertRaises(ValueError):
                add_correction_receipt(store, appeal["appeal_id"], "DELETE_EVERYTHING", "x")

    def test_ledger_detects_tampering(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.jsonl"
            append_event(path, "A", {"value": 1})
            append_event(path, "B", {"value": 2})
            self.assertTrue(verify_ledger(path)["valid"])
            lines = path.read_text().splitlines()
            item = json.loads(lines[0])
            item["payload"]["value"] = 9
            lines[0] = json.dumps(item)
            path.write_text("\n".join(lines) + "\n")
            self.assertFalse(verify_ledger(path)["valid"])

    def test_missing_ledger_is_valid_empty_chain(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = verify_ledger(Path(tmp) / "missing.jsonl")
            self.assertTrue(result["valid"])
            self.assertEqual(result["events"], 0)


if __name__ == "__main__":
    unittest.main()
