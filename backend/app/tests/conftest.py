"""Fixtures for the ceiling-height ladder monotonicity package.

Assertions live in test_height_ladder.py; conversions and failure messages
live in height_ladder_support.py. The two combos mirror the clean seed rows
in app/seed.py: 主卧一圈+素色53 and 大花匹配+大花64 (its seeded match roll).
"""

import pytest

from height_ladder_support import RAISED_HEIGHT_STEPS, Combo, rolls_at_height

# Seed mirror: app/seed.py clean walls/rolls rows.
MASTER_BEDROOM_PLAIN53 = Combo(
    key="master_bedroom_plain53",
    wall_name="主卧一圈",
    roll_name="素色53",
    perimeter=16.0,
    base_height=2.7,
    roll_width=0.53,
    roll_length=10.0,
    pattern_cm=0.0,
)

FEATURE_WALL_FLOWER64 = Combo(
    key="feature_wall_flower64",
    wall_name="大花匹配",
    roll_name="大花64",
    perimeter=20.0,
    base_height=2.8,
    roll_width=0.53,
    roll_length=10.0,
    pattern_cm=64.0,
)

LADDER_COMBOS = (MASTER_BEDROOM_PLAIN53, FEATURE_WALL_FLOWER64)


@pytest.fixture(params=LADDER_COMBOS, ids=[c.key for c in LADDER_COMBOS])
def combo(request):
    """Each fixed wall+roll combination (one per clean seed pair)."""
    return request.param


@pytest.fixture
def plain_combo():
    """The 主卧一圈+素色53 combo.

    Its roll has pattern_cm=0, so ceiling height alone decides the drop
    length and any non-positive height is rejected by the engine — which is
    what the two rejection cases anchor on.
    """
    return MASTER_BEDROOM_PLAIN53


@pytest.fixture
def baseline_rolls(combo):
    """Baseline rolls at the combo's seed ceiling height, via the engine."""
    return rolls_at_height(combo, combo.base_height)


@pytest.fixture
def raised_rolls(combo):
    """Rolls at each raised step, aligned with RAISED_HEIGHT_STEPS."""
    return [rolls_at_height(combo, step) for step in RAISED_HEIGHT_STEPS]
