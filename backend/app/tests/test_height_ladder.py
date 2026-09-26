"""Ceiling-height ladder monotonicity assertions.

Fixtures live in conftest.py; conversions and failure messages live in
height_ladder_support.py. The two raised steps (3.4 m, 4.4 m) and the
expected rolls per combo are documented in height_ladder.md.
"""

import pytest

from height_ladder_support import (
    HEIGHT_PROBE_NEGATIVE,
    HEIGHT_PROBE_ZERO,
    RAISED_HEIGHT_STEPS,
    below_baseline_message,
    no_strict_step_message,
    rolls_at_height,
    step_regression_message,
)


def test_each_raised_step_not_below_baseline(combo, baseline_rolls, raised_rolls):
    for height, rolls in zip(RAISED_HEIGHT_STEPS, raised_rolls):
        assert rolls >= baseline_rolls, below_baseline_message(
            combo, combo.base_height, baseline_rolls, height, rolls
        )


def test_raised_steps_do_not_regress(combo, raised_rolls):
    first_height, second_height = RAISED_HEIGHT_STEPS
    first_rolls, second_rolls = raised_rolls
    assert second_rolls >= first_rolls, step_regression_message(
        combo, first_height, first_rolls, second_height, second_rolls
    )


def test_at_least_one_step_strictly_above_baseline(combo, baseline_rolls, raised_rolls):
    raised_pairs = list(zip(RAISED_HEIGHT_STEPS, raised_rolls))
    assert any(rolls > baseline_rolls for _, rolls in raised_pairs), no_strict_step_message(
        combo, combo.base_height, baseline_rolls, raised_pairs
    )


def test_zero_ceiling_height_rejected(plain_combo):
    with pytest.raises(ValueError, match="invalid drop length"):
        rolls_at_height(plain_combo, HEIGHT_PROBE_ZERO)


def test_negative_ceiling_height_rejected(plain_combo):
    with pytest.raises(ValueError, match="invalid drop length"):
        rolls_at_height(plain_combo, HEIGHT_PROBE_NEGATIVE)
