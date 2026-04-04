import asyncio
import os
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import pool, text
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv

# --- STEP 1: LOAD ENV FROM ROOT ---
# current_file_path is project/alembic/env.py
# project_root is project/
current_file_path = Path(__file__).resolve()
project_root = current_file_path.parent.parent
dotenv_path = project_root / ".env"

if not dotenv_path.exists():
    print(f"CRITICAL: .env file not found at {dotenv_path}")
load_dotenv(dotenv_path, override=True)

# --- STEP 2: CONSTRUCT DATABASE URL MANUALLY ---
DB_USER = os.getenv("DB_USERNAME", "postgres")
DB_PASS = os.getenv("DB_SECRET_KEY", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "")

# We build the asyncpg URL specifically for Alembic's async engine
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# DEBUG: Check if variables are actually loading (Hiding password for safety)
print(f"--- DEBUG: ENV LOADING ---")
print(f"Project Root: {project_root}")
print(f"Connecting as: {DB_USER} to {DB_HOST}:{DB_PORT}/{DB_NAME}")
print(f"--------------------------")

# --- STEP 3: IMPORT MODELS ---
from src.db.base import Base

# Import all models to ensure they register with Base.metadata
from src.db.models.AppUsers import AppUser
from src.db.models.RBAC import Permissions, RolePermissions, Roles, UserRoles

# --- STEP 4: ALEMBIC CONFIG ---
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

print("--- DEBUG 1: REGISTERED TABLES IN PYTHON ---")
print(f"Found: {list(target_metadata.tables.keys())}")
print("--------------------------------------------")

def do_run_migrations(connection: Connection) -> None:
    # Force the connection to use the public schema
    connection.execute(text("SET search_path TO public"))

    db_name = connection.execute(text("SELECT current_database()")).scalar()
    print(f"--- DEBUG 2: DATABASE CONNECTION SUCCESSFUL: {db_name} ---")

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()
async def run_async_migrations() -> None:
    connectable = create_async_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )

    try:
        async with connectable.begin() as connection:
            await connection.run_sync(do_run_migrations)
    except Exception as e:
        print(f"CRITICAL ERROR during connection: {e}")
        raise e
    finally:
        await connectable.dispose()


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (for --sql)."""
    # Replace % with %% for Alembic's config parser
    url = DATABASE_URL.replace("%", "%%")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


# --- STEP 5: EXECUTION ---
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
