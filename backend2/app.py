# app.py
import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

# 导入新的生成函数
from main_backend import generate_ppt_file

app = FastAPI(title="PPT Generator Pro API")

# 定义请求的数据格式 (增加参数)
class PPTRequest(BaseModel):
    topic: str
    use_ai: bool = False
    template_name: str = "template.pptx"  # 默认模版
    font_name: str = "Microsoft YaHei"    # 默认字体


@app.post("/generate")
async def generate_ppt_endpoint(request: PPTRequest):
    """
    接收参数：主题、AI开关、模版名称、字体名称
    """
    # 清理文件名中的非法字符
    safe_topic = "".join([c for c in request.topic if c.isalnum() or c in (' ','-','_')]).strip()
    filename = f"output_{safe_topic}.pptx"
    
    # 检查模版文件是否存在
    template_path = request.template_name
    # 这儿可以加一个逻辑，比如只允许从 'templates/' 文件夹读取，防止路径遍历攻击
    # template_path = os.path.join("templates", request.template_name)
    
    print(f"收到请求: Topic={request.topic}, Template={template_path}, Font={request.font_name}")

    # 调用核心逻辑
    output_path = generate_ppt_file(
        topic=request.topic, 
        output_filename=filename, 
        template_path=template_path,
        font_name=request.font_name,
        use_ai=request.use_ai
    )
    
    if output_path and os.path.exists(output_path):
        return FileResponse(
            path=output_path,
            filename=filename,
            media_type='application/vnd.openxmlformats-officedocument.presentationml.presentation'
        )
    else:
        raise HTTPException(status_code=500, detail="PPT 生成失败，请检查后端日志")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)