import nbformat as nbf
import json
import re
from typing import List, Dict, Any

class NotebookBuilder:
    """
    Transforms structural text interpretations directly into valid native Jupyter Notebook files.
    """

    def build_from_json_string(self, raw_json_str: str) -> str:
        cleaned_str = raw_json_str.strip()
        
        if cleaned_str.startswith("```json"):
            cleaned_str = cleaned_str[7:]
        if cleaned_str.endswith("```"):
            cleaned_str = cleaned_str[:-3]
            
        cleaned_str = cleaned_str.strip()

        if not cleaned_str.startswith("["):
            cleaned_str = "[" + cleaned_str
        if not cleaned_str.endswith("]"):
            cleaned_str = cleaned_str + "]"

        nb = nbf.v4.new_notebook()
        nb['cells'] = []

        try:
            cells_data = json.loads(cleaned_str)
            for cell in cells_data:
                cell_type = cell.get("type", "markdown")
                content = cell.get("content", "")

                if cell_type == "code":
                    nb['cells'].append(nbf.v4.new_code_cell(content))
                else:
                    nb['cells'].append(nbf.v4.new_markdown_cell(content))
        except Exception as e:
            nb['cells'].append(nbf.v4.new_markdown_cell(f"# Generation Error\nFailed to map raw output. Error: {str(e)}"))

        return nbf.writes(nb)
