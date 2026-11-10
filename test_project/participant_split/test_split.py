"""Behavior checks for the participant-level split contract."""

import unittest

from split import split_rows


ROWS = [
    {"sample_id": "A1", "participant_id": "A"},
    {"sample_id": "A2", "participant_id": "A"},
    {"sample_id": "B1", "participant_id": "B"},
    {"sample_id": "B2", "participant_id": "B"},
    {"sample_id": "C1", "participant_id": "C"},
    {"sample_id": "C2", "participant_id": "C"},
    {"sample_id": "D1", "participant_id": "D"},
    {"sample_id": "D2", "participant_id": "D"},
]


class SplitRowsTests(unittest.TestCase):
    def test_participants_do_not_cross_splits_and_rows_are_preserved(self):
        result = split_rows(ROWS, test_fraction=0.25, seed=0)
        train_ids = {row["participant_id"] for row in result["train"]}
        test_ids = {row["participant_id"] for row in result["test"]}
        self.assertFalse(train_ids & test_ids)
        self.assertTrue(result["train"])
        self.assertTrue(result["test"])
        self.assertCountEqual(result["train"] + result["test"], ROWS)

        repeated = ROWS + [dict(ROWS[0])]
        repeated_result = split_rows(repeated, test_fraction=0.25, seed=0)
        self.assertCountEqual(
            repeated_result["train"] + repeated_result["test"], repeated
        )

    def test_blank_participant_id_is_rejected_with_row_position(self):
        bad_rows = ROWS[:2] + [{"sample_id": "bad", "participant_id": "  "}]
        with self.assertRaisesRegex(ValueError, r"row 3"):
            split_rows(bad_rows)

    def test_missing_and_non_string_participant_ids_are_rejected(self):
        invalid_rows = [
            {"sample_id": "bad"},
            {"sample_id": "bad", "participant_id": None},
            {"sample_id": "bad", "participant_id": ""},
            {"sample_id": "bad", "participant_id": 1},
            {"sample_id": "bad", "participant_id": True},
        ]
        for bad_row in invalid_rows:
            with self.subTest(bad_row=bad_row):
                with self.assertRaisesRegex(ValueError, r"row 2"):
                    split_rows([ROWS[0], bad_row])

    def test_assignment_does_not_depend_on_input_order(self):
        left = split_rows(ROWS, test_fraction=0.25, seed=0)
        right = split_rows(list(reversed(ROWS)), test_fraction=0.25, seed=0)
        self.assertEqual(
            {row["participant_id"] for row in left["test"]},
            {row["participant_id"] for row in right["test"]},
        )

    def test_two_participants_stay_on_separate_nonempty_sides(self):
        rows = ROWS[:4]
        for fraction in (0.01, 0.99):
            with self.subTest(fraction=fraction):
                result = split_rows(rows, test_fraction=fraction, seed=0)
                self.assertTrue(result["train"])
                self.assertTrue(result["test"])
                self.assertNotEqual(
                    result["train"][0]["participant_id"],
                    result["test"][0]["participant_id"],
                )


if __name__ == "__main__":
    unittest.main()
