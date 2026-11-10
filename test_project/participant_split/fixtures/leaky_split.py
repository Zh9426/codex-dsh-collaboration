"""Intentionally incorrect row-level split for replaying the workflow test."""

from random import Random


def split_rows(rows, test_fraction=0.25, seed=0):
    shuffled = list(rows)
    Random(seed).shuffle(shuffled)
    test_count = max(1, round(len(shuffled) * test_fraction))
    return {"train": shuffled[test_count:], "test": shuffled[:test_count]}
