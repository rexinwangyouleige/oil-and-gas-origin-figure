# -*- coding: utf-8 -*-
"""ogfig.templates — 按 config.py 的规范生成预设 .otpu 模板。

    python -m ogfig.templates            # 重建 templates/ 下全部预设
    python -m ogfig.templates og_line    # 只建一个

改了 config.py（字号、线宽、刻度长度…）后重跑一次即可。

模板只是"基线"：页面尺寸、层位置、刻度朝向、次刻度、边框、线宽、字号会被记住；
**字体不会**（从模板新建的图，文字一律回到 SimSun，坑 #29），所以脚本出图时
Page.style() / style.apply_axes() 仍会再刷一遍。两者结合：模板管常用图，脚本兜底。
"""
import os
import sys

import originpro as op

from . import style as st

PRESETS = {
    'og_line':    dict(base='line', size=(90, 70), desc='单面板 XY 折线 / 散点（线性轴）'),
    'og_loglog':  dict(base='line', size=(90, 70), desc='双对数：试井 log-log 诊断、黏度–剪切速率',
                       xscale='log10', yscale='log10'),
    'og_stack':   dict(base='line', size=(90, 110), desc='叠谱（XRD / FTIR / Raman / NMR T2），Y 轴不显示刻度',
                       hide_y=True),
    'og_doubley': dict(base='doubley', size=(90, 70), desc='双 Y 轴：左层 g[0]，右层 g[1] 用 y2'),
}

MARGIN = (14, 6, 6, 11)       # 单面板模板的 左 右 上 下 mm（双 Y 右侧多留给右轴）
MARGIN_DY = (14, 14, 6, 11)


def _frame(graph, size, margin):
    W, H = size
    ml, mr, mt, mb = margin
    return (ml / W * 100, mt / H * 100, (W - ml - mr) / W * 100, (H - mt - mb) / H * 100)


def _place(gl, pos):
    st.activate(gl)
    op.lt_exec('layer.left=%.2f; layer.top=%.2f; layer.width=%.2f; layer.height=%.2f; layer.factor=1;' % pos)


def build(name):
    cfg = PRESETS[name]
    g = op.new_graph(template=cfg['base'], lname='TPL_' + name)
    st.set_page_mm(g, *cfg['size'])
    if cfg['base'] == 'doubley':
        pos = _frame(g, cfg['size'], MARGIN_DY)
        _place(g[0], pos)
        _place(g[1], pos)
        st.apply_dual_axes(g[0], g[1])
    else:
        gl = g[0]
        _place(gl, _frame(g, cfg['size'], MARGIN))
        st.apply_axes(gl)
        if cfg.get('xscale'):
            gl.xscale = cfg['xscale']
        if cfg.get('yscale'):
            gl.yscale = cfg['yscale']
        if cfg.get('hide_y'):
            st.activate(gl)
            gl.lt_exec('layer.y.showLabels=0; layer.y.ticks=0;')
    for gl in g:
        st.drop_legends(gl)
    os.makedirs(st.TEMPLATE_DIR, exist_ok=True)
    op.lt_exec('win -a %s' % g.name)
    op.lt_exec('template_saveas template:=%s filepath:="%s\\";' % (name, st.TEMPLATE_DIR))
    g.destroy()
    path = os.path.join(st.TEMPLATE_DIR, name + '.otpu')
    return path if os.path.exists(path) else None


def main(names):
    op.set_show(False)
    try:
        for n in names or PRESETS:
            p = build(n)
            print('%-11s %s  %s' % (n, 'OK ' if p else 'FAIL', PRESETS[n]['desc']))
    finally:
        if getattr(op, 'oext', False):
            op.exit()


if __name__ == '__main__':
    main(sys.argv[1:])
