import json
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from models import PresentationData

# 加载 .env 环境变量
load_dotenv(override=True)
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_ppt_content(topic: str, use_ai: bool = True) -> PresentationData:
    """
    生成 PPT 内容结构数据。
    :param topic: 用户输入的主题
    :param use_ai: True=调用OpenAI, False=使用本地Mock数据
    """
    print(f"🧠 [LLM] 正在处理主题: '{topic}' (Use AI: {use_ai})...")

    # === A. Mock 模式 (队友的逻辑) ===
    if not use_ai:
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            json_path = os.path.join(current_dir, "mock_data.json")
            with open(json_path, "r", encoding="utf-8") as f:
                data_dict = json.load(f)
            # 强行覆盖 topic 以显得真实
            data_dict["topic"] = topic
            return PresentationData(**data_dict)
        except Exception as e:
            print(f"❌ Mock数据读取失败: {e}")
            return PresentationData(topic="Error", slides=[])

    # === B. 真实 AI 模式 (你的逻辑融合) ===
    # 核心 Prompt: 融合了 backend2 的 JSON 指令和 backend 的数据结构
    system_prompt = """
    你是一个专业的 PPT 生成助手。请根据用户主题生成 PPT 内容结构。
    
    输出必须是严格的 JSON 格式，不要包含 Markdown 标记。
    JSON 结构示例：
    {
        "topic": "PPT主题",
        "slides": [
            {
                "id": 1,
                "layout": "title_cover",
                "title": "主标题",
                "subtitle": "副标题"
            },
            {
                "id": 2,
                "layout": "content_list",
                "title": "目录",
                "content": { "bullet_points": ["要点1", "要点2"] }
            },
            {
                "id": 3,
                "layout": "two_column",
                "title": "要点2",
                "content": { "content_left": ["要点2.1"], "content_right": ["要点2.2"] }
            },
            {
                "id": 4,
                "layout": "image_page", 
                "title": "概念展示",
                "visual": {
                    "need_image": true,
                    "image_prompt": "futuristic city skyline, cyberpunk style, high quality",
                    "caption": "未来城市概念图"
                }
            },
            {
                "id": 5,
                "layout": "table",
                "title": "数据对比",
                "table_data": {
                    "headers": ["指标", "传统模式", "AI模式"],
                    "rows": [["效率", "低", "高"], ["成本", "高", "低"]]
                }
            },
            {
                "id": 6,
                "layout": "chart",
                "title": "数据对比",
                "chart_data": {
                    "title": "销量增长趋势",
                    "chart_type": "COLUMN_CLUSTERED",
                    "labels": ["2023", "2024", "2025", "2026"],
                    "values": [1500, 2200, 3500, 5000]
                }
            }
        ]
    }
    要求：
    1. 生成 5-8 页幻灯片。
    2. 必须包含至少 1 页 'chart'(图表) 或 'table'(表格)，以及 1 页 'image_page'(图片页)。
    3. visual.image_prompt 必须是英文关键词。
    """

    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo", # 如果有 gpt-4 效果更好
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"请为主题 '{topic}' 生成一份专业的 PPT 大纲。"}
            ],
            temperature=0.7,
            response_format={"type": "json_object"} # 强制 JSON 模式
        )
        
        content_str = response.choices[0].message.content
        data_dict = json.loads(content_str)
        
        # 转换为 Pydantic 对象进行校验
        return PresentationData(**data_dict)

    except Exception as e:
        print(f"❌ OpenAI 调用或解析失败: {e}")
        # 如果失败，回退到 Mock 模式防止程序崩溃
        print("🔄 自动回退到 Mock 模式...")
        return await generate_ppt_content(topic, use_ai=False)