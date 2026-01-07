from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from llm_service import generate_ppt_content
from ppt_engine import create_pptx_file
import uvicorn
import os

# initialize FastAPI app
app = FastAPI()

# mount static files for downloading generated ppts
os.makedirs("generated_ppts", exist_ok=True)
app.mount("/download", StaticFiles(directory="generated_ppts"), name="download")

class TopicRequest(BaseModel):
    topic: str

@app.post("/api/generate")
async def generate_ppt(req: TopicRequest):
    print(f"🚀 received request: {req.topic}")
    
    # 1. invoke LLM service to get PPT content
    ppt_data = await generate_ppt_content(req.topic)
    
    # 2. invoke PPT rendering engine to create PPTX file
    filename = create_pptx_file(ppt_data)
    
    # 3. construct download URL
    download_url = f"http://localhost:8000/download/{filename}"
    
    return {
        "status": "success",
        "topic": ppt_data.topic,
        "download_url": download_url
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)