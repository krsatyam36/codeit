import os
from fastapi import FastAPI, UploadFile, File, Query, Form, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from typing import AsyncGenerator

from codeit.services.pdf_processor import PDFProcessor
from codeit.services.ollama_client import OllamaClient
from codeit.services.notebook_builder import NotebookBuilder

app = FastAPI(title="Codeit Backend Service Router")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

pdf_processor = PDFProcessor()
ollama_client = OllamaClient()
notebook_builder = NotebookBuilder()

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard_ui(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

async def response_stream_generator(paper_data: dict, model: str) -> AsyncGenerator[str, None]:
    accumulated_response_text = ""
    async for text_chunk in ollama_client.generate_notebook_structure(paper_data, model):
        accumulated_response_text += text_chunk
        yield text_chunk
        
    notebook_file_content = notebook_builder.build_from_json_string(accumulated_response_text)
    yield f"\n\n{notebook_file_content}"

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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ArXiv Error: {str(e)}")
