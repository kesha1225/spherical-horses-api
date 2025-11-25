import datetime

from advanced_alchemy.base import CommonTableAttributes, orm_registry
from advanced_alchemy.mixins import UUIDv7PrimaryKey
from advanced_alchemy.types import DateTimeUTC
from sqlalchemy import text
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    validates,
)

from source.shared.times import get_utcnow


class ServerDefault:
    true = "true"
    false = "false"
    empty_dict = "{}"
    now = text("CURRENT_TIMESTAMP")
    uuid = text("gen_random_uuid()")


class OnDelete:
    cascade = "CASCADE"
    set_null = "SET NULL"
    restrict = "RESTRICT"


class BaseTable(CommonTableAttributes, DeclarativeBase, UUIDv7PrimaryKey):
    registry = orm_registry

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTimeUTC(timezone=True),
        default=get_utcnow,
        server_default=ServerDefault.now,
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTimeUTC(timezone=True),
        default=get_utcnow,
        server_default=ServerDefault.now,
        onupdate=get_utcnow,
        server_onupdate=ServerDefault.now,
    )

    @validates("created_at", "updated_at")
    def validate_tz_info(self, _: str, value: datetime.datetime) -> datetime.datetime:
        if value.tzinfo is None:
            value = value.replace(tzinfo=datetime.UTC)
        return value
