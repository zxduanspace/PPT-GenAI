# AI PPT Generator - Backend Service

本项目是一个基于 Python 的自动化 PPT 生成后端服务。它结合了 OpenAI (LLM) 进行内容生成，以及 `python-pptx` 进行原生 PPTX 文件渲染。

## 🛠️ 安装与配置后端

### 1. 安装依赖
```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置文件
在 backend/ 目录下创建一个名为 .env 的文件，填入你的 OpenAI API Key
```bash
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx
```

### 3. 启动服务
```bash
python main.py
```

### 4. 后端接口调用
在浏览器打开：http://127.0.0.1:8000/docs

找到 /generate 接口，点击Execute调用