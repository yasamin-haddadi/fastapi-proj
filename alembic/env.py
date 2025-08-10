import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from movie_app.users.v1.models import user, role, permission, role_permission

# 🔧 Add the `src` directory to sys.path to enable absolute imports
current_dir = os.path.dirname(os.path.realpath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)


# ⚙️ Load app settings and SQLAlchemy Base (metadata for models)
from movie_app.core.config import get_settings
from movie_app.infrastructure.database.base import Base

# 📦 Alembic config object from alembic.ini
config = context.config
settings = get_settings()
config.set_main_option('sqlalchemy.url', str(settings.DATABASE_URL))


# 📝 Set up logging if alembic.ini has logging config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 🧱 Metadata for autogeneration of migrations
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

