from fastapi import APIRouter, Depends

from app.core.database import get_db
from app.core.exceptions import DatabaseError
from app.modules.auth.deps import get_current_user

router = APIRouter(prefix="/items", tags=["items"], dependencies=[Depends(get_current_user)])


@router.get("/")
async def list_items():
    db = get_db()
    if db is None:
        raise DatabaseError()
    items = await db["items"].find().to_list(100)
    return items
