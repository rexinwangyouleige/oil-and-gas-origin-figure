# -*- coding: utf-8 -*-
"""模板 3 —— 叠谱图（XRD / XPS / Raman 通用）：竖排偏移 + 高亮区间 + 分隔虚线。

    python catalog/spectra/xrd_stack.py
"""
import os
import sys

import numpy as np

SKILL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, SKILL)

from ogfig import Page, export, style          # noqa: E402

OUT = os.path.join(SKILL, 'catalog', 'out')
os.makedirs(OUT, exist_ok=True)

rng = np.random.default_rng(5)

two_theta = np.linspace(5, 45, 900)
labels = ['A  fresh', 'B  30 min', 'C  60 min', 'D  120 min', 'E  240 min']
PEAKS = [(10.2, 1.00, 0.35), (11.6, 0.55, 0.30), (17.4, 0.42, 0.40),
         (20.0, 0.95, 0.30), (24.6, 0.60, 0.45), (32.1, 0.75, 0.35)]


def pattern(scale):
    y = np.zeros_like(two_theta)
    for pos, amp, wid in PEAKS:
        y += amp * scale * np.exp(-((two_theta - pos) / wid) ** 2)
    y += rng.normal(0, 0.006, two_theta.size)
    return y


pg = Page(rows=1, cols=1, size_mm=(90, 110), template='og_stack', lname='OGFIG_STACK')
ws = pg.sheet('XRD', 7)
ws.from_list(0, two_theta, lname='2theta', units='degree')

scales = [1.00, 0.86, 0.72, 0.55, 0.38]
OFFSET = 1.15
for i, (lab, s) in enumerate(zip(labels, scales)):
    y = pattern(s) + i * OFFSET
    ws.from_list(1 + i, y, lname=lab)

for i in range(len(labels)):
    pg.plot(0, ws, 1 + i, 0, kind='l', color=style.C[i % len(style.C)])

gl = pg.layer(0)
gl.rescale()
pg.style(0, '2θ (°)', 'Intensity (a.u.)')     # 直接写 Unicode θ：用 \g(q) 会走 Symbol 字体
style.limits(gl, x=(5, 45), y=(-0.3, len(labels) * OFFSET + 0.2), xinc=10)
style.activate(gl)
gl.lt_exec('layer.y.showLabels=0; layer.y.ticks=0;')     # 叠谱 Y 轴不显示刻度（放在 style 之后）

# 每条谱线右端标样品名，同色
for i, lab in enumerate(labels):
    style.text_label(gl, lab.split('  ')[-1], 35.5, i * OFFSET + 0.55, color=style.C[i % len(style.C)])

# 高亮两个特征区（用半透明色块的方式：Origin 里用 add_line 画不出填充，这里用文字区标注）
for x0, x1, lab in ((9.2, 11.2, '(001)'), (23.2, 25.8, '(110)')):
    ytop = len(labels) * OFFSET + 0.05
    pg.annotate(0, lab, x0 + 0.2, ytop, color='#404040')

# 每条谱线的基线用细虚线分隔（line 对象）
for i in range(1, len(labels)):
    yline = i * OFFSET - 0.55
    try:
        ln = gl.add_line(5.5, yline, 44.5, yline)
        if ln:
            ln.width = 1
    except Exception as e:
        print('add_line skipped:', str(e)[:50])

pg.drop_legends()
pg.finish()

paths = export.save(pg.g, os.path.join(OUT, 'xrd_stack.png'))
print(export.report(pg.g, paths))
