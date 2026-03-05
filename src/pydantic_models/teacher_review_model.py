from pydantic import BaseModel, Field
from typing import Annotated, Optional

class TeacherReview(BaseModel):

    name: Annotated[str, Field(default='anonymous', max_length=25)]
    rating: Annotated[int, Field(..., ge=1, le=10)]
    review_msg: Annotated[Optional[str], Field(None, max_length=500)]