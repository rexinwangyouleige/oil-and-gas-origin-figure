# -*- coding: utf-8 -*-
"""模板 2 —— 组合图：柱状（产量）+ 折线（含水率），左右并排共享类别轴。

    python catalog/production/bar_line_side_by_side.py

说明：真正的左右双 Y 轴用 Origin 自带 doubley 模板（见 bar_line_dualy.py）；
这里演示的是另一种排法：两个量各占一个面板，左右并排。
"""
import os
import sys

import numpy as np

SKILL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, SKILL)

from ogfig import Page, export, style          # noqa: E402

OUT = os.path.join(SKILL, 'catalog', 'out')
os.makedirs(OUT, exist_ok=True)

blocks = ['B-01', 'B-02', 'B-03', 'B-04', 'B-05']
cum = np.array([2.4, 3.1, 2.7, 3.8, 4.2])           # 10^8 m3
cum_err = np.array([0.18, 0.22, 0.16, 0.25, 0.20])
wc = np.array([38, 47, 55, 63, 71])                  # %

pg = Page(rows=1, cols=2, size_mm=(180, 70), lname='OGFIG_DUAL')

ws = pg.sheet('BLOCK', 4)
ws.from_list(0, np.arange(1, len(blocks) + 1), lname='Index')
ws.from_list(1, cum, lname='Cumulative gas', units='10^8 m3')
ws.from_list(2, cum_err, lname='err')
ws.from_list(3, wc, lname='Water cut', units='%')

# (a) 柱状 + 误差棒
pg.bar(0, ws, 0, [1], errs=[2], colors=[style.C[0]])
pg.style(0, '', 'Cumulative gas (10\\+(8) m\\+(3))')

# (b) 折线 + 标记
pg.plot(1, ws, 3, 0, kind='ls', color=style.C[2])
pg.style(1, '', 'Water cut (%)')

style.limits(pg.layer(0), x=(0.3, len(blocks) + 0.7), y=(0, 5.2), xinc=1, yinc=1)
style.limits(pg.layer(1), x=(0.3, len(blocks) + 0.7), y=(30, 80), xinc=1, yinc=10)
for i in (0, 1):
    pg.categories(i, blocks)                     # 类别名按 mm 居中写在轴下

pg.drop_legends()
pg.letter(0, 'a')
pg.letter(1, 'b')
pg.finish()

paths = export.save(pg.g, os.path.join(OUT, 'bar_line_side_by_side.png'))
print(export.report(pg.g, paths))
