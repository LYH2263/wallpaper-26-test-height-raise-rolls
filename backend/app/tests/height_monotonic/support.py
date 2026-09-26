"""层高抬升单调测例包的辅助换算与失败消息。

只放纯函数与常量：不碰数据库、不读历史行（calc_runs）。
引擎取数入口 app.engines.wallpaper_math.roll_count 由 conftest 的夹具调用。
"""

from collections import namedtuple

# 一个抬升档：label 用于失败消息与对照说明，delta_m 是相对基准层高的增量（米）。
Step = namedtuple("Step", ["label", "delta_m"])

# 两档抬升：档一 +0.7m（常规挑高），档二 +1.8m（跃层 / loft 挑高）。
# 取值理由与逐组换算结果见同目录 README.md。
LIFT_STEPS = (
    Step("档一", 0.7),
    Step("档二", 1.8),
)

# 某一层高下引擎取数的快照。
Point = namedtuple("Point", ["height_m", "drops", "strips_per_roll", "rolls"])


def height_after_lift(base_height_m, step):
    """把基准层高按抬升档换算成目标层高（米，保留到毫米）。"""
    target = round(float(base_height_m) + float(step.delta_m), 3)
    if target <= 0:
        raise ValueError(f"抬升后层高必须为正，得到 {target}")
    return target


def format_point(point):
    """单行描述一个取数点，如：层高 2.70m → 11 卷（31 幅 / 每卷 3 条）。"""
    return (
        f"层高 {point.height_m:.2f}m → {point.rolls} 卷"
        f"（{point.drops} 幅 / 每卷 {point.strips_per_roll} 条）"
    )


def below_baseline_message(combo_name, baseline, step_label, raised):
    """某一档卷数低于基准时的失败消息。"""
    return (
        f"[{combo_name}] 抬升档卷数低于基准："
        f"基准 {format_point(baseline)}；"
        f"{step_label} {format_point(raised)}"
    )


def step_regression_message(combo_name, prev_label, prev_point, next_label, next_point):
    """后一档卷数低于前一档时的失败消息。"""
    return (
        f"[{combo_name}] 抬升档之间出现回落："
        f"{prev_label} {format_point(prev_point)}；"
        f"{next_label} {format_point(next_point)}"
    )


def no_strict_step_message(combo_name, baseline, raised_points):
    """两档都没有严格大于基准时的失败消息。"""
    raised_text = "；".join(
        f"{step.label} {format_point(point)}"
        for step, point in zip(LIFT_STEPS, raised_points)
    )
    return (
        f"[{combo_name}] 两档抬升均未严格超过基准："
        f"基准 {format_point(baseline)}；{raised_text}"
    )
