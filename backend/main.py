from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from llm_service import generate_ppt_content
from ppt_engine import create_pptx_file
import uvicorn
import os

app = FastAPI(title="AI PPT Generator Pro")

# 挂载静态文件目录，用于下载生成的 PPT
os.makedirs("generated_ppts", exist_ok=True)
app.mount("/download", StaticFiles(directory="generated_ppts"), name="download")

# 定义请求体
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