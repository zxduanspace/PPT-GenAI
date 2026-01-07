from pptx import Presentation
from pptx.chart.data import CategoryChartData 
from pptx.enum.chart import XL_CHART_TYPE    
from models import PresentationData
import os
import uuid

LAYOUT_CONFIG = {
    # === 1. 学术风格 ===
    "academic": {
        "file": "templates/academic.pptx",
        "layouts": {
            "title_cover": {"layout_idx": 0, "title_idx": 2, "subtitle_idx": 3},
            "content_list": {"layout_idx": 1, "title_idx": 0, "body_idx": 1},
            "two_column": {"layout_idx": 2, "title_idx": 0, "left_idx": 1, "right_idx": 2},
            "chart": {"layout_idx": 3, "chart_idx": 1}
        }
    },
    
    # === 2. 商业风格 ===
    "business": {
        "file": "templates/business.pptx",
        "layouts": {
            "title_cover": {"layout_idx": 0, "title_idx": 0, "subtitle_idx": 1},
            "content_list": {"layout_idx": 1, "title_idx": 0, "body_idx": 1},
            "two_column": {"layout_idx": 2, "title_idx": 0, "left_idx": 1, "right_idx": 2},
            "chart": {"layout_idx": 3, "chart_idx": 1}
        }
    },
    
    # === 3. 教学风格 ===
    "teaching": {
        "file": "templates/teaching.pptx",
        "layouts": {
            "title_cover": {"layout_idx": 0, "title_idx": 0, "subtitle_idx": 13},
            "content_list": {"layout_idx": 1, "title_idx": 0, "body_idx": 1},
            "two_column": {"layout_idx": 2, "title_idx": 0, "left_idx": 1, "right_idx": 2},
            "chart": {"layout_idx": 3, "chart_idx": 1}
        }
    }
}

def create_pptx_file(data: PresentationData, theme: str = "academic") -> str:
    """
    :param theme: 'academic', 'business', 'teaching'
    """
    print(f"🎨 [Render] 正在渲染 PPT: {data.topic}...")

    # 1. 加载对应主题的配置
    # 如果找不到这个主题，就默认回退到 business
    current_config = LAYOUT_CONFIG.get(theme, LAYOUT_CONFIG["academic"])
    
    # 2. 找到文件路径
    template_path = current_config["file"]
    print(f"🎨 [Render] 正在使用主题: {theme}, 文件: {template_path}")
    
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"找不到模板文件: {template_path}")
        
    prs = Presentation(template_path)

    # 2. 遍历数据，一页页生成
    for slide_data in data.slides:

        # A. 获取当前页面的配置 (如果找不到就默认用 content_list)
        layout_key = slide_data.layout
        layout_map = current_config["layouts"].get(layout_key, current_config["layouts"]["content_list"])
        
        # B. 创建页面
        slide_layout = prs.slide_layouts[layout_map["layout_idx"]]
        slide = prs.slides.add_slide(slide_layout)
        
        # C. 填充标题 (绝大多数页面都有标题)
        try:
            if slide_data.title:
                title_shape = slide.placeholders[layout_map["title_idx"]]
                title_shape.text = slide_data.title
        except:
            pass
            
        # D. 根据布局类型，填充特定内容
        
        # --- 情况 1: 封面页 (Title Cover) ---
        if slide_data.layout == "title_cover":
            # 尝试填充副标题
            if slide_data.subtitle:
                # 使用 try-except 防止模板里没有这个占位符导致报错
                try:
                    # 获取副标题占位符
                    subtitle_shape = slide.placeholders[layout_map["subtitle_idx"]]
                    subtitle_shape.text = slide_data.subtitle
                except KeyError:
                    print(f"⚠️ 警告: 布局找不到副标题占位符")

        # --- 情况 2: 列表页 (Content List) ---
        elif slide_data.layout == "content_list":
            # 填充列表内容
            if slide_data.content and slide_data.content.bullet_points:
                try:
                    content_shape = slide.placeholders[layout_map["body_idx"]]
                    
                    # 获取文本框对象 (TextFrame)
                    tf = content_shape.text_frame
                    tf.clear() # 清除模板里默认的提示文字
                    
                    # 循环填入 Bullet Points
                    for point in slide_data.content.bullet_points:
                        p = tf.add_paragraph()
                        p.text = point
                        p.level = 0 # 缩进级别 (0是一级要点)
                        
                except KeyError:
                    print(f"⚠️ 警告: 布局找不到正文占位符")
            
            # 填充大段文本
            if slide_data.content and slide_data.content.text_body:
                try:
                    content_shape = slide.placeholders[layout_map["body_idx"]]
                    
                    # 获取文本框对象 (TextFrame)
                    tf = content_shape.text_frame
                    tf.clear() # 清除模板里默认的提示文字
                    
                    # 直接填入大段文本
                    p = tf.add_paragraph()
                    p.text = slide_data.content.text_body
                    p.level = 0
                    
                except KeyError:
                    print(f"⚠️ 警告: 布局找不到正文占位符")

                    
        # --- 情况 3: 左右对比页(two column) ...
        elif layout_key == "two_column":
            try:
                # 填左边
                if slide_data.content and slide_data.content.content_left:
                    tf_left = slide.placeholders[layout_map["left_idx"]].text_frame
                    tf_left.clear()
                    for item in slide_data.content.content_left:
                        p = tf_left.add_paragraph()
                        p.text = item
                        p.level = 0
                
                # 填右边
                if slide_data.content and slide_data.content.content_right:
                    tf_right = slide.placeholders[layout_map["right_idx"]].text_frame
                    tf_right.clear()
                    for item in slide_data.content.content_right:
                        p = tf_right.add_paragraph()
                        p.text = item
                        p.level = 0
            except KeyError:
                print(f"⚠️ 警告: 对比页占位符索引错误，请检查 template")

        # --- 情况 4: 图表页 (Chart) ---
        elif layout_key == "chart" and slide_data.chart_data:
            try:
                # 1. 准备数据
                chart_data = CategoryChartData()
                chart_data.categories = slide_data.chart_data.labels # X轴
                # 添加数据系列 (Series)
                chart_data.add_series(slide_data.chart_data.title, slide_data.chart_data.values)

                # 2. 找到占位符的位置 (关键步骤：借用占位符的坐标)
                placeholder = slide.placeholders[layout_map["chart_idx"]]
                
                # 3. 在该位置插入真实图表 (COLUMN_CLUSTERED 是柱状图)
                slide.shapes.add_chart(
                    XL_CHART_TYPE.COLUMN_CLUSTERED, 
                    placeholder.left, placeholder.top, 
                    placeholder.width, placeholder.height, 
                    chart_data
                )
                
                # 4. 删掉原本的占位符框
                placeholder.element.getparent().remove(placeholder.element)
                
            except Exception as e:
                print(f"⚠️ 图表生成失败: {e}")
    
    # 3. 保存文件，返回文件名
    # 生成唯一文件名
    filename = f"{uuid.uuid4()}.pptx"
    save_path = os.path.join("generated_ppts", filename)
    
    # 确保目录存在
    os.makedirs("generated_ppts", exist_ok=True)
    
    prs.save(save_path)
    print(f"✅ [Render] 文件保存至: {save_path}")
    
    return filename