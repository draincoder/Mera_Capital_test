import logging

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from database.crud import get_db, Database
from app.models import Pnl


logger = logging.getLogger(__name__)
router = APIRouter()


@router.get('/index', response_model=Pnl)
async def get_index_period(DateFrom: int = None, DateTo: int = None, db: Database = Depends(get_db)):
    try:
        exc = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Invalid dates')
        if DateFrom and DateTo:
            if DateFrom <= DateTo:
                return await db.get_statistics(DateFrom, DateTo)
            else:
                raise exc
        else:
            return await db.get_statistics()
    except Exception as e:
        logger.error(e)
        raise exc
