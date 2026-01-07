from pptx import Presentation
from models import PresentationData
import os
import uuid

LAYOUT_MAPPING = {
    "title_cover": 3,    # 封面页 Layout Index
    "content_list": 1,   # 列表页 Layout Index
    # "two_column": 2    # 以后再加
}

PLACEHOLDER_MAPPING = {
    "title": 0,          # 标题通常都是 idx 0
    "subtitle": 13,       # 封面副标题 idx
    "content": 1         # 正文列表 idx
}

def create_pptx_file(data: PresentationData) -> str:
    print(f"🎨 [Render] 正在渲染 PPT: {data.topic}...")
    
    # 1. load template
    if not os.path.exists("template.pptx"):
        raise FileNotFoundError("找不到 template.pptx，请先准备模板文件！")
        
    prs = Presentation("template.pptx")

    # 2. 遍历数据，一页页生成
    for slide_data in data.slides:
        
        # A. 获取布局索引 (如果 JSON 里写了不存在的布局，默认用 content_list)
        layout_idx = LAYOUT_MAPPING.get(slide_data.layout, 1)
        slide_layout = prs.slide_layouts[layout_idx]
        
        # B. 创建幻灯片
        slide = prs.slides.add_slide(slide_layout)
        
        # C. 填充标题 (绝大多数页面都有标题)
        # slide.shapes.title 是 python-pptx 提供的快捷方式，等同于找 idx=0
        if slide.shapes.title: 
            slide.shapes.title.text = slide_data.title
            
        # D. 根据布局类型，填充特定内容
        
        # --- 情况 1: 封面页 (Title Cover) ---
        if slide_data.layout == "title_cover":
            # 尝试填充副标题
            if slide_data.subtitle:
                # 使用 try-except 防止模板里没有这个占位符导致报错
                try:
                    # 获取副标题占位符
                    subtitle_shape = slide.placeholders[PLACEHOLDER_MAPPING["subtitle"]]
                    subtitle_shape.text = slide_data.subtitle
                except KeyError:
                    print(f"⚠️ 警告: 布局 {layout_idx} 找不到副标题占位符")

        # --- 情况 2: 列表页 (Content List) ---
        elif slide_data.layout == "content_list":
            # 尝试填充列表内容
            if slide_data.content and slide_data.content.bullet_points:
                try:
                    content_shape = slide.placeholders[PLACEHOLDER_MAPPING["content"]]
                    
                    # 获取文本框对象 (TextFrame)
                    tf = content_shape.text_frame
                    tf.clear() # 清除模板里默认的提示文字
                    
                    # 循环填入 Bullet Points
                    for point in slide_data.content.bullet_points:
                        p = tf.add_paragraph()
                        p.text = point
                        p.level = 0 # 缩进级别 (0是一级要点)
                        
                except KeyError:
                    print(f"⚠️ 警告: 布局 {layout_idx} 找不到正文占位符")
                    
        # --- 未来可以加 情况 3: 图片页 ...
    
    # 3. 保存文件，返回文件名
    # 生成唯一文件名
    filename = f"{uuid.uuid4()}.pptx"
    save_path = os.path.join("generated_ppts", filename)
    
    # 确保目录存在
    os.makedirs("generated_ppts", exist_ok=True)
    
    prs.save(save_path)
    print(f"✅ [Render] 文件保存至: {save_path}")
    
    return filename