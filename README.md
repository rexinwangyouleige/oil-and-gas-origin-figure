# oil-and-gas-origin-figure

用 Python（originpro）驱动 Origin，产出石油天然气领域 SCI 论文图的技能包：**Python 编排 → Origin 渲染 → 模板打底 → 脚本兜底 → 出图必自检**。

一次出 PNG / TIF(600 dpi) / PDF(矢量) / OPJU，并按固定样式规范自检（尺寸、字体、字号 7–9 pt、出界、文字重叠、细线）。

## 预览

| 2×2 拼图（递减 / 含水 / 措施 / 试井） | 柱状 + 3D 饼（inset 内嵌） |
|---|---|
| ![decline dashboard](catalog/out/decline_dashboard_2x2.png) | ![bar + pie inset](catalog/out/bar_pie3d_inset.png) |

| TG / DTG 双 Y | 自动图例（normal / bold 风格档） |
|---|---|
| ![tga dtg](catalog/out/tga_dtg_dualy.png) | ![trend legend](catalog/out/trend_legend.png) |

| 明显版（bold：字号 10、线 2 pt） | 四角占满 → 加高页面放右上角 |
|---|---|
| ![bold](catalog/out/trend_legend_bold.png) | ![grow](catalog/out/trend_legend_grow.png) |

## 目录

```
SKILL.md                工作流：明确论点 → 看数据 → 选图 → 预演 → 出图 → 自检 → 交付
ogfig/                  引擎：Page / DualY、style、export、check、cli、templates、data、config
catalog/                图型素材库（INDEX.md 是关键词 → 脚本对照表），预览在 catalog/out/
templates/              预设 .otpu（og_line / og_loglog / og_stack / og_doubley）
references/             style-spec 硬性规范 / chart-selection 选图规则 / pitfalls 44 条实测坑 /
                        origin-2026b-cheatsheet 属性速查 / originpro API 手册
```

## 环境

- Windows + **Origin 2024b 及以上**（2024 早期 10.1.x 有文字上划线、线宽改不动的 bug；2026b / 10.3 实测正常）
- Python 3.10+，`pip install originpro numpy pandas pymupdf`
- 字体：Times New Roman + 宋体（Windows 自带）

## 快速开始

```bash
python -m ogfig.cli doctor                    # 环境自检：Origin 版本、模板、字体
python -m ogfig.cli spec --journal single     # 预演：尺寸 / 字号 / 线宽 / 配色（不开 Origin）
python -m ogfig.cli inspect data.xlsx         # 看数据：列名、范围、单调性、跨量级提示

python catalog/production/decline_dashboard_2x2.py    # 跑一个现成图型
python catalog/production/bar_pie3d.py                # 柱状 + 3D 饼（inset，默认）
python catalog/production/bar_pie3d.py side           # 同一批数据的并排版式
python catalog/production/trend_legend.py             # 多曲线 + 自动图例（四角挑最空的）
python catalog/production/trend_legend.py bold        # 明显版：字号 10 / 线 2.0 pt / 轴 1.5 pt
python catalog/production/trend_legend.py grow        # 四角都占满 → 放大坐标区
python catalog/production/trend_legend.py cols        # 6 条曲线 → 图例自动两列
python catalog/production/trend_legend.py tight       # Fit Page/Layer 去白边
```

脚本都在 skill 根目录跑，产物落在 `catalog/out/<名字>.png / .tif / .pdf / .opju / _gray.png`。

## 安装到各类 agent 工具

**Claude Code / VS Code Copilot / DeepSeek Harness / Codex / Cursor / Cline / WorkBuddy…** 的安装位置、验证方法、
以及一段可以**直接粘给豆包等 AI 让它帮你装**的提示词，都写在 **[INSTALL.md](INSTALL.md)**。

最短路径（Windows，通用位置；Claude Code 用 `~/.claude/skills`、DSH 用 `~/.dsh/skills`）：

```powershell
git clone --branch v0.2.2 --depth 1 https://github.com/rexinwangyouleige/oil-and-gas-origin-figure.git `
  "$env:USERPROFILE\.agents\skills\oil-and-gas-origin-figure"
```

装完在会话里说一句"用 oil-and-gas-origin-figure 画一张产量递减图"即可触发。

> 能读 `SKILL.md` 的 agent 都支持本技能；没有 skills 目录的工具，把
> `~/.agents/skills/oil-and-gas-origin-figure/SKILL.md` 写进它的项目规则（`AGENTS.md` / `.cursor/rules`）即可。

## 作为 agent skill 使用

把整个目录放进你的 skills 目录（例如 `~/.dsh/skills/`、`~/.claude/skills/`、`~/.agents/skills/`），带 `SKILL.md` 即可被识别；
模型按 SKILL.md 的工作流调用 `ogfig` 出图。详见 [INSTALL.md](INSTALL.md)。

## 样式规范（默认值，不必每次重申）

西文 Times New Roman / 中文宋体；字号 7–9 pt（刻度 7、轴标题 8、图例与标注 8、面板字母 9）；
有数据的边主刻度朝内、无次刻度、上边框只留线；双 Y 用 Origin 自带 doubley；题注无边框；
线宽：坐标轴 0.75 pt、曲线 1.0 pt、主刻度长 3。
**图例**：多曲线 / 多序列默认加，文字取列 long name、无边框、自动放四角里最空的角；
**硬规则：图例绝不压数据**——四角都占住就放大坐标区重试（最多 3 轮）、再不行把字号降到 7 pt，最后才告警退化；
条目多时自动排 1 / 2 / 3 列（`ncols=2` 可强制）。
**两档风格**：`normal`（投稿，即上述数值）与 `bold`（明显版：字号 9–11、轴 1.5 pt、线 2.0 pt、刻度长 4.5、符号 6），`style.set_preset('bold')` 切换。
**去白边**：`pg.fit_page()` 调 Origin 的「页面→图层」「图层→页面」两条命令，页面边界=内容边界。
全部可在 `ogfig/config.py` 的 `BASE` / `STYLE_PRESETS` 里改。

## 版式用语（说错就画错）

| 想要 | 说这些词 | 实现 |
|---|---|---|
| 小图套在大图里 | **内嵌小图 / inset / 画中画** | 一个坐标区 + 第二层压在空白处 |
| 两块并排或上下 | 并排双面板、分面 facet、subplot | `Page(1, 2)` / `Page(2, 2)` |
| 同一 X 两套单位 | 双 Y 轴 | `DualY`（`og_doubley` 模板） |

"组合图 + 一个画布"默认按 **inset** 理解（一张图、一个坐标区），不是并排。

## 版本历史

| 版本 | 内容 |
|---|---|
| **v0.2.2** | 新增 [INSTALL.md](INSTALL.md)：Claude Code / VS Code Copilot / DeepSeek Harness / Codex / Cursor / Cline / WorkBuddy 的安装位置、验证步骤、更新卸载，以及**一段可直接粘给豆包等 AI 的安装提示词** |
| **v0.2.1** | 图例**绝不压数据**（零墨迹角 → 放大坐标区 3 轮 → 7 pt → 告警）；多列排布（`ncols` 自动/指定）；`pg.fit_page()` 去白边（Origin「页面→图层」+「图层→页面」）；清理实验死代码 |
| **v0.2.0** | **自动图例**（文字取列 long name、无边框、自动挑空白角）；**`bold` 明显版风格档**（字号 9–11、轴 1.5 pt、线 2.0 pt、刻度 4.5、符号 6、页边距同步放大）；`catalog/production/trend_legend.py` 示例 |
| v0.1.0 | 首个可用版本：ogfig 引擎（Page / DualY / style / export / check / cli / templates）、9 个图型脚本、样式规范、坑清单、2026b 速查、API 手册 |

## 许可

[MIT](LICENSE)
