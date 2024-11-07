from typing import Optional, List

from pydantic import BaseModel, Field, field_validator


class CategoryExample(BaseModel):
    title: str
    code: str


class Category(BaseModel):
    id: str = Field(alias="_id")
    favicon: str = ""
    name: str
    description: str
    examples: Optional[CategoryExample] = None
    
    @field_validator("id")
    def convert_objectid(cls, v):
       return str(v)
   
class AddCategory(BaseModel):
    favicon: str = ""
    name: str
    description: str
    examples: Optional[CategoryExample] = None

class DeleteCategory(BaseModel):
    id: str