# Spherical Horse API

REST API для управления сферическими конями в вакууме.

## Запуск

### Docker (рекомендуется)

```bash
docker-compose -f docker/docker-compose.yml up -d
```

### Локально

```bash
pip install -r requirements.txt
createdb spherical_horses
alembic upgrade head
uvicorn source.web.app:app --reload
```

Переменные окружения (`.env`):

```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/spherical_horses
```

## API

| Метод  | Путь                  | Описание             |
| ------ | --------------------- | -------------------- |
| GET    | `/api/v1/horses/`     | Список (с фильтрами) |
| GET    | `/api/v1/horses/{id}` | Получить по ID       |
| POST   | `/api/v1/horses/`     | Создать              |
| PATCH  | `/api/v1/horses/{id}` | Обновить             |
| DELETE | `/api/v1/horses/{id}` | Удалить              |

**Query параметры для списка:** `skip`, `limit`, `name`, `min_radius`, `max_radius`, `sort_by`, `sort_order`

## Документация

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
