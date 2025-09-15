from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId
import re
class Project(BaseModel):
    id: Optional[str] = Field(alias="_id")
    project_id: str = Field(..., min_length=1)

    @validator('project_id')
    def validate_project_id(cls, value):
        import re
        if not re.match(r'^[a-zA-Z0-9_-]+$', value):
            raise ValueError('project_id must be alphanumeric, with optional - or _')
        return value

    class Config:
        arbitrary_types_allowed = True
        