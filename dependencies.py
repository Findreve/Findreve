from typing import Annotated
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from model import database

SessionDep = Annotated[AsyncSession, Depends(database.Database.get_session)]
