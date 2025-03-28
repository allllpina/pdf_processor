from pydantic import BaseModel
from typing import Optional

class ParseText(BaseModel):
    file_name: str

class CreatePdfFromText(BaseModel):
    filename: Optional[str] = None
    title: Optional[str] = None
    font_size: Optional[int] = 15
    text_lines: list[str]