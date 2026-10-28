# Origin 2026b + originpro 速查表（本机实测版）

> **出图前先看这一页**，能覆盖 90 % 的情况；查不到再翻 `originpro_API_手册.md`（同目录），
> 最后才去官方在线文档。不要再用"改一个属性导一次图"的方式试错。

本机环境（2026-10 实测）：

| 项 | 值 |
|---|---|
| Origin | **2026b**（10.3），安装目录 `<Origin 安装目录>` |
| Python | 3.13.14（`python` 能 `import originpro` 即可，自带解释器也行） |
| originpro | 1.1.12（+ OriginExt） |
| 页面尺寸 | `page.kar=0; page.width=4252; page.height=3071;`（像素，resx=600 → 180×130 mm；或 `style.set_page_mm(g, 180, 130)`） |
| 导出验证 | `g.save_fig(path, width=4252)` → 180 mm @600 dpi |

连接（每条脚本开头都这样写）：

```python
import originpro as op
op.new()            # 起/连一个 Origin 实例
op.attach()         # 关键：切到"正在运行的那个"窗口，否则会操作一个隐形实例
op.set_show(True)   # 让它可见
print(op.org_ver()) # 10.30018 = 2026
```

---

## 1. 内置图形模板（已逐个实测，`op.new_graph(template=...)`）

**双 Y 轴不是"拼"出来的，是模板自带的** —— 这就是 `doubley`：

| 模板名 | 层数 | 用途 |
|---|---|---|
| `line` | 1 | 折线（默认，万能底板） |
| `scatter` / `linesymb` | 1 | 散点 / 点+线 |
| `column` / `bar` / `stackcolumn` / `stackbar` | 1 | 柱状、条形、堆叠 |
| `area` / `stackarea` | 1 | 面积、堆叠面积 |
| **`doubley`** | **2** | **双 Y 轴（左 g[0]、右 g[1]）** |
| `pie` / `doughnut` | 1 | 饼图（**3D**）/ 圆环 |
| **`pie2d`** | 1 | **2D 饼图**（正式出图用这个；`pie` 出来是 3D 的） |
| `box` / `violin` | 1 | 箱线 / 小提琴 |
| `contour` / `heatmap` / `image` | 1 | 等高线 / 热图 / 位图 |
| `polar` / `ternary` / `3d` / `bubble` | 1 | 极坐标 / 三元 / 3D / 气泡 |

> 想找还有哪些模板？直接列安装目录的 `.otp`：`Get-ChildItem "<Origin 安装目录>" -Filter *.otp`（实测存在 `WATER3D.otp`、`WATERFAL.otp`、`3DBARS.otp` 等）。
> ⚠️ 但 `WATER3D`（3D 瀑布）用 `plotxy` 驱动时只出"实心墙体"或单条曲线，分组的 6 条瀑布出不来 → 瀑布图用"错位叠层 2D 曲线"更稳，见 `catalog/thermal/tga_waterfall.py`。

**不存在**（写了会报 `NoneType has no len()`）：`histogram`、`errorbar`、`waterfall`、`double_x`、
`line+symbol`、`pareto`、`qc`、`surface`、`smith`、`bridge`。
直方图用 `column` 自己算 bin；误差棒用 `add_plot(..., colyerr=...)`。

---

## 2. `add_plot` 图类型代码

```python
gl.add_plot(wks, coly, colx=-1, colz=-1, type='?', colyerr=-1, colxerr=-1)
```

| type | 含义 |
|---|---|
| `'l'` | 折线 |
| `'s'` | 散点 |
| `'y'` | 线+符号（符号填充改不动，见坑） |
| `'c'` | 柱/条 |
| `'?'` | 交给模板决定（饼图页里就用它） |

`'ls'` **不支持**（KeyError）。要"线 + 实心点"就调两次：先 `'l'` 再 `'s'`。

---

## 3. 属性速查（LabTalk 路径，用 `gl.lt_exec()` 写）

| 想做什么 | 写法 |
|---|---|
| 轴范围 / 步长 | `layer.x.from=0; layer.x.to=800; layer.x.inc=100;` |
| 轴范围（API） | `gl.set_xlim(0, 800)`, `gl.xlim` |
| 刻度朝内 / 朝外 | `layer.x.ticks=1`（内）/ `2`（外）；位掩码 1+4=5 表示主内+次内 |
| 去掉次刻度 | `layer.x.minorTicks=0; layer.x.mticklength=0;` |
| 四边框 | `layer.x.showAxes=3; layer.y.showAxes=3;` |
| 上/右边框不要刻度 | `layer.x2.ticks=0; layer.x2.ticklength=0; layer.y2.ticks=0; layer.y2.ticklength=0;`（别设 `showLabels=0`，会连主轴数字一起关掉） |
| 刻度标签字号 | `layer.x.label.pt=7;` |
| **刻度标签字体** | `layer.x.label.font=font(Times New Roman);` ← **必须用 `font()`**；`font` 是数字型 Windows 字体索引，写成字符串 `="Times New Roman"` 会被**静默忽略**（官方文档 layer-axis-label-obj 明确写了 numeric） |
| 轴标题字号 | `layer.x.title.pt=16;` |
| **轴标题字体** | `xb.font=font(Times New Roman); yl.font=font(Times New Roman); xt.font=...; yr.font=...;` ← 标题是 text 对象（xb=下X、xt=上X、yl=左Y、yr=右Y），`layer.x.title.font` **无效** |
| 轴标题文字 | `gl.axis('x').title = 'Temperature (℃)'`（会覆盖列名自动标题） |
| 轴颜色 / 粗细 | `layer.y.color=color(0,0,0); layer.y.thickness=1.6;` |
| 对数轴 | `gl.yscale = 'log10'` |
| **图例字体** | `legend.font=font(Times New Roman); legend.pt=11;` |
| **数据标签字体**（饼图百分比/柱顶数字） | `layer.plot1.label.font=font(Times New Roman); layer.plot1.label.pt=12;` |
| **每层样式前先切层** | `op.lt_exec('page.active=N')` —— `lt_exec` 里的 `layer.*` 只作用于当前激活层，多图层（doubley 右层）不切层就会写错层 |
| 层位置（多面板） | `page.active=N; layer.left/top/width/height=`（**top 从页面顶部算**，值小=靠上） |
| 层索引 | `gl.index()`（0 基），`page.active` 是 1 基 |
| 图例 | `gl.label('legend').remove()` |
| **给某段 x 区间铺底色** | 造一条"顶到上边界"的辅助曲线（x 只在目标区间），`p.set_fill_area(above=op.ocolor('#DCEEF7'), type=1)` —— **above 要传 OColor 整数**，传 1 会变成黑色 |
| 文本 | `lab = gl.add_label('x', x, y)` → `gl.lt_exec(f'{lab.name}.font=font(Times New Roman); {lab.name}.fsize=18;')`、`set_int('rotate',0)`、`set_int('color', op.ocolor('#C0504D'))`；或直接 `style.text_label()` |
| 导出 | `g.save_fig(path, width=4252)`；`type='tif'/'pdf'/'emf'` |

⚠️ **双 Y 图两条坑**（都是 2026b 上实测的）：

1. **轴颜色跟着该层第一条曲线变**。先画一条 `transparency=100` 的黑线，再画彩色曲线：
   ```python
   p0 = gl.add_plot(ws, ycol, xcol, -1, 'l'); p0.color = '#000000'; p0.transparency = 100
   ```
2. 右层要关掉自己的 X 轴：`layer.x.showAxes=0; layer.x2.showAxes=0; layer.x.showLabels=0;`3. **doubley 模板默认不显示 X 刻度数字**，要显式 `layer.x.showLabels=1`（否则只有刻度线没有数字）4. 柱宽 set_cmd('-w 55') 在 2026 上无效，柱宽只能用 GUI 的 Plot Details 调；脚本里接受默认宽度

---

## 4. 六个常用配方（可直接抄）

### R1 双 Y 轴（左柱状 + 右折线）—— 完整可跑版见 `catalog/production/bar_line_dualy.py`（已封装成 `ogfig.DualY`）

```python
g = op.new_graph(template='doubley')
L, R = g[0], g[1]

L.activate()
guide = L.add_plot(ws, ycol, xcol, -1, 'l'); guide.color = '#000000'
guide.transparency = 100                     # 透明引导线，锁住黑色轴
bar = L.add_plot(ws, ycol, xcol, -1, 'c'); bar.color = C[0]
L.lt_exec('layer.x.showLabels=1; layer.y.showLabels=1;')   # ← 模板默认不显示 X 数字，必须显式打开
L.lt_exec('layer.x.ticks=1; layer.y.ticks=1; layer.x.minorTicks=0; layer.y.minorTicks=0;')

R.activate()
R.add_plot(ws, ycol2, xcol, -1, 'l').color = C[2]
R.add_plot(ws, ycol2, xcol, -1, 's').color = C[2]           # 线上加实心点
R.lt_exec('layer.x.showAxes=0; layer.x2.showAxes=0; layer.x.showLabels=0;')
``# 右层：y 是内侧隐藏轴，右边看得见的是 y2 —— 刻度/字体都要写给 y2``
R.lt_exec('layer.y2.ticks=1; layer.y2.ticklength=6; layer.y2.minorTicks=0;')
R.lt_exec('layer.y2.label.pt=7; layer.y2.label.font=font(Times New Roman);')
R.lt_exec('layer.y.ticks=1; layer.y.minorTicks=0;')          # 右轴同样朝内
```

### R2 叠谱图（XRD / XPS / Raman）

```python
for i, (lab, y) in enumerate(curves):
    pg.plot(0, ws, col_of[i], 0, kind='l', color=C[i])   # 数据已加 i*offset
    pg.annotate(0, lab, 42, i * offset + 0.3, color=C[i])
```
Y 刻度关掉：`layer.y.showLabels=0; layer.y.ticks=0;`

### R3 柱状 + 误差棒

```python
pg.bar(0, ws, xcol, [ycol1, ycol2], errs=[ecol1, ecol2], colors=C[:2])
gl.lt_exec('layer.x.label.type=10; layer.x.label.string$="A B C";')  # 见坑 C
```

### R4 饼图（3D → 2D 在 Plot Details 里改，脚本只管出图）

```python
g = op.new_graph(template='pie')
g[0].add_plot(ws, ycol, xcol, -1, '?')     # '?' 让饼图模板自己决定
```

### R5 多面板（2×2 等）

```python
from ogfig import Page
pg = Page(rows=2, cols=2, journal='double')   # 自动 page.active + 百分比定位
```

### R6 分类轴标签

**不要**用 `layer.x.label.type=10`（和 Times New Roman 冲突会变方框）。
把刻度数字关掉，用 `pg.annotate()` 在轴下方写文字。

---

## 5. 排错顺序（别再瞎试）

1. 先查本文件第 3 节的属性表；
2. 查 `originpro_API_手册.md`（同目录，6272 行，含全部类/方法/docstring）；
3. 查官方在线：https://docs.originlab.com/labtalk/ref/ （属性名）或 https://www.originlab.com/python/doc/originpro/annotated.html
4. 还不行，写一个 15 行的最小复现脚本（单层、单曲线）验证属性是否生效，再回到大图。

**判断成败的唯一标准是导出图看一眼**：`lt_exec()` 永远返回 None，写错也不报错。

---

## 6. 参考资料位置

| 文件 | 内容 |
|---|---|
| `docs/Origin_User_Guide_2026b_E.pdf` | 官方用户指南（476 页，图形/分析总览） |
| `docs/Origin_Tutorial_2026b_E.pdf` | 官方教程（61 页，分步操作） |
| `docs/LabTalk_Scripting_Guide_E.pdf` | LabTalk 脚本指南（510 页） |
| `references/originpro_API_手册.md` | originpro 1.1.12 全量 API docstring（离线） |
