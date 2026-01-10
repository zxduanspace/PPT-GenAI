# AI PPT Generator - Backend Service

> **Auto-generating professional PowerPoint slides from a single topic using LLM and Native Rendering.**

## 📋 System Requirements

Before running the backend, ensure your environment meets the following criteria:

* **Operating System:** Windows 10/11, macOS, or Linux (Ubuntu 20.04+ recommended).
* **Python Version:** Python **3.10** or higher.
* **Network:** Active internet connection (required for OpenAI API & Image downloading).
* **API Keys:** A valid **OpenAI API Key** (with access to GPT-4 or GPT-3.5-Turbo).

---

## 📂 Project Structure

The backend follows a modular architecture, separating the API layer, LLM logic, and Rendering engine.

```bash
backend/
├── generated_ppts/        # Output directory for generated .pptx files
├── templates/             # Stores master PowerPoint template files (e.g., academic.pptx)
├── .env                   # Environment variables (API Keys & Config) - *Not committed*
├── analyze_template.py    # Utility script to inspect PPTX placeholders & indices
├── llm_service.py         # AI Logic: Handles OpenAI API calls & Prompt Engineering
├── main.py                # Application Entry: FastAPI app & Route definitions
├── mock_data.json         # Fallback Data: Provides stability when AI fails
├── models.py              # Data Layer: Pydantic models for type safety & validation
├── ppt_engine.py          # Core Engine: python-pptx logic, auto-fit algorithms & rendering
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

---

## 🛠️ Installation & Setup (Local Development)

Follow these steps to run the backend locally.

### 1. Clone the Repository

```bash
git clone [https://github.com/zxduanspace/PPT-GenAI.git](https://github.com/zxduanspace/PPT-GenAI.git)
cd backend
```

### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configuration

Create a file named `.env` in the root `backend/` directory, add your OpenAI API Key and other configurations:

```ini
# Required: Your OpenAI API Key
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx
```

### 4. Start the Server

Run the following command to start the FastAPI server:

```bash
python main.py
```

You should see output indicating the server is running at `http://127.0.0.1:8000`.

---

## 🚀 Usage

### 5. Access API Documentation

Open your browser and navigate to:
👉 **http://127.0.0.1:8000/docs**

This Swagger UI allows you to test endpoints interactively.

### 6. Generate a PPT (Example)

Locate the `POST /generate` (or `/api/render_pptx`) endpoint in Swagger, click **"Try it out"**, and send a JSON payload:

```json
{
  "topic": "The Future of AI",
  "slide_count": 8,
  "theme": "academic",
  "use_ai_images": true
}
```

The server will return a downloadable URL or the binary file of the generated `.pptx`.

---

## ☁️ Deployment Guide

You can deploy this backend using **Docker**. Docker ensures the environment is consistent across all machines.

### 1. Create a Dockerfile

Create a file named `Dockerfile` in the `backend/` directory with the following content:

```dockerfile
# Use official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirement file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 8000
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Build and Run

Run the following commands in your terminal:

```bash
# Build the Docker image
docker build -t ai-ppt-backend .

# Run the container (Remember to pass your API Key)
docker run -d -p 8000:8000 -e OPENAI_API_KEY=sk-proj-your-key-here ai-ppt-backend
```