from pydantic import BaseModel
from typing import Optional

class ParseText(BaseModel):
    file_name: str