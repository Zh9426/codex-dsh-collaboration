"""Participant-level train/test split.

All records that share a ``participant_id`` are kept on the same side of the
split.  The assignment is computed from the *set* of participant identifiers
with a fixed seed, so the same records always produce the same assignment no
matter what order the rows arrive in.
"""

from random import Random


def _participant_id(row, row_number):
    """Return the row's participant id, or raise ``ValueError`` when invalid."""
    try:
        participant_id = row["participant_id"]
    except (KeyError, TypeError):
        participant_id = None
    # Only nonempty strings identify a participant.  Rejecting other types
    # (notably 1 and True, which compare and hash alike as dict keys) keeps
    # the grouping and its input-order stability well defined.
    if not isinstance(participant_id, str) or not participant_id.strip():
        raise ValueError(
            f"row {row_number}: participant_id must be a nonempty string"
        )
    return participant_id


def _group_by_participant(rows):
    """Group rows by participant id while validating every record."""
    groups = {}
    for row_number, row in enumerate(rows, start=1):
        participant_id = _participant_id(row, row_number)
        groups.setdefault(participant_id, []).append(row)
    return groups


def _test_participant_count(participant_count, test_fraction):
    """Number of participants to place in the test side."""
    if participant_count == 0:
        return 0
    try:
        fraction = float(test_fraction)
    except (TypeError, ValueError):
        raise ValueError("test_fraction must be a number between 0 and 1") from None
    if fraction <= 0:
        return 0
    if fraction >= 1:
        return participant_count
    if participant_count < 2:
        # A single participant cannot populate both sides.
        return 0
    target = round(participant_count * fraction)
    return min(max(target, 1), participant_count - 1)


def split_rows(rows, test_fraction=0.25, seed=0):
    """Split ``rows`` into train/test without separating a participant's records.

    Returns ``{"train": [...], "test": [...]}`` containing every input row
    exactly once.  When there are at least two participants and
    ``0 < test_fraction < 1`` both sides are non-empty.
    """
    groups = _group_by_participant(rows)
    participants = sorted(groups, key=lambda item: (type(item).__name__, repr(item)))
    Random(seed).shuffle(participants)

    test_count = _test_participant_count(len(participants), test_fraction)
    test_participants = set(participants[:test_count])

    train = []
    test = []
    for participant_id in participants:
        target = test if participant_id in test_participants else train
        target.extend(groups[participant_id])
    return {"train": train, "test": test}
