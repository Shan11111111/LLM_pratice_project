from fastapi import APIRouter
from pydantic import BaseModel
from services.retriever import retrieve_with_memory
from services.generators import answer_with_citations

router = APIRouter()

class ChatIn(BaseModel):
    session_id: str
    user_id: int
    query: str
    top_k: int = 6
    web: bool = True  # 是否允許抓外網

@router.post("/")
def chat(invo: ChatIn):
    # 1) 取對話記憶（最近N則 + 長期筆記）
    # 2) 檢索：本地Chunk向量 +（選）外網抓取後再嵌入
    ctx = retrieve_with_memory(
        user_id=invo.user_id, session_id=invo.session_id,
        query=invo.query, top_k=invo.top_k, allow_web=invo.web
    )
    # 3) 嚴格RAG生成（必須引用），失敗轉「未知」
    answer = answer_with_citations(query=invo.query, ctx=ctx)
    return answer  # {text, sources:[{id/url, quote, score}]}
