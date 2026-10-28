# -*- coding: utf-8 -*-
"""瀑布图（waterfall）：6 条升温速率下的 TGA 曲线，按 Y 方向错位叠放。

说明：Origin 自带 WATER3D.otp（3D 瀑布）/ WATERFAL.otp（2D 瀑布）两个模板，
但用脚本 plotxy 驱动时只能得到"实心墙体"或单条曲线，分组的 6 条曲线出不来；
这里用 origin 里最稳的"错位叠层"做法，视觉上就是标准瀑布图，而且完全可控。
"""
import os
import sys

import numpy as np
import originpro as op

SKILL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, SKILL)
from ogfig import export, style              # noqa: E402

OUT = os.path.join(SKILL, 'catalog', 'out')
os.makedirs(OUT, exist_ok=True)
FONT = style.F_LATIN
PT_TICK, PT_TITLE, PT_NOTE = (style.PREFS[k] for k in ('fs_tick', 'fs_title', 'fs_note'))
AX, TL = style.DEFAULTS['axis_thickness'], style.DEFAULTS['tick_length']
C = style.C

rates = ['5 ℃/min', '10 ℃/min', '15 ℃/min', '20 ℃/min', '25 ℃/min', '30 ℃/min']
CX = (list(C) + [style.GRAY] * len(rates))[:len(rates)]   # 6 条：THERM 5 色 + 深灰


op.new()
op.attach()
op.set_show(True)

for p in list(op.pages()):
    try:
        if (p.lname or '').startswith('WF_'):
            p.destroy()
    except Exception:
        pass

T = np.linspace(30, 800, 400)
OFFSET = 58.0
ws_data = []
for k, rate in enumerate(rates):
    # 升温速率越高，失重曲线整体右移
    Tc = 300 + 22 * k
    w = 100 - (95 / (1 + np.exp(-(T - Tc) / (55 + 2 * k))))
    ws_data.append((rate, w + 0 * k))

g = op.new_graph(template='line', lname='WF_plot')
style.set_page_mm(g, 90, 110)              # 真实毫米，pt 即成图字号
gl = g[0]
style.activate(gl)
gl.lt_exec('layer.left=%.2f; layer.top=%.2f; layer.width=%.2f; layer.height=%.2f; layer.factor=1;'
           % (14 / 90 * 100, 5 / 110 * 100, 72 / 90 * 100, 94 / 110 * 100))   # 按 mm 留出轴标题

wb = op.new_book(lname='WF_data')
if isinstance(wb, list):
    wb = wb[0]
ws = wb[0]
ws.name = 'TGA'
ws.cols = 1 + 2 * len(rates)
ws.from_list(0, T, lname='Temperature (℃)')
for k, (rate, w) in enumerate(ws_data):
    ws.from_list(1 + 2 * k, w + k * OFFSET, lname=rate)
    ws.from_list(2 + 2 * k, np.full_like(T, k * OFFSET), lname='base')

# 画 6 条错位曲线 + 它们的基线（细灰线）
for k, (rate, w) in enumerate(ws_data):
    p = gl.add_plot(ws, 1 + 2 * k, 0, -1, 'l')
    if p:
        p.color = CX[k]
    b = gl.add_plot(ws, 2 + 2 * k, 0, -1, 'l')
    if b:
        b.color = '#C8C8C8'

gl.rescale()
gl.lt_exec('layer.x.from=30; layer.x.to=800; layer.x.inc=100;')
gl.lt_exec('layer.y.from=-8; layer.y.to=%d;' % int((len(rates) - 1) * OFFSET + 112))
gl.lt_exec('layer.y.showLabels=0; layer.y.ticks=0;')          # 瀑布图 Y 不显示刻度
gl.lt_exec(f'layer.x.ticks=1; layer.x.ticklength={TL}; layer.x.minorTicks=0;')
gl.lt_exec(f'layer.x.thickness={AX}; layer.y.thickness={AX}; layer.factor=1;')
gl.lt_exec('layer.x2.ticks=0; layer.x2.ticklength=0;')
gl.lt_exec(f'layer.x.label.pt={PT_TICK}; layer.x.title.pt={PT_TITLE};')
gl.lt_exec(f'layer.x.label.font=font({FONT});')
gl.lt_exec(f'xb.font=font({FONT}); yl.font=font({FONT});')
gl.axis('x').title = 'Temperature (℃)'
gl.axis('y').title = 'Weight (%, offset)'
style.title_style(gl, ('xb', 'yl'), PT_TITLE)

# 每条曲线右端标速率
for k, (rate, w) in enumerate(ws_data):
    style.text_label(gl, rate, 600, k * OFFSET + 30, color=CX[k], pt=PT_NOTE)   # 放在右端平台上方，不压曲线

try:
    lb = gl.label('legend')
    if lb:
        lb.remove()
except Exception:
    pass

op.lt_exec('doc -uw')
paths = export.save(g, os.path.join(OUT, 'waterfall.png'))
print(export.report(g, paths))
