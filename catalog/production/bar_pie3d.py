# -*- coding: utf-8 -*-
"""柱状图 + 3D 饼组合图，两种版式：

  inset（默认）= 一个坐标区里，3D 饼当**内嵌小图**（inset）压在坐标区右上角的空白处
  side         = 左右两个面板，饼图单占一块（180 × 80）

一页两个**不同类型的层**：
  layer0 = 3D Pie 层（Origin 自带模板 `pie`；2026b 上 `pie` 就是 3D、`pie2d` 才是 2D）
  layer1 = 普通 XY 层（`add_layer(0)` 加出来，当柱状用）
两层默认铺满整页，必须自己按毫米定位：内嵌时饼图层要落在**主轴框里面**（别压到上/右框线），
底边要让开第 3、4 根柱子的柱顶。

运行：python catalog/production/bar_pie3d.py          # inset
      python catalog/production/bar_pie3d.py side     # 并排双面板
输出：catalog/out/bar_pie3d_<layout>.png / .tif / .pdf / .opju / _gray.png + 自检报告

规范：Times New Roman 7–9 pt、刻度朝内、无次刻度、题注无框、字号与线宽只从 style 取。
    3D 饼是**用户指定**的图型（style-spec 里 3D 饼列在"别用"，只看占比时更推荐 2D 饼 / 横向柱）。
    唯一的例外是扇形配色：3D 饼的扇形颜色由 Origin 的系统色序（By Points）决定，脚本读不到也改不了
    单个扇形，所以柱状图画成同一组 5 色（WEDGE_C），靠颜色把柱子和扇区对起来。
坑：#1 层定位要 page.active、#21 切层、#25 四类文字各自的字体属性、#27 layer.factor、
    #31 饼图百分比用 `layer.plotN.label.fsize`（不是 `.pt`）
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
PT_TICK, PT_NOTE = (style.PREFS[k] for k in ('fs_tick', 'fs_note'))

LAYOUT = (sys.argv[1] if len(sys.argv) > 1 else 'inset').lower()
if LAYOUT not in ('inset', 'side'):
    raise SystemExit('用法：python catalog/production/bar_pie3d.py [inset|side]')

# 版式：页面 mm、柱状层、饼层（都是 左 / 上 / 宽 / 高，mm，上从页面顶部算）
SPEC = {
    # 内嵌：饼左边框 78 mm 落在第 4 根柱子右侧，底边 43 mm 让开 60 那根柱子（柱顶 44 mm）
    'inset': dict(page=(120, 80), bar=(14.0, 9.0, 102.0, 59.0), pie=(78.0, 10.0, 38.0, 33.0),
                  letters=False, bar_labels=False),
    'side': dict(page=(180, 80), bar=(14.0, 9.0, 74.0, 59.0), pie=(104.0, 9.0, 66.0, 62.0),
                 letters=True, bar_labels=True),
}
CFG = SPEC[LAYOUT]

# ---------------- 演示数据：5 个区块年产量，合计 400 ×10⁴ t ----------------
# 占比刻意取整（33 / 25 / 18 / 15 / 9 %）：Origin 的饼图百分比是"有效数字"格式，
# 数据不是整数占比时会出现 14% 和 14.0% 混排。
BLOCKS = ['Tahe', 'Shunbei', 'Hade', 'Yakela', 'Other']
PROD = np.array([132.0, 100.0, 72.0, 60.0, 36.0])
SHARE = PROD / PROD.sum() * 100.0            # 33 25 18 15 9 (%)
WEDGE_C = ['#F14040', '#1A6FDF', '#37AD6B', '#B177DE', '#CC9900']

LEGEND_ON_PIE = False                        # 饼图不给图例：区块名在柱状图的类别轴上


def _place_mm(gl, frame, page_mm):
    """按毫米定位一个层（top 从页面顶部算，坑 #1）。"""
    left, top, width, height = frame
    PW, PH = page_mm
    style.activate(gl)
    op.lt_exec('layer.left=%.3f; layer.top=%.3f; layer.width=%.3f; layer.height=%.3f; layer.factor=1;'
               % (left / PW * 100, top / PH * 100, width / PW * 100, height / PH * 100))


def bar_labels(pg, i, xs, ys, texts, dy_mm=3.0):
    """柱顶数值：按毫米把文字摆在柱子上方居中（不用 Origin 的数据标签，格式可控）。"""
    gl = pg.layer(i)
    frame = pg.frames[i]
    for x, y, t in zip(xs, ys, texts):
        x, y = float(x), float(y)          # add_label 的 x1/y1 只吃 float，numpy 标量会 TypeError
        lab = style.text_label(gl, t, x, y, pt=PT_TICK)
        if lab is None:
            continue
        w_mm, _ = style.text_size_mm(lab, pt=PT_TICK)
        xm, ym = style.data_to_mm(gl, frame, x, y)
        style.place_mm(gl, lab, frame, xm - w_mm / 2, ym - dy_mm - 1.6)


def centered_caption(i, text, y_mm=1.2):
    """饼图上方一句话说明"这是占比"，替代被删掉的图例（区块名在柱状图的类别轴上）。"""
    gl, frame = pg.layer(i), pg.frames[i]
    lab = style.text_label(gl, text, 0.0, 0.0, pt=PT_NOTE)
    if lab is None:
        return None
    w_mm, _ = style.text_size_mm(lab, pt=PT_NOTE)
    L, T, W, H = frame
    style.place_mm(gl, lab, frame, L + (W - w_mm) / 2.0, T + y_mm)
    return lab


# ---------------- 页面：pie 模板打底，再加一个 XY 层 ----------------
pg = Page(1, 2, template='pie', size_mm=CFG['page'], lname='OGFIG_BARPIE')
PIE, BAR = pg.layer(0), pg.layer(1)
pw, ph = pg.size_mm

pg.frames[BAR.index()] = CFG['bar']
pg.frames[PIE.index()] = CFG['pie']
_place_mm(BAR, pg.frames[BAR.index()], (pw, ph))
_place_mm(PIE, pg.frames[PIE.index()], (pw, ph))

ws = pg.sheet('PROD', 2 + len(BLOCKS))
ws.from_list(0, BLOCKS, lname='Block')
ws.from_list(1, PROD, lname='Production')
ws.from_list(2, np.arange(1, len(BLOCKS) + 1), lname='Index')
for k, name in enumerate(BLOCKS):            # 每个区块一列：只在自己那一行有值 → 单根柱，单色
    v = np.full(len(BLOCKS), np.nan)
    v[k] = PROD[k]
    ws.from_list(3 + k, v, lname=name)
print('layout %s | shares (%%) %s' % (LAYOUT, ', '.join('%.1f' % s for s in SHARE)))

# ---------------- (a) 柱状图 ----------------
style.activate(BAR)
made = []
for k in range(len(BLOCKS)):
    p = BAR.add_plot(ws, 3 + k, 2, -1, 'c')
    if p is None:
        continue
    p.color = WEDGE_C[k]
    made.append(p)
print('bar plots:', len(made))

style.apply_axes(BAR, '', 'Production (10\\+(4) t)')
BAR.rescale()
style.limits(BAR, x=(0.3, len(BLOCKS) + 0.7), y=(0, 150), yinc=30)
pg.categories(BAR.index(), BLOCKS)
if CFG['bar_labels']:
    bar_labels(pg, BAR.index(), np.arange(1, len(BLOCKS) + 1), PROD,
               ['%g' % v for v in PROD])

# ---------------- 3D 饼图 ----------------
style.activate(PIE)
pie = PIE.add_plot(ws, 1, 0, -1, '?')        # y=Production，x=Block（文本类别）→ 饼图自带区块名图例
print('pie plot:', pie)
PIE.lt_exec('layer.x.showAxes=0; layer.y.showAxes=0; layer.x2.showAxes=0; layer.y2.showAxes=0;')
PIE.lt_exec('layer.x.showLabels=0; layer.y.showLabels=0;')
try:
    style.set_fonts(PIE, nplots=1)           # 图例 / 扇形百分比（layer.plot1.label.fsize，坑 #31）
except Exception as e:
    print('set_fonts(pie) failed:', e)
if not LEGEND_ON_PIE:
    style.drop_legends(PIE)
centered_caption(PIE.index(), 'Share of total production (%)')

# ---------------- 面板字母、收尾 ----------------
# 注：规范要求面板字母 9 pt 粗体，但 2026b 上文字对象加粗没有生效的写法——
#     Page.letter 的 set_int('bold',1)、LabTalk `<name>.bold=1` 都是静默无效（PDF 里仍是
#     TimesNewRomanPSMT），而 `.font=font(Times New Roman:bold)` 会把字形打坏（同坑 #12）。
if CFG['letters']:
    for idx, ch in ((BAR.index(), 'a'), (PIE.index(), 'b')):
        pg.letter(idx, ch, dx_mm=12.0, dy_mm=4.3)
pg.finish()

paths = export.save(pg.g, os.path.join(OUT, 'bar_pie3d_%s.png' % LAYOUT))
print(export.report(pg.g, paths))
