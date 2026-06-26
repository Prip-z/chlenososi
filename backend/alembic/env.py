import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 2. ИМПОРТИРУЕМ КОНФИГ И МОДЕЛИ
from app.core.config import configs
from sqlmodel import SQLModel

import app.model.base_model
import app.model.map_graph
import app.model.user



config = context.config

config.set_main_option("sqlalchemy.url", configs.DATABASE_URI)

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 4. УКАЗЫВАЕМ МЕТАДАННЫЕ ДЛЯ АВТОГЕНЕРАЦИИ
target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
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
    """Run migrations in 'online' mode."""
    
    # engine_from_config прочитает настройки с префиксом "sqlalchemy.", 
    # а мы туда выше как раз прокинули наш url через set_main_option
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