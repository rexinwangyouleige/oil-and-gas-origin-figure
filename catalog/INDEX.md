# 图型素材库（catalog）

**用户说的图 → 找下表关键词 → 复制对应脚本改数据。** 有现成脚本就先复制再改，不要从零写；
没有就按 `references/chart-selection.md` 的要点用 `Page` + 模板现写，跑通后存进这里并补一行。

所有脚本都能直接跑（在 skill 根目录）：`python catalog/<方向>/<名字>.py`，
输出到 `catalog/out/<名字>.png / .tif / .pdf / .opju / _gray.png`，并打印自检报告。
`catalog/out/` 里只长期保留每个脚本的 `.png` 作为效果预览；其他格式随时可以重跑生成，不入库。

| 关键词（中 / 英） | 脚本 | 用到的模板 / 类 | 尺寸 |
|---|---|---|---|
| 产量递减、Arps、含水率、措施对比、试井、log-log、拼图 2×2 / decline, water cut, PTA, dashboard | `production/decline_dashboard_2x2.py` | `Page(2, 2)` + `og_line` | 180 × 130 |
| 柱状 + 折线、产量 + 含水、双 Y 轴 / bar + line, dual Y | `production/bar_line_dualy.py` | `DualY` + `og_doubley` | 90 × 70 |
| 并排双面板、类别轴、区块对比 / side by side, categorical | `production/bar_line_side_by_side.py` | `Page(1, 2)` + `categories()` | 180 × 70 |
| 饼图 + 折线、产量构成 / pie + line | `production/pie_line.py` | `pie2d` + 加一个 line 层 | 180 × 80 |
| 柱状 + 3D 饼、**内嵌小图 / inset / 画中画**、绝对量 + 占比 / bar + 3D pie inset | `production/bar_pie3d.py`（默认 inset；加参数 `side` 出并排两面板） | `Page(1, 2, template='pie')` + 手工毫米定位 | 120 × 80（inset）/ 180 × 80（side） |
| 热重、TG、DTG、失重 / TGA, DTG | `thermal/tga_dtg_dualy.py`（读真实 xlsx） | `DualY` + `og_doubley` | 90 × 70 |
| 瀑布图、错位叠放、升温速率 / waterfall, heating rate | `thermal/tga_waterfall.py` | `line` + 手动定位 | 90 × 110 |
| 叠谱、XRD、Raman、NMR T2 / stacked spectra | `spectra/xrd_stack.py` | `Page` + `og_stack` | 90 × 110 |

## 待补（按 chart-selection.md 里标"脚本"的条目）

三 Y 轴（驱替：采收率 / 含水 / 压力 vs PV）、相渗 + 分流、压汞孔径分布、深度剖面（反向 Y）、
FTIR（反向 X）、龙卷风图、等值线 / 热图、三元图。

## 新增脚本的约定

1. 文件头 docstring：一句话说明 + 运行命令 + 用到的规范 / 坑号。
2. 开头三行固定：`SKILL = ...`、`sys.path.insert(0, SKILL)`、`OUT = os.path.join(SKILL, 'catalog', 'out')`。
3. 字号、线宽、颜色只从 `style` / `PREFS` 取，不写死数字。
4. 结尾 `paths = export.save(...)`、`print(export.report(...))`，自检 PASS 并看过 PNG 再入库。
