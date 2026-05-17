import os
from fastapi import FastAPI, UploadFile, File, Query, Form, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from typing import AsyncGenerator

from codeit.services.pdf_processor import PDFProcessor
from codeit.services.ollama_client import OllamaClient
from codeit.services.notebook_builder import NotebookBuilder
from codeit.services.sandbox_engine import SandboxEngine

app = FastAPI(title="Codeit IDE & Execution Backend")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

pdf_processor = PDFProcessor()
ollama_client = OllamaClient()
notebook_builder = NotebookBuilder()
sandbox_engine = SandboxEngine()

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard_ui(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

async def response_stream_generator(paper_data: dict, model: str) -> AsyncGenerator[str, None]:
    async for text_chunk in ollama_client.generate_notebook_structure(paper_data, model):
        yield text_chunk

@app.post("/api/convert/pdf")
async def convert_pdf(file: UploadFile = File(...), model: str = Form("qwen2.5-coder:14b-instruct")):
    try:
        pdf_bytes = await file.read()
        paper_data = await pdf_processor.extract_from_bytes(pdf_bytes)
        return StreamingResponse(response_stream_generator(paper_data, model), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF Error: {str(e)}")

@app.post("/api/convert/arxiv")
async def convert_arxiv(url: str = Query(...), model: str = Query("qwen2.5-coder:14b-instruct")):
    try:
        paper_data = await pdf_processor.fetch_from_arxiv(url)
        return StreamingResponse(response_stream_generator(paper_data, model), media_type="text/plain")
    exception as e:
        raise HTTPException(status_code=500, detail=f"ArXiv Error: {str(e)}")

@app.post("/api/run")
async def execute_code(code: str = Form(...)):
    """Executes raw Python code in the ephemeral sandbox."""
    try:
        stdout, stderr, retcode = await sandbox_engine.execute(code)
        return JSONResponse({
            "stdout": stdout,
            "stderr": stderr,
            "exit_code": retcode
        })
    except Exception as e:
        return JSONResponse({
            "stdout": "",
            "stderr": f'[CRITICAL ENGINE FAILURE] {str(e)}',
            "exit_code": 500
        })
