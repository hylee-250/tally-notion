from pydantic import BaseModel
from typing import Optional

class TallyResponse(BaseModel):
    이름: str
    날짜: str  # ex: "Apr 10, 2025"
    시간: str  # ex: "12:30"
    연락처: str
    학년: str
    입학_테스트_희망_시간: Optional[str] = None