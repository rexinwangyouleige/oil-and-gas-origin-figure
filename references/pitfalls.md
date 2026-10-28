# 坑清单（Origin 2026 实测）

每一条都在本机复现过。**写新脚本前先扫一遍；样式改了没反应，先来这里查，再去翻手册。**
带"已内置"的条目，用 `ogfig` 的函数就不会踩；直接写 `op.lt_exec` 时要自己处理。

| # | 坑 | 正确做法 |
|---|---|---|
| 1 | 图层**不会**按你建的顺序摆放，`set_float('layer.left')` 完全无效 | `op.lt_exec(f'page.active={gl.index()+1}')` 再写 `layer.left/top/width/height`；`top` **从页面顶部**算，值小=靠上 |
| 2 | 刻度方向改了没反应 | `layer.x.ticks` 是**位掩码**：1=major in, 2=major out, 4=minor in, 8=minor out；SCI 风格用 `5` |
| 3 | 刻度间隔不受控 | `layer.x.inc = 0.2`（不是 nticks） |
| 4 | `g.add_layer(2)` 建右 Y 双轴：2024 上层定位失效、图直接不显示；2026 上刻度跑到内侧、量程串到左轴 | `Page` 里不做双 Y（原来的 `Page.twin()` 已删除）。双 Y 一律用 doubley 模板，见 #15 |
| 5 | `p.symbol_interior = 1/2` 对 line+symbol('y') 的符号填充无效 | 拆成 `'l'` + `'s'` 两次 `add_plot`，点自动实心 |
| 6 | `gl.lt_exec()` **永远返回 None**，失败也看不出来 | 任何样式改动后必须导图目视验收；`export.save` 里内置了"导出即报尺寸" |
| 7 | Origin 2024 (10.1.0) 每个文本对象上方多一条 1–2 px 细线 | 升级到 2024b+。已实测：`frame/border/box/frametype/linewidth/background` 全部改不动；另存纯 ASCII 路径也无效（差值 0） |
| 8 | 一次性 `op.new()` 会**再起一个隐藏 Origin**，你操作的不是用户那个窗口 | 永远 `op.new()` 紧接 `op.attach()`，并检查 `op.pages()` 非空；空闲实例要及时 `Stop-Process` 清掉 |
| 9 | 图例（legend）会污染版式 | `gl.label('legend').remove()` |
| 10 | 导出只有宽度参数，高度跟页面比例走 | 页面先用 `style.set_page_mm()` 设成真实毫米（`Page` 已内置），`export.save` 再按页面宽度导出，出来的宽高就是期刊尺寸 |
| 11 | **线宽、虚线样式在 Origin 2024 上改不动**：`p.set_cmd('-w 4')` / `set rr -w 4` / `set Book_B -w 4` 全是空操作；`line.width` 之类属性不存在 | **Origin 2026（10.3）已恢复正常**，`-w` 生效。2024 上只能保持默认线宽。`p.set_cmd()` 在 Python 3.13 + originpro 1.1.12 下可能抛内部异常，所以 `panels._safe_set()` 用 try/except 包住，绝不让样式把整张图搞崩 |
| 12 | 给文本设 `label.set_str('font', ...)` 会把字形打坏（变成一排方框） | 用 LabTalk：`<对象名>.font=font(Times New Roman);`（2026 实测 PDF 里是 TimesNewRomanPSMT）。`style.text_label()` 已内置 |
| 13 | 双 log 轴上面板字母会跑到中间 | 不要用"数据范围的百分比"猜位置。`Page.letter()` / `caption()` 按**页面 mm** 定位：`style.place_mm()` 把 mm 换成数据坐标（log 轴按对数插值）再写文字对象的 `x1/y1`（左上角） |
| 14 | `add_label` 文字对象用 `set_float('pt', 18)` 设字号不准（2026 实测 18 → 21.8 pt）；`pt` / `size` / `fontsize` 都不是正确属性 | 用 `<对象名>.fsize=18;`（2026 实测 PDF 里正好 18.0 pt）。`style.text_label()` 已内置；对象名取 `lab.name` |
| 15 | 手搓右 Y 轴（`add_layer(2)`）在 2026 上刻度会跑到内侧、量程串到左轴 | **用 Origin 自带双 Y 模板**：`op.new_graph(template='doubley')` → 得到 2 个层，`g[0]` 左轴、`g[1]` 右轴。把右层 `layer.x.showAxes/labels=0`，各自 `rescale()` + 各自设 y 范围，就是标准的双 Y 图（`examples/tpl_dtg_dual.py` 就是这么做的） |
| 16 | 给 X 轴换类别名用 `layer.x.label.type=10` 会变方框（和 Times New Roman 冲突） | 用 `Page.categories(i, names)`：关掉 X 刻度数字，按 mm 把类别名居中写在轴下 |
| 17 | 轴标题被自动改成列名（显示成 "w 5 °C (%)" 之类） | Origin 会把标题自动绑定到列 long name。要么把列 long name 直接起成 `Weight (%)` / `DTG (%/℃)`，要么别用 `layer.x.title$=`；用 `gl.axis('x').title = ...` 之前先把列名改好 |
| 18 | **双 Y 图的轴颜色会跟着该层第一条曲线变**（右轴变蓝、左轴变红） | 先在该层画一条 `transparency = 100` 的黑色引导线（`p.color='#000000'; p.transparency=100`），轴就固定成黑色，随后再画彩色曲线。左右两层都要做 |
| 19 | 不显式设字号，就会用 Origin 默认尺寸 | 刻度数字每层写 `layer.x.label.pt` / `layer.y.label.pt`；轴标题见 #30；字体见 #20 |
| 20 | **`layer.x.label.font="Times New Roman"` 静默失效**（PDF 里仍是 SimSun） | `layer.axis.label.font` 是**数字型 Windows 字体索引**，必须 `layer.x.label.font=font(Times New Roman);` 轴**标题**则是 text 对象：`xb.font=font(...); yl.font=font(...); xt.font=...; yr.font=...;`（`layer.x.title.font` 无效）。验证方法：导出 PDF，用 PyMuPDF 看 `get_page_fonts()` 里有没有 `TimesNewRomanPSMT` |
| 21 | **`gl.lt_exec()` 里的 `layer.xxx` 只作用于"当前激活层"**，不是 `gl` 对应的那层;而 `page.active` 又是作用在"当前激活窗口"上的 | 双 Y 图（doubley 右层）最典型：不切层就写样式，全落到左层或无效 → 右轴刻度朝外、字体宋体。正确顺序是**两步**：`op.lt_exec('win -a ' + 图页名)` 再 `op.lt_exec(f'page.active={gl.index()+1}')`。`ogfig.style.apply_axes()` 已内置 |
| 22 | **`doubley` 的第二层里，右边看得见的是 `y2`，`y` 是内侧隐藏轴** | 在右层写样式必须用 `layer.y2.*`：`y2.ticks=1`（朝内）、`y2.label.font=font(Times New Roman)`、`y2.label.pt=14`、`y2.from/to/inc`。写到 `layer.y` 上全部无效、且不报错 —— 这一条是用户手工改完对比出来的（`y2.ticks 10→1`、`y2.label.font 1→349` 两处就对了） |
| 23 | **多图层重叠时，底层那层的右边框刻度会和上层的右轴刻度叠成两套** | 底层（doubley 的 layer1）把右边框设成"只画线"：`layer.y2.ticks=0; layer.y2.ticklength=0;`（**别动 showAxes**，否则框线一起消失）。右轴刻度只由上层 `layer2.y2` 负责。同理上边框：`layer.x2.ticks=0; layer.x2.ticklength=0;` |
| 24 | 在 2026 里 `layer.y2.showLabels=0` / `layer.x2.showLabels=0` 会把**主轴（左/下）的标签一起关掉** | 只想关"边框那侧"的刻度时，只设 `ticks=0` 和 `ticklength=0`，不要碰 `showLabels` |
| 25 | **Origin 的文字分四套属性，字体各管各的**，只设一处就会留宋体 | ① 刻度标签 `layer.x.label.font=font(Times New Roman)`；② 轴标题 `xb.font= / yl.font= / xt.font= / yr.font=`；③ **图例 `legend.font=`**；④ **数据标签 `layer.plotN.label.font=`（饼图百分比、柱顶数字都在这）**。四类全设完，用 PDF 检查：`fitz` 读 `get_page_fonts()`，只应看到 `TimesNewRomanPSMT`（中文才允许 SimSun） |
| 26 | 写了 `page.width` / `page.height`，读回来宽度却不对（180 mm 变成 183.4 mm） | 页面默认锁宽高比（`page.kar=1`）：改高会按比例带走宽。先 `page.kar=0;` 再写宽高，单位是像素（`page.resx` 每英寸，2026 默认 600）。`style.set_page_mm()` 已内置 |
| 27 | 多面板里刻度数字、轴标题比设定的小一号（14 pt 变 12.7 pt） | 层缩小后 Origin 自动把 `layer.factor` 降到 0.9，层内文字整体缩放。定位后写 `layer.factor=1;`（`Page._layout` 已内置） |
| 28 | **曲线细得几乎看不见**（0.004 pt） | `set <plot> -w` 的单位是 **1/500 pt**：1 pt 要写 `-w 500`。原来写 `-w 2.0` 等于 0.004 pt。`style.line_width_cmd(pt)` 已换算，`Page.plot(width=1.2)` 直接给 pt |
| 29 | **从 .otpu 模板新建的图，文字全回到 SimSun**；空标题被存成隐藏（`show=0`） | 模板只记住页面、层位置、刻度、线宽、字号，不记字体。出图时照样跑 `Page.style()` / `apply_axes()` 刷字体；`style.title_style()` 会把有文字的标题重新 `show=1` |
| 30 | **多层页面里轴标题字号设不动**（Origin 默认 22 pt，成图 21.8 pt） | `layer.y.title.pt=` 和 LabTalk `yl.fsize=` 在 add_layer 加出来的层里会落空。走对象 API：`gl.label('yl').set_float('fsize', 8)`、`set_int('font', font索引)`。`style.title_style()` 已内置 |
| 31 | 饼图百分比、柱顶数值的字号 `layer.plotN.label.pt=` 无效 | 数据标签字号是 **`layer.plotN.label.fsize`**；图例是 `legend.fsize`。`style.set_fonts()` 已内置 |
| 32 | add_layer 加的层，上 / 右边框比左 / 下边框粗 | 边框线宽按轴分开存：`layer.x2.thickness` / `layer.y2.thickness` 也要设。`apply_axes()` 已内置 |
| 33 | `gl.xscale` 读回来是整数码，不是字符串 | 1 = linear、2 = log10、8 = ln、9 = log2；写入时才用 `'log10'`。判断 log 轴用 `style.is_log(gl, 'x')`（原来字符串判断永远为假，导致 (d) 面板字母错位） |
| 34 | 希腊字母用 `\g(q)` 转义，PDF 里是 Symbol 字体 | 直接写 Unicode（`2θ (°)`、`Δp`、`μm`），Times New Roman 自带这些字形 |
| 35 | 双 Y 右层里自己的 `yl` / `xb` 标题会显示出来，压在左层标题上 | 右层只保留 `yr`，`yl` / `xb` 设 `show=0`；右轴标题外移 1 mm 防止压到刻度数字。`apply_dual_axes()` 已内置 |
| 36 | **3D 饼的扇形颜色改不了**：`set -c color(...)` 只把整个饼刷成一个色；`layer.pie3d / pie.tilt / pie.thickness / pie.depth` 这些候选属性名读回来全是 nan（不存在） | 扇形色 = Origin 系统色序（By Points），脚本读不到也写不了。要配色一致就反过来：导出一次取色，再把同图的柱子 / 曲线刷成那 5 个扇区色；或在 GUI 的 Plot Details 里改 Color List。见 `catalog/production/bar_pie3d.py` |
| 37 | **文字对象加粗无效**：`label.set_int('bold',1)`、LabTalk `<name>.bold=1` 都静默失败，PDF 里仍是 `TimesNewRomanPSMT` | 目前无解，接受常规字重（字号仍按 9 pt）。别试 `<name>.font=font(Times New Roman:bold)`——会把字形打成一排乱码（同 #12） |
| 38 | **`add_label` / `text_label` 的 x1/y1 只吃 Python float**：传 numpy 标量（如 `np.arange` 的元素）→ `TypeError: argument 3 of type 'double'` | 调之前 `x, y = float(x), float(y)`；`Page.categories()` 传的是 Python int，所以平时不报错 |
