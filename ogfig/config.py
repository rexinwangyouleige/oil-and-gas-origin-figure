# -*- coding: utf-8 -*-
"""ogfig.config — 你的偏好，全部在这里改。改完直接重跑脚本，不用动别的文件。

⚠️ 下面是用户的硬性规范（每次出图必须遵守，不用再提醒）：
   1. 所有文字西文一律 Times New Roman、中文一律宋体：轴标题、刻度标签、曲线标注、图例、面板字母。
   2. 字号 7–9 pt（"明显版"档 9–11 pt）：刻度标签 7 / 轴标题 8 / 图例与曲线标注 8 / 面板字母 9。
      这是**成图实际尺寸下**的 pt：Page 会按 page_mm（或 journal 档位）把 Origin 页面设成真实毫米，
      导出时宽度也按这个毫米数算，所以 PDF 里量出来就是 7 / 8 / 9 pt。
   3. 刻度：有数据的边（左、下、右）主刻度朝内；无数据的上边框只留框线、不要刻度。
   4. 次刻度一律不要。
   5. 轴标题里的单位不要重复出现（例如 DTG 已有 (%/℃) 就不再加单位）。
   6. 双 Y 轴用 Origin 自带 doubley 模板，右侧那根轴的刻度也必须朝内。
   7. 图例：文字取自表格列 long name；无边框；放在坐标区四个角里最空的那个角；
      四个角都放不下时把页面上边加高，放右上角（见 STYLE_PRESETS / LEGEND）。

## 两档风格预设（STYLE_PRESETS）

    'normal'  默认：字号 7/8/8/9，轴 0.75 pt、线 1.0 pt、刻度长 3、符号 4 —— 期刊单双栏常规版
    'bold'    明显版：字号 9/10/10/11，轴 1.5 pt、线 2.0 pt、刻度长 4.5、符号 6 —— 幻灯片 / 挂图 / 答辩

改档位：脚本里 `style.set_preset('bold')`，或把下面的 `PRESET` 改成 'bold' 当默认。
"""
import copy

PALETTES = {
    # 通用
    'OG':    ['#1F4E79', '#C0504D', '#9BBB59', '#F79646', '#4BACC6', '#7F7F7F'],
    'SPE':   ['#003366', '#CC0000', '#006633', '#FF9900', '#660099', '#4BACC6'],
    'OKABE': ['#0072B2', '#D55E00', '#009E73', '#CC79A7', '#F0E442', '#56B4E9'],

    # 顶刊色卡（用户提供的 5 张图）
    'BATT':  ['#BADDF3', '#C8C3E1', '#B581B4', '#B1A8D3', '#B5C3EA',
              '#7FBDB0', '#F4E09B', '#EAB170', '#DA8176', '#7BADDF'],
    'HYDRO': ['#F7CCCD', '#F6D8AE', '#DCE79C', '#B8DA9B', '#9DD09F',
              '#95D1C9', '#96CFF0', '#B4DCE1'],
    'PVSK':  ['#AFD58C', '#5EB9E9', '#77CADB', '#A7CD38', '#E9B539', '#AAD8C2',
              '#EED5E6', '#69A930', '#43BBC2', '#E55E5E', '#437235'],
    'SAC':   ['#F9CAA8', '#81CFF4', '#979BCC', '#AECE22', '#F4A468',
              '#2C9DD9', '#EA7479', '#DFEBF6', '#E2EDD9', '#2E6DB6'],

    # 温度序列（冷→热），TGA/DSC 这类图默认用这个
    'THERM': ['#2C6FAF', '#2A9D8F', '#C0504D', '#E9B539', '#7B5AA6'],
}

# ---------------- 版式 / 配色 / 字体（与"风格档"无关的部分） ----------------
BASE = {
    # 配色
    'palette': 'THERM',
    'colors': None,

    # 字体（硬性）
    'font_latin': 'Times New Roman',
    'font_cjk': 'SimSun',

    # 刻度（硬性）
    'tick_major': 'in',
    'minor_ticks': False,
    'frame_ticks': False,

    # 版式
    'journal': 'double',            # 'single' 90x70 / '1.5' 140x105 / 'double' 180x130 (mm)
    'page_mm': None,
    'margin_mm': (14, 4, 6, 11),    # 左 右 上 下：留给刻度数字 + 轴标题 + 面板字母
    'margin_dual_mm': (14, 14, 6, 11),
    'gap_mm': (16, 15),
    'dual_y_template': 'doubley',

    # 图例（Page.legend 用）
    'legend_pad_mm': 2.0,       # 图例距坐标区边框
    'legend_grow_mm': 15.0,     # 四角都放不下时，把该行坐标区加高多少（图例仍留在框内）
    'legend_ink_max': 0.0,    # 候选角里墨迹像素占比超过它就算"有东西"，换下一个角
    'legend_probe_px': 1000,    # 判断空白用的探针图宽度（像素）
}

# ---------------- 两档风格预设 ----------------
STYLE_PRESETS = {
    'normal': {
        'fs_tick': 7, 'fs_title': 8, 'fs_note': 8, 'fs_letter': 9,
        'axis_thickness': 0.75, 'line_width': 1.0, 'tick_length': 3, 'symbol_size': 4,
    },
    'bold': {
        'fs_tick': 9, 'fs_title': 10, 'fs_note': 10, 'fs_letter': 11,
        'axis_thickness': 1.5, 'line_width': 2.0, 'tick_length': 4.5, 'symbol_size': 6,
        # 字号大了，页边距也要跟着放开（10 pt 的轴标题比 8 pt 高 ~25%，14 mm 左边距会压出界）
        'margin_mm': (17, 4, 8, 13),
        'margin_dual_mm': (17, 15, 8, 13),
    },
}

PRESET = 'normal'          # 'normal'（默认）或 'bold'（明显版）

PREFS = copy.deepcopy(BASE)
PREFS.update(STYLE_PRESETS[PRESET])
PREFS['preset'] = PRESET
