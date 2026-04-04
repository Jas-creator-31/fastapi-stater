from sqlalchemy.ext.asyncio import (
    
    create_async_engine,
    async_sessionmaker,
    AsyncSession

)
from sqlalchemy.engine import URL
from dotenv import load_dotenv
import os


load_dotenv()

db_username = os.getenv("DB_USERNAME")
db_secret_key = os.getenv("DB_SECRET_KAY")
db_host = os.getenv("DB_HOST")
db_port_env = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_port: int = int(db_port_env) if db_port_env else 5432

database_url = URL.create(
    drivername="postgresql+asyncpg",
    username=db_username,
    password=db_secret_key,
    host=db_host,
    port=db_port,
    database=db_name,
)


engine = create_async_engine(database_url)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession
)
