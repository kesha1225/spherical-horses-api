import uuid
from typing import Annotated

from advanced_alchemy.filters import LimitOffset, OrderBy, SearchFilter
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy import ColumnElement
from source.db.models.horse import SphericalHorse
from source.db.services.horse import HorseService
from source.schemas.horse import (
    HorseCreate,
    HorseListResponse,
    HorseResponse,
    HorseUpdate,
    SortOrder,
)
from source.web.dependencies import get_horse_service

router = APIRouter(prefix="/api/v1/horses", tags=["Сферические кони"])


@router.get(
    "/",
    response_model=HorseListResponse,
    summary="Получить список сферических коней",
    description="""
    Возвращает список сферических коней с поддержкой пагинации, фильтрации и сортировки.

    **Фильтры:**
    - `name` - поиск по имени (частичное совпадение, регистронезависимый)
    - `min_radius` / `max_radius` - фильтр по диапазону радиуса

    **Сортировка:**
    - `sort_by` - поле для сортировки
    - `sort_order` - направление сортировки (asc/desc)
    """,
    responses={
        status.HTTP_200_OK: {
            "description": "Список коней успешно получен",
            "model": HorseListResponse,
        },
    },
)
async def list_horses(
    service: Annotated[HorseService, Depends(get_horse_service)],
    skip: Annotated[
        int, Query(ge=0, description="Количество записей для пропуска")
    ] = 0,
    limit: Annotated[
        int, Query(ge=1, le=100, description="Максимальное количество записей")
    ] = 10,
    name: Annotated[
        str | None, Query(description="Фильтр по имени (частичное совпадение)")
    ] = None,
    min_radius: Annotated[
        float | None, Query(gt=0, description="Минимальный радиус")
    ] = None,
    max_radius: Annotated[
        float | None, Query(gt=0, description="Максимальный радиус")
    ] = None,
    sort_by: Annotated[str, Query(description="Поле для сортировки")] = "created_at",
    sort_order: Annotated[
        SortOrder, Query(description="Порядок сортировки")
    ] = SortOrder.DESC,
) -> HorseListResponse:
    filters: list[LimitOffset | OrderBy | SearchFilter] = [
        LimitOffset(limit=limit, offset=skip),
        OrderBy(field_name=sort_by, sort_order=sort_order.value),
    ]

    if name:
        filters.append(SearchFilter(field_name="name", value=name, ignore_case=True))

    statement_filters: list[
        LimitOffset | OrderBy | SearchFilter | ColumnElement[bool]
    ] = []
    if min_radius is not None:
        statement_filters.append(SphericalHorse.radius >= min_radius)
    if max_radius is not None:
        statement_filters.append(SphericalHorse.radius <= max_radius)

    horses, total = await service.list_and_count(*filters, *statement_filters)

    return HorseListResponse(
        items=[HorseResponse.model_validate(h) for h in horses],
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{horse_id}",
    response_model=HorseResponse,
    summary="Получить сферического коня по ID",
    description="Возвращает детальную информацию о конкретном сферическом коне по его уникальному идентификатору.",
    responses={
        status.HTTP_200_OK: {
            "description": "Конь успешно найден",
            "model": HorseResponse,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Конь с указанным ID не найден",
        },
    },
)
async def get_horse(
    horse_id: Annotated[uuid.UUID, Path(description="Уникальный идентификатор коня")],
    service: Annotated[HorseService, Depends(get_horse_service)],
) -> HorseResponse:
    horse = await service.get_one_or_none(id=horse_id)
    if horse is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Сферический конь с ID {horse_id} не найден",
        )
    return HorseResponse.model_validate(horse)


@router.post(
    "/",
    response_model=HorseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать нового сферического коня",
    description="""
    Создаёт нового сферического коня в вакууме.

    **Обязательные поля:**
    - `name` - имя коня
    - `radius` - радиус сферы в метрах
    - `color` - цвет коня
    """,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Конь успешно создан",
            "model": HorseResponse,
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Ошибка валидации входных данных",
        },
    },
)
async def create_horse(
    data: HorseCreate,
    service: Annotated[HorseService, Depends(get_horse_service)],
) -> HorseResponse:
    horse = await service.create(data)
    return HorseResponse.model_validate(horse)


@router.patch(
    "/{horse_id}",
    response_model=HorseResponse,
    summary="Обновить данные сферического коня",
    description="""
    Частично обновляет данные существующего сферического коня.

    Можно обновить любое из полей:
    - `name`, `radius`, `color`

    Передавайте только те поля, которые нужно изменить.
    """,
    responses={
        status.HTTP_200_OK: {
            "description": "Конь успешно обновлён",
            "model": HorseResponse,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Конь с указанным ID не найден",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Ошибка валидации входных данных",
        },
    },
)
async def update_horse(
    horse_id: Annotated[uuid.UUID, Path(description="Уникальный идентификатор коня")],
    data: HorseUpdate,
    service: Annotated[HorseService, Depends(get_horse_service)],
) -> HorseResponse:
    horse = await service.get_one_or_none(id=horse_id)
    if horse is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Сферический конь с ID {horse_id} не найден",
        )
    updated_horse = await service.update(
        data,
        item_id=horse_id,
        auto_commit=True,
    )
    return HorseResponse.model_validate(updated_horse)


@router.delete(
    "/{horse_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить сферического коня",
    description="Удаляет сферического коня из вакуума по его уникальному идентификатору.",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Конь успешно удалён",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Конь с указанным ID не найден",
        },
    },
)
async def delete_horse(
    horse_id: Annotated[uuid.UUID, Path(description="Уникальный идентификатор коня")],
    service: Annotated[HorseService, Depends(get_horse_service)],
) -> None:
    horse = await service.get_one_or_none(id=horse_id)
    if horse is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Сферический конь с ID {horse_id} не найден",
        )
    await service.delete(horse_id)
