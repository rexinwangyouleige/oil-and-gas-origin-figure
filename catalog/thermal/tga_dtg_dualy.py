# -*- coding: utf-8 -*-
"""TG + DTG 双 Y 轴（页岩油-CO2 三个温度，读真实 xlsx）。

    python catalog/thermal/tga_dtg_dualy.py

左层：Weight (%)，实线；右层：DTG (%/℃)，同色虚线 —— 同一样品同色，TG / DTG 靠线型区分。
数据：SRC 目录下每个 xlsx 前两行是表头，三列为 T / w / 其他。
"""
import os
import sys

import numpy as np
import pandas as pd

SKILL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, SKILL)
from ogfig import DualY, export, style        # noqa: E402

SRC = r"C:\Users\lvmeng\Desktop\shale oil"
OUT = os.path.join(SKILL, 'catalog', 'out')
os.makedirs(OUT, exist_ok=True)
C = style.THERM[:3]
FILES = [("5 ℃", "页岩油-CO2-5℃-min.xlsx"),
         ("10 ℃", "页岩油-CO2-10℃-min.xlsx"),
         ("20 ℃", "页岩油-CO2-20℃-min.xlsx")]


def smooth(y, win=121):
    # 两端补边，避免 convolve('same') 的零填充把首尾 DTG 拉出假台阶
    pad = win // 2
    ypad = np.r_[np.full(pad, y[0]), y, np.full(pad, y[-1])]
    return np.convolve(ypad, np.ones(win) / win, mode='valid')


pg = DualY(journal='single', lname='DTG_DUAL')
ws = pg.sheet('TGA', 1 + 3 * len(FILES))
ws.from_list(0, np.zeros(1), lname='pad')

series, col = [], 1
for label, fn in FILES:
    df = pd.read_excel(os.path.join(SRC, fn), header=None, skiprows=2)
    df.columns = ['T', 'w', 'K']
    df = df.apply(pd.to_numeric, errors='coerce').dropna()
    m = (df['T'] >= 35) & (df['T'] <= 800)
    grid = np.linspace(35, 800, 700)
    w = np.interp(grid, df['T'][m].to_numpy(), df['w'][m].to_numpy())
    dtg = -np.gradient(smooth(w), grid)
    dtg[dtg < 0] = 0
    # 坑 #17：轴标题会绑定第一条曲线的列 long name，所以第一组直接起成标题文字
    ws.from_list(col, grid, lname='Temperature (℃)' if col == 1 else 'T ' + label)
    ws.from_list(col + 1, w, lname='Weight (%)' if col == 1 else 'w ' + label)
    ws.from_list(col + 2, dtg, lname='DTG (%/℃)' if col == 1 else 'DTG ' + label)
    series.append((label, col, col + 1, col + 2))
    col += 3

pg.guide(ws, series[0][2], series[0][1])
for k, (label, cx, cw, cd) in enumerate(series):
    pg.plot(0, ws, cw, cx, kind='l', color=C[k], width=1.2)
pg.guide(ws, series[0][3], series[0][1], right=True)
for k, (label, cx, cw, cd) in enumerate(series):
    pg.plot_right(ws, cd, cx, kind='l', color=C[k], dash=2)

pg.style_dual('Temperature (℃)', 'Weight (%)', 'DTG (%/℃)')
style.limits(pg.left, x=(0, 800), y=(0, 105), xinc=200, yinc=20)
style.activate(pg.right)
pg.right.lt_exec('layer.x.from=0; layer.x.to=800; layer.y.from=0; layer.y.to=0.62; layer.y.inc=0.1;'
                 'layer.y2.from=0; layer.y2.to=0.62; layer.y2.inc=0.1;')

pg.drop_legends()
for k, (label, *_ ) in enumerate(series):
    style.text_label(pg.left, label, 600, 98 - 9 * k, color=C[k])
pg.finish()

paths = export.save(pg.g, os.path.join(OUT, 'tga_dtg_dualy.png'))
print(export.report(pg.g, paths))
