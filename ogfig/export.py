# -*- coding: utf-8 -*-
"""ogfig.export — 一次出 png + tif + pdf（+ opju），并跑程序自检。"""
import os

import originpro as op

from . import style as st


def save(graph, path, mm=None, dpi=600, pdf=True, tif=True, opju=True):
    """Export a graph page to <path>.png (+ .tif 600 dpi, + .pdf vector, + .opju 工程).

    mm=None 时按图页的真实宽度（Page 已设成期刊毫米数）导出，字号 pt 与成图一致；
    显式给 mm 且与页面宽度不同，导出的位图会整体缩放，字号也跟着变。
    opju=True 时把当前工程另存为 <path>.opju，方便返修时在 GUI 里微调。
    """
    base, ext = os.path.splitext(path)
    out = []
    if mm is None:
        mm = st.page_mm(graph)[0]
    w = max(400, int(round(mm / 25.4 * dpi)))

    png = base + '.png'
    out.append(graph.save_fig(png, width=w))
    if tif:
        out.append(graph.save_fig(base + '.tif', type='tif', width=w))
    if pdf:
        out.append(graph.save_fig(base + '.pdf', type='pdf'))
    if opju:
        op.lt_exec('doc -uw')
        if op.save(base + '.opju'):
            out.append(base + '.opju')
    return [p for p in out if p]


def report(graph, paths, check=True):
    """文件清单 + 自检报告（PDF）+ 灰度预览（PNG）+ 版本警告。"""
    lines = []
    for p in paths:
        try:
            lines.append('%-40s %7.0f KB' % (os.path.basename(p), os.path.getsize(p) / 1024.0))
        except OSError:
            lines.append('%-40s MISSING' % p)
    if check:
        from . import check as ck
        size = st.page_mm(graph) if graph is not None else None
        for p in paths:
            if p.lower().endswith('.pdf'):
                lines.append(ck.format_report(ck.audit_pdf(p, size_mm=size)))
            elif p.lower().endswith('.png'):
                lines.append('gray preview: ' + os.path.basename(ck.grayscale(p)))
    warn = st.overline_warning()
    if warn:
        lines.append(warn)
    return '\n'.join(lines)
