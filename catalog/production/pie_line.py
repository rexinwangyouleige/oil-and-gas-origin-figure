# -*- coding: utf-8 -*-
"""组合图验证：左 = 饼图（产量构成），右 = 折线（含水率趋势）。

关键：一个页面里用两个**不同类型的层**
  layer1 = Pie 层（模板 pie 自带）
  layer2 = 普通 Line 层（add_layer(0) 加出来）
两层都默认铺满整页，必须自己按百分比定位。
"""
import os
import sys

import numpy as np
import originpro as op

SKILL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, SKILL)
from ogfig import export, style          # noqa: E402

OUT = os.path.join(SKILL, 'catalog', 'out')
os.makedirs(OUT, exist_ok=True)
FONT = style.F_LATIN
PT_TICK, PT_TITLE, PT_NOTE = (style.PREFS[k] for k in ('fs_tick', 'fs_title', 'fs_note'))
AX, TL = style.DEFAULTS['axis_thickness'], style.DEFAULTS['tick_length']
C = ["#2C6FAF", "#2A9D8F", "#C9A227", "#C0504D", "#7B5AA6"]


op.new()
op.attach()
op.set_show(True)

for p in list(op.pages()):
    try:
        if (p.lname or '').startswith('PIE_'):
            p.destroy()
    except Exception:
        pass

wb = op.new_book(lname='PIE_data')
if isinstance(wb, list):
    wb = wb[0]
ws1 = wb[0]
ws1.name = 'SHARE'
ws1.cols = 3
blocks = ['B-01', 'B-02', 'B-03', 'B-04', 'B-05']
share = np.array([28.0, 24.0, 21.0, 16.0, 11.0])
ws1.from_list(0, share, lname='Share (%)')
ws1.from_list(1, np.arange(1, 6), lname='Index')
ws1.from_list(2, blocks, lname='Block')

ws2 = wb.add_sheet('WC')
ws2.cols = 2
month = np.arange(1, 13)
wc = np.array([18, 21, 24, 27, 31, 36, 42, 49, 55, 61, 66, 70], dtype=float)
ws2.from_list(0, month, lname='Month')
ws2.from_list(1, wc, lname='Water cut (%)')

# ---------------- 页面：pie 模板 + 再加一个 line 层 ----------------
g = op.new_graph(template='pie2d', lname='PIE_LINE')
style.set_page_mm(g, 180, 80)              # 真实毫米，pt 即成图字号
PIE, LINE = g[0], g.add_layer(0)
print('layers:', len(g), '| pie idx', PIE.index(), '| line idx', LINE.index())

# 左半 = 饼图，右半 = 折线
for gl, (left, top, w, h) in ((PIE, (8, 12, 36, 74)), (LINE, (54, 12, 40, 74))):
    style.activate(gl)
    gl.lt_exec('layer.left=%d; layer.top=%d; layer.width=%d; layer.height=%d;' % (left, top, w, h))

# ---------------- 饼图 ----------------
style.activate(PIE)
p = PIE.add_plot(ws1, 0, 2, -1, '?')   # 用文本类别列，饼图自带图例就会显示区块名
print('pie plot:', p)
PIE.lt_exec('layer.x.showAxes=0; layer.y.showAxes=0;')
PIE.lt_exec('layer.x.showLabels=0; layer.y.showLabels=0;')
PIE.lt_exec('layer.x2.showAxes=0; layer.y2.showAxes=0;')
# 尽量转 2D（不同版本属性名可能不同，失败就保持默认）
for cmd in ('layer.pie3d=0;', 'layer.pie.depth=0;', 'layer.pie3dangle=0;'):
    try:
        PIE.lt_exec(cmd)
    except Exception:
        pass
# 每一块单独上色
try:
    for i in range(len(share)):
        PIE.lt_exec('set -c color(%d,%d,%d);' % tuple(int(C[i][j:j + 2], 16) for j in (1, 3, 5)))
except Exception:
    pass

# ---------------- 折线 ----------------
style.activate(LINE)
lp = LINE.add_plot(ws2, 1, 0, -1, 'l')
if lp:
    lp.color = C[0]
mk = LINE.add_plot(ws2, 1, 0, -1, 's')
if mk:
    mk.color = C[0]
    mk.symbol_kind = 2
    mk.symbol_size = style.DEFAULTS['symbol_size']
LINE.rescale()
LINE.lt_exec('layer.y.from=0; layer.y.to=80; layer.y.inc=20;')
LINE.lt_exec('layer.x.from=0; layer.x.to=13; layer.x.inc=2;')
LINE.lt_exec(f'layer.y.ticks=1; layer.y.ticklength={TL}; layer.y.minorTicks=0;')
LINE.lt_exec(f'layer.x.ticks=1; layer.x.ticklength={TL}; layer.x.minorTicks=0;')
LINE.lt_exec('layer.x2.ticks=0; layer.x2.ticklength=0;')
LINE.lt_exec('layer.y2.ticks=0; layer.y2.ticklength=0;')
LINE.lt_exec(f'layer.y.thickness={AX}; layer.x.thickness={AX}; layer.factor=1;')
LINE.lt_exec(f'layer.x.label.pt={PT_TICK}; layer.y.label.pt={PT_TICK};')
LINE.lt_exec(f'layer.x.title.pt={PT_TITLE}; layer.y.title.pt={PT_TITLE};')
LINE.lt_exec(f'layer.x.label.font=font({FONT}); layer.y.label.font=font({FONT});')
LINE.lt_exec(f'xb.font=font({FONT}); yl.font=font({FONT});')
LINE.axis('x').title = 'Month'
LINE.axis('y').title = 'Water cut (%)'
style.title_style(LINE, ('xb', 'yl'), PT_TITLE)

try:                                  # 只删折线层的图例，保留饼图的（它列出区块名）
    _lb = LINE.label('legend')
    if _lb:
        _lb.remove()
    # 图例字体：legend.font 是数字字体索引，必须用 font()
    PIE.lt_exec('legend.font=font(%s); legend.fsize=%g;' % (FONT, PT_NOTE))
    # 饼图扇形上的百分比是"数据标签"，属性在 layer.plotN.label.font
    PIE.lt_exec('layer.plot1.label.font=font(%s);' % FONT)
    PIE.lt_exec('layer.plot1.label.fsize=%g;' % PT_NOTE)   # 数据标签字号是 fsize（坑 #31）
except Exception:
    pass

# 标注：只在最左侧放短名字，百分比由饼图自己标在扇形上
# 名字已由饼图图例给出，这里不再重复标注
style.text_label(LINE, 'Water cut', 1.0, 74, color=C[0], pt=PT_NOTE)

op.lt_exec('doc -uw')
paths = export.save(g, os.path.join(OUT, 'pie_line.png'))
print(export.report(g, paths))
