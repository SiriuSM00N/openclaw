#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
美术作品集 PPT 模板 - 黑金游戏国风
配色：黑金 + 简约云纹回纹
风格：简约现代 × 游戏国风
布局：大图少字
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

# ========== 黑金配色方案 ==========
COLORS = {
    'bg_dark': RGBColor(18, 18, 20),       # 深黑背景 #121214
    'bg_light': RGBColor(28, 28, 32),      # 浅黑背景 #1C1C20
    'bg_card': RGBColor(35, 35, 40),       # 卡片背景 #232328
    'gold_main': RGBColor(212, 175, 55),   # 主金色 #D4AF37
    'gold_light': RGBColor(235, 205, 105), # 浅金色 #EBCD69
    'gold_dark': RGBColor(165, 135, 45),   # 深金色 #A5872D
    'text_white': RGBColor(255, 255, 255), # 纯白文字
    'text_gray': RGBColor(180, 180, 185),  # 灰色文字
    'text_dim': RGBColor(120, 120, 125),   # 暗文字
    'accent_red': RGBColor(180, 60, 50),   # 点缀红（可选）
}

def add_cloud_corner(slide, x, y, size, color=COLORS['gold_main'], rotation=0):
    """添加简约云纹角花（用弧形模拟）"""
    # 主云纹
    cloud = slide.shapes.add_shape(MSO_SHAPE.ARC, x, y, size, size)
    cloud.fill.background()
    cloud.line.color.rgb = color
    cloud.line.width = Pt(2)
    cloud.rotation = rotation
    
    # 辅助云纹
    cloud2 = slide.shapes.add_shape(MSO_SHAPE.ARC, x + size*0.3, y + size*0.1, size*0.6, size*0.6)
    cloud2.fill.background()
    cloud2.line.color.rgb = color
    cloud2.line.width = Pt(1.5)
    cloud2.rotation = rotation + 30
    
    return cloud

def add_hui_pattern(slide, x, y, width, height, color=COLORS['gold_main']):
    """添加简约回纹边框"""
    # 上边框回纹
    segment_width = width / 8
    for i in range(8):
        if i % 2 == 0:
            line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 
                x + i * segment_width, y, segment_width, Pt(2))
            line.fill.solid()
            line.fill.fore_color.rgb = color
            line.line.fill.background()
        else:
            line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 
                x + i * segment_width, y + Pt(3), segment_width, Pt(2))
            line.fill.solid()
            line.fill.fore_color.rgb = color
            line.line.fill.background()
    
    return

def add_decorative_line(slide, x1, y1, x2, y2, color=COLORS['gold_main'], width=Pt(1.5)):
    """添加装饰线条"""
    line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x1, y1, x2, y2)
    line.line.color.rgb = color
    line.line.width = width
    return line

def add_gold_glow(slide, x, y, width, height, color=COLORS['gold_main']):
    """添加金色光晕效果"""
    glow = slide.shapes.add_shape(MSO_SHAPE.OVAL, x, y, width, height)
    glow.fill.solid()
    glow.fill.fore_color.rgb = color
    glow.fill.transparency = 0.85
    glow.line.fill.background()
    return glow

def add_image_placeholder_big(slide, x, y, width, height, label="【点击替换图片】"):
    """添加大图占位框（简约风格）"""
    # 外框
    outer = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, width, height)
    outer.fill.solid()
    outer.fill.fore_color.rgb = COLORS['bg_card']
    outer.fill.transparency = 0.5
    outer.line.color.rgb = COLORS['gold_main']
    outer.line.width = Pt(2)
    
    # 内框（虚线）
    inner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x + Pt(10), y + Pt(10), 
                                   width - Pt(20), height - Pt(20))
    inner.fill.background()
    inner.line.color.rgb = COLORS['gold_dark']
    inner.line.width = Pt(1)
    inner.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    
    # 提示文字
    text_box = slide.shapes.add_textbox(x, y + height/2 - Inches(0.3), width, Inches(0.6))
    text_frame = text_box.text_frame
    text_para = text_frame.paragraphs[0]
    text_para.text = label
    text_para.font.size = Pt(14)
    text_para.font.color.rgb = COLORS['text_dim']
    text_para.font.name = "Microsoft YaHei"
    text_para.alignment = PP_ALIGN.CENTER
    
    return outer

# ==================== 封面页 ====================
def add_cover_slide(prs):
    """封面页 - 黑金游戏国风"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 深色背景
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLORS['bg_dark']
    bg.line.fill.background()
    
    # === 金色光晕装饰 ===
    add_gold_glow(slide, Inches(10), Inches(0), Inches(4), Inches(4), COLORS['gold_main'])
    add_gold_glow(slide, Inches(0), Inches(5), Inches(3), Inches(3), COLORS['gold_dark'])
    
    # === 四角云纹装饰 ===
    add_cloud_corner(slide, Inches(0.3), Inches(0.3), Inches(1.2), rotation=0)
    add_cloud_corner(slide, Inches(11.8), Inches(0.3), Inches(1.2), rotation=90)
    add_cloud_corner(slide, Inches(0.3), Inches(6.3), Inches(1.2), rotation=270)
    add_cloud_corner(slide, Inches(11.8), Inches(6.3), Inches(1.2), rotation=180)
    
    # === 顶部回纹装饰 ===
    add_hui_pattern(slide, Inches(1.5), Inches(0.1), Inches(10.3), Inches(0.1), COLORS['gold_main'])
    
    # === 底部回纹装饰 ===
    add_hui_pattern(slide, Inches(1.5), Inches(7.35), Inches(10.3), Inches(0.1), COLORS['gold_main'])
    
    # === 中央大标题"集"字 ===
    title = slide.shapes.add_textbox(Inches(5.2), Inches(1.5), Inches(3), Inches(4))
    title_frame = title.text_frame
    title_para = title_frame.paragraphs[0]
    title_para.text = "集"
    title_para.font.size = Pt(150)
    title_para.font.color.rgb = COLORS['gold_main']
    title_para.font.name = "STSong"
    title_para.alignment = PP_ALIGN.CENTER
    
    # === 左侧竖排小字 ===
    left_vertical = slide.shapes.add_textbox(Inches(4.4), Inches(2.5), Inches(0.7), Inches(2.5))
    left_frame = left_vertical.text_frame
    left_para = left_frame.paragraphs[0]
    left_para.text = "作\n品\n集"
    left_para.font.size = Pt(18)
    left_para.font.color.rgb = COLORS['text_gray']
    left_para.font.name = "STSong"
    left_para.alignment = PP_ALIGN.CENTER
    
    # === 右侧竖排小字 ===
    right_vertical = slide.shapes.add_textbox(Inches(8.4), Inches(2.5), Inches(0.7), Inches(2.5))
    right_frame = right_vertical.text_frame
    right_para = right_frame.paragraphs[0]
    right_para.text = "游\n戏\n美\n术"
    right_para.font.size = Pt(18)
    right_para.font.color.rgb = COLORS['text_gray']
    right_para.font.name = "STSong"
    right_para.alignment = PP_ALIGN.CENTER
    
    # === 底部横线 ===
    add_decorative_line(slide, Inches(4.5), Inches(5.8), Inches(8.9), Inches(5.8), COLORS['gold_main'], Pt(2))
    
    # === 底部文字 ===
    bottom_text = slide.shapes.add_textbox(Inches(4.5), Inches(6.1), Inches(4.4), Inches(0.6))
    bottom_frame = bottom_text.text_frame
    bottom_para = bottom_frame.paragraphs[0]
    bottom_para.text = "小天狼星 · GAME ARTIST · 2024-2025"
    bottom_para.font.size = Pt(12)
    bottom_para.font.color.rgb = COLORS['gold_light']
    bottom_para.font.name = "Microsoft YaHei"
    bottom_para.alignment = PP_ALIGN.CENTER
    
    return slide

# ==================== 角色主介绍页 ====================
def add_character_main_slide(prs, char_name, char_title):
    """角色主介绍页 - 大图少字"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 深色背景
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLORS['bg_dark']
    bg.line.fill.background()
    
    # === 左上角云纹 ===
    add_cloud_corner(slide, Inches(0.3), Inches(0.3), Inches(1), rotation=0)
    
    # === 右上角云纹 ===
    add_cloud_corner(slide, Inches(12), Inches(0.3), Inches(1), rotation=90)
    
    # === 顶部回纹 ===
    add_hui_pattern(slide, Inches(1.5), Inches(0.1), Inches(10.3), Inches(0.1), COLORS['gold_dark'])
    
    # === 角色名（大字）===
    name_box = slide.shapes.add_textbox(Inches(8.5), Inches(0.6), Inches(4.3), Inches(1.2))
    name_frame = name_box.text_frame
    name_para = name_frame.paragraphs[0]
    name_para.text = char_name
    name_para.font.size = Pt(42)
    name_para.font.color.rgb = COLORS['gold_main']
    name_para.font.name = "STSong"
    name_para.alignment = PP_ALIGN.RIGHT
    
    # === 角色副标题 ===
    subtitle_box = slide.shapes.add_textbox(Inches(8.5), Inches(1.6), Inches(4.3), Inches(0.5))
    subtitle_frame = subtitle_box.text_frame
    subtitle_para = subtitle_frame.paragraphs[0]
    subtitle_para.text = char_title
    subtitle_para.font.size = Pt(14)
    subtitle_para.font.color.rgb = COLORS['text_gray']
    subtitle_para.font.name = "Microsoft YaHei"
    subtitle_para.alignment = PP_ALIGN.RIGHT
    
    # === 装饰横线 ===
    add_decorative_line(slide, Inches(8.5), Inches(2), Inches(12.7), Inches(2), COLORS['gold_main'], Pt(1.5))
    
    # === 角色立绘主图（左侧超大图）===
    main_art = add_image_placeholder_big(slide, Inches(0.5), Inches(0.5), Inches(7.5), Inches(6.5), 
                                          "【角色立绘】\n右键 → 更改图片")
    
    # === 右侧小图区域（三视图）===
    # 正面
    front = add_image_placeholder_big(slide, Inches(8.5), Inches(2.4), Inches(1.8), Inches(2.8), "正面")
    
    # 侧面
    side = add_image_placeholder_big(slide, Inches(10.6), Inches(2.4), Inches(1.8), Inches(2.8), "侧面")
    
    # 背面
    back = add_image_placeholder_big(slide, Inches(8.5), Inches(5.4), Inches(1.8), Inches(1.8), "背面")
    
    # === 页面编号 ===
    page_num = slide.shapes.add_textbox(Inches(12.5), Inches(7.1), Inches(0.5), Inches(0.3))
    page_frame = page_num.text_frame
    page_para = page_frame.paragraphs[0]
    page_para.text = "01"
    page_para.font.size = Pt(10)
    page_para.font.color.rgb = COLORS['text_dim']
    page_para.font.name = "Microsoft YaHei"
    page_para.alignment = PP_ALIGN.RIGHT
    
    return slide

# ==================== 角色细节页 ====================
def add_character_detail_slide(prs, char_name, detail_type):
    """角色细节页 - 表情/动作"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 背景
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLORS['bg_dark']
    bg.line.fill.background()
    
    # === 右下角云纹 ===
    add_cloud_corner(slide, Inches(12), Inches(6.2), Inches(1), rotation=180)
    
    # === 标题 ===
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(8), Inches(1))
    title_frame = title_box.text_frame
    title_para = title_frame.paragraphs[0]
    title_para.text = char_name
    title_para.font.size = Pt(36)
    title_para.font.color.rgb = COLORS['gold_main']
    title_para.font.name = "STSong"
    
    subtitle_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.3), Inches(8), Inches(0.4))
    subtitle_frame = subtitle_box.text_frame
    subtitle_para = subtitle_frame.paragraphs[0]
    subtitle_para.text = detail_type
    subtitle_para.font.size = Pt(14)
    subtitle_para.font.color.rgb = COLORS['text_gray']
    subtitle_para.font.name = "Microsoft YaHei"
    
    # === 装饰线 ===
    add_decorative_line(slide, Inches(0.5), Inches(1.7), Inches(2.5), Inches(1.7), COLORS['gold_main'], Pt(1.5))
    
    # === 大图展示区（3 张）===
    positions = [
        (Inches(0.5), Inches(2.1), Inches(3.8), Inches(4.8), "细节 01"),
        (Inches(4.7), Inches(2.1), Inches(3.8), Inches(4.8), "细节 02"),
        (Inches(8.9), Inches(2.1), Inches(3.8), Inches(4.8), "细节 03"),
    ]
    
    for x, y, w, h, label in positions:
        add_image_placeholder_big(slide, x, y, w, h, label)
    
    # === 页面编号 ===
    page_num = slide.shapes.add_textbox(Inches(12.5), Inches(7.1), Inches(0.5), Inches(0.3))
    page_frame = page_num.text_frame
    page_para = page_frame.paragraphs[0]
    page_para.text = "02"
    page_para.font.size = Pt(10)
    page_para.font.color.rgb = COLORS['text_dim']
    page_para.font.name = "Microsoft YaHei"
    page_para.alignment = PP_ALIGN.RIGHT
    
    return slide

# ==================== 场景概念页 ====================
def add_concept_slide(prs, concept_name, concept_subtitle):
    """场景概念页 - 超大图展示"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 背景
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLORS['bg_dark']
    bg.line.fill.background()
    
    # === 左上角云纹 ===
    add_cloud_corner(slide, Inches(0.3), Inches(0.3), Inches(1), rotation=0)
    
    # === 标题 ===
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(8), Inches(0.8))
    title_frame = title_box.text_frame
    title_para = title_frame.paragraphs[0]
    title_para.text = concept_name
    title_para.font.size = Pt(36)
    title_para.font.color.rgb = COLORS['gold_main']
    title_para.font.name = "STSong"
    
    subtitle_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.2), Inches(8), Inches(0.4))
    subtitle_frame = subtitle_box.text_frame
    subtitle_para = subtitle_frame.paragraphs[0]
    subtitle_para.text = concept_subtitle
    subtitle_para.font.size = Pt(14)
    subtitle_para.font.color.rgb = COLORS['text_gray']
    subtitle_para.font.name = "Microsoft YaHei"
    
    # === 装饰线 ===
    add_decorative_line(slide, Inches(0.5), Inches(1.6), Inches(2.5), Inches(1.6), COLORS['gold_main'], Pt(1.5))
    
    # === 主概念图（超大）===
    main_concept = add_image_placeholder_big(slide, Inches(0.5), Inches(2), Inches(8.5), Inches(4.8), 
                                              "【主概念图】\n场景原画/氛围图")
    
    # === 右侧细节图（2 张竖排）===
    detail1 = add_image_placeholder_big(slide, Inches(9.4), Inches(2), Inches(3.4), Inches(2.2), "细节 01")
    detail2 = add_image_placeholder_big(slide, Inches(9.4), Inches(4.6), Inches(3.4), Inches(2.2), "细节 02")
    
    # === 页面编号 ===
    page_num = slide.shapes.add_textbox(Inches(12.5), Inches(7.1), Inches(0.5), Inches(0.3))
    page_frame = page_num.text_frame
    page_para = page_frame.paragraphs[0]
    page_para.text = "03"
    page_para.font.size = Pt(10)
    page_para.font.color.rgb = COLORS['text_dim']
    page_para.font.name = "Microsoft YaHei"
    page_para.alignment = PP_ALIGN.RIGHT
    
    return slide

# ==================== 过渡页 ====================
def add_transition_slide(prs, section_name, section_num):
    """章节过渡页 - 极简大气"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 背景
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLORS['bg_dark']
    bg.line.fill.background()
    
    # === 金色光晕 ===
    add_gold_glow(slide, Inches(9), Inches(0), Inches(5), Inches(5), COLORS['gold_dark'])
    
    # === 四角云纹 ===
    add_cloud_corner(slide, Inches(0.3), Inches(0.3), Inches(1.5), rotation=0)
    add_cloud_corner(slide, Inches(11.5), Inches(5.7), Inches(1.5), rotation=180)
    
    # === 章节编号（超大半透明）===
    num_bg = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(4), Inches(6))
    num_bg_frame = num_bg.text_frame
    num_bg_para = num_bg_frame.paragraphs[0]
    num_bg_para.text = section_num
    num_bg_para.font.size = Pt(180)
    num_bg_para.font.color.rgb = COLORS['bg_card']
    num_bg_para.font.name = "STSong"
    num_bg_para.alignment = PP_ALIGN.LEFT
    
    # === 章节名（前景金色）===
    title = slide.shapes.add_textbox(Inches(1.5), Inches(2.8), Inches(10), Inches(2))
    title_frame = title.text_frame
    title_para = title_frame.paragraphs[0]
    title_para.text = section_name
    title_para.font.size = Pt(54)
    title_para.font.color.rgb = COLORS['gold_main']
    title_para.font.name = "STSong"
    title_para.alignment = PP_ALIGN.CENTER
    
    # === 英文副标题 ===
    subtitle = slide.shapes.add_textbox(Inches(1.5), Inches(4.5), Inches(10), Inches(0.6))
    subtitle_frame = subtitle.text_frame
    subtitle_para = subtitle_frame.paragraphs[0]
    subtitle_para.text = "CHAPTER"
    subtitle_para.font.size = Pt(14)
    subtitle_para.font.color.rgb = COLORS['text_dim']
    subtitle_para.font.name = "Microsoft YaHei"
    subtitle_para.alignment = PP_ALIGN.CENTER
    
    return slide

# ==================== 封底页 ====================
def add_back_cover_slide(prs):
    """封底页"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 背景
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLORS['bg_dark']
    bg.line.fill.background()
    
    # === 金色光晕 ===
    add_gold_glow(slide, Inches(10), Inches(0), Inches(4), Inches(4), COLORS['gold_main'])
    add_gold_glow(slide, Inches(0), Inches(5), Inches(3), Inches(3), COLORS['gold_dark'])
    
    # === 四角云纹 ===
    add_cloud_corner(slide, Inches(0.3), Inches(0.3), Inches(1.2), rotation=0)
    add_cloud_corner(slide, Inches(11.8), Inches(0.3), Inches(1.2), rotation=90)
    add_cloud_corner(slide, Inches(0.3), Inches(6.3), Inches(1.2), rotation=270)
    add_cloud_corner(slide, Inches(11.8), Inches(6.3), Inches(1.2), rotation=180)
    
    # === 顶部回纹 ===
    add_hui_pattern(slide, Inches(1.5), Inches(0.1), Inches(10.3), Inches(0.1), COLORS['gold_main'])
    
    # === 底部回纹 ===
    add_hui_pattern(slide, Inches(1.5), Inches(7.35), Inches(10.3), Inches(0.1), COLORS['gold_main'])
    
    # === 感谢文字 ===
    thanks = slide.shapes.add_textbox(Inches(4), Inches(2.2), Inches(5.5), Inches(1.5))
    thanks_frame = thanks.text_frame
    thanks_para = thanks_frame.paragraphs[0]
    thanks_para.text = "感谢观看"
    thanks_para.font.size = Pt(48)
    thanks_para.font.color.rgb = COLORS['gold_main']
    thanks_para.font.name = "STSong"
    thanks_para.alignment = PP_ALIGN.CENTER
    
    # === 联系方式 ===
    contact = slide.shapes.add_textbox(Inches(4), Inches(3.8), Inches(5.5), Inches(2))
    contact_frame = contact.text_frame
    contact_frame.word_wrap = True
    
    contact_lines = [
        ("小天狼星 | Game Artist", 16, COLORS['gold_light']),
        ("", 10, COLORS['text_dim']),
        ("📧 your.email@example.com", 13, COLORS['text_gray']),
        ("📱 微信：your_wechat", 13, COLORS['text_gray']),
        ("🎨 ArtStation: your-profile", 13, COLORS['text_gray']),
    ]
    
    for i, line in enumerate(contact_lines):
        para = contact_frame.add_paragraph() if i > 0 else contact_frame.paragraphs[0]
        para.text = line[0]
        para.font.size = Pt(line[1])
        para.font.color.rgb = line[2] if len(line) > 2 else COLORS['text_gray']
        para.font.name = "Microsoft YaHei"
        para.alignment = PP_ALIGN.CENTER
    
    return slide

# ==================== 生成所有页面 ====================
print("🦐 正在生成黑金游戏国风美术作品集...")

# 封面
add_cover_slide(prs)

# 第一章：角色设计
add_transition_slide(prs, "角色设计", "01")
add_character_main_slide(prs, "角色名称", "游戏主角 · 设定")
add_character_detail_slide(prs, "角色名称", "表情与动作")

# 第二章：场景概念
add_transition_slide(prs, "场景概念", "02")
add_concept_slide(prs, "场景概念 A", "Environment Concept")
add_concept_slide(prs, "场景概念 B", "Key Art")

# 封底
add_back_cover_slide(prs)

# 保存
output_path = "/Users/sirius/.openclaw/workspace-default/美术作品集_黑金国风.pptx"
prs.save(output_path)

print(f"✅ PPT 已生成：{output_path}")
print(f"📄 共 8 页")
print(f"   - 封面 ×1")
print(f"   - 过渡页 ×2")
print(f"   - 角色主介绍 ×1")
print(f"   - 角色细节 ×1")
print(f"   - 场景概念 ×2")
print(f"   - 封底 ×1")
print(f"🎨 风格：黑金游戏国风")
print(f"   - 配色：深黑背景 + 金色装饰")
print(f"   - 花纹：简约云纹角花 + 回纹边框")
print(f"   - 布局：大图少字，高端大气")
