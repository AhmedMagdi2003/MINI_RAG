from pydantic import BaseModel, Field, validator, ConfigDict
from typing import Optional
from bson.objectid import ObjectId
class Project(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    
    project_id : str = Field(...,min_length=1)
    id : Optional[ObjectId] = Field(default=None, alias="_id")

    @validator('project_id')
    def validator_project_id(cls,value):
        if not value.isalnum():
            raise ValueError("project_id must be in alphanumeric")
        else:
            return value
