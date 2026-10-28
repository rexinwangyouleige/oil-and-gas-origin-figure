# -*- coding: utf-8 -*-
"""柱状（月产油量）+ 折线（含水率），双 Y 轴。

    python catalog/production/bar_line_dualy.py

  · DualY：og_doubley 模板，左层柱、右层线（坑 #15、#22）
  · 每层先画透明黑引导线，轴颜色不跟曲线走（坑 #18）
  · 曲线标注直接写在线旁，不用图例
"""
import os
import sys

import numpy as np

SKILL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, SKILL)
from ogfig import DualY, export, style        # noqa: E402

OUT = os.path.join(SKILL, 'catalog', 'out')
os.makedirs(OUT, exist_ok=True)
C_BAR, C_LINE = style.C[0], style.C[2]

rng = np.random.default_rng(7)
month = np.arange(1, 13)
oil = np.array([2.8, 2.6, 2.9, 3.2, 3.4, 3.3, 3.0, 2.7, 2.9, 3.1, 3.0, 2.8])
oil = np.round(oil + rng.normal(0, 0.06, oil.size), 2)
wc = np.array([18, 21, 24, 27, 31, 36, 42, 49, 55, 61, 66, 70], dtype=float)

pg = DualY(journal='single', lname='COMBO')
ws = pg.sheet('MONTH', 3)
ws.from_list(0, month, lname='Month')
ws.from_list(1, oil, lname='Oil production')
ws.from_list(2, wc, lname='Water cut')

# 左层：柱
pg.guide(ws, 1)
pg.bar(0, ws, 0, [1], colors=[C_BAR])
# 右层：线 + 实心点
pg.guide(ws, 2, right=True)
pg.plot_right(ws, 2, 0, kind='ls', color=C_LINE)

pg.style_dual('Month', 'Oil production (10\\+(4) t)', 'Water cut (%)')
style.limits(pg.left, x=(0.4, 12.6), y=(0, 4.5), xinc=1, yinc=1)
style.activate(pg.right)
pg.right.lt_exec('layer.x.from=0.4; layer.x.to=12.6; layer.y.from=0; layer.y.to=90; layer.y.inc=20;'
                 'layer.y2.from=0; layer.y2.to=90; layer.y2.inc=20;')

pg.drop_legends()
pg.caption(0, 'Oil production', where='tl')
style.text_label(pg.right, 'Water cut', 8.6, 80, color=C_LINE)
pg.finish()

paths = export.save(pg.g, os.path.join(OUT, 'bar_line_dualy.png'))
print(export.report(pg.g, paths))
