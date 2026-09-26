"""Support helpers for the ceiling-height ladder monotonicity tests.

Every number is recomputed from the pure engine entry
``app.engines.wallpaper_math.roll_count`` — the same calculator that
``app.services.estimate_service.run_estimate`` delegates to. No ``calc_runs``
history rows are read anywhere in this package, so the monotonicity
assertions cannot be faked by comparing two stored history rows.

See ``height_ladder.md`` for the combo table and the expected rolls ladder.
"""

from dataclasses import dataclass

from app.engines.wallpaper_math import roll_count

# Raised ceiling-height steps in metres, shared by both combos and applied on
# top of each combo's seed height. Picked so that for each combo every step
# keeps rolls >= baseline and at least one step is strictly larger:
#   主卧一圈+素色53 (base 2.7 m): 11 -> 16 -> 16 rolls
#   大花匹配+大花64 (base 2.8 m): 19 -> 19 -> 38 rolls
RAISED_HEIGHT_STEPS = (3.4, 4.4)

# Probe heights for the two rejection cases. Zero and negative stay in
# separate test functions so one can never stand in for the other.
HEIGHT_PROBE_ZERO = 0.0
HEIGHT_PROBE_NEGATIVE = -0.5


@dataclass(frozen=True)
class Combo:
    """One fixed wall+roll combination mirroring a clean seed row pair."""

    key: str
    wall_name: str
    roll_name: str
    perimeter: float
    base_height: float
    roll_width: float
    roll_length: float
    pattern_cm: float

    @property
    def label(self) -> str:
        return f"{self.wall_name}+{self.roll_name}"


def engine_kwargs(combo: Combo, height: float) -> dict:
    """Aux conversion: combo attributes + ceiling height -> roll_count kwargs."""
    return {
        "perimeter": float(combo.perimeter),
        "height": float(height),
        "roll_width": float(combo.roll_width),
        "roll_length": float(combo.roll_length),
        "pattern_cm": float(combo.pattern_cm),
    }


def result_at_height(combo: Combo, height: float) -> dict:
    """Full engine result for the combo at the given ceiling height."""
    return roll_count(**engine_kwargs(combo, height))


def rolls_at_height(combo: Combo, height: float) -> int:
    """Rolls count from the pure engine entry at the given ceiling height."""
    return int(result_at_height(combo, height)["rolls"])


def below_baseline_message(
    combo: Combo,
    baseline_height: float,
    baseline_rolls: int,
    raised_height: float,
    raised_rolls: int,
) -> str:
    return (
        f"{combo.label}: rolls fell below baseline after raising ceiling height; "
        f"baseline height={baseline_height}m rolls={baseline_rolls}, "
        f"raised height={raised_height}m rolls={raised_rolls}"
    )


def step_regression_message(
    combo: Combo,
    lower_height: float,
    lower_rolls: int,
    higher_height: float,
    higher_rolls: int,
) -> str:
    return (
        f"{combo.label}: rolls regressed between raised steps; "
        f"height={lower_height}m rolls={lower_rolls}, "
        f"height={higher_height}m rolls={higher_rolls}"
    )


def no_strict_step_message(
    combo: Combo,
    baseline_height: float,
    baseline_rolls: int,
    raised_pairs: list,
) -> str:
    steps = ", ".join(f"height={h}m rolls={r}" for h, r in raised_pairs)
    return (
        f"{combo.label}: no raised step strictly above baseline; "
        f"baseline height={baseline_height}m rolls={baseline_rolls}, "
        f"raised steps: {steps}"
    )
