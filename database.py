from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database URL: Ensure the 'Student_project' DB exists and credentials are correct
DATABASE_URL = "postgresql+asyncpg://postgres:apu24@localhost:5432/Student_project"

# Create an asynchronous engine
engine = create_async_engine(
    DATABASE_URL, 
    echo=True,       # Logs SQL statements; set to False in production
    future=True      # Ensures SQLAlchemy 2.0 style usage
)

# Create session factory for AsyncSession
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False  # Keeps attributes accessible after commit
)

# Base class for models (used with declarative models)
Base = declarative_base()

# Dependency to get DB session (use in FastAPI with Depends)
async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()  # ✅ Ensures clean session closure
