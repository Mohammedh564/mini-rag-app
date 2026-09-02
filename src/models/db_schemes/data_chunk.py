from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from bson.objectid import ObjectId


class DataChunk(BaseModel):

    _id: Optional[ObjectId]
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: str
    chunk_order: str = Field(..., gt=0)
    chunk_project_id: ObjectId

    model_config = ConfigDict(arbitrary_types_allowed=True)