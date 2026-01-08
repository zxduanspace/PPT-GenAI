from pydantic import BaseModel, Field
from typing import List, Optional, Union

# === 1. 基础组件 ===
class TableData(BaseModel):
    """表格数据结构"""
    headers: List[str] = Field(description="表头")
    rows: List[List[Union[str, int, float]]] = Field(description="表格行数据")

class ChartData(BaseModel):
    """图表数据结构"""
    title: Optional[str] = None
    chart_type: str = "COLUMN_CLUSTERED"
    labels: List[str]
    values: List[float]

class Content(BaseModel):
    """文本内容组件"""
    text_body: Optional[str] = Field(None, description="大段文本")
    bullet_points: Optional[List[str]] = Field(None, description="列表要点")
    content_left: Optional[List[str]] = Field(None, description="左侧栏文本")
    content_right: Optional[List[str]] = Field(None, description="右侧栏文本")

# === 2. 视觉/图片组件 ===
class Visual(BaseModel):
    """图片生成需求"""
    need_image: bool = False
    image_prompt: Optional[str] = Field(None, description="AI绘图关键词(英文)")
    image_url: Optional[str] = Field(None, description="直接指定的图片URL(可选)")
    caption: Optional[str] = Field(None, description="图片下方的说明文字")

# === 3. 单页幻灯片结构 ===
class Slide(BaseModel):
    id: int
    # 扩充了 layout 类型，增加了 table 和 image_page
    layout: str = Field(description="布局类型: title_cover, content_list, two_column, chart, table, image_page")
    title: Optional[str] = Field(None, description="幻灯片标题")
    subtitle: Optional[str] = Field(None, description="副标题(仅封面页有效)")
    
    # 不同类型的数据容器
    content: Optional[Content] = None
    chart_data: Optional[ChartData] = None
    table_data: Optional[TableData] = None
    visual: Optional[Visual] = None

# === 4. 整体 PPT 结构 ===
class PresentationData(BaseModel):
    topic: str = Field(description="PPT主题")
    slides: List[Slide] = Field(description="幻灯片页面列表")