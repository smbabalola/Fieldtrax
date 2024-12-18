import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, create_engine
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Add parent directory to path
BASE_PATH = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_PATH)

# Import app modules
from app.database import Base
# Import ALL models that should be included in migrations
# from app.models.authsystem.authorization.role import Role
from app.models.authsystem.permission import Permission
from app.models.authsystem.role import Role
# Import your wellbore models
from app.models.authsystem import *
from app.models.jobsystem import *
from app.models.rigsystem import *
from app.models.logisticsystem import *
# Add this
# Import any other models that need to be included in migrations
# from app.models.wellsystem import *  # If you have a models module, import all models
from app.core.config import settings

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def get_url():
    return f"mssql+pyodbc://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_SERVER')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}?driver={os.getenv('DB_DRIVER').replace(' ', '+')}"

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_url()
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
    connectable = create_engine(get_url())

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()