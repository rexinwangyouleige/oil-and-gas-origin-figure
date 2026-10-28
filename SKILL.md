---
name: oil-and-gas-origin-figure
description: 用 Python 驱动 Origin（originpro）产出石油天然气领域 SCI 论文图，按用户固定的样式规范（Times New Roman + 宋体、7–9 pt、刻度朝内、无次刻度、doubley 双 Y）出 PNG/TIF/PDF/OPJU 并自动自检。适用于油气工程（产量递减、含水、试井 log-log、驱替、相渗、压汞、NMR T2）、油气化学（TG/DTG、XRD/FTIR/Raman 叠谱、流变、吸附、界面张力）、油气能源（构成、区块对比）的单图与多面板拼图。用户提到 Origin 画图、论文配图、SCI 图、期刊图、多面板、双 Y 轴、"这个数据怎么画"时使用。
---

# oil-and-gas-origin-figure

**Python 编排、Origin 渲染、模板打底、脚本兜底、出图必自检。**

```
oil-and-gas-origin-figure/
├── SKILL.md               本文件：工作流
├── ogfig/                 引擎：Page / DualY、style、export、check、cli、templates、data、config
├── catalog/               图型素材库，INDEX.md 是关键词 → 脚本对照表；输出在 catalog/out/
├── templates/             预设 .otpu（og_line / og_loglog / og_stack / og_doubley）
└── references/
    ├── style-spec.md      用户的硬性样式规范 + 配色用法        ← 每次出图前读
    ├── chart-selection.md 油气三类方向的选图规则                ← 选图时读
    ├── pitfalls.md        38 条 Origin 实测坑                  ← 写新脚本 / 样式不生效时读
    ├── origin-2026b-cheatsheet.md  模板清单、属性速查、配方
    └── originpro_API_手册.md       originpro 全量 API（6000+ 行，按需 grep，别整篇读）
```

## 硬性规范（摘要，详见 references/style-spec.md）

西文 Times New Roman、中文宋体，覆盖所有文字；字号 7–9 pt（刻度 7 / 标题 8 / 标注 8 / 字母 9 粗体）；
有数据的边主刻度朝内、上边框只留线、无次刻度；单位不重复；双 Y 用 doubley；题注无边框。
这些都是默认值，**不用等用户再提**。和通用作图建议冲突时（例如有人主张 Arial、不用双 Y），以这里为准。

## 工作流（不要跳步）

### 0. 明确论点
问清（或从上下文推断并说出你的假设）：这张图要让读者相信什么？目标期刊 / 版式？
单图还是拼图？用户已指定图型时，直接进第 2 步。

**先对齐版式用语**（"组合图"这个词最容易听错，见下表）：

| 用户想要 | 说这些词 | 实现 |
|---|---|---|
| 小图套在大图里 | **内嵌小图 / inset / 画中画 / 局部放大图** | 一个坐标区 + 第二个层压在空白处（`catalog/production/bar_pie3d.py` 默认版式） |
| 两块并排 / 上下分 | 并排双面板、双面板、分面 facet、subplot | `Page(1, 2)` / `Page(2, 2)` |
| 同一 X、两套单位 | 双 Y 轴 | `DualY`（`og_doubley` 模板） |

- **默认按 inset 理解**：用户说"组合图 + 一个画布"时，指的是**一张图、一个坐标区**、小图压在坐标区的空白处，
  **不是**并排两个面板；只有明确说"并排 / 两个面板 / 左右分"时才用 `Page`。
- 版式只需问清三件事：**从属**（谁内嵌在谁里）、**锚点 + 占比**（右上角？宽 1/3？）、**避让**（不许压柱子 / 框线）。
- 用户没说清就按"右上角、宽 1/3、不压数据不压框"做，并在交付时说明这个假设。

### 1. 看数据
```bash
python -m ogfig.cli doctor              # 第一次用或换机器时：Origin 版本、模板、字体
python -m ogfig.cli inspect data.xlsx   # 列名、类型、范围、单调性、跨量级提示、初步建议
```
**用全部数据**：不抽样、不挑列；必须删行 / 列时说明删了多少、为什么。

### 2. 选图
查 `references/chart-selection.md`，给出 **首选 + 理由 + 1 个备选**。
用户要的图不合适（例如 n<5 画均值柱、无关变量凑双 Y、一面板 > 5 条线）时，先说明问题和替代方案，由用户决定。
再查 `catalog/INDEX.md`：有对应脚本 → 复制改；没有 → 用 `Page` + 模板现写。
"柱状 + 饼 / 占比"这类组合：**默认做成 inset**（`production/bar_pie3d.py`），并排版是加参数 `side` 的备选。

### 3. 预演
```bash
python -m ogfig.cli spec --journal single     # 不开 Origin，打印尺寸 / 字号 / 线宽 / 配色
```
把"版式 + 每个面板画什么 + 轴范围 + 配色"用一两句话告诉用户，拿不准的先确认，再开 Origin。

### 4. 出图
```python
from ogfig import Page, DualY, style, export

pg = Page(rows=2, cols=2, journal='double')        # 页面 = 180 × 130 mm，边距按 mm
ws = pg.sheet('PROD', 3)
ws.from_list(0, t, lname='Time', units='d')
ws.from_list(1, q, lname='Rate')
pg.plot(0, ws, 1, 0, kind='logy', color=style.C[0])  # 'l' 's' 'ls' 'logy' 'loglog'
pg.style(0, 'Production time (d)', 'q\\-(g) (10\\+(4) m\\+(3)/d)')
pg.categories(2, ['Baseline', 'Acid', 'Frac'])       # 类别轴
pg.caption(0, 'Well A-12', where='tr')               # 框内空白角
pg.drop_legends()
for i, ch in enumerate('abcd'):
    pg.letter(i, ch)                                 # 最后加，按 mm 对齐
pg.finish()
paths = export.save(pg.g, r'D:\fig\fig1.png')       # png + tif(600 dpi) + pdf + opju
print(export.report(pg.g, paths))                    # 自检报告 + 灰度预览
```
双 Y：`pg = DualY(journal='single')` → `pg.guide(ws, y)` 先画透明引导线 → 左层 `pg.plot(0, ...)` / `pg.bar(0, ...)`
→ `pg.guide(ws, y2, right=True)` → `pg.plot_right(...)` → `pg.style_dual(xt, yt, y2t)`。参见 `catalog/production/bar_line_dualy.py`。

模板：`Page(..., template='og_loglog')`；新图型先用脚本，同一种图做到第三次再存模板（见 `templates/README.md`）。

数据工具 `ogfig.data`（只依赖 numpy）：`arps` / `fit_arps`（递减拟合，返回 qi、Di、b、R²）、`corey`（相渗）、
`fractional_flow`（分流率）、`pressure_derivative`（试井导数）、`water_cut`、`cumulative`。

### 5. 自检闭环（三层都要过）
1. **程序层**：`export.report` 打印的报告必须 `[PASS]`：尺寸、字体、字号 7–9、出界、文字重叠、细线。
   单独复查：`python -m ogfig.cli check fig1.pdf --mm 180 130`。
2. **读图层**：用 Read 工具打开导出的 PNG 和 `_gray.png`，逐项看：
   - 标注 / 图例 / 题注有没有压曲线或数据点
   - 面板字母是否同一偏移、同一字号，标题有没有缺失或重复
   - 刻度数字是否拥挤（拥挤就加大 `inc`），曲线颜色在灰度下能否区分
   - 轴标题单位是否正确、上下标是否渲染（`q_g`、`10⁴`、`m³`）
3. **规范层**：对照 `references/style-spec.md` 第 1 节逐条核对。

任何一层不过 → 改脚本 → 重跑 → 再查，直到全过。**不要只凭"脚本没报错"就交付**：`lt_exec` 写错也不报错（坑 #6）。

### 6. 交付
告诉用户：输出文件路径（png / tif / pdf / opju / _gray.png）、自检结果、做了哪些假设。
新做的图型跑通后，按 `catalog/INDEX.md` 的约定存进 catalog 并补一行索引。

## 改偏好

全部在 `ogfig/config.py` 的 `PREFS`：配色 `palette`、自定义色 `colors`、版式 `journal` / `page_mm`、
边距 `margin_mm` / `gap_mm` / `margin_dual_mm`、字号 `fs_tick` / `fs_title` / `fs_note` / `fs_letter`、
字体 `font_latin` / `font_cjk`、线宽 `line_width` / `axis_thickness`、刻度 `tick_length` / `tick_major`。
改完重跑 `python -m ogfig.cli templates`，让模板跟上新规范。

## 先决条件

Windows + Origin 2024b 及以上（2024 早期版 10.1.x 有文字上划线、线宽改不动的 bug；已实测 2026 / 10.3 正常）；
Python 3.10+，`pip install originpro numpy pandas pymupdf`。脚本用 `op.new(); op.attach()` 连接 Origin，
跑完 `op.exit()`；如有残留的无窗口 Origin64 进程，确认是脚本起的再结束。
