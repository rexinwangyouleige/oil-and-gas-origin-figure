# -*- coding: utf-8 -*-
"""ogfig.cli — 出图前后的命令行工具（在 skill 根目录运行）。

    python -m ogfig.cli doctor                 # 环境：Python / originpro / Origin 版本 / 模板 / 字体
    python -m ogfig.cli inspect data.xlsx      # 数据：列名、类型、行数、范围、跨量级提示、选图建议
    python -m ogfig.cli spec [--journal 1.5]   # 预演：不开 Origin，打印本次出图会用的尺寸 / 字号 / 线宽 / 配色
    python -m ogfig.cli check fig1.pdf [--mm 180 130]   # 自检已导出的 PDF
    python -m ogfig.cli templates [og_line ...]          # 重建预设模板
"""
import argparse
import importlib.util
import json
import os
import sys


def _doctor():
    res = {'python': sys.version.split()[0]}
    res['originpro'] = bool(importlib.util.find_spec('originpro'))
    res['pymupdf'] = bool(importlib.util.find_spec('fitz'))
    res['pandas'] = bool(importlib.util.find_spec('pandas'))
    fonts = os.path.join(os.environ.get('WINDIR', r'C:\Windows'), 'Fonts')
    res['font_times'] = os.path.exists(os.path.join(fonts, 'times.ttf'))
    res['font_simsun'] = os.path.exists(os.path.join(fonts, 'simsun.ttc'))
    from . import style as st
    from .templates import PRESETS
    res['templates'] = {n: os.path.exists(os.path.join(st.TEMPLATE_DIR, n + '.otpu')) for n in PRESETS}
    if res['originpro']:
        import originpro as op
        try:
            v = op.org_ver()
            res['origin_version'] = v
            res['origin_ok'] = not str(v).startswith('10.1')     # 2024 早期版有上划线 / 线宽 bug
        finally:
            if getattr(op, 'oext', False):
                op.exit()
    need = ('originpro', 'pymupdf', 'font_times')
    res['status'] = 'ready' if all(res.get(k) for k in need) and res.get('origin_ok', False) else 'action-required'
    if not all(res['templates'].values()):
        res['hint'] = '模板未建全：python -m ogfig.cli templates'
    return res


def _inspect(path, sheet=None):
    import numpy as np
    import pandas as pd
    ext = os.path.splitext(path)[1].lower()
    if ext in ('.xlsx', '.xls'):
        df = pd.read_excel(path, sheet_name=sheet or 0)
    elif ext in ('.txt', '.dat', '.tsv'):
        df = pd.read_csv(path, sep=None, engine='python')
    else:
        df = pd.read_csv(path)
    cols = []
    for c in df.columns:
        s = pd.to_numeric(df[c], errors='coerce')
        num = s.notna().mean() > 0.9
        info = dict(name=str(c), numeric=bool(num), n=int(df[c].notna().sum()))
        if num:
            v = s.dropna()
            info.update(min=float(v.min()), max=float(v.max()),
                        monotonic=bool(v.is_monotonic_increasing or v.is_monotonic_decreasing))
            pos = v[v > 0]
            if len(pos) and pos.max() / pos.min() > 1e3:
                info['hint'] = '跨 %.0f 个量级，考虑 log 轴' % np.log10(pos.max() / pos.min())
        else:
            info['levels'] = int(df[c].nunique())
        cols.append(info)
    num = [c for c in cols if c['numeric']]
    cat = [c for c in cols if not c['numeric']]
    sug = []
    if num and num[0].get('monotonic'):
        sug.append('第 1 个数值列单调 → 当 X，其余做折线（时间 / 温度 / PV / 深度）')
    if cat and num:
        sug.append('有类别列 → 柱状 / 箱线（每组 n<10 时叠散点）')
    if len(num) >= 3 and not (num[0].get('monotonic')):
        sug.append('多个数值列无序 → 交会图（散点）或相关矩阵')
    return dict(file=os.path.basename(path), rows=len(df), columns=cols, suggestions=sug,
                catalog='对照 catalog/INDEX.md 找对应图型脚本')


def main(argv=None):
    ap = argparse.ArgumentParser(prog='ogfig')
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('doctor')
    a = sub.add_parser('inspect')
    a.add_argument('file')
    a.add_argument('--sheet')
    a = sub.add_parser('spec')
    a.add_argument('--journal')
    a.add_argument('--mm', nargs=2, type=float)
    a = sub.add_parser('check')
    a.add_argument('pdf', nargs='+')
    a.add_argument('--mm', nargs=2, type=float)
    a = sub.add_parser('templates')
    a.add_argument('names', nargs='*')
    args = ap.parse_args(argv)

    if args.cmd == 'doctor':
        print(json.dumps(_doctor(), ensure_ascii=False, indent=2))
    elif args.cmd == 'inspect':
        print(json.dumps(_inspect(args.file, args.sheet), ensure_ascii=False, indent=2))
    elif args.cmd == 'spec':
        from . import style as st
        s = st.spec(args.journal, args.mm)
        s['line'] = dict(st.DEFAULTS)
        s['palette'] = st.C
        print(json.dumps(s, ensure_ascii=False, indent=2))
    elif args.cmd == 'check':
        from . import check as ck
        ok = True
        for p in args.pdf:
            rep = ck.audit_pdf(p, size_mm=args.mm)
            ok &= rep['ok']
            print(ck.format_report(rep))
        return 0 if ok else 1
    elif args.cmd == 'templates':
        from . import templates
        templates.main(args.names)
    return 0


if __name__ == '__main__':
    sys.exit(main())
