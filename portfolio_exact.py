#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
美术作品集 PPT 模板 - 1:1 精确还原参考图
风格：新中式美术设定集（龙门无宵坊风格）
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.dml import MSO_LINE_DASH_STYLE

# 创建 16:9 演示文稿
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# ========== 精确配色（从参考图取样）==========
COLORS = {
    'bg': RGBColor(246, 243, 238),         # 米白背景 #F6F3EE
    'bg_light': RGBColor(250, 248, 244),    # 浅米白 #FAF8F4
    'bg_dark': RGBColor(235, 230, 220),     # 深米白 #EBE6DC
    'text_main': RGBColor(55, 55, 55),      # 主文字 #373737
    'text_light': RGBColor(140, 135, 125),  # 浅文字 #8C877D
    'text_gold': RGBColor(165, 145, 115),   # 金色文字 #A59173
    'accent_green': RGBColor(135, 155, 140), # 淡绿灰 #879B8C
    'accent_red': RGBColor(175, 130, 120),   # 淡红褐 #AF8278
    'accent_blue': RGBColor(125, 145, 160),  # 淡蓝灰 #7D91A0
    'accent_gold': RGBColor(190, 170, 140),  # 淡金 #BEAA8C
    'ink_dark': RGBColor(70, 70, 75),        # 水墨深 #46464B
    'ink_light': RGBColor(150, 150, 155),    # 水墨浅 #96969B
}

def add_ink_wash(slide, x, y, width, height, color=COLORS['bg_light'], transparency=0.6, rotation=0):
    """添加水墨烟雾装饰（用椭圆组合模拟）"""
    # 主烟雾
    smoke1 = slide.shapes.add_shape(MSO_SHAPE.OVAL, x, y, width * 0.6, height * 0.8)
    smoke1.fill.solid()
    smoke1.fill.fore_color.rgb = color
    smoke1.fill.transparency = transparency
    smoke1.line.fill.background()
    smoke1.rotation = rotation
    
    # 辅助烟雾
    smoke2 = slide.shapes.add_shape(MSO_SHAPE.OVAL, x + width * 0.3, y + height * 0.1, width * 0.5, height * 0.6)
    smoke2.fill.solid()
    smoke2.fill.fore_color.rgb = color
    smoke2.fill.transparency = transparency + 0.1
    smoke2.line.fill.background()
    smoke2.rotation = rotation + 15
    
    return smoke1

def add_decorative_line(slide, x1, y1, x2, y2, color=COLORS['accent_gold'], width=Pt(2)):
    """添加装饰线条"""
    line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x1, y1, x2, y2)
    line.line.color.rgb = color
    line.line.width = width
    line.line.transparency = 0  # 不透明，确保可见
    return line

def add_seal(slide, x, y, size, text=""):
    """添加印章效果"""
    seal = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, size, size)
    seal.fill.solid()
    seal.fill.fore_color.rgb = COLORS['accent_red']
    seal.fill.transparency = 0.5  # 减少透明，更明显
    seal.line.color.rgb = COLORS['accent_red']
    seal.line.width = Pt(2)  # 加粗边框
    
    if text:
        seal_text = slide.shapes.add_textbox(x, y, size, size)
        seal_frame = seal_text.text_frame
        seal_para = seal_frame.paragraphs[0]
        seal_para.text = text
        seal_para.font.size = Pt(14)  # 加大字体
        seal_para.font.color.rgb = COLORS['accent_red']
        seal_para.font.name = "STSong"
        seal_para.alignment = PP_ALIGN.CENTER
    
    return seal

def add_hexagon_decor(slide, x, y, size, color=COLORS['accent_green'], filled=False):
    """添加六边形装饰"""
    hex_shape = slide.shapes.add_shape(MSO_SHAPE.HEXAGON, x, y, size, size * 0.87)
    if filled:
        hex_shape.fill.solid()
        hex_shape.fill.fore_color.rgb = color
        hex_shape.fill.transparency = 0.7  # 减少透明，更明显
        hex_shape.line.color.rgb = color
        hex_shape.line.width = Pt(1.5)  # 加粗边框
    else:
        hex_shape.fill.background()
        hex_shape.line.color.rgb = color
        hex_shape.line.width = Pt(2)  # 加粗边框
        hex_shape.line.transparency = 0  # 不透明
    return hex_shape

def add_image_placeholder(slide, x, y, width, height, label="图片占位", dashed=True):
    """添加图片占位框"""
    placeholder = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, width, height)
    placeholder.fill.solid()
    placeholder.fill.fore_color.rgb = COLORS['bg_light']
    placeholder.fill.transparency = 0.3
    
    if dashed:
        placeholder.line.color.rgb = COLORS['accent_green']
        placeholder.line.width = Pt(2.5)  # 加粗虚线框
        placeholder.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    else:
        placeholder.line.color.rgb = COLORS['accent_green']
        placeholder.line.width = Pt(2)  # 加粗实线框
    
    # 添加提示文字
    text_box = slide.shapes.add_textbox(x, y + height/2 - Inches(0.25), width, Inches(0.5))
    text_frame = text_box.text_frame
    text_para = text_frame.paragraphs[0]
    text_para.text = label
    text_para.font.size = Pt(12)
    text_para.font.color.rgb = COLORS['text_light']
    text_para.font.name = "Microsoft YaHei"
    text_para.alignment = PP_ALIGN.CENTER
    
    return placeholder

# ==================== 封面页 ====================
def add_cover_slide(prs):
    """封面页 - 精确还原参考图布局"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 背景
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLORS['bg']
    bg.line.fill.background()
    
    # === 左上角水墨装饰 ===
    add_ink_wash(slide, Inches(0), Inches(0), Inches(5), Inches(3.5), COLORS['bg_dark'], 0.7, 0)
    add_ink_wash(slide, Inches(0.5), Inches(0.5), Inches(3), Inches(2), COLORS['bg_light'], 0.5, 15)
    
    # === 右下角水墨装饰 ===
    add_ink_wash(slide, Inches(9), Inches(4.5), Inches(4.5), Inches(3), COLORS['bg_dark'], 0.65, 180)
    
    # === 中央大标题"集"字 ===
    title = slide.shapes.add_textbox(Inches(5), Inches(1.8), Inches(3.5), Inches(4))
    title_frame = title.text_frame
    title_para = title_frame.paragraphs[0]
    title_para.text = "集"
    title_para.font.size = Pt(140)
    title_para.font.color.rgb = COLORS['ink_dark']
    title_para.font.name = "STSong"
    title_para.alignment = PP_ALIGN.CENTER
    
    # === 左侧竖排小字"作品集" ===
    left_vertical = slide.shapes.add_textbox(Inches(4.3), Inches(2.5), Inches(0.6), Inches(2.5))
    left_frame = left_vertical.text_frame
    left_para = left_frame.paragraphs[0]
    left_para.text = "作\n品\n集"
    left_para.font.size = Pt(16)
    left_para.font.color.rgb = COLORS['text_light']
    left_para.font.name = "STSong"
    left_para.alignment = PP_ALIGN.CENTER
    
    # === 右侧竖排小字"美术设定" ===
    right_vertical = slide.shapes.add_textbox(Inches(8.8), Inches(2.5), Inches(0.6), Inches(2.5))
    right_frame = right_vertical.text_frame
    right_para = right_frame.paragraphs[0]
    right_para.text = "美\n术\n设\n定"
    right_para.font.size = Pt(16)
    right_para.font.color.rgb = COLORS['text_light']
    right_para.font.name = "STSong"
    right_para.alignment = PP_ALIGN.CENTER
    
    # === 底部横线装饰 ===
    add_decorative_line(slide, Inches(4), Inches(6.2), Inches(9.5), Inches(6.2), COLORS['accent_gold'], Pt(0.75))
    
    # === 底部文字 ===
    bottom_text = slide.shapes.add_textbox(Inches(4), Inches(6.4), Inches(5.5), Inches(0.5))
    bottom_frame = bottom_text.text_frame
    bottom_para = bottom_frame.paragraphs[0]
    bottom_para.text = "小天狼星 · 游戏策划 · PORTFOLIO 2024-2025"
    bottom_para.font.size = Pt(11)
    bottom_para.font.color.rgb = COLORS['text_gold']
    bottom_para.font.name = "Microsoft YaHei"
    bottom_para.alignment = PP_ALIGN.CENTER
    
    # === 右上角六边形装饰组 ===
    add_hexagon_decor(slide, Inches(11), Inches(0.5), Inches(1), COLORS['accent_green'], True)
    add_hexagon_decor(slide, Inches(11.8), Inches(0.8), Inches(0.8), COLORS['accent_green'], False)
    add_hexagon_decor(slide, Inches(11), Inches(1.1), Inches(1), COLORS['accent_green'], False)
    
    # === 左上角印章 ===
    add_seal(slide, Inches(0.3), Inches(0.3), Inches(0.8), "集")
    
    return slide

# ==================== 角色介绍页（核心页面）====================
def add_character_main_slide(prs, char_name, char_subtitle):
    """角色主介绍页 - 1:1 还原参考图角色页布局"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 背景
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLORS['bg']
    bg.line.fill.background()
    
    # === 左上角水墨装饰 ===
    add_ink_wash(slide, Inches(0), Inches(0), Inches(4), Inches(2.5), COLORS['bg_dark'], 0.6, 0)
    
    # === 右侧六边形装饰组 ===
    add_hexagon_decor(slide, Inches(10.8), Inches(0.6), Inches(1.1), COLORS['accent_green'], True)
    add_hexagon_decor(slide, Inches(11.7), Inches(1), Inches(0.9), COLORS['accent_green'], False)
    add_hexagon_decor(slide, Inches(10.8), Inches(1.4), Inches(1.1), COLORS['accent_green'], False)
    add_hexagon_decor(slide, Inches(11.5), Inches(1.8), Inches(0.8), COLORS['accent_blue'], True)
    
    # === 角色名（大字）===
    name_box = slide.shapes.add_textbox(Inches(7.8), Inches(0.4), Inches(5), Inches(1.5))
    name_frame = name_box.text_frame
    name_para = name_frame.paragraphs[0]
    name_para.text = char_name
    name_para.font.size = Pt(48)
    name_para.font.color.rgb = COLORS['ink_dark']
    name_para.font.name = "STSong"
    name_para.alignment = PP_ALIGN.RIGHT
    
    # === 角色副标题 ===
    subtitle_box = slide.shapes.add_textbox(Inches(7.8), Inches(1.7), Inches(5), Inches(0.5))
    subtitle_frame = subtitle_box.text_frame
    subtitle_para = subtitle_frame.paragraphs[0]
    subtitle_para.text = char_subtitle
    subtitle_para.font.size = Pt(16)
    subtitle_para.font.color.rgb = COLORS['accent_red']
    subtitle_para.font.name = "Microsoft YaHei"
    subtitle_para.alignment = PP_ALIGN.RIGHT
    
    # === 装饰横线 ===
    add_decorative_line(slide, Inches(7.8), Inches(2.1), Inches(12.5), Inches(2.1), COLORS['accent_gold'], Pt(0.75))
    
    # === 角色立绘主图（左侧大图）===
    main_art = add_image_placeholder(slide, Inches(0.6), Inches(0.6), Inches(5.8), Inches(6.2), "【角色立绘】\n替换为你的作品", dashed=True)
    
    # === 三视图区域（右侧）===
    # 正面图
    front_view = add_image_placeholder(slide, Inches(7.8), Inches(2.5), Inches(1.4), Inches(3.2), "正面", dashed=True)
    
    # 侧面图
    side_view = add_image_placeholder(slide, Inches(9.5), Inches(2.5), Inches(1.4), Inches(3.2), "侧面", dashed=True)
    
    # 背面图
    back_view = add_image_placeholder(slide, Inches(11.2), Inches(2.5), Inches(1.4), Inches(3.2), "背面", dashed=True)
    
    # === 三视图标签 ===
    for i, (x, label) in enumerate([(7.8, "正面"), (9.5, "侧面"), (11.2, "背面")]):
        label_box = slide.shapes.add_textbox(Inches(x), Inches(5.8), Inches(1.4), Inches(0.4))
        label_frame = label_box.text_frame
        label_para = label_frame.paragraphs[0]
        label_para.text = label
        label_para.font.size = Pt(11)
        label_para.font.color.rgb = COLORS['text_light']
        label_para.font.name = "Microsoft YaHei"
        label_para.alignment = PP_ALIGN.CENTER
    
    # === 角色介绍文字区 ===
    desc_box = slide.shapes.add_textbox(Inches(7.8), Inches(6.1), Inches(5), Inches(1.1))
    desc_frame = desc_box.text_frame
    desc_frame.word_wrap = True
    
    desc_lines = [
        ("角色背景 / 设计理念", 13, True),
        ("", 10),
        ("在此处填写角色的详细信息，包括性格特点、", 10),
        ("背景故事、以及在游戏中的定位...", 10),
    ]
    
    for i, line in enumerate(desc_lines):
        para = desc_frame.add_paragraph() if i > 0 else desc_frame.paragraphs[0]
        para.text = line[0]
        para.font.size = Pt(line[1])
        para.font.color.rgb = COLORS['accent_red'] if len(line) > 2 else COLORS['text_light']
        para.font.name = "Microsoft YaHei"
        if len(line) > 2:
            para.font.bold = True
    
    # === 页面编号 ===
    page_num = slide.shapes.add_textbox(Inches(12.5), Inches(7.1), Inches(0.5), Inches(0.3))
    page_frame = page_num.text_frame
    page_para = page_frame.paragraphs[0]
    page_para.text = "01"
    page_para.font.size = Pt(9)
    page_para.font.color.rgb = COLORS['text_light']
    page_para.font.name = "Microsoft YaHei"
    page_para.alignment = PP_ALIGN.RIGHT
    
    return slide

# ==================== 角色细节页 ====================
def add_character_detail_slide(prs, char_name, detail_title):
    """角色细节/表情/动作页"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 背景
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLORS['bg']
    bg.line.fill.background()
    
    # === 右下角水墨装饰 ===
    add_ink_wash(slide, Inches(9.5), Inches(5), Inches(3.8), Inches(2.5), COLORS['bg_dark'], 0.6, 180)
    
    # === 标题区 ===
    title_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.5), Inches(8), Inches(1))
    title_frame = title_box.text_frame
    title_para = title_frame.paragraphs[0]
    title_para.text = char_name
    title_para.font.size = Pt(36)
    title_para.font.color.rgb = COLORS['ink_dark']
    title_para.font.name = "STSong"
    
    subtitle_box = slide.shapes.add_textbox(Inches(0.6), Inches(1.3), Inches(8), Inches(0.4))
    subtitle_frame = subtitle_box.text_frame
    subtitle_para = subtitle_frame.paragraphs[0]
    subtitle_para.text = detail_title
    subtitle_para.font.size = Pt(14)
    subtitle_para.font.color.rgb = COLORS['accent_blue']
    subtitle_para.font.name = "Microsoft YaHei"
    
    # === 装饰线 ===
    add_decorative_line(slide, Inches(0.6), Inches(1.7), Inches(2.5), Inches(1.7), COLORS['accent_gold'], Pt(0.75))
    
    # === 表情/动作网格（3x2）===
    positions = [
        (0.6, 2.1), (3.2, 2.1), (5.8, 2.1),   # 上排
        (0.6, 4.5), (3.2, 4.5), (5.8, 4.5),   # 下排
    ]
    labels = ["表情 01", "表情 02", "表情 03", "动作 01", "动作 02", "动作 03"]
    
    for (x, y), label in zip(positions, labels):
        add_image_placeholder(slide, Inches(x), Inches(y), Inches(2.3), Inches(2.1), label, dashed=True)
    
    # === 右侧说明区 ===
    note_box = slide.shapes.add_textbox(Inches(8.5), Inches(2.1), Inches(4.3), Inches(4.8))
    note_frame = note_box.text_frame
    note_frame.word_wrap = True
    
    note_lines = [
        ("设计说明", 16, True),
        ("", 10),
        ("在此处详细描述角色的表情变化、", 11),
        ("动作设计思路、以及动画表现要点。", 11),
        ("", 12),
        ("关键词", 14, True),
        ("", 8),
        ("• 表情丰富度", 11),
        ("• 动作流畅性", 11),
        ("• 性格体现", 11),
        ("• 视觉识别度", 11),
    ]
    
    for i, line in enumerate(note_lines):
        para = note_frame.add_paragraph() if i > 0 else note_frame.paragraphs[0]
        para.text = line[0]
        para.font.size = Pt(line[1])
        para.font.color.rgb = COLORS['accent_red'] if len(line) > 2 else COLORS['text_main']
        para.font.name = "Microsoft YaHei"
        if len(line) > 2:
            para.font.bold = True
    
    # === 页面编号 ===
    page_num = slide.shapes.add_textbox(Inches(12.5), Inches(7.1), Inches(0.5), Inches(0.3))
    page_frame = page_num.text_frame
    page_para = page_frame.paragraphs[0]
    page_para.text = "02"
    page_para.font.size = Pt(9)
    page_para.font.color.rgb = COLORS['text_light']
    page_para.font.name = "Microsoft YaHei"
    page_para.alignment = PP_ALIGN.RIGHT
    
    return slide

# ==================== 概念设计页 ====================
def add_concept_slide(prs, concept_name, concept_type):
    """场景/道具概念设计页"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 背景
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLORS['bg']
    bg.line.fill.background()
    
    # === 左上角水墨装饰 ===
    add_ink_wash(slide, Inches(0), Inches(0), Inches(3.5), Inches(2), COLORS['bg_dark'], 0.6, 0)
    
    # === 标题区 ===
    title_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.5), Inches(7), Inches(1))
    title_frame = title_box.text_frame
    title_para = title_frame.paragraphs[0]
    title_para.text = concept_name
    title_para.font.size = Pt(36)
    title_para.font.color.rgb = COLORS['ink_dark']
    title_para.font.name = "STSong"
    
    subtitle_box = slide.shapes.add_textbox(Inches(0.6), Inches(1.3), Inches(7), Inches(0.4))
    subtitle_frame = subtitle_box.text_frame
    subtitle_para = subtitle_frame.paragraphs[0]
    subtitle_para.text = concept_type
    subtitle_para.font.size = Pt(14)
    subtitle_para.font.color.rgb = COLORS['accent_green']
    subtitle_para.font.name = "Microsoft YaHei"
    
    # === 装饰线 ===
    add_decorative_line(slide, Inches(0.6), Inches(1.7), Inches(2.5), Inches(1.7), COLORS['accent_gold'], Pt(0.75))
    
    # === 设计稿网格（2x2）===
    positions = [
        (0.6, 2.1, "设计稿 A"),
        (5.2, 2.1, "设计稿 B"),
        (0.6, 4.8, "设计稿 C"),
        (5.2, 4.8, "设计稿 D"),
    ]
    
    for x, y, label in positions:
        add_image_placeholder(slide, Inches(x), Inches(y), Inches(4.3), Inches(2.4), label, dashed=True)
    
    # === 右侧说明区 ===
    note_box = slide.shapes.add_textbox(Inches(8.5), Inches(2.1), Inches(4.3), Inches(4.8))
    note_frame = note_box.text_frame
    note_frame.word_wrap = True
    
    note_lines = [
        ("设计理念", 16, True),
        ("", 10),
        ("在此处填写概念设计的核心思路和", 11),
        ("创意来源，包括参考素材、文化背景等。", 11),
        ("", 12),
        ("关键词", 14, True),
        ("", 8),
        ("• 东方美学", 11),
        ("• 现代融合", 11),
        ("• 功能性与美观", 11),
        ("• 世界观契合", 11),
    ]
    
    for i, line in enumerate(note_lines):
        para = note_frame.add_paragraph() if i > 0 else note_frame.paragraphs[0]
        para.text = line[0]
        para.font.size = Pt(line[1])
        para.font.color.rgb = COLORS['accent_red'] if len(line) > 2 else COLORS['text_main']
        para.font.name = "Microsoft YaHei"
        if len(line) > 2:
            para.font.bold = True
    
    # === 页面编号 ===
    page_num = slide.shapes.add_textbox(Inches(12.5), Inches(7.1), Inches(0.5), Inches(0.3))
    page_frame = page_num.text_frame
    page_para = page_frame.paragraphs[0]
    page_para.text = "03"
    page_para.font.size = Pt(9)
    page_para.font.color.rgb = COLORS['text_light']
    page_para.font.name = "Microsoft YaHei"
    page_para.alignment = PP_ALIGN.RIGHT
    
    return slide

# ==================== 过渡页 ====================
def add_transition_slide(prs, section_name, section_num):
    """章节过渡页"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 背景
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLORS['bg']
    bg.line.fill.background()
    
    # === 大面积水墨背景 ===
    add_ink_wash(slide, Inches(1.5), Inches(0.8), Inches(10), Inches(5.5), COLORS['bg_dark'], 0.75, 0)
    add_ink_wash(slide, Inches(2), Inches(1.2), Inches(8), Inches(4.5), COLORS['bg_light'], 0.6, 10)
    
    # === 章节编号（大字半透明）===
    num_bg = slide.shapes.add_textbox(Inches(0.5), Inches(1), Inches(4), Inches(5))
    num_bg_frame = num_bg.text_frame
    num_bg_para = num_bg_frame.paragraphs[0]
    num_bg_para.text = section_num
    num_bg_para.font.size = Pt(150)
    num_bg_para.font.color.rgb = COLORS['bg_light']
    num_bg_para.font.name = "STSong"
    num_bg_para.alignment = PP_ALIGN.CENTER
    
    # === 章节名（前景）===
    title = slide.shapes.add_textbox(Inches(3.5), Inches(2.8), Inches(7), Inches(2))
    title_frame = title.text_frame
    title_para = title_frame.paragraphs[0]
    title_para.text = section_name
    title_para.font.size = Pt(54)
    title_para.font.color.rgb = COLORS['ink_dark']
    title_para.font.name = "STSong"
    title_para.alignment = PP_ALIGN.CENTER
    
    # === 英文副标题 ===
    subtitle = slide.shapes.add_textbox(Inches(3.5), Inches(4.5), Inches(7), Inches(0.6))
    subtitle_frame = subtitle.text_frame
    subtitle_para = subtitle_frame.paragraphs[0]
    subtitle_para.text = "CHAPTER"
    subtitle_para.font.size = Pt(14)
    subtitle_para.font.color.rgb = COLORS['text_gold']
    subtitle_para.font.name = "Microsoft YaHei"
    subtitle_para.alignment = PP_ALIGN.CENTER
    
    # === 装饰元素 ===
    add_hexagon_decor(slide, Inches(0.8), Inches(0.6), Inches(0.9), COLORS['accent_green'], False)
    add_hexagon_decor(slide, Inches(11.8), Inches(6.2), Inches(0.9), COLORS['accent_green'], False)
    
    return slide

# ==================== 灵感/参考页 ====================
def add_inspiration_slide(prs):
    """灵感参考页（宝丽来风格）"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 背景
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLORS['bg']
    bg.line.fill.background()
    
    # === 左上角水墨装饰 ===
    add_ink_wash(slide, Inches(0), Inches(0), Inches(4), Inches(3), COLORS['bg_dark'], 0.6, 0)
    
    # === 标题 ===
    title_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.5), Inches(6), Inches(0.8))
    title_frame = title_box.text_frame
    title_para = title_frame.paragraphs[0]
    title_para.text = "创作灵感"
    title_para.font.size = Pt(32)
    title_para.font.color.rgb = COLORS['ink_dark']
    title_para.font.name = "STSong"
    
    # === 宝丽来照片组 ===
    # 照片 1
    polaroid1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.6), Inches(2.8), Inches(3.3))
    polaroid1.fill.solid()
    polaroid1.fill.fore_color.rgb = RGBColor(255, 255, 255)
    polaroid1.line.color.rgb = COLORS['accent_gold']
    polaroid1.line.width = Pt(0.75)
    
    photo1_inner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.75), Inches(1.75), Inches(2.5), Inches(2.5))
    photo1_inner.fill.solid()
    photo1_inner.fill.fore_color.rgb = COLORS['bg_light']
    photo1_inner.line.color.rgb = COLORS['text_light']
    photo1_inner.line.width = Pt(1)
    photo1_inner.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    
    caption1 = slide.shapes.add_textbox(Inches(0.75), Inches(4.35), Inches(2.5), Inches(0.4))
    cap1_frame = caption1.text_frame
    cap1_para = cap1_frame.paragraphs[0]
    cap1_para.text = "参考素材 01"
    cap1_para.font.size = Pt(10)
    cap1_para.font.color.rgb = COLORS['text_light']
    cap1_para.font.name = "Microsoft YaHei"
    cap1_para.alignment = PP_ALIGN.CENTER
    
    # 照片 2
    polaroid2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(3.7), Inches(1.6), Inches(2.8), Inches(3.3))
    polaroid2.fill.solid()
    polaroid2.fill.fore_color.rgb = RGBColor(255, 255, 255)
    polaroid2.line.color.rgb = COLORS['accent_gold']
    polaroid2.line.width = Pt(0.75)
    
    photo2_inner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(3.85), Inches(1.75), Inches(2.5), Inches(2.5))
    photo2_inner.fill.solid()
    photo2_inner.fill.fore_color.rgb = COLORS['bg_light']
    photo2_inner.line.color.rgb = COLORS['text_light']
    photo2_inner.line.width = Pt(1)
    photo2_inner.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    
    caption2 = slide.shapes.add_textbox(Inches(3.85), Inches(4.35), Inches(2.5), Inches(0.4))
    cap2_frame = caption2.text_frame
    cap2_para = cap2_frame.paragraphs[0]
    cap2_para.text = "参考素材 02"
    cap2_para.font.size = Pt(10)
    cap2_para.font.color.rgb = COLORS['text_light']
    cap2_para.font.name = "Microsoft YaHei"
    cap2_para.alignment = PP_ALIGN.CENTER
    
    # 照片 3
    polaroid3 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(1.6), Inches(2.8), Inches(3.3))
    polaroid3.fill.solid()
    polaroid3.fill.fore_color.rgb = RGBColor(255, 255, 255)
    polaroid3.line.color.rgb = COLORS['accent_gold']
    polaroid3.line.width = Pt(0.75)
    
    photo3_inner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.95), Inches(1.75), Inches(2.5), Inches(2.5))
    photo3_inner.fill.solid()
    photo3_inner.fill.fore_color.rgb = COLORS['bg_light']
    photo3_inner.line.color.rgb = COLORS['text_light']
    photo3_inner.line.width = Pt(1)
    photo3_inner.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    
    caption3 = slide.shapes.add_textbox(Inches(6.95), Inches(4.35), Inches(2.5), Inches(0.4))
    cap3_frame = caption3.text_frame
    cap3_para = cap3_frame.paragraphs[0]
    cap3_para.text = "参考素材 03"
    cap3_para.font.size = Pt(10)
    cap3_para.font.color.rgb = COLORS['text_light']
    cap3_para.font.name = "Microsoft YaHei"
    cap3_para.alignment = PP_ALIGN.CENTER
    
    # === 右侧文字区 ===
    note_box = slide.shapes.add_textbox(Inches(8.5), Inches(1.6), Inches(4.3), Inches(5.2))
    note_frame = note_box.text_frame
    note_frame.word_wrap = True
    
    note_lines = [
        ("灵感来源", 16, True),
        ("", 10),
        ("在此处记录创作过程中的灵感来源、", 11),
        ("参考的文化元素、艺术作品、以及", 11),
        ("任何激发创意的素材。", 11),
        ("", 12),
        ("关键词", 14, True),
        ("", 8),
        ("• 传统文化", 11),
        ("• 现代演绎", 11),
        ("• 视觉叙事", 11),
        ("• 情感表达", 11),
    ]
    
    for i, line in enumerate(note_lines):
        para = note_frame.add_paragraph() if i > 0 else note_frame.paragraphs[0]
        para.text = line[0]
        para.font.size = Pt(line[1])
        para.font.color.rgb = COLORS['accent_red'] if len(line) > 2 else COLORS['text_main']
        para.font.name = "Microsoft YaHei"
        if len(line) > 2:
            para.font.bold = True
    
    # === 页面编号 ===
    page_num = slide.shapes.add_textbox(Inches(12.5), Inches(7.1), Inches(0.5), Inches(0.3))
    page_frame = page_num.text_frame
    page_para = page_frame.paragraphs[0]
    page_para.text = "04"
    page_para.font.size = Pt(9)
    page_para.font.color.rgb = COLORS['text_light']
    page_para.font.name = "Microsoft YaHei"
    page_para.alignment = PP_ALIGN.RIGHT
    
    return slide

# ==================== 封底页 ====================
def add_back_cover_slide(prs):
    """封底页"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 背景
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLORS['bg']
    bg.line.fill.background()
    
    # === 水墨装饰 ===
    add_ink_wash(slide, Inches(0), Inches(0), Inches(5), Inches(3.5), COLORS['bg_dark'], 0.7, 0)
    add_ink_wash(slide, Inches(9), Inches(4.5), Inches(4.5), Inches(3), COLORS['bg_dark'], 0.65, 180)
    
    # === 感谢文字 ===
    thanks = slide.shapes.add_textbox(Inches(4), Inches(2.5), Inches(5.5), Inches(1.5))
    thanks_frame = thanks.text_frame
    thanks_para = thanks_frame.paragraphs[0]
    thanks_para.text = "感谢观看"
    thanks_para.font.size = Pt(48)
    thanks_para.font.color.rgb = COLORS['ink_dark']
    thanks_para.font.name = "STSong"
    thanks_para.alignment = PP_ALIGN.CENTER
    
    # === 联系方式 ===
    contact = slide.shapes.add_textbox(Inches(4), Inches(4), Inches(5.5), Inches(2))
    contact_frame = contact.text_frame
    contact_frame.word_wrap = True
    
    contact_lines = [
        ("联系方式", 16, True),
        ("", 8),
        ("📧 Email: your.email@example.com", 12),
        ("📱 微信：your_wechat", 12),
        ("💼 作品集：your-portfolio.com", 12),
    ]
    
    for i, line in enumerate(contact_lines):
        para = contact_frame.add_paragraph() if i > 0 else contact_frame.paragraphs[0]
        para.text = line[0]
        para.font.size = Pt(line[1])
        para.font.color.rgb = COLORS['accent_red'] if len(line) > 2 else COLORS['text_main']
        para.font.name = "Microsoft YaHei"
        if len(line) > 2:
            para.font.bold = True
        para.alignment = PP_ALIGN.CENTER
    
    # === 底部装饰线 ===
    add_decorative_line(slide, Inches(4), Inches(6.2), Inches(9.5), Inches(6.2), COLORS['accent_gold'], Pt(0.75))
    
    return slide

# ==================== 生成所有页面 ====================
print("🦐 正在 1:1 还原新中式美术作品集 PPT...")

# 封面
add_cover_slide(prs)

# 第一章：角色设计
add_transition_slide(prs, "角色设计", "01")
add_character_main_slide(prs, "角色名称", "龙门无宵坊 · 主角设定")
add_character_detail_slide(prs, "角色名称", "表情与动作设计")

# 第二章：概念设计
add_transition_slide(prs, "概念设计", "02")
add_concept_slide(prs, "场景概念", "Environment Concept")
add_concept_slide(prs, "道具设计", "Prop Design")

# 灵感页
add_inspiration_slide(prs)

# 封底
add_back_cover_slide(prs)

# 保存
output_path = "/Users/sirius/.openclaw/workspace-default/美术作品集_精确还原.pptx"
prs.save(output_path)

print(f"✅ PPT 已生成：{output_path}")
print(f"📄 共 10 页")
print(f"   - 封面 ×1")
print(f"   - 过渡页 ×2")
print(f"   - 角色主介绍 ×1")
print(f"   - 角色细节 ×1")
print(f"   - 概念设计 ×2")
print(f"   - 灵感参考 ×1")
print(f"   - 封底 ×1")
print(f"🎨 风格：新中式美术设定集（1:1 还原参考图）")
print(f"📝 提示：所有虚线框都可以右键→更改图片来替换")
