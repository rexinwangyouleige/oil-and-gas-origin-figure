# -*- coding: utf-8 -*-
"""ogfig.check — 出图后的程序自检（不需要 Origin，只读导出的 PDF / PNG）。

    from ogfig import check
    rep = check.audit_pdf('fig1.pdf', size_mm=(180, 130))
    print(check.format_report(rep))
    check.grayscale('fig1.png')          # -> fig1_gray.png，看配色灰度下能否区分

检查项（对应 SKILL.md 第 5 步）：
  尺寸     PDF 页面 = 期刊毫米数（±1.5 mm）
  字体     西文只允许 Times New Roman；含中文的片段才允许宋体
  字号     7–9 pt（上下标允许更小）
  出界     文字不能超出页面
  重叠     文字与文字的字形框不能互相压住
  细线     曲线 / 坐标轴线宽 ≥ 0.25 pt（防止 set -w 单位写错，坑 #28）
"""
import itertools
import os
import re

import fitz

from .config import PREFS

MM = 25.4 / 72
CJK = re.compile(r'[㐀-鿿]')


def _spans(page):
    out = []
    lid = 0
    for b in page.get_text('dict')['blocks']:
        for ln in b.get('lines', []):
            lid += 1
            horiz = abs(ln['dir'][1]) < 1e-3
            for sp in ln['spans']:
                t = sp['text'].strip()
                if not t:
                    continue
                size = sp['size']
                if horiz:
                    # 字形框：基线上 0.72 em、下 0.18 em，比行框紧，避免把行距误判成重叠
                    x0, _, x1, _ = sp['bbox']
                    base = sp['origin'][1]
                    rect = fitz.Rect(x0, base - 0.72 * size, x1, base + 0.18 * size)
                else:                     # 竖排（Y 轴标题）：bbox 本身就够紧
                    rect = fitz.Rect(sp['bbox'])
                out.append(dict(text=t, font=sp['font'], size=size, rect=rect, line=lid))
    return out


def audit_pdf(path, size_mm=None, fs_range=None, min_line_pt=0.25):
    """返回 dict：每项 ok + 细节。size_mm 不给就只报告不判定。"""
    lo = min(PREFS.get(k, 7) for k in ('fs_tick', 'fs_title', 'fs_note', 'fs_letter'))
    hi = max(PREFS.get(k, 9) for k in ('fs_tick', 'fs_title', 'fs_note', 'fs_letter'))
    fs_range = fs_range or (lo, hi)
    doc = fitz.open(path)
    page = doc[0]
    r = page.rect
    spans = _spans(page)
    rep = {'file': os.path.basename(path)}

    w, h = r.width * MM, r.height * MM
    rep['size'] = dict(value='%.1f x %.1f mm' % (w, h),
                       ok=size_mm is None or (abs(w - size_mm[0]) < 1.5 and abs(h - size_mm[1]) < 1.5))

    bad_font = sorted({'%s ("%s")' % (s['font'], s['text'][:12]) for s in spans
                       if 'TimesNewRoman' not in s['font'].replace(' ', '')
                       and not (CJK.search(s['text']) and 'SimSun' in s['font'])})
    rep['fonts'] = dict(value=sorted({s['font'] for s in spans}), ok=not bad_font, bad=bad_font[:6])

    def _is_script(s):           # 上下标：短、比正文小
        return len(s['text']) <= 3 and s['size'] < fs_range[0]
    bad_size = sorted({'%.1f pt "%s"' % (s['size'], s['text'][:12]) for s in spans
                       if not _is_script(s)
                       and not (fs_range[0] - 0.35 <= s['size'] <= fs_range[1] + 0.35)})
    rep['font_size'] = dict(value=sorted({round(s['size'], 1) for s in spans}), ok=not bad_size,
                            bad=bad_size[:6])

    out = [s['text'][:16] for s in spans
           if s['rect'].x0 < -0.5 or s['rect'].y0 < -0.5 or s['rect'].x1 > r.width + 0.5
           or s['rect'].y1 > r.height + 0.5]
    rep['in_page'] = dict(value=len(out), ok=not out, bad=out[:6])

    over = []
    for a, b in itertools.combinations(spans, 2):
        if a['line'] == b['line']:        # 同一行里的上下标贴着正文是正常的
            continue
        i = a['rect'] & b['rect']
        if not i.is_empty and i.get_area() > 0.2 * min(a['rect'].get_area(), b['rect'].get_area()):
            over.append('"%s" × "%s"' % (a['text'][:12], b['text'][:12]))
    rep['overlap'] = dict(value=len(over), ok=not over, bad=over[:8])

    thin = 0
    for dr in page.get_drawings():
        wd = dr.get('width')
        if dr.get('color') is not None and wd is not None and 0 < wd < min_line_pt:
            thin += 1
    rep['line_width'] = dict(value='%d 条 < %.2f pt' % (thin, min_line_pt), ok=thin == 0)
    doc.close()
    rep['ok'] = all(v['ok'] for k, v in rep.items() if isinstance(v, dict))
    return rep


def format_report(rep):
    lines = ['[%s] %s' % ('PASS' if rep['ok'] else 'FAIL', rep['file'])]
    for k in ('size', 'fonts', 'font_size', 'in_page', 'overlap', 'line_width'):
        v = rep[k]
        lines.append('  %-4s %-10s %s' % ('ok' if v['ok'] else 'XX', k, v['value']))
        for b in v.get('bad', []) if not v['ok'] else []:
            lines.append('              - %s' % b)
    return '\n'.join(lines)


def grayscale(png, out=None):
    """灰度预览：<name>_gray.png。"""
    out = out or os.path.splitext(png)[0] + '_gray.png'
    pix = fitz.Pixmap(png)
    if pix.alpha:
        pix = fitz.Pixmap(pix, 0)
    fitz.Pixmap(fitz.csGRAY, pix).save(out)
    return out
