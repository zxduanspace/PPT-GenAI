from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from llm_service import generate_ppt_content
from ppt_engine import create_pptx_file
import uvicorn
import os
from models import PresentationData

app = FastAPI(title="AI PPT Generator Pro")

# 挂载静态文件目录，用于下载生成的 PPT
os.makedirs("generated_ppts", exist_ok=True)
app.mount("/download", StaticFiles(directory="generated_ppts"), name="download")

# --- 接口 A: 生成大纲 (Preview) ---
class OutlineRequest(BaseModel):
    topic: str
    slide_length: int = 8
    theme: str = "academic"
    use_ai: bool = True

@app.post("/api/generate_outline")
async def generate_outline(req: OutlineRequest):
    print(f"🧠 [Step 1] 正在构思大纲: Topic={req.topic}")
    # 调用 LLM 服务
    ppt_data = await generate_ppt_content(req.topic, use_ai=req.use_ai)
        
    # 直接返回 Pydantic 对象，FastAPI 会自动转成 JSON
    return {
        "status": "success",
        "data": ppt_data
    }

# --- 接口 B: 渲染文件 (Render) ---
class RenderRequest(BaseModel):
    theme: str = "academic"
    ppt_data: PresentationData

@app.post("/api/render_pptx")
async def render_pptx(req: RenderRequest):
    print(f"🎨 [Step 2] 正在渲染文件: Theme={req.theme}, Slides={len(req.ppt_data.slides)}")
    # 调用渲染引擎
    # 注意：这里 req.data 已经是校验好的 PresentationData 对象了，直接用！
    filename = create_pptx_file(req.ppt_data, req.theme)
        
    # 拼接下载链接 (实际部署建议配置 BASE_URL)
    download_url = f"http://localhost:8000/download/{filename}"
        
    return {
        "status": "success",
        "download_url": download_url,
    }
    

# --- 综合接口C: 一步到位生成 PPT ---
class GenRequest(BaseModel):
    topic: str
    theme: str = "academic"
    use_ai: bool = True  # 新增开关: True=真实生成, False=快速测试

@app.post("/api/generate")
async def generate_ppt(req: GenRequest):
    print(f"🚀 收到请求: Topic={req.topic}, AI={req.use_ai}")
    
    # 1. 调用 LLM 服务生成内容 (融合了 mock 和 real AI)
    ppt_data = await generate_ppt_content(req.topic, req.use_ai)
    
    # 2. 调用渲染引擎生成文件 (融合了图片、表格、自适应文本)
    filename = create_pptx_file(ppt_data, req.theme)
    
    # 3. 返回下载链接
    # 注意: localhost 在服务器部署时需要改为服务器 IP
    download_url = f"http://localhost:8000/download/{filename}"
    
    return {
        "status": "success",
        "topic": ppt_data.topic,
        "download_url": download_url,
        "slide_count": len(ppt_data.slides)
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)