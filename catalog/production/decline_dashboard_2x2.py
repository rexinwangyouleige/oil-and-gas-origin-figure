# -*- coding: utf-8 -*-
"""Example 1 — production / decline dashboard (2x2, 180 mm double column).

    python catalog/production/decline_dashboard_2x2.py

The four panels an O&G production paper usually needs:
  (a) gas rate on a semi-log axis with a fitted Arps decline
  (b) water cut build-up for two wells
  (c) post-treatment cumulative gas, bars with error bars
  (d) pressure-transient log-log diagnostic (dp and t*dp/dt)
"""
import os
import sys

import numpy as np

SKILL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, SKILL)

from ogfig import Page, data, export, style          # noqa: E402

OUT = os.path.join(SKILL, 'catalog', 'out')
os.makedirs(OUT, exist_ok=True)

rng = np.random.default_rng(2026)

# ----------------------------------------------------------------- (a) decline
t = np.linspace(5, 900, 60)
q_true = data.arps(t, qi=58.0, Di=0.0034, b=0.78)
q_obs = q_true * (1 + rng.normal(0, 0.035, t.size))
fit = data.fit_arps(t, q_obs)
t_fit = np.linspace(t.min(), t.max(), 200)
q_fit = data.arps(t_fit, fit['qi'], fit['Di'], fit['b'])

# ---------------------------------------------------------------- (b) water cut
t2 = np.linspace(0, 1200, 80)
wc_a = 100.0 / (1.0 + np.exp(-(t2 - 620) / 140.0))
wc_b = 100.0 / (1.0 + np.exp(-(t2 - 880) / 190.0)) * 0.92

# ------------------------------------------------------------------ (c) cum gas
labels = ['Baseline', 'Acid', 'Frac', 'Frac+surf']
cum = np.array([1.62, 1.94, 2.31, 2.58])
cum_err = np.array([0.08, 0.09, 0.11, 0.10])

# ------------------------------------------------------------------- (d) PTA
tp = np.logspace(-1, 3.0, 90)
dp = 0.9 * tp ** 0.35 * (1 - np.exp(-tp / 3.0)) + 0.004 * tp
dder = data.pressure_derivative(tp, dp)

# ======================================================================= build
pg = Page(rows=2, cols=2, journal='double')

ws = pg.sheet('DEC', 4)
ws.from_list(0, t, lname='Time', units='d')
ws.from_list(1, q_obs, lname='Measured', units='10^4 m3/d')
ws.from_list(2, q_true, lname='Arps fit')

ws_w = pg.sheet('WC', 3)
ws_w.from_list(0, t2, lname='Time', units='d')
ws_w.from_list(1, wc_a, lname='Well A-12')
ws_w.from_list(2, wc_b, lname='Well B-07')

ws_b = pg.sheet('CUM', 9)
ws_b.from_list(0, np.arange(1, 5), lname='Index')
for i in range(4):
    col = np.full(4, np.nan)
    col[i] = cum[i]
    ws_b.from_list(1 + i, col, lname=labels[i], units='10^8 m3')
    ecol = np.full(4, np.nan)
    ecol[i] = cum_err[i]
    ws_b.from_list(5 + i, ecol, lname='err')

ws_p = pg.sheet('PTA', 3)
ws_p.from_list(0, tp, lname='Time', units='h')
ws_p.from_list(1, dp, lname='dp')
ws_p.from_list(2, dder, lname='Derivative')

# (a) semi-log decline with fitted line
pg.plot(0, ws, 'B', kind='s', color=style.OG[0], size=3)
pg.plot(0, ws, 'C', kind='logy', color=style.FIT_GRAY, dash=2, width=1.2)
pg.style(0, 'Production time (d)', 'q\\-(g) (10\\+(4) m\\+(3)/d)')
pg.annotate(0, 'Arps %s, b = %.2f' % (fit['model'], fit['b']), 420, 55, style.GRAY)
pg.annotate(0, 'R\\+(2) = %.3f' % fit['R2'], 420, 44, style.GRAY)
pg.layer(0).lt_exec('layer.y.from=8; layer.y.to=70; layer.x.from=0; layer.x.to=960;')

# (b) water cut
pg.plot(1, ws_w, 'B', kind='l', color=style.OG[1])
pg.plot(1, ws_w, 'C', kind='l', color=style.OG[4], dash=3)
pg.style(1, 'Production time (d)', 'Water cut (%)')
style.limits(pg.layer(1), x=(0, 1200), y=(0, 100), xinc=400, yinc=20)
pg.annotate(1, 'A-12', 300, 12, style.OG[1])
pg.annotate(1, 'B-07', 700, 55, style.OG[4])

# (c) bars with error bars
pg.bar(2, ws_b, 0, [1, 2, 3, 4], errs=[5, 6, 7, 8], colors=style.OG[:4])
pg.style(2, '', 'Cumulative gas (10\\+(8) m\\+(3))')
style.limits(pg.layer(2), x=(0.4, 4.6), xinc=1)
pg.categories(2, labels)                     # 类别名：关掉刻度数字，按 mm 写在轴下（坑 #16）

# (d) pressure transient log-log
pg.plot(3, ws_p, 'B', kind='loglog', color=style.OG[0])
pg.plot(3, ws_p, 'C', kind='loglog', color=style.OG[1], dash=2)
pg.style(3, 'Elapsed time (h)', '\u0394p (MPa)')
pg.annotate(3, "t\u00b7dp/dt", 40, 0.05, style.OG[1])

pg.drop_legends()
for i, ch in enumerate('abcd'):
    pg.letter(i, ch)
pg.finish()

paths = export.save(pg.g, os.path.join(OUT, 'decline_dashboard_2x2.png'))
print(export.report(pg.g, paths))
