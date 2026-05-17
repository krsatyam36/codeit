import fitz  # PyMuPDF
import httpx
import re
from typing import Dict, Any

class PDFProcessor:
    """
    Handles extraction of text, metadata, and mathematical blocks from raw PDFs or arXiv URLs.
    """

    async def extract_from_bytes(self, pdf_bytes: bytes) -> Dict[str, Any]:
        """
        Inputs:
            pdf_bytes (bytes): The raw binary content of an uploaded PDF file.
        Outputs:
            Dict[str, Any]: A dictionary containing the 'title', raw 'text', and extracted 'equations'.
        Description:
            Parses an in-memory PDF file page by page using PyMuPDF, extracts plain text, 
            and captures rough LaTeX-style equation blocks using regex matching patterns.
        """
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        full_text = ""
        for page in doc:
            full_text += page.get_text()

        # Clean basic multi-column line breaks
        cleaned_text = re.sub(r'(?<!\n)\n(?!\n)', ' ', full_text)
        
        # Simple heuristic regex to pull out elements that look like LaTeX block expressions
        equations = re.findall(r'(\$\$.*?\$\$|\$.*?\$)', full_text, re.DOTALL)

        # Attempt to isolate a title from the first few lines
        lines = [line.strip() for line in full_text.split('\n') if line.strip()]
        title = lines[0] if lines else "Unknown Research Paper"

        return {
            "title": title[:150],
            "text": cleaned_text,
            "equations": list(set(equations))[:20]  # Cap at unique 20 equations for context space
        }

    async def fetch_from_arxiv(self, url: str) -> Dict[str, Any]:
        """
        Inputs:
            url (str): A direct arXiv link (e.g., https://arxiv.org/abs/2401.xxxxx or https://arxiv.org/pdf/2401.xxxxx).
        Outputs:
            Dict[str, Any]: Extracted content dictionary identical to extract_from_bytes.
        Description:
            Normalizes an arXiv abstract/landing URL into a direct PDF download link, streams 
            the binary payload via an async HTTP client, and forwards it to extract_from_bytes.
        """
        # Convert abstract links to direct pdf links
        pdf_url = url.replace("arxiv.org/abs/", "arxiv.org/pdf/")
        if not pdf_url.endswith(".pdf") and "pdf" not in pdf_url:
            pdf_url += ".pdf"

        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(pdf_url, timeout=30.0)
            if response.status_code != 200:
                raise ValueError(f"Failed to fetch paper from arXiv target endpoint. Status: {response.status_code}")
            
        return await self.extract_from_bytes(response.content)
