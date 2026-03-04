from pydantic import BaseModel, Field
from typing import Optional

class CategoryCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    color: Optional[str] = Field('#808080', pattern='^#[0-9A-Fa-f]{6}$')