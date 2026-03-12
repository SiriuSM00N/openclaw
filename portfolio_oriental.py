#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
美术作品集 PPT 模板 - 新中式设定集风格
参考：龙门无宵坊美术集
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Cm
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_LINE_DASH_STYLE

# 创建演示文稿 16:9
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# 配色方案（新中式低饱和）
COLORS = {
    'bg': RGBColor(248, 245, 240),        # 米白背景
    'bg_light': RGBColor(252, 250, 248),   # 浅米白
    'text_dark': RGBColor(60, 60, 60),     # 深灰文字
    'text_light': RGBColor(120, 120, 120), # 浅灰文字
    'accent_green': RGBColor(140, 165, 145),  # 淡绿
    'accent_red': RGBColor(180, 135, 130),    # 淡红
    'accent_blue': RGBColor(130, 150, 170),   # 淡蓝
    'accent_gold': RGBColor(195, 175, 145),   # 淡金
    'ink': RGBColor(80, 80, 85),              # 水墨色
}

def add_smoke_decoration(slide, x, y, width, height, color=COLORS['bg_light'], rotation=0):
    """添加烟雾装饰元素"""
    smoke = slide.shapes.add_shape(MSO_SHAPE.CLOUD, x, y, width, height)
    smoke.fill.solid()
    smoke.fill.fore_color.rgb = color
    smoke.line.fill.background()
    smoke.rotation = rotation
    smoke.transparency = 0.7
    return smoke

def add_hexagon(slide, x, y, size, color=COLORS['accent_green'], filled=True):
    """添加六边形装饰"""
    hex_shape = slide.shapes.add_shape(MSO_SHAPE.HEXAGON, x, y, size, size * 0.87)
    if filled:
        hex_shape.fill.solid()
        hex_shape.fill.fore_color.rgb = color
        hex_shape.fill.transparency = 0.8
        hex_shape.line.color.rgb = color
        hex_shape.line.width = Pt(1)
    else:
        hex_shape.fill.background()
        hex_shape.line.color.rgb = color
        hex_shape.line.width = Pt(1.5)
    return hex_shape

def add_vertical_text(slide, text, x, y, font_size=14, color=COLORS['text_dark'], bold=False):
    """添加竖排文字"""
    textbox = slide.shapes.add_textbox(x, y, Inches(0.8), Inches(3))
    frame = textbox.text_frame
    frame.word_wrap = False
    
    para = frame.paragraphs[0]
    para.text = text
    para.font.size = Pt(font_size)
    para.font.color.rgb = color
    para.font.bold = bold
    para.font.name = "STSong"  # 华文宋体
    
    return textbox

def add_cover_slide(prs):
    """封面页 - 模仿参考图左上角"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 背景
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLORS['bg']
    bg.line.fill.background()
    
    # 烟雾装饰（左上）
    add_smoke_decoration(slide, Inches(0), Inches(0), Inches(5), Inches(3), rotation=45)
    
    # 烟雾装饰（右下）
    add_smoke_decoration(slide, Inches(8), Inches(4.5), Inches(5), Inches(3), rotation=225)
    
    # 大标题"集"字
    title = slide.shapes.add_textbox(Inches(4.5), Inches(2), Inches(4), Inches(3.5))
    title_frame = title.text_frame
    title_para = title_frame.paragraphs[0]
    title_para.text = "集"
    title_para.font.size = Pt(120)
    title_para.font.color.rgb = COLORS['ink']
    title_para.font.name = "STSong"
    title_para.alignment = PP_ALIGN.CENTER
    
    # 副标题 - 竖排
    add_vertical_text(slide, "作品集", Inches(3.8), Inches(2.2), 18, COLORS['text_light'])
    add_vertical_text(slide, "美术设定", Inches(8.8), Inches(2.2), 18, COLORS['text_light'])
    
    # 底部信息
    info = slide.shapes.add_textbox(Inches(1), Inches(6.5), Inches(11), Inches(0.6))
    info_frame = info.text_frame
    info_para = info_frame.paragraphs[0]
    info_para.text = "小天狼星 · 游戏策划 · 2024-2025"
    info_para.font.size = Pt(14)
    info_para.font.color.rgb = COLORS['text_light']
    info_para.font.name = "Microsoft YaHei"
    info_para.alignment = PP_ALIGN.CENTER
    
    return slide

def add_character_slide(prs, char_name, char_title):
    """角色介绍页 - 模仿参考图角色页"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 背景
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLORS['bg']
    bg.line.fill.background()
    
    # 左上烟雾
    add_smoke_decoration(slide, Inches(0), Inches(0), Inches(4), Inches(2.5), rotation=30)
    
    # 右侧六边形装饰组
    add_hexagon(slide, Inches(10.5), Inches(0.8), Inches(1.2), COLORS['accent_green'])
    add_hexagon(slide, Inches(11.5), Inches(1.2), Inches(1), COLORS['accent_green'], filled=False)
    add_hexagon(slide, Inches(10.5), Inches(1.6), Inches(1.2), COLORS['accent_green'], filled=False)
    
    # 角色名（大字）
    name_box = slide.shapes.add_textbox(Inches(7.5), Inches(0.5), Inches(5), Inches(1.5))
    name_frame = name_box.text_frame
    name_para = name_frame.paragraphs[0]
    name_para.text = char_name
    name_para.font.size = Pt(42)
    name_para.font.color.rgb = COLORS['ink']
    name_para.font.name = "STSong"
    name_para.alignment = PP_ALIGN.RIGHT
    
    # 角色标题
    title_box = slide.shapes.add_textbox(Inches(7.5), Inches(1.8), Inches(5), Inches(0.5))
    title_frame = title_box.text_frame
    title_para = title_frame.paragraphs[0]
    title_para.text = char_title
    title_para.font.size = Pt(18)
    title_para.font.color.rgb = COLORS['accent_red']
    title_para.font.name = "Microsoft YaHei"
    title_para.alignment = PP_ALIGN.RIGHT
    
    # 角色立绘占位符（左侧大图）
    char_art = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(5.5), Inches(5.5))
    char_art.fill.solid()
    char_art.fill.fore_color.rgb = COLORS['bg_light']
    char_art.line.color.rgb = COLORS['accent_green']
    char_art.line.width = Pt(2)
    char_art.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    
    # 立绘提示文字
    art_text = slide.shapes.add_textbox(Inches(0.8), Inches(3.3), Inches(5.5), Inches(0.5))
    art_text_frame = art_text.text_frame
    art_text_para = art_text_frame.paragraphs[0]
    art_text_para.text = "【角色立绘】"
    art_text_para.font.size = Pt(16)
    art_text_para.font.color.rgb = COLORS['text_light']
    art_text_para.font.name = "Microsoft YaHei"
    art_text_para.alignment = PP_ALIGN.CENTER
    
    # 三视图占位符（右侧小图）
    for i, pos in enumerate(["正面", "侧面", "背面"]):
        view_x = Inches(7.5) + i * Inches(1.7)
        view = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, view_x, Inches(2.5), Inches(1.5), Inches(3))
        view.fill.solid()
        view.fill.fore_color.rgb = COLORS['bg_light']
        view.line.color.rgb = COLORS['accent_green']
        view.line.width = Pt(1.5)
        view.line.dash_style = MSO_LINE_DASH_STYLE.DASH
        
        # 三视图标签
        view_label = slide.shapes.add_textbox(view_x, Inches(4), Inches(1.5), Inches(0.4))
        label_frame = view_label.text_frame
        label_para = label_frame.paragraphs[0]
        label_para.text = pos
        label_para.font.size = Pt(12)
        label_para.font.color.rgb = COLORS['text_light']
        label_para.font.name = "Microsoft YaHei"
        label_para.alignment = PP_ALIGN.CENTER
    
    # 角色介绍文字框
    desc_box = slide.shapes.add_textbox(Inches(7.5), Inches(5.8), Inches(5), Inches(1.3))
    desc_frame = desc_box.text_frame
    desc_frame.word_wrap = True
    desc_para = desc_frame.paragraphs[0]
    desc_para.text = "角色背景介绍 / 设计理念 / 关键词\n在此处填写角色的详细信息..."
    desc_para.font.size = Pt(12)
    desc_para.font.color.rgb = COLORS['text_light']
    desc_para.font.name = "Microsoft YaHei"
    
    # 页面编号
    page_num = slide.shapes.add_textbox(Inches(12.5), Inches(7), Inches(0.5), Inches(0.3))
    page_frame = page_num.text_frame
    page_para = page_frame.paragraphs[0]
    page_para.text = "1"
    page_para.font.size = Pt(10)
    page_para.font.color.rgb = COLORS['text_light']
    page_para.font.name = "Microsoft YaHei"
    page_para.alignment = PP_ALIGN.RIGHT
    
    return slide

def add_concept_slide(prs, concept_name):
    """概念设计页 - 模仿参考图设计稿页"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 背景
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLORS['bg']
    bg.line.fill.background()
    
    # 右下烟雾
    add_smoke_decoration(slide, Inches(9), Inches(5), Inches(4), Inches(2.5), rotation=180)
    
    # 标题
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(8), Inches(1))
    title_frame = title_box.text_frame
    title_para = title_frame.paragraphs[0]
    title_para.text = concept_name
    title_para.font.size = Pt(36)
    title_para.font.color.rgb = COLORS['ink']
    title_para.font.name = "STSong"
    
    # 副标题
    subtitle_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(8), Inches(0.4))
    subtitle_frame = subtitle_box.text_frame
    subtitle_para = subtitle_frame.paragraphs[0]
    subtitle_para.text = "Concept Design"
    subtitle_para.font.size = Pt(14)
    subtitle_para.font.color.rgb = COLORS['accent_blue']
    subtitle_para.font.name = "Microsoft YaHei"
    
    # 设计稿占位符（网格布局）
    # 左上图
    sketch1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(2), Inches(3.5), Inches(2.5))
    sketch1.fill.solid()
    sketch1.fill.fore_color.rgb = COLORS['bg_light']
    sketch1.line.color.rgb = COLORS['accent_green']
    sketch1.line.width = Pt(1.5)
    sketch1.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    
    # 右上图
    sketch2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.8), Inches(2), Inches(3.5), Inches(2.5))
    sketch2.fill.solid()
    sketch2.fill.fore_color.rgb = COLORS['bg_light']
    sketch2.line.color.rgb = COLORS['accent_green']
    sketch2.line.width = Pt(1.5)
    sketch2.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    
    # 左下图
    sketch3 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(4.8), Inches(3.5), Inches(2.3))
    sketch3.fill.solid()
    sketch3.fill.fore_color.rgb = COLORS['bg_light']
    sketch3.line.color.rgb = COLORS['accent_green']
    sketch3.line.width = Pt(1.5)
    sketch3.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    
    # 右下图
    sketch4 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.8), Inches(4.8), Inches(3.5), Inches(2.3))
    sketch4.fill.solid()
    sketch4.fill.fore_color.rgb = COLORS['bg_light']
    sketch4.line.color.rgb = COLORS['accent_green']
    sketch4.line.width = Pt(1.5)
    sketch4.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    
    # 占位提示
    for i, sketch in enumerate([sketch1, sketch2, sketch3, sketch4], 1):
        txt = slide.shapes.add_textbox(
            sketch.left, sketch.top + sketch.height/2 - Inches(0.25),
            sketch.width, Inches(0.5)
        )
        txt_frame = txt.text_frame
        txt_para = txt_frame.paragraphs[0]
        txt_para.text = f"设计稿 {i}"
        txt_para.font.size = Pt(14)
        txt_para.font.color.rgb = COLORS['text_light']
        txt_para.font.name = "Microsoft YaHei"
        txt_para.alignment = PP_ALIGN.CENTER
    
    # 设计说明
    note_box = slide.shapes.add_textbox(Inches(9), Inches(2), Inches(3.8), Inches(4.5))
    note_frame = note_box.text_frame
    note_frame.word_wrap = True
    note_para = note_frame.paragraphs[0]
    note_para.text = "设计理念\n\n在此处填写设计的核心思路和创意来源...\n\n关键词：\n• 东方美学\n• 现代融合\n• 角色特征"
    note_para.font.size = Pt(12)
    note_para.font.color.rgb = COLORS['text_dark']
    note_para.font.name = "Microsoft YaHei"
    
    return slide

def add_transition_slide(prs, section_name):
    """过渡页 - 模仿参考图过渡页"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 背景
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLORS['bg']
    bg.line.fill.background()
    
    # 大面积烟雾装饰
    add_smoke_decoration(slide, Inches(2), Inches(1), Inches(9), Inches(5), rotation=0)
    
    # 章节名（大字半透明）
    section = slide.shapes.add_textbox(Inches(1), Inches(1.5), Inches(11), Inches(4.5))
    section_frame = section.text_frame
    section_para = section_frame.paragraphs[0]
    section_para.text = section_name
    section_para.font.size = Pt(80)
    section_para.font.color.rgb = COLORS['bg_light']
    section_para.font.name = "STSong"
    section_para.alignment = PP_ALIGN.CENTER
    
    # 前景文字
    title = slide.shapes.add_textbox(Inches(1), Inches(3), Inches(11), Inches(1.5))
    title_frame = title.text_frame
    title_para = title_frame.paragraphs[0]
    title_para.text = section_name
    title_para.font.size = Pt(48)
    title_para.font.color.rgb = COLORS['ink']
    title_para.font.name = "STSong"
    title_para.alignment = PP_ALIGN.CENTER
    
    return slide

def add_polaroid_slide(prs):
    """宝丽来照片风格页 - 模仿参考图右上角"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 背景
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLORS['bg']
    bg.line.fill.background()
    
    # 左上烟雾
    add_smoke_decoration(slide, Inches(0), Inches(0), Inches(4), Inches(3), rotation=60)
    
    # 宝丽来照片框
    polaroid = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1), Inches(1.5), Inches(3.5), Inches(4.2))
    polaroid.fill.solid()
    polaroid.fill.fore_color.rgb = RGBColor(255, 255, 255)
    polaroid.line.color.rgb = COLORS['accent_gold']
    polaroid.line.width = Pt(1)
    
    # 照片内框
    photo_inner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.15), Inches(1.65), Inches(3.2), Inches(3.2))
    photo_inner.fill.solid()
    photo_inner.fill.fore_color.rgb = COLORS['bg_light']
    photo_inner.line.color.rgb = COLORS['text_light']
    photo_inner.line.width = Pt(1)
    photo_inner.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    
    # 照片提示
    photo_text = slide.shapes.add_textbox(Inches(1.15), Inches(2.8), Inches(3.2), Inches(0.5))
    photo_text_frame = photo_text.text_frame
    photo_text_para = photo_text_frame.paragraphs[0]
    photo_text_para.text = "【照片】"
    photo_text_para.font.size = Pt(14)
    photo_text_para.font.color.rgb = COLORS['text_light']
    photo_text_para.font.name = "Microsoft YaHei"
    photo_text_para.alignment = PP_ALIGN.CENTER
    
    # 右侧文字区
    text_box = slide.shapes.add_textbox(Inches(5.5), Inches(1.5), Inches(7), Inches(5))
    text_frame = text_box.text_frame
    text_frame.word_wrap = True
    
    lines = [
        ("创作灵感", 20, True),
        ("", 10),
        ("在此处记录创作过程中的灵感来源、", 14),
        ("参考素材、以及设计思路。", 14),
        ("", 15),
        ("关键词", 18, True),
        ("", 10),
        ("• 东方元素", 14),
        ("• 现代演绎", 14),
        ("• 角色塑造", 14),
        ("• 视觉叙事", 14),
    ]
    
    for i, line in enumerate(lines):
        para = text_frame.add_paragraph() if i > 0 else text_frame.paragraphs[0]
        para.text = line[0]
        para.font.size = Pt(line[1])
        para.font.color.rgb = COLORS['accent_red'] if len(line) > 2 else COLORS['text_dark']
        para.font.name = "Microsoft YaHei"
        para.font.bold = len(line) > 2
    
    return slide

# ============ 生成所有页面 ============
print("🦐 正在生成新中式美术作品集 PPT...")

add_cover_slide(prs)                    # 封面
add_transition_slide(prs, "角色设计")    # 过渡页 1
add_character_slide(prs, "角色 A", "龙門无宵坊 · 主角")  # 角色页 1
add_character_slide(prs, "角色 B", "龙門无宵坊 · 配角")  # 角色页 2
add_transition_slide(prs, "概念设计")    # 过渡页 2
add_concept_slide(prs, "场景概念")       # 概念页 1
add_concept_slide(prs, "道具设计")       # 概念页 2
add_polaroid_slide(prs)                 # 宝丽来灵感页
add_cover_slide(prs)                    # 封底（复用封面）

# 保存
output_path = "/Users/sirius/.openclaw/workspace-default/美术作品集_新中式.pptx"
prs.save(output_path)

print(f"✅ PPT 已生成：{output_path}")
print(f"📄 共 9 页：封面 + 过渡页×2 + 角色页×2 + 概念页×2 + 灵感页 + 封底")
print(f"🎨 风格：新中式美术设定集（水墨烟雾 + 低饱和配色）")
print(f"📝 提示：替换占位框为你的作品图即可")
