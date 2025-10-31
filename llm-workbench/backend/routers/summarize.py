from fastapi import APIRouter
from pydantic import BaseModel
from services.generators import make_pptx

router = APIRouter()

class SumIn(BaseModel):
    session_id: str
    outline: list[str]           # 由前端或LLM先產出大綱
    target: str = "pptx"         # pptx / pdf / markdown

@router.post("/pptx")
def to_pptx(invo: SumIn):
    path = make_pptx(invo.session_id, invo.outline)
    return {"download": f"/static/{path.name}"}
