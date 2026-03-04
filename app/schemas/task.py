from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
import uuid

class TaskCreateSchema(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    priority: str = Field('medium', pattern='^(low|medium|high)$')
    due_date: Optional[datetime] = None
    category_id: Optional[str] = None
    
    @validator('category_id')
    def validate_uuid(cls, v):
        if v:
            try:
                uuid.UUID(v)
            except ValueError:
                raise ValueError('Invalid category ID format')
        return v

class TaskUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    priority: Optional[str] = Field(None, pattern='^(low|medium|high)$')
    due_date: Optional[datetime] = None
    category_id: Optional[str] = None
    
    @validator('category_id')
    def validate_uuid(cls, v):
        if v:
            try:
                uuid.UUID(v)
            except ValueError:
                raise ValueError('Invalid category ID format')
        return v

class TaskStatusUpdateSchema(BaseModel):
    status: str = Field(..., pattern='^(todo|in_progress|done|archived)$')