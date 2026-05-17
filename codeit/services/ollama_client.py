import httpx
import json
from typing import Dict, Any, AsyncGenerator

class OllamaClient:
    """
    Interfaces directly with the local Ollama REST API instance.
    """

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "qwen2.5-coder:14b-instruct"):
        self.base_url = base_url
        self.model = model

    async def generate_notebook_structure(self, paper_data: Dict[str, Any]) -> AsyncGenerator[str, None]:
        """
        Inputs:
            paper_data (Dict[str, Any]): Dictionary matching the layout emitted by the PDFProcessor.
        Outputs:
            AsyncGenerator[str, None]: Yields progressive text chunks of the structured JSON response stream.
        Description:
            Assembles a tailored prompt instructions payload demanding a valid JSON execution map back from 
            the local Ollama LLM. The schema cleanly segments Markdown descriptions from functional PyTorch code cells.
        """
        prompt = f"""
You are an expert AI/ML Embedded Software Engineer. Your task is to analyze the following research paper and translate its core methodology and algorithms into a completely executable, clean, and self-contained PyTorch/Python script block.

The implementation MUST focus on CPU execution and reduced/mock data scaling so it runs seamlessly on local consumer hardware.

Paper Title: {paper_data['title']}

Raw Excerpts / Key Text:
{paper_data['text'][:6000]}

Extracted Key Math/Equations:
{', '.join(paper_data['equations'])}

You MUST respond strictly with a valid JSON array of objects, and nothing else. Do not wrap it in markdown code blocks like ```json.
Each object in the array represents a cell in a Jupyter notebook and MUST match this exact format:
[
  {{"type": "markdown", "content": "# Section Title\\nDetailed theoretical description using LaTeX equations where appropriate."}},
  {{"type": "code", "content": "import torch\\n# Complete, functional python code implementation block"}}
]

Provide sections for: Abstract/Introduction, Core Methodology, Complete Algorithm Implementation, and a Mock Execution Experiment Loop.
"""

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": 0.2
            }
        }

        async with httpx.AsyncClient(timeout=300.0) as client:
            async with client.stream("POST", f"{self.base_url}/api/generate", json=payload) as response:
                if response.status_code != 200:
                    yield json.dumps([{"type": "markdown", "content": f"### Error interacting with Ollama engine service: HTTP {response.status_code}"}])
                    return
                
                buffer = ""
                async for chunk in response.aiter_text():
                    if not chunk:
                        continue
                    # Handle typical line-delimited streaming JSON from Ollama endpoints
                    for line in chunk.split("\n"):
                        if line.strip():
                            try:
                                parsed = json.loads(line)
                                response_text = parsed.get("response", "")
                                yield response_text
                            except json.JSONDecodeError:
                                pass
