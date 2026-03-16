from pydantic import BaseModel, Field
from typing import Annotated, Optional
from datetime import datetime, timezone, timedelta

pak_timezone = timezone(timedelta(hours=5))


class TeacherReview(BaseModel):
    name: Annotated[str, Field(default='anonymous', max_length=25)]
    rating: Annotated[int, Field(..., ge=1, le=5)]
    review_msg: Annotated[Optional[str], Field(None, max_length=500)]
    created_at: datetime = None

    def __init__(self, **data):
        super().__init__(**data)
        self.created_at = datetime.now(pak_timezone).replace(tzinfo=None)