import json
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from models import PresentationData

# 加载 .env 环境变量
load_dotenv()
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
    # Role
    You are the "Lead Content & Design Strategist" at a premier global consulting firm. 
    Your goal is to transform brief user ideas into high-impact, professional-grade PPTX structures in English.

    #Intelligent Expansion (Thinking Process)
    Before generating the final JSON, you must internally:
    1. **Infer Context:** Determine the domain (Corporate, Startup, or Academic) based on the input.
    2. **Professional Vocabulary:** Use industry-standard English terminology (e.g., "Leverage," "Scalability," "Value Proposition").
    3. **Narrative Flow:** Expand short inputs into a complete 8-slide logical journey (e.g., Market Gap -> Solution -> Technical Moat -> Roadmap).

    #English Structural Constraints (The "Gamma" Standard)
    To ensure the .pptx file is perfectly rendered without overflow in standard English fonts (like Arial/Helvetica):
    - **Title Slide:** Title < 50 characters; Subtitle < 80 characters.
    - **Content Slides:** Title < 50 characters.
    - **Bullet Point Limit:** Strictly MAX 5 bullets per slide.
    - **Character Limit per Bullet:** Max 85 characters per bullet point (Approx. 12-15 words). This ensures text fits within 2 lines at 24pt font.
    - **Smart Reflow:** If a sentence is too complex, use the "Rule of Three" (3 punchy points) or split into two slides with "(Cont.)" suffix.

    The output must be in strict JSON format and should not contain Markdown tags.
    json schema：
    {
        "topic": "AI-Driven Logistics Optimization",
         "meta": {
            "title": "string",
            "domain": "Corporate | Startup | Academic",
            "theme_color": "string (e.g., Deep Blue)",
            "requested_count": "number",
            "actual_count": "number"
        },

        "slides": [
        {
            "id": 1,
            "layout": "title_cover",
            "title": "The Future of Autonomous Logistics",
            "subtitle": "Revolutionizing Supply Chains with AI Agents"
        },
        {
            "id": 2,
            "layout": "content_list",
            "title": "Executive Summary",
            "content": { 
                "bullet_points": [
                    "Integration of real-time route optimization",
                    "Reduction in last-mile delivery latency",
                    "Enhanced predictive maintenance for drone fleets"
                ] 
            }
        },
        {
            "id": 3,
            "layout": "image_page", 
            "title": "Concept Visualization",
            "visual": {
                "need_image": true,
                "image_prompt": "Futuristic automated warehouse with robotic arms, cyan and silver lighting, photorealistic 8k",
                "caption": "Digital twin of a next-generation sorting facility"
            }
        },
        {
            "id": 4,
            "layout": "table",
            "title": "Performance Benchmark: AI vs. Traditional",
            "table_data": {
                "headers": ["Metric", "Traditional Model", "AI-Agent Model"],
                "rows": [
                    ["Operational Efficiency", "Low", "Excellent"], 
                    ["Cost per Delivery", "High", "Significantly Lower"],
                    ["Error Rate", "4.5%", "0.2%"]
                ]
            }
        },
        {
            "id": 5,
            "layout": "metric",
            "title": "Key Market Impact",
            "metric": { 
                "value": "85%", 
                "label": "Cost Savings", 
                "desc": "Expected reduction in overhead for urban logistics by 2027." 
            }
        },
        {
            "id": 6,
            "layout": "steps",
            "title": "Implementation Roadmap",
            "steps": [ 
                { "label": "Phase 1: Integration", "desc": "Connecting AI nodes to existing ERP systems." },
                { "label": "Phase 2: Training", "desc": "Fine-tuning localized routing models." },
                { "label": "Phase 3: Deployment", "desc": "Full-scale rollout across major metropolitan hubs." }
            ]
        },
        {
            "id": 7,
            "layout": "swot",
            "title": "Strategic SWOT Analysis",
            "swot": { 
                "s": ["Real-time adaptability", "Scalable infrastructure"], 
                "w": ["High initial R&D costs", "Dependency on high-speed connectivity"], 
                "o": ["Expansion into global markets", "Partnerships with e-commerce giants"], 
                "t": ["Rapid regulatory changes", "Cybersecurity threats"] 
            }
        }
        ]
    }
    You are an intelligent designer. Select 3-5 appropriate layout_ids from the library to build a cohesive narrative. 
    Do not use all layouts in a single presentation. For example, use SWOT_MATRIX only for Corporate strategy.
    You must only provide content fields that match the layout_id. For example, if layout_id is BIG_METRIC, do not provide bullet_points. 
    Provide metric_value and metric_label instead.


# Final Output Format
Output ONLY a valid JSON object. No conversational filler.

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