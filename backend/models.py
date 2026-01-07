from pydantic import BaseModel, Field
from typing import List, Optional

# 1. 内容部分 (对应 PPT 里的 Bullet Points 或正文)
class Content(BaseModel):
    text_body: Optional[str] = Field(None, description="大段文本")
    bullet_points: Optional[List[str]] = Field(None, description="列表要点")

# 2. 视觉部分 (对应配图需求)
class Visual(BaseModel):
    need_image: bool = False
    image_prompt: Optional[str] = None
    image_url: Optional[str] = None

# 3. 单页幻灯片结构
class Slide(BaseModel):
    # 限制 layout 只能是这几种，方便渲染端处理
    id: int
    layout: str = Field(description="布局类型: title, content, two_column") 
    title: str = Field(description="幻灯片标题")
    subtitle: Optional[str] = Field(None, description="副标题，仅 title 布局需要")
    content: Optional[Content] = Field(None, description="正文内容")
    image_prompt: Optional[str] = Field(None, description="生成的配图提示词")

# 4. 整个 PPT 的结构
class PresentationData(BaseModel):
    topic: str = Field(description="演讲主题")
    slides: List[Slide] = Field(description="幻灯片列表")