from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from source.db.session import get_db
from source.db.services.horse import HorseService


async def get_horse_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> HorseService:
    return HorseService(session=db)
