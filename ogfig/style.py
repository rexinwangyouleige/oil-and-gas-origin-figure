# -*- coding: utf-8 -*-
"""ogfig.style — 配色、期刊档位、字体与刻度策略。

所有可调项在 ogfig/config.py；这里只做合并与执行。
"""
import os

import originpro as op

from .config import PALETTES, PREFS

# ---------------------------------------------------------------- palettes
OG = PALETTES['OG']
SPE = PALETTES['SPE']
OKABE = PALETTES['OKABE']
BATT = PALETTES['BATT']
HYDRO = PALETTES['HYDRO']
PVSK = PALETTES['PVSK']
SAC = PALETTES['SAC']
THERM = PALETTES['THERM']
C = PREFS.get('colors') or PALETTES[PREFS.get('palette', 'THERM')]

GRAY = '#595959'
FIT_GRAY = '#404040'
F_LATIN = PREFS.get('font_latin', 'Times New Roman')

DEFAULTS = dict(
    axis_thickness=PREFS.get('axis_thickness', 0.75),
    tick_length=PREFS.get('tick_length', 3),
    mtick_length=0,
    tick_thickness=PREFS.get('axis_thickness', 0.75),
    line_width=PREFS.get('line_width', 1.0),
    symbol_size=PREFS.get('symbol_size', 4),
    symbol_kind=2,
    tick_mask=1 if PREFS.get('tick_major', 'in') == 'in' else 2,
)

# ---------------------------------------------------------------- journals
# 档位只管页面尺寸（mm）；字号一律取 PREFS 里的绝对 pt
JOURNAL = {
    'single': dict(width=90, height=70),
    '1.5':    dict(width=140, height=105),
    'double': dict(width=180, height=130),
}


def spec(journal=None, size_mm=None):
    """Active spec：页面尺寸（mm）+ 字号（pt）。

    尺寸优先级：size_mm 参数 > PREFS['page_mm'] > journal 档位。
    """
    name = journal or PREFS.get('journal', 'double')
    s = dict(JOURNAL.get(name, JOURNAL['double']))
    size = size_mm or PREFS.get('page_mm')
    if size:
        s['width'], s['height'] = float(size[0]), float(size[1])
    s['fs_tick'] = PREFS.get('fs_tick', 14)
    s['fs_title'] = PREFS.get('fs_title', 16)
    s['fs_letter'] = PREFS.get('fs_letter', 18)
    s['fs_ann'] = PREFS.get('fs_note', 18)
    s['font'] = PREFS.get('font_latin', 'Times New Roman')
    s['name'] = name
    return s


# ---------------------------------------------------------------- templates
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates')
_FALLBACK = {'og_line': 'line', 'og_loglog': 'line', 'og_stack': 'line', 'og_doubley': 'doubley'}


def template_path(name):
    """skill 自带模板 → templates/<name>.otpu 的完整路径；没建过就退回对应的 Origin 内置模板。"""
    p = os.path.join(TEMPLATE_DIR, name + '.otpu')
    if os.path.exists(p):
        return p
    return _FALLBACK.get(name, name)


# ---------------------------------------------------------------- page / layer
def activate(gl):
    """两步切层：先激活图窗口，再切层 —— lt_exec 里的 layer.* 只认当前激活层（坑 #21）。"""
    page = gl.lt_range().split(']')[0][1:]
    op.lt_exec('win -a ' + page)
    op.lt_exec('page.active=%d' % (gl.index() + 1))


def set_page_mm(graph, width_mm, height_mm):
    """把图页设成真实毫米尺寸。

    page.width / page.height 的单位是像素，换算基准是 page.resx / page.resy（2026 默认 600）。
    页面默认锁定宽高比（page.kar=1）：只改宽，高会按比例跟着变，再改高，宽又被带走。
    必须先 page.kar=0 再写宽高（坑 #26）。
    页面设成真实尺寸后，layer.x.label.pt=7 在导出的 PDF 里就是 7 pt。
    """
    op.lt_exec('win -a ' + graph.name)
    rx = op.lt_float('page.resx') or 600.0
    ry = op.lt_float('page.resy') or 600.0
    op.lt_exec('page.kar=0;')
    op.lt_exec('page.width=%d;' % round(rx * width_mm / 25.4))
    op.lt_exec('page.height=%d;' % round(ry * height_mm / 25.4))


def page_mm(graph):
    """读回图页的 (宽, 高) mm。"""
    op.lt_exec('win -a ' + graph.name)
    rx = op.lt_float('page.resx') or 600.0
    ry = op.lt_float('page.resy') or 600.0
    return (op.lt_float('page.width') / rx * 25.4,
            op.lt_float('page.height') / ry * 25.4)


def _font_cmd(axis):
    """刻度标签字体。

    ⚠️ `layer.x.label.font` 是**数字型字体索引**（Windows 枚举），不是字体名字符串；
    写 `="Times New Roman"` 会被静默忽略。必须用 font() 函数：
        layer.x.label.font = font(Times New Roman);
    见 https://docs.originlab.com/labtalk/ref/layer-axis-label-obj/
    """
    return 'layer.%s.label.font=font(%s);' % (axis, F_LATIN)


def _title_font_cmd():
    """轴标题字体：标题是 text 对象，名字是 xb / yl / xt / yr，不是 layer.x.title。"""
    return ('xb.font=font(%s); yl.font=font(%s); xt.font=font(%s); yr.font=font(%s);'
            % (F_LATIN, F_LATIN, F_LATIN, F_LATIN))


def title_style(gl, names=('xb', 'yl'), pt=None):
    """轴标题（xb / yl / xt / yr 文字对象）的字号和字体，走对象 API（坑 #30）。

    LabTalk 的 `yl.fsize=` 与 `layer.y.title.pt=` 在多层页面里会落空，Origin 默认 22 pt 留着；
    `gl.label('yl').set_float('fsize', 8)` 每层都生效。
    """
    pt = pt or spec()['fs_title']
    idx = int(op.lt_float('font(%s)' % F_LATIN))
    for nm in names:
        lb = gl.label(nm)
        if lb is None:
            continue
        lb.set_float('fsize', pt)
        lb.set_int('font', idx)
        # 模板里空标题会被存成隐藏（show=0），有文字就重新显示（坑 #29）
        if (lb.text or '').strip():
            lb.set_int('show', 1)


def set_fonts(gl, nplots=None):
    """把这一层的**所有**文字刷成 Times New Roman。

    Origin 里四类文字各有各的属性，漏一类就会留宋体：
      刻度标签  layer.x/y.label.font
      轴标题    xb / yl / xt / yr 的 .font
      图例      legend.font
      数据标签  layer.plotN.label.font   ← 饼图百分比、柱顶数值都在这
    """
    lt = gl.lt_exec
    for ax in ('x', 'y', 'x2', 'y2'):
        lt(_font_cmd(ax))
    lt(_title_font_cmd())
    try:
        lt('legend.font=font(%s);' % F_LATIN)
    except Exception:
        pass
    try:
        n = nplots if nplots else len(gl.plot_list())
    except Exception:
        n = 0
    pt = spec()['fs_ann']
    lt('legend.fsize=%g;' % pt)
    for i in range(1, max(n, 1) + 1):
        # 数据标签：字体 font()、字号 fsize（.pt 不存在，坑 #31）
        lt('layer.plot%d.label.font=font(%s); layer.plot%d.label.fsize=%g;' % (i, F_LATIN, i, pt))


def apply_axes(gl, xtitle='', ytitle='', fs_tick=None, fs_title=None,
               right_axis='frame', **kw):
    """四边框、有数据的边主刻度朝内、无次刻度、无数据的上边框只留线。

    right_axis:
      'frame'（默认）→ 右侧是边框：无刻度、无标签；
      'data'        → 右侧是第二根数据轴（双 Y 图）：刻度朝内 + 显示标签。
    """
    s = spec()
    fs_tick = fs_tick or s['fs_tick']
    fs_title = fs_title or s['fs_title']
    d = dict(DEFAULTS, **kw)
    activate(gl)
    lt = gl.lt_exec
    lt(f'layer.x.thickness={d["axis_thickness"]}; layer.y.thickness={d["axis_thickness"]};')
    # 上 / 右边框线宽单独一套：add_layer 加的层默认更粗（坑 #32）
    lt(f'layer.x2.thickness={d["axis_thickness"]}; layer.y2.thickness={d["axis_thickness"]};')
    lt('layer.x.showAxes=3; layer.y.showAxes=3;')          # 四边框
    # 有数据的边：主刻度朝内，无次刻度
    tick_val = 1 if PREFS.get('tick_major', 'in') == 'in' else 2
    lt(f'layer.x.ticks={tick_val}; layer.y.ticks={tick_val};')
    lt(f'layer.x.ticklength={d["tick_length"]}; layer.y.ticklength={d["tick_length"]};')
    lt('layer.x.minorTicks=0; layer.y.minorTicks=0;')
    lt(f'layer.x.mticklength={d["mtick_length"]}; layer.y.mticklength={d["mtick_length"]};')
    # 上边框永远没有刻度；只设 ticks/ticklength，不碰 showLabels（坑 #24）
    lt('layer.x2.ticks=0; layer.x2.ticklength=0;')
    if right_axis == 'data':
        lt(f'layer.y2.ticks={tick_val}; layer.y2.ticklength={d["tick_length"]};')
        lt('layer.y2.minorTicks=0; layer.y2.mticklength=0; layer.y2.showLabels=1;')
        lt(f'layer.y2.label.pt={fs_tick}; layer.y2.title.pt={fs_title};')
        lt(_font_cmd('y2'))
    else:
        lt('layer.y2.ticks=0; layer.y2.ticklength=0;')
    lt(f'layer.x.label.pt={fs_tick}; layer.y.label.pt={fs_tick};')
    lt(f'layer.x.title.pt={fs_title}; layer.y.title.pt={fs_title};')
    lt(_font_cmd('x'))
    lt(_font_cmd('y'))
    lt(_title_font_cmd())
    lt('layer.x.showLabels=1; layer.y.showLabels=1;')
    lt('layer.x.showGrids=0; layer.y.showGrids=0;')
    lt('layer.factor=1;')                                   # 坑 #27
    try:                       # 图例 + 数据标签（饼图百分比、柱顶数值）
        set_fonts(gl)
    except Exception:
        pass
    gl.axis('x').title = xtitle or ''
    gl.axis('y').title = ytitle or ''
    title_style(gl, ('xb', 'yl'), fs_title)


def guide_line(gl, sheet, ycol, xcol=0):
    """透明黑引导线：每层第一条曲线决定轴颜色（坑 #18），先画它把轴锁成黑色。"""
    activate(gl)
    p = gl.add_plot(sheet, ycol, xcol, -1, 'l')
    if p is not None:
        p.color = '#000000'
        try:
            p.transparency = 100
        except Exception:
            pass
    return p


def apply_dual_axes(left, right, xtitle='', ytitle='', y2title='', fs_tick=None, fs_title=None):
    """doubley 两层的轴样式（坑 #21–#24）。

    左层：x / y 照常，右边框 y2 与上边框 x2 只留线；
    右层：只留右侧那根 y2（刻度朝内、Times New Roman），自己的 x 轴全关。
    """
    s = spec()
    fs_tick = fs_tick or s['fs_tick']
    fs_title = fs_title or s['fs_title']
    d = DEFAULTS
    apply_axes(left, xtitle, ytitle, fs_tick=fs_tick, fs_title=fs_title)
    activate(left)
    left.lt_exec('layer.y2.ticks=0; layer.y2.ticklength=0; layer.y2.mticklength=0;')

    activate(right)
    lt = right.lt_exec
    lt('layer.x.showAxes=0; layer.x2.showAxes=0; layer.x.showLabels=0; layer.x2.showLabels=0;')
    lt('layer.y2.showAxes=2; layer.y2.showLabels=2;')
    lt('layer.y2.thickness=%g; layer.y2.ticks=1; layer.y2.ticklength=%g;'
       % (d['axis_thickness'], d['tick_length']))
    lt('layer.y2.minorTicks=0; layer.y2.mticklength=0;')
    lt('layer.y2.label.pt=%g; layer.y2.title.pt=%g;' % (fs_tick, fs_title))
    lt(_font_cmd('y2'))
    lt('layer.factor=1;')
    if y2title:
        # 右层看得见的标题是 yr（y2 的标题），yl 是内侧隐藏轴的（坑 #22）
        right.lt_exec('label -yr %s' % y2title)
    title_style(right, ('yr',), fs_title)
    yr = right.label('yr')
    if yr is not None:                      # Origin 把右轴标题贴得太近，会压到刻度数字：外移 1 mm
        yr.set_int('left', yr.get_int('left') + round(op.lt_float('page.resx') / 25.4))
    for nm in ('yl', 'xb'):                 # 右层自己的左 / 下标题会叠在左层标题上，关掉
        lb = right.label(nm)
        if lb is not None:
            lb.set_int('show', 0)
    try:
        set_fonts(right)
    except Exception:
        pass


def limits(gl, x=None, y=None, xinc=None, yinc=None):
    activate(gl)
    if x is not None:
        gl.lt_exec(f'layer.x.from={x[0]}; layer.x.to={x[1]};')
    if y is not None:
        gl.lt_exec(f'layer.y.from={y[0]}; layer.y.to={y[1]};')
    if xinc:
        gl.lt_exec(f'layer.x.inc={xinc};')
    if yinc:
        gl.lt_exec(f'layer.y.inc={yinc};')


def line_width_cmd(width_pt):
    """`set <plot> -w` 的单位是 1/500 pt（坑 #28）：1 pt 要写 -w 500。"""
    return '-w %d' % round(width_pt * 500)


# ---------------------------------------------------------------- mm 定位
def frame_mm(gl, graph):
    """层边框在页面上的位置 (left, top, width, height)，单位 mm，top 从页面顶部算。"""
    W, H = page_mm(graph)
    activate(gl)
    return (op.lt_float('layer.left') / 100 * W, op.lt_float('layer.top') / 100 * H,
            op.lt_float('layer.width') / 100 * W, op.lt_float('layer.height') / 100 * H)


def is_log(gl, ax):
    """gl.xscale / yscale 读回来是整数码：1 linear、2 log10、8 ln、9 log2（写入时才用字符串）。"""
    v = getattr(gl, ax + 'scale', 1)
    return v in (2, 8, 9) or str(v).lower() in ('log10', 'ln', 'log2')


def mm_to_data(gl, frame, x_mm, y_mm):
    """页面上的 (x_mm, y_mm) → 该层的数据坐标；log 轴按对数插值（坑 #13）。"""
    import math
    L, T, W, H = frame
    fx = (x_mm - L) / W
    fy = (T + H - y_mm) / H
    out = []
    for ax, f in (('x', fx), ('y', fy)):
        lo, hi = (float(v) for v in gl.axis(ax).limits[:2])
        if is_log(gl, ax) and lo > 0 and hi > 0:
            out.append(10 ** (math.log10(lo) + f * (math.log10(hi) - math.log10(lo))))
        else:
            out.append(lo + f * (hi - lo))
    return out


def data_to_mm(gl, frame, x, y):
    """mm_to_data 的反函数：数据坐标 → 页面 mm。"""
    import math
    L, T, W, H = frame
    out = []
    for ax, v in (('x', x), ('y', y)):
        lo, hi = (float(u) for u in gl.axis(ax).limits[:2])
        if is_log(gl, ax) and lo > 0 and hi > 0 and v > 0:
            f = (math.log10(v) - math.log10(lo)) / (math.log10(hi) - math.log10(lo))
        else:
            f = (v - lo) / (hi - lo)
        out.append(f)
    return L + out[0] * W, T + (1 - out[1]) * H


def text_size_mm(lab, graph=None, pt=None):
    """估算单行文字的 (宽, 高) mm：Times New Roman 平均字宽约 0.5 em。
    （文字对象的 .width/.height 单位不稳定，实测不可用。）"""
    import re
    pt = pt or spec()['fs_ann']
    try:
        txt = re.sub(r'\\[+-]\(([^)]*)\)', r'\1', lab.text)
    except Exception:
        txt = 'XXXX'
    em = pt * 25.4 / 72
    return 0.5 * em * len(txt), 1.2 * em


def place_mm(gl, lab, frame, x_mm, y_mm):
    """把文字对象的左上角放到页面 (x_mm, y_mm)。x1 / y1 是文字左上角的数据坐标。"""
    x, y = mm_to_data(gl, frame, x_mm, y_mm)
    gl.lt_exec('%s.x1=%.10g; %s.y1=%.10g;' % (lab.name, x, lab.name, y))


def text_label(gl, text, x, y, color=None, pt=None, bold=0, rotate=0):
    """无边框题注/标注（Origin 2026 起文本对象默认无框）。

    字号、字体走 LabTalk 的 `<name>.fsize` / `<name>.font=font(...)`（坑 #12、#14）：
    `set_float('pt')` 设出来的字号不对，`set_str('font', ...)` 会把字形打坏。
    """
    pt = pt or spec()['fs_ann']
    activate(gl)
    lab = gl.add_label(text, x, y)
    if not lab:
        return None
    gl.lt_exec('%s.font=font(%s); %s.fsize=%g;' % (lab.name, F_LATIN, lab.name, pt))
    lab.set_int('bold', bold)
    lab.set_int('rotate', rotate)
    if color:
        try:
            lab.set_int('color', op.ocolor(color))
        except Exception:
            pass
    return lab


def drop_legends(gl):
    try:
        lb = gl.label('legend')
        if lb:
            lb.remove()
    except Exception:
        pass


def overline_warning():
    try:
        v = str(op.org_ver())
    except Exception:
        return ''
    if v.startswith('10.1'):
        return ('[ogfig] Origin %s 有"文字上方多一条细线"的已知 bug，'
                '升级到 2024b（10.15）+ 即可消失。' % v[:9])
    return ''
