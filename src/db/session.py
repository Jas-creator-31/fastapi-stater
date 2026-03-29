from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession)
from sqlalchemy.engine import URL
from dotenv import load_dotenv
import os

load_dotenv()

db_username: str = os.getenv("DB_USERNAME")
db_secret_key: str = os.getenv("DB_SECRET_KEY")
db_host: str = os.getenv("DB_HOST")
db_port_env: str = os.getenv("DB_PORT")
db_name: str = os.getenv("DB_NAME")
db_port: int = int(db_port_env) if db_port_env else 5432


DATABASE_URL = URL.create(
    drivername="postgresql+asyncpg",
    username=db_username,
    password=db_secret_key,
    host=db_host,
    port=db_port,
    database=db_name,
)

engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession
)
