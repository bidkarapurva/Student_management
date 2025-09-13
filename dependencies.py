from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from database import SessionLocal  # Import SessionLocal from database.py

# Dependency: Provides a DB session for routes/services
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
