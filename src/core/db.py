from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.decl_api import DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:///./eisenhour.db"

engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base: DeclarativeBase = declarative_base()
