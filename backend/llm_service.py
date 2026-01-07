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
async def generate_ppt_content(topic: str) -> PresentationData:
    print(f"🧠 [LLM] 正在为 '{topic}' 构思大纲...")
    
    # 这是一个 Mock (模拟) 函数，暂时不消耗 Token
    # 模拟从本地文件读取数据，方便测试渲染引擎
    try:
        # 1. 确定文件路径
        # 假设 llm_service.py 和 mock_data.json 都在 backend 目录下
        # os.path.dirname(__file__) 获取当前脚本所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, "mock_data.json")

        # 2. 读取文件
        with open(json_path, "r", encoding="utf-8") as f:
            data_dict = json.load(f)

        # 3. 转换为 Pydantic 对象 (这一步会进行数据校验)
        presentation = PresentationData(**data_dict)
        
        # 4. (可选) 如果你想假装是根据用户输入生成的，可以把 topic 覆盖掉
        # presentation.topic = topic 
        
        return presentation

    except FileNotFoundError:
        print("❌ 错误：找不到 backend/mock_data.json 文件！")
        return PresentationData(topic="Error", slides=[])
    except json.JSONDecodeError:
        print("❌ 错误：JSON 格式不对！请检查逗号和引号。")
        return PresentationData(topic="Error", slides=[])
    except Exception as e:
        print(f"❌ 数据校验失败: {e}")
        return PresentationData(topic="Error", slides=[])
    
    # verify data format matches Pydantic definition
    # return PresentationData(**mock_json)