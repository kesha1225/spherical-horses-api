import asyncio
import operator
from logging.config import fileConfig

from advanced_alchemy.base import orm_registry
from alembic import context
from alembic.autogenerate import rewriter
from alembic.operations import ops
from alembic.runtime.environment import EnvironmentContext
from sqlalchemy import Column, pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from source.db.models import *  # noqa: F403
from source.shared.settings import settings

config = context.config
config.set_main_option("sqlalchemy.url", settings.database_url)


if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = orm_registry.metadata

writer = rewriter.Rewriter()


@writer.rewrites(ops.CreateTableOp)
def order_columns(
    context: EnvironmentContext,
    revision: tuple[str, ...],
    op: ops.CreateTableOp,
) -> ops.CreateTableOp:
    """Orders ID first and the audit columns at the end."""
    special_names = {
        "id": -100,
        "sa_orm_sentinel": 3001,
        "created_at": 3002,
        "updated_at": 3002,
    }
    cols_by_key = [
        (
            special_names.get(col.key, index) if isinstance(col, Column) else 2000,
            col.copy(),  # type: ignore[attr-defined]
        )
        for index, col in enumerate(op.columns)
    ]
    columns = [col for _, col in sorted(cols_by_key, key=operator.itemgetter(0))]
    return ops.CreateTableOp(
        op.table_name,
        columns,
        schema=op.schema,
        # Remove when https://github.com/sqlalchemy/alembic/issues/1193 is fixed
        _namespace_metadata=op._namespace_metadata,
        **op.kw,
    )


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
