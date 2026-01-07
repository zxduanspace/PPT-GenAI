import json
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from models import PresentationData

# load .env variables
load_dotenv()

# initialize client
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- prompt engineering 在这里写核心逻辑 ---
# This is a Mock function that does not consume Tokens for now
async def generate_ppt_content(topic: str) -> PresentationData:
    print(f"🧠 [LLM] 正在为 '{topic}' 构思大纲...")
    
    # simulate LLM returned JSON (hardcoded)
    mock_json = {
        "topic": topic,
        "slides": [
            {
                "id": 1,
                "layout": "title_cover",
                "title": f"关于 {topic} 的深度解析",
                "subtitle": "AI 生成演示文稿",
                "content": {},
                "visual": {"need_image": False}
            },
            {
                "id": 2,
                "layout": "content_list",
                "title": "核心痛点",
                "content": {
                    "bullet_points": ["效率低下", "人工成本高", "缺乏创新"]
                },
                "visual": {"need_image": False}
            }
        ]
    }
    
    # verify data format matches Pydantic definition
    return PresentationData(**mock_json)