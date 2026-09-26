"""夹具：固定两组 墙×卷 组合，先算基准 rolls，再按两档抬升层高取数。

取数只走引擎纯算入口 app.engines.wallpaper_math.roll_count，
不插历史行、不读 calc_runs，避免用两条历史行字段对比冒充单调性。
"""

import pytest

from app.engines.wallpaper_math import roll_count

from support import LIFT_STEPS, Point, height_after_lift


class ComboSpec:
    """一组固定的 墙×卷 组合，取值与 app/seed.py 的种子数据一致。"""

    def __init__(self, name, perimeter, height, roll_width, roll_length, pattern_cm):
        self.name = name
        self.perimeter = perimeter
        self.height = height
        self.roll_width = roll_width
        self.roll_length = roll_length
        self.pattern_cm = pattern_cm

    def point_at(self, height_m):
        """在指定层高下走引擎纯算入口取数。"""
        calc = roll_count(
            self.perimeter, height_m, self.roll_width, self.roll_length, self.pattern_cm
        )
        return Point(height_m, calc["drops"], calc["strips_per_roll"], calc["rolls"])


# 两组组合：主卧一圈配素色53；大花匹配墙配其种子卷大花64。
COMBO_SPECS = (
    ComboSpec("主卧一圈×素色53", 16.0, 2.7, 0.53, 10.0, 0),
    ComboSpec("大花匹配×大花64", 20.0, 2.8, 0.53, 10.0, 64),
)


class ComboCase:
    """一个组合的基准点与两档抬升点（按 LIFT_STEPS 顺序）。"""

    def __init__(self, spec):
        self.spec = spec
        self.baseline = spec.point_at(spec.height)
        self.raised = [
            (step, spec.point_at(height_after_lift(spec.height, step)))
            for step in LIFT_STEPS
        ]


@pytest.fixture(params=COMBO_SPECS, ids=[spec.name for spec in COMBO_SPECS])
def combo_case(request):
    """每组组合一份：基准 + 两档抬升，共两次参数化。"""
    return ComboCase(request.param)
