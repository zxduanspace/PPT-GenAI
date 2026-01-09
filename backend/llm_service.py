import json
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from models import PresentationData

# 加载 .env 环境变量
load_dotenv(override=True)
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# === B. 真实 AI 模式 (你的逻辑融合) ===
    # 核心 Prompt: 融合了 backend2 的 JSON 指令和 backend 的数据结构
def build_system_prompt(slide_count: int):

    return f"""
    # Role
    You are the "Lead Content & Design Strategist" at a premier global consulting firm. 
    Your goal is to transform brief user ideas into high-impact, professional-grade PPTX structures in English.

    #Intelligent Expansion (Thinking Process)
    Before generating the final JSON, you must internally:
    1. **Infer Context:** Determine the domain (Corporate, Startup, or Academic) based on the input.
    2. **Professional Vocabulary:** Use industry-standard English terminology (e.g., "Leverage," "Scalability," "Value Proposition").
    3. **Narrative Flow:** Expand short inputs into a complete 8-slide logical journey (e.g., Market Gap -> Solution -> Technical Moat -> Roadmap).

    # English Content Density Strategy (Optimized for 24pt Auto-fit)
    To ensure the presentation appears professional and data-rich, while respecting the rendering engine's font limits:

    - **Density Goal:** The current layout supports up to 2 full lines per bullet point. You must maximize this space.
    - **Target Length:** Write **25-35 words** per bullet point (approx. 180-220 characters). This is the "Sweet Spot" for professional depth.
    - **Structure:** Avoid simple phrases. Use the pattern: **"Core Insight + Supporting Data/Context"**.
    - **Bullet Count:** Strictly **4-5 bullets** per slide.
    - **Overflow Prevention:** Do NOT exceed 40 words per bullet, as the engine cannot shrink text below 24pt. 
    - **Style:** Professional, academic, and substantial. No conversational filler.
    
    The output must be in strict JSON format and should not contain Markdown tags.

    # CONTENT DENSITY RULES (The "Anti-Brevity" Protocol)
    To ensure the output looks professional and fills the layout:

    1. **"Bullet Points" Mode (Layout: content_list / two_column):**
    - **Length:** Each bullet point must be a **mini-paragraph** (minimum **40-60 words**).
    - **Structure:** Use the **"Claim + Evidence + Impact"** formula for every point.
     - *Bad:* "AI improves efficiency."
     - *Good:* "Implementing generative AI in the coding workflow automates 40% of repetitive syntax generation (Claim), which essentially removes human error from the debugging loop (Evidence), resulting in a projected 25% reduction in time-to-market for the Q4 product release (Impact)."
    - **Quantity:** Provide 4-5 such detailed points per slide.

    2. **"Text Body" Mode (Layout: content_list with 'text_body'):**
   - **Length:** Generate **150-250 words** of continuous, cohesive text. 
   - **Style:** Academic, formal, and analytical. equivalent to a section in a white paper.

    3. **Data Simulation:**
   - Whenever possible, invent **realistic-sounding data/percentages** to back up your claims. General statements are forbidden.

    # Layout & Content Rules (Strict Adherence Required)

    1. **title_cover (Cover Slide):**
   - The Main Title must be grand, professional, and engaging.
   - Font Safety: The title uses a massive 72pt font.
   - Length Limit: Strictly limit the Main Title to **maximum 40 characters** (approx. 3-6 words).
   - The Subtitle must specifically clarify the scope and context of the presentation.

    2. **content_list (Bullet Points Mode):**
   - When using `"bullet_points"`, generate **4-6 points** per slide.
   - **Critical:** Content must be deep and expansive. Do NOT use short phrases.
   - *Bad Example:* "Efficiency improved."
   - *Good Example:* "By implementing AI automation workflows, approval efficiency increased by 300%, significantly reducing the need for manual intervention."

    3. **content_list (Text Body Mode):**
   - When using the `"text_body"` field, the content must be highly detailed and substantial.
   - Avoid brief summaries. Aim for approximately **100-200 words** per slide to provide comprehensive depth.
   - You can ADD a `"visual"` object alongside `"text_body"`.

    4. **two_column (Comparison):**
   - Maintain visual balance (e.g., 3 items on the left, 3 items on the right).
   - Use this layout for comparisons such as "Current Status vs. Future State," "Problems vs. Solutions," or "Strengths vs. Weaknesses."

    5. **image_page (Concept Visualization):**
   - Set `"need_image": true`.
   - The `"image_prompt"` **MUST be in English**.
   - The description must be extremely specific, including the subject, style, lighting, and render quality.
   - *Example:* "futuristic smart factory, isometric view, neon blue lighting, unreal engine 5 render, highly detailed, 8k".

    6. **table (Data Grid):**
   - The number of columns in `"headers"` and `"rows"` must be **strictly consistent**.
   - Data must appear realistic, professional, and logically sound.

    7. **chart (Data Visualization):**
   - The list lengths of `"labels"` (X-axis) and `"values"` (Y-axis) must be **perfectly aligned**.
   - Numerical values must follow a logical trend appropriate for the topic.

    # JSON Schema (Output Format)
    You must output a valid JSON object matching EXACTLY this structure. Do NOT invent new keys.

    ```json
    {{
    "topic": "Your Topic",
    "slides": [
        {{
            "id": 1, 
            "layout": "title_cover", 
            "title": "Main Title", 
            "subtitle": "Subtitle" 
        }},
        {{ 
            "id": 2, 
            "layout": "content_list", 
            "title": "Agenda / Context", 
            "content": {{ 
                "bullet_points": [
                "The global specialty coffee market is projected to expand at a CAGR of 11.3% from 2024 to 2030, driven significantly by the rising consumer preference for ethically sourced, single-origin beans in the Asia-Pacific region.",
                "Supply chain disruptions, exacerbated by climate change impact on Arabica yields in Brazil and Vietnam, have necessitated a 15% price increase in wholesale green coffee futures over the last fiscal quarter."
                ]
            }} 
        }},
        {{ 
            "id": 3, 
            "layout": "two_column", 
            "title": "Deep Analysis", 
            "content": {{ 
                "content_left": ["Left item 1...", "Left item 2..."], 
                "content_right": ["Right item 1...", "Right item 2..."] 
            }} 
        }},
        {{ 
            "id": 4, 
            "layout": "image_page", 
            "title": "Concept Art", 
            "visual": {{ 
                "need_image": true, 
                "image_prompt": "Specific English prompt...", 
                "caption": "Caption description..." 
            }} 
        }},
        {{ 
            "id": 5, 
            "layout": "table", 
            "title": "Data Comparison", 
            "table_data": {{ 
                "headers": ["Metric", "Value"], 
                "rows": [["Efficiency", "High"], ["Cost", "Low"]] 
            }} 
        }},
        {{ 
            "id": 6, 
            "layout": "chart", 
            "title": "Growth Trend", 
            "chart_data": {{ 
                "title": "Yearly Revenue", 
                "chart_type": "COLUMN_CLUSTERED", 
                "labels": ["2023", "2024"], 
                "values": [10, 20] 
            }} 
        }},
        {{ 
            "id": 7, 
            "layout": "content_list", 
            "title": "Executive Summary", 
            "content": {{ 
                "text_body": "A very detailed paragraph containing approximately 100-200 words explaining the core concept..." 
            }} 
        }},
        {{ 
            "id": 8, 
            "layout": "content_list", 
            "title": "Executive Summary", 
            "content": {{ 
                "text_body": "A very detailed paragraph containing approximately 100-200 words explaining the core concept..." 
            }},
            "visual": {{ 
                "need_image": true, 
                "image_prompt": "Specific English prompt...", 
                "caption": "Caption description..." 
            }}  
        }}
    ]
    }}

    # Structure Constraints

    1. **Total Slide Count:** Generate EXACTLY {slide_count} slides.
    The output JSON `slides` array must contain exactly {slide_count} objects.

    2. **Mandatory Layout Inclusion:**
    To ensure visual variety, the presentation MUST include:
   - **At least ONE** data visualization chart slide (use either layout `'chart'` ).
    - **At least ONE** data visualization table slide (use either layout OR `'table'`).
   - **At least ONE** conceptual visualization slide (use layout `'image_page'`).

    3. **Content Distribution:**
   - Slide 1 must be `'title_cover'`, and `'title_cover'` only use once.
   - Use `'content_list'` (with text_body) for detailed explanations.
   - Use `'two_column'` for comparisons.
   - Do not repeat the same layout more than 3 times in a row (except for content_list).

    4. **Visual Pacing & Distribution (Critical):**
   - **Do NOT clump visual slides together.** For example, do not put all charts and images at the very end.
   - **Interleave layouts:** You must alternate between text-heavy layouts ('content_list', 'two_column') and visual layouts ('chart', 'table', 'image_page').
   - **Rhythm:** Ideally, insert a visual slide after every 2-3 text slides to keep the audience engaged.

    # Final Output Format
    Output ONLY a valid JSON object. No conversational filler.
"""

async def generate_ppt_content(topic: str, use_ai: bool = True, slide_length: int = 10) -> PresentationData:
    """
    生成 PPT 内容结构数据。
    :param topic: 用户输入的主题
    :param use_ai: True=调用OpenAI, False=使用本地Mock数据
    :param slide_length: 期望的幻灯片数量
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
    
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo", # 如果有 gpt-4 效果更好
            messages=[
                {"role": "system", "content": build_system_prompt(slide_count=slide_length)},
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