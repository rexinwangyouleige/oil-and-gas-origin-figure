# -*- coding: utf-8 -*-
"""ogfig.panels — the Page object: a grid of Origin layers you fill with plots.

    pg = Page(2, 2, journal='double')              # 页面 = 180 x 130 mm（真实尺寸）
    pg = Page(1, 1, size_mm=(90, 70))              # 或直接给毫米
    ws = pg.sheet('PROD', 4)
    ws.from_list(0, t, lname='Time', units='d')
    pg.plot(0, ws, 1, 0, kind='logy')
    pg.style(0, 'Time (d)', 'q\\-(g) (10\\+(4) m\\+(3)/d)')
    pg.caption(0, 'Well A-12', where='tl')

双 Y 轴不在 Page 里做：用 Origin 自带 doubley 模板，用 ogfig.DualY（og_doubley 模板），见 catalog/production/bar_line_dualy.py。
"""
import os

import originpro as op
from . import style as st
from .config import PREFS


def _safe_set(plot, opt):
    """`set` option on a data plot; never let styling kill a build."""
    try:
        plot.set_cmd(opt)
    except Exception:
        pass


class Page:
    def __init__(self, rows=1, cols=1, journal=None, size_mm=None, lname='OGFIG',
                 template='og_line', margin=None, gap=None, connect=True):
        """rows x cols 面板网格。

        size_mm  : (宽, 高) mm；不给就用 PREFS['page_mm']，再不给用 journal 档位。
        margin   : (左, 右, 上, 下) mm，默认 PREFS['margin_mm']。
        gap      : (横向, 纵向) mm，默认 PREFS['gap_mm']。
        template : skill 自带模板名（templates/*.otpu，见 templates/README.md）或 Origin 内置模板名；
                   模板给基线样式，脚本随后照样执行 style()，两者结合。
        """
        self.rows, self.cols = rows, cols
        self.spec = st.spec(journal, size_mm)
        self.journal = self.spec['name']
        self.size_mm = (self.spec['width'], self.spec['height'])

        if connect:
            op.new()
            op.attach()
            op.set_show(True)

        self._cleanup(lname)
        self.g = op.new_graph(template=st.template_path(template), lname=lname)
        # 先定页面物理尺寸，再加层、定位：layer 的百分比是相对页面算的
        st.set_page_mm(self.g, *self.size_mm)
        for _ in range(rows * cols - 1):
            self.g.add_layer(0)

        self.layers = [self.g[i] for i in range(rows * cols)]
        self.book = None
        self.legend_scores = None
        self._legend_idx = []          # 要进图例的 plot 序号（1 基），Page.plot/bar 自动记
        self._layout(margin or PREFS.get('margin_mm', (14, 4, 6, 11)),
                     gap or PREFS.get('gap_mm', (16, 15)))

    # ------------------------------------------------------------------ admin
    @staticmethod
    def _cleanup(lname):
        for p in list(op.pages()):
            try:
                if (p.lname or '').startswith(lname):
                    p.destroy()
            except Exception:
                pass

    def _layout(self, margin, gap):
        """margin / gap 以 mm 给出，这里换成 layer.left/top/width/height 用的页面百分比。"""
        W, H = self.size_mm
        ml, mr = margin[0] / W * 100, margin[1] / W * 100
        mt, mb = margin[2] / H * 100, margin[3] / H * 100
        gx, gy = gap[0] / W * 100, gap[1] / H * 100
        w = (100 - ml - mr - gx * (self.cols - 1)) / self.cols
        h = (100 - mt - mb - gy * (self.rows - 1)) / self.rows
        # 每个面板边框的 mm 位置 (left, top, width, height)，字母 / 题注 / 图例按它定位
        self.frames = []
        for idx in range(len(self.layers)):
            r, c = divmod(idx, self.cols)
            self.frames.append(((ml + c * (w + gx)) / 100 * W, (mt + r * (h + gy)) / 100 * H,
                                w / 100 * W, h / 100 * H))
        for idx in range(len(self.layers)):
            self._apply_frame(idx)

    def _apply_frame(self, idx):
        """把 self.frames[idx] 的毫米位置写成层的百分比位置（top 从页面顶部算，坑 #1）。"""
        left, top, width, height = self.frames[idx]
        PW, PH = self.size_mm
        gl = self.layers[idx]
        st.activate(gl)
        op.lt_exec('layer.left=%.3f; layer.top=%.3f; layer.width=%.3f; layer.height=%.3f;'
                   % (left / PW * 100, top / PH * 100, width / PW * 100, height / PH * 100))
        # 层缩小后 Origin 会把 layer.factor 自动降到 0.9，层内文字跟着缩（坑 #27）
        op.lt_exec('layer.factor=1;')

    # ---------------------------------------------------------------- workbook
    def sheet(self, name='DATA', ncols=6):
        if self.book is None:
            wb = op.new_book(lname='OGFIG_data')
            if isinstance(wb, list):
                wb = wb[0]
            self.book = wb
            ws = wb[0]
            ws.name = name
        else:
            ws = self.book.add_sheet(name)
        ws.cols = ncols
        return ws

    # ------------------------------------------------------------------- plots
    def layer(self, i):
        return self.layers[i]

    def plot(self, i, sheet, ycol, xcol=-1, kind='l', color=None, dash=None,
             width=None, size=None, symbol=None, rescale=True):
        """kind: 'l' line, 's' scatter, 'ls' line+symbol, 'logy', 'loglog', 'logx'."""
        gl = self.layers[i]
        st.activate(gl)
        d = st.DEFAULTS
        width = width or d['line_width']
        size = size or d['symbol_size']
        symbol = symbol if symbol is not None else d['symbol_kind']

        logx = kind in ('loglog', 'logx')
        logy = kind in ('logy', 'loglog')
        base = {'logy': 'l', 'loglog': 'l', 'logx': 'l'}.get(kind, kind)

        def _one(t):
            p = gl.add_plot(sheet, ycol, xcol, -1, t)
            if p is None:
                return None
            if color:
                p.color = color
            if t == 'l':
                _safe_set(p, st.line_width_cmd(width))
                if dash:
                    _safe_set(p, '-d %d' % dash)
            else:
                p.symbol_kind = symbol
                p.symbol_size = size
            return p

        made = []
        n0 = len(gl.plot_list())
        if base == 'ls':
            made.append(_one('l'))
            made.append(_one('s'))
        elif base in ('l', 's'):
            made.append(_one(base))
        else:
            made.append(_one('l'))

        if made and made[0] is not None:
            self._legend_idx.append(n0 + 1)      # 'ls' 只记线那一条，图例不会出现两遍

        if logx:
            gl.xscale = 'log10'
        if logy:
            gl.yscale = 'log10'
        if rescale:
            gl.rescale()
        return made

    def bar(self, i, sheet, xcol, cols, errs=None, colors=None, width_pct=60, rescale=True):
        gl = self.layers[i]
        st.activate(gl)
        colors = colors or st.C
        made = []
        n0 = len(gl.plot_list())
        for k, c in enumerate(cols):
            e = errs[k] if errs else -1
            p = gl.add_plot(sheet, c, xcol, -1, 'c', colyerr=e)
            if p is None:
                continue
            p.color = colors[k % len(colors)]
            _safe_set(p, '-w %d' % width_pct)
            made.append(p)
        if made:
            self._legend_idx.extend(range(n0 + 1, len(gl.plot_list()) + 1))
        if rescale:
            gl.rescale()
        return made

    def style(self, i, xtitle='', ytitle='', tick_label_type=None):
        gl = self.layers[i]
        s = self.spec
        st.apply_axes(gl, xtitle, ytitle, fs_tick=s['fs_tick'], fs_title=s['fs_title'])
        if tick_label_type:
            gl.lt_exec(tick_label_type)
        return gl

    # -------------------------------------------------------------- annotation
    def annotate(self, i, text, x, y, color=None, bold=0, rotate=0):
        return st.text_label(self.layers[i], text, x, y, color=color,
                             pt=self.spec['fs_ann'], bold=bold, rotate=rotate)

    def caption(self, i, text, where='tl', pad_mm=2.0):
        """无边框题注，放在面板框内的空白角落（tl / tr / bl / br），距边框 pad_mm。"""
        gl = self.layers[i]
        L, T, W, H = self.frames[i]
        lab = st.text_label(gl, text, 0, 0, pt=self.spec['fs_ann'], bold=0)
        if lab is None:
            return None
        w_mm, h_mm = st.text_size_mm(lab, self.g)
        x = L + pad_mm if 'l' in where else L + W - pad_mm - w_mm
        y = T + pad_mm if where.startswith('t') else T + H - pad_mm - h_mm
        st.place_mm(gl, lab, self.frames[i], x, y)
        return lab

    def categories(self, i, names, positions=None, pad_mm=1.2):
        """类别轴：关掉 X 刻度数字，把 names 居中写在每个位置的轴下方（默认位置 1..n）。"""
        gl = self.layers[i]
        st.activate(gl)
        gl.lt_exec('layer.x.showLabels=0;')
        positions = positions or list(range(1, len(names) + 1))
        L, T, W, H = self.frames[i]
        pt = self.spec['fs_tick']
        y0 = float(gl.axis('y').limits[0])
        out = []
        for name, x in zip(names, positions):
            lab = st.text_label(gl, name, x, y0, pt=pt)
            if lab is None:
                continue
            w_mm, _ = st.text_size_mm(lab, pt=pt)
            xm, _ = st.data_to_mm(gl, self.frames[i], x, y0)
            st.place_mm(gl, lab, self.frames[i], xm - w_mm / 2, T + H + pad_mm)
            out.append(lab)
        return out

    def letter(self, i, ch, dx_mm=None, dy_mm=3.5):
        """面板字母 (a)(b)(c)：左上角框外，所有面板同一偏移（按 mm 定位，log 轴同样准）。

        dx_mm 默认 = 左页边距 - 1 mm，即和最左侧 Y 轴标题大致对齐。
        """
        gl = self.layers[i]
        L, T, W, H = self.frames[i]
        dx = dx_mm if dx_mm is not None else PREFS.get('margin_mm', (14,))[0] - 1
        lab = st.text_label(gl, '(%s)' % ch, 0, 0, pt=self.spec['fs_letter'], bold=1)
        if lab is not None:
            st.place_mm(gl, lab, self.frames[i], L - dx, T - dy_mm)
        return lab

    def drop_legends(self):
        for gl in self.layers:
            st.drop_legends(gl)

    # ---------------------------------------------------------------- legend
    def _ink_mask(self):
        """导一张小图并二值化，用来判断"哪儿是空白"。返回 bool 数组（True=有内容）。"""
        import tempfile

        import fitz
        import numpy as np
        path = os.path.join(tempfile.gettempdir(), 'ogfig_ink_probe.png')
        self.g.save_fig(path, width=int(PREFS.get('legend_probe_px', 1000)))
        pix = fitz.Pixmap(path)
        if pix.alpha:
            pix = fitz.Pixmap(pix, 0)
        gray = fitz.Pixmap(fitz.csGRAY, pix)
        arr = np.frombuffer(gray.samples, dtype=np.uint8).reshape(gray.height, gray.width)
        return arr < 245

    def _corner_ink(self, mask, i, size, pad_mm):
        """四个角放同样大的框，各自的墨迹占比（0 = 全空）。"""
        h_px, w_px = mask.shape
        PW, PH = self.size_mm
        sx, sy = w_px / PW, h_px / PH
        L, T, W, H = self.frames[i]
        lw, lh = size
        out = {}
        for where in ('tr', 'tl', 'br', 'bl'):
            x0 = L + pad_mm if where[1] == 'l' else L + W - pad_mm - lw
            y0 = T + pad_mm if where[0] == 't' else T + H - pad_mm - lh
            px0, px1 = max(0, int(x0 * sx)), min(w_px, int((x0 + lw) * sx))
            py0, py1 = max(0, int(y0 * sy)), min(h_px, int((y0 + lh) * sy))
            sub = mask[py0:py1, px0:px1]
            out[where] = float(sub.mean()) if sub.size else 1.0
        return out

    def _grow_top(self, delta_mm):
        """页面上边加高 delta_mm，所有层跟着下移 → 顶部留一条空白带放图例。"""
        if delta_mm <= 0:
            return self.size_mm
        W, H = self.size_mm
        self.frames = [(L, T + delta_mm, w, h) for (L, T, w, h) in self.frames]
        self.size_mm = (W, H + delta_mm)
        st.set_page_mm(self.g, *self.size_mm)
        for idx in range(len(self.layers)):
            self._apply_frame(idx)
        return self.size_mm

    def legend(self, i=0, where='auto', pad_mm=None, pt=None, grow=True):
        """给第 i 个面板加图例：文字取列 long name、无边框、自动找最空的角。

        where : 'auto'（默认：四角里墨迹最少的）或 'tl' / 'tr' / 'bl' / 'br'
        grow  : 四角都被数据占住时，是否把页面上边加高 legend_grow_mm（默认 20），放右上角
        返回  : 实际用的位置，'tr'/'tl'/'br'/'bl'，加高后放的是 'tr-grow'
        """
        gl = self.layers[i]
        pad = PREFS.get('legend_pad_mm', 2.0) if pad_mm is None else pad_mm
        st.activate(gl)
        lb = st.make_legend(gl, pt=pt)
        if self._legend_idx:
            # 只列"每个数据列一条"：'ls' 会画线 + 点两次，不收敛就会重复两条（坑 #42）
            try:
                txt = '\r\n'.join('\\l(%d) %%(%d)' % (k, k)
                                  for k in dict.fromkeys(self._legend_idx))
                lb.set_str('text', txt)
                op.lt_exec('doc -uw')
            except Exception as e:
                print('set legend text failed, 用 Origin 自动条目:', e)
        size = st.legend_size_mm(gl)

        corner = where
        if where == 'auto':
            gl.lt_exec('legend.show=0;')            # 量完尺寸先藏起来，别把自己算成障碍物
            mask = self._ink_mask()
            gl.lt_exec('legend.show=1;')
            scores = self._corner_ink(mask, i, size, pad)
            self.legend_scores = scores
            order = ('tr', 'tl', 'br', 'bl')
            corner = min(order, key=lambda k: (scores[k], order.index(k)))
            if scores[corner] > PREFS.get('legend_ink_max', 0.004):
                corner = None

        if corner is None:
            if not grow:
                corner = 'tr'
                st.legend_place(gl, self.frames[i], corner, pad, size)
                return corner
            self._grow_top(PREFS.get('legend_grow_mm', 20.0))
            L, T, W, H = self.frames[i]
            st.legend_place_mm(gl, self.frames[i], L + W - pad - size[0], pad, size)
            return 'tr-grow'

        st.legend_place(gl, self.frames[i], corner, pad, size)
        return corner

    def finish(self):
        op.lt_exec('doc -uw')


class DualY(Page):
    """双 Y 轴单面板：og_doubley 模板（坑 #15），左层 self.left = layer(0)，右层 self.right。

        pg = DualY(journal='single', lname='COMBO')
        pg.guide(ws, 1); pg.bar(0, ws, 0, [1])                  # 左轴
        pg.guide(ws, 2, right=True); pg.plot_right(ws, 2, 0, kind='ls')
        pg.style_dual('Month', 'Oil production (10\\+(4) t)', 'Water cut (%)')
    """

    def __init__(self, journal=None, size_mm=None, lname='OGFIG_DY', margin=None, connect=True):
        m = margin or PREFS.get('margin_dual_mm', (14, 14, 6, 11))
        super().__init__(1, 1, journal=journal, size_mm=size_mm, lname=lname,
                         template='og_doubley', margin=m, connect=connect)
        self.left = self.layers[0]
        self.right = self.g[1]
        L, T, W, H = self.frames[0]
        PW, PH = self.size_mm
        st.activate(self.right)
        op.lt_exec('layer.left=%.2f; layer.top=%.2f; layer.width=%.2f; layer.height=%.2f; layer.factor=1;'
                   % (L / PW * 100, T / PH * 100, W / PW * 100, H / PH * 100))

    def guide(self, sheet, ycol, xcol=0, right=False):
        """先画透明黑引导线，锁住轴颜色（坑 #18）。每层第一条曲线之前调用。"""
        return st.guide_line(self.right if right else self.left, sheet, ycol, xcol)

    def plot_right(self, sheet, ycol, xcol=-1, **kw):
        """在右层画曲线；参数同 Page.plot。"""
        self.layers.append(self.right)
        try:
            return self.plot(len(self.layers) - 1, sheet, ycol, xcol, **kw)
        finally:
            self.layers.pop()

    def style_dual(self, xtitle='', ytitle='', y2title=''):
        st.apply_dual_axes(self.left, self.right, xtitle, ytitle, y2title,
                           fs_tick=self.spec['fs_tick'], fs_title=self.spec['fs_title'])

    def drop_legends(self):
        for gl in (self.left, self.right):
            st.drop_legends(gl)
