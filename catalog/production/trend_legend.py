# -*- coding: utf-8 -*-
"""图例 + 风格档演示：三口井的产油量递减曲线。

三件事一次说清：
  1. **图例**：`pg.legend(0)` 自动建图例，条目文字直接来自工作表的**列 long name**（中文 + 西文混排），
     无边框，自动挑四个角里最空的那个；四角都占满时页面上边自动加高、放右上角。
  2. **风格档**：`style.set_preset('bold')` 切成"明显版"（字号 10、线 2.0 pt、轴 1.5 pt、刻度长 4.5）。
  3. **自检**：export.report 会按当前档位的字号范围校验（normal 7–9 / bold 9–11）。

运行：
    python catalog/production/trend_legend.py          # 常规档 + 自动找空白角
    python catalog/production/trend_legend.py bold     # 明显版
    python catalog/production/trend_legend.py grow     # 四角都占满 → 加高页面放右上角
输出：catalog/out/trend_legend[_bold|_grow].png / .tif / .pdf / .opju / _gray.png
"""
import os
import sys

import numpy as np
import originpro as op

SKILL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, SKILL)
from ogfig import Page, export, style          # noqa: E402

OUT = os.path.join(SKILL, 'catalog', 'out')
os.makedirs(OUT, exist_ok=True)

MODE = (sys.argv[1] if len(sys.argv) > 1 else 'normal').lower()
if MODE not in ('normal', 'bold', 'grow'):
    raise SystemExit('用法：python catalog/production/trend_legend.py [normal|bold|grow]')

if MODE == 'bold':
    style.set_preset('bold')                   # 字号 10 / 线 2.0 pt / 轴 1.5 pt
print('preset =', style.PREFS['preset'], '| fs_tick/title/note =',
      style.PREFS['fs_tick'], style.PREFS['fs_title'], style.PREFS['fs_note'])

# ---------------- 演示数据：三口井的产油量（10⁴ t）随生产时间（月）递减 ----------------
t = np.arange(1, 25, 2, dtype=float)           # 1..23 月，每 2 月一个点
WELLS = [
    ('A 井 q\\-(o) (10\\+(4) t)', 100.0, 0.085),
    ('B 井 q\\-(o) (10\\+(4) t)', 78.0, 0.062),
    ('C 井 q\\-(o) (10\\+(4) t)', 55.0, 0.041),
]
curves = [(name, qi * np.exp(-d * t)) for name, qi, d in WELLS]

pg = Page(1, 1, journal='single', lname='OGFIG_LEGEND')
ws = pg.sheet('PROD', 1 + len(WELLS))
ws.from_list(0, t, lname='生产时间 t', units='month')
for k, (name, y) in enumerate(curves):
    ws.from_list(1 + k, y, lname=name)

for k in range(len(WELLS)):
    pg.plot(0, ws, 1 + k, 0, kind='ls', color=style.C[k], width=style.DEFAULTS['line_width'])
style.apply_axes(pg.layer(0), '生产时间 Time (month)', '产油量 Production (10\\+(4) t)')
pg.layer(0).rescale()
style.limits(pg.layer(0), x=(0, 24), y=(0, 120), xinc=4, yinc=20)

if MODE == 'grow':                             # 故意把四个角都占住，逼出"加高页面"分支
    env = pg.sheet('ENV', 3)
    env.from_list(0, np.array([0.0, 24.0]), lname='生产时间 t')
    env.from_list(1, np.array([5.0, 115.0]), lname='上包络 Envelope (10\\+(4) t)')
    env.from_list(2, np.array([115.0, 5.0]), lname='下包络 Envelope (10\\+(4) t)')
    pg.plot(0, env, 1, 0, kind='l', color=style.GRAY, dash=3)
    pg.plot(0, env, 2, 0, kind='l', color=style.GRAY, dash=3)

pg.layer(0).rescale()
style.limits(pg.layer(0), x=(0, 24), y=(0, 120), xinc=4, yinc=20)

where = pg.legend(0)                           # ← 自动找空白角；没地方就加高页面
print('legend corner:', where, '| scores:', pg.legend_scores)
print('page mm:', tuple(round(v, 1) for v in pg.size_mm))

pg.finish()
name = 'trend_legend' if MODE == 'normal' else 'trend_legend_%s' % MODE
paths = export.save(pg.g, os.path.join(OUT, name + '.png'))
print(export.report(pg.g, paths))
