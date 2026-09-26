"""层高抬升单调断言：每档不低于基准、档间不回落、每组至少一档严格变大。

另含两条独立的拒绝用例：层高为 0、层高为负，互不顶替。
"""

import pytest

from app.engines.wallpaper_math import roll_count

from support import (
    below_baseline_message,
    no_strict_step_message,
    step_regression_message,
)


def test_each_step_not_below_baseline(combo_case):
    baseline = combo_case.baseline
    for step, point in combo_case.raised:
        assert point.rolls >= baseline.rolls, below_baseline_message(
            combo_case.spec.name, baseline, step.label, point
        )


def test_steps_not_regressing(combo_case):
    raised = combo_case.raised
    for (prev_step, prev), (next_step, nxt) in zip(raised, raised[1:]):
        assert nxt.rolls >= prev.rolls, step_regression_message(
            combo_case.spec.name, prev_step.label, prev, next_step.label, nxt
        )


def test_at_least_one_step_strictly_above_baseline(combo_case):
    baseline = combo_case.baseline
    assert any(
        point.rolls > baseline.rolls for _, point in combo_case.raised
    ), no_strict_step_message(
        combo_case.spec.name, baseline, [point for _, point in combo_case.raised]
    )


def test_reject_zero_height():
    """层高为 0：drop_len 为 0，引擎必须拒绝（与负层高用例各自独立）。"""
    with pytest.raises(ValueError, match="invalid drop length"):
        roll_count(16.0, 0.0, 0.53, 10.0, 0)


def test_reject_negative_height():
    """层高为负：drop_len 为负，引擎必须拒绝（与零层高用例各自独立）。"""
    with pytest.raises(ValueError, match="invalid drop length"):
        roll_count(16.0, -0.5, 0.53, 10.0, 0)
