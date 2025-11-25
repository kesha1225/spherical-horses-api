import uuid
from datetime import datetime
from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class SortOrder(StrEnum):
    ASC = "asc"
    DESC = "desc"


class HorseBase(BaseModel):
    name: Annotated[
        str,
        Field(
            min_length=1,
            max_length=255,
            description="Имя сферического коня",
            examples=["Буцефал"],
        ),
    ]
    radius: Annotated[
        float,
        Field(
            gt=0,
            description="Радиус сферы в метрах",
            examples=[1.5],
        ),
    ]
    color: Annotated[
        str,
        Field(
            min_length=1,
            max_length=100,
            description="Цвет коня",
            examples=["белый"],
        ),
    ]


class HorseCreate(HorseBase):
    pass


class HorseUpdate(BaseModel):
    name: Annotated[
        str | None,
        Field(
            min_length=1,
            max_length=255,
            description="Имя сферического коня",
            examples=["Буцефал"],
        ),
    ] = None
    radius: Annotated[
        float | None,
        Field(
            gt=0,
            description="Радиус сферы в метрах",
            examples=[1.5],
        ),
    ] = None
    color: Annotated[
        str | None,
        Field(
            min_length=1,
            max_length=100,
            description="Цвет коня",
            examples=["белый"],
        ),
    ] = None


class HorseResponse(HorseBase):
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[uuid.UUID, Field(description="Уникальный идентификатор коня")]
    created_at: Annotated[datetime, Field(description="Дата и время создания")]
    updated_at: Annotated[
        datetime, Field(description="Дата и время последнего обновления")
    ]


class HorseListResponse(BaseModel):
    items: list[HorseResponse]
    total: Annotated[int, Field(description="Общее количество записей")]
    skip: Annotated[int, Field(description="Текущий offset")]
    limit: Annotated[int, Field(description="Текущий лимит")]
