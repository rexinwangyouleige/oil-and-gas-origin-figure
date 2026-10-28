# 预设模板（.otpu）

由 `python -m ogfig.cli templates` 按 `ogfig/config.py` 生成；改了字号 / 线宽 / 刻度后重跑一次。

| 模板 | 内容 | 用法 |
|---|---|---|
| `og_line` | 单层 XY，线性轴，四边框、主刻度朝内、无次刻度、上 / 右框只留线 | `Page(...)` 默认 |
| `og_loglog` | 同上，X / Y 都是 log10 | `Page(..., template='og_loglog')` |
| `og_stack` | 同上，Y 轴不显示刻度和数字（叠谱） | `Page(..., template='og_stack')` |
| `og_doubley` | doubley 两层：左层常规；右层只留 y2（朝内）、自己的 X 轴关掉 | `DualY(...)` |

## 模板与脚本怎么分工

- **模板**记住：页面尺寸、层位置、刻度方向与长度、次刻度、边框、线宽、字号。
- **模板记不住**：字体（新图文字回到 SimSun）、空标题会被隐藏（坑 #29）。
- 所以出图时脚本仍会执行 `Page.style()` / `DualY.style_dual()`：模板给基线，脚本兜底。
  新图型先用脚本做；同一种图做到第三次，再考虑存成模板加进 `ogfig/templates.py` 的 `PRESETS`。
- 找不到 .otpu（没生成过）时，`style.template_path()` 自动退回 Origin 内置的 `line` / `doubley`，脚本照样能跑。

## 在 GUI 里手调后存成自己的模板

在 Origin 里把一张图调到满意 → 激活该图 → 命令窗口执行：

```
template_saveas template:=og_mine filepath:="<skill 路径>\templates\";
```

然后 `Page(..., template='og_mine')` 即可（`filepath:=` 才能存到指定目录，`path:=` 无效）。
