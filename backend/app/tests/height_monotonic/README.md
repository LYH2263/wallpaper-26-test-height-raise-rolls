# 层高抬升单调测例包 — 对照说明

## 组合与取数

两组组合取值与 `app/seed.py` 种子数据一致；取数只走引擎纯算入口
`app.engines.wallpaper_math.roll_count`，不插历史行、不读 `calc_runs`。

| 组合 | 墙（周长 / 基准层高） | 卷（幅宽 / 卷长 / 花高） |
| --- | --- | --- |
| 主卧一圈×素色53 | 16.0m / 2.70m | 0.53m / 10.0m / 0cm |
| 大花匹配×大花64 | 20.0m / 2.80m | 0.53m / 10.0m / 64cm |

## 两档抬升取值

- 档一：基准层高 **+0.7m**（常规挑高）
- 档二：基准层高 **+1.8m**（跃层 / loft 挑高）

逐组换算（`support.height_after_lift`，保留到毫米）与引擎取数结果：

| 组合 | 基准 | 档一（+0.7m） | 档二（+1.8m） |
| --- | --- | --- | --- |
| 主卧一圈×素色53 | 2.70m → 11 卷 | 3.40m → 16 卷（严格增大） | 4.50m → 16 卷 |
| 大花匹配×大花64 | 2.80m → 19 卷 | 3.50m → 19 卷（持平） | 4.60m → 38 卷（严格增大） |

取值理由：档一让主卧组每卷条数 3→2 跨过一个整数边界，严格增大落在档一；
大花组档一仍维持每卷 2 条（持平），档二把对花后条长推过 5.0m（每卷 2→1 条），
严格增大落在档二。两档配合使每组都至少有一档严格大于基准。

## 断言

1. 每档 rolls ≥ 基准 rolls；
2. 档二 rolls ≥ 档一 rolls（档间不回落）；
3. 每组至少一档 rolls 严格 > 基准。

失败消息打印组合名、基准与抬升后的层高和 rolls
（`support.below_baseline_message` / `step_regression_message` / `no_strict_step_message`）。

## 拒绝用例（两条独立用例，互不顶替）

- `test_reject_zero_height`：层高 0 → `ValueError`；
- `test_reject_negative_height`：层高为负 → `ValueError`。

## 边界说明

基准卷数 11 / 19 与 `app/tests/test_wallpaper_math.py` 既有引擎断言一致；
本包只新增测例，不改动 `wallpaper_math` 与既有断言。
