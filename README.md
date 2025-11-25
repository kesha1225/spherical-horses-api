# Spherical Horse API

REST API для управления сферическими конями в вакууме.

## Быстрый старт с Docker

```bash
docker-compose -f docker/docker-compose.yml up -d
```

API будет доступен на http://localhost:8000

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Локальная разработка

```bash
# С использованием uv
uv sync

# Или с pip
pip install -r requirements.txt
```

### Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/spherical_horses
DEBUG=false
```

### Создание базы данных

```bash
createdb spherical_horses
alembic upgrade head
```

### Запуск сервера

```bash
uvicorn source.web.app:app --reload
```

## API Эндпоинты

| Метод  | Путь                   | Описание                   |
| ------ | ---------------------- | -------------------------- |
| GET    | `/api/v1/horses/`      | Список коней (с фильтрами) |
| GET    | `/api/v1/horses/{id}`  | Получить коня по ID        |
| POST   | `/api/v1/horses/`      | Создать нового коня        |
| PATCH  | `/api/v1/horses/{id}`  | Обновить данные коня       |
| DELETE | `/api/v1/horses/{id}`  | Удалить коня               |

### Query параметры для списка

| Параметр     | Тип    | Описание                      |
| ------------ | ------ | ----------------------------- |
| `skip`       | int    | Пропустить N записей (offset) |
| `limit`      | int    | Лимит записей (1-100)         |
| `name`       | string | Поиск по имени (частичное)    |
| `min_radius` | float  | Минимальный радиус            |
| `max_radius` | float  | Максимальный радиус           |
| `sort_by`    | string | Поле сортировки               |
| `sort_order` | string | Направление (asc/desc)        |

## Примеры запросов

### Создание коня

```bash
curl -X POST http://localhost:8000/api/v1/horses/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Буцефал",
    "radius": 1.5,
    "color": "белый"
  }'
```

### Получение списка с фильтрами

```bash
curl "http://localhost:8000/api/v1/horses/?name=Буцефал&sort_by=name&sort_order=asc"
```

### Обновление коня

```bash
curl -X PATCH http://localhost:8000/api/v1/horses/{id} \
  -H "Content-Type: application/json" \
  -d '{"radius": 2.0}'
```

### Удаление коня

```bash
curl -X DELETE http://localhost:8000/api/v1/horses/{id}
```

## Структура проекта

```
source/
├── db/
│   ├── models/
│   │   ├── extensions.py    # BaseTable с UUIDv7PrimaryKey
│   │   └── horse.py         # SphericalHorse модель
│   ├── repositories/
│   │   └── horse.py         # HorseRepository (advanced-alchemy)
│   ├── services/
│   │   └── horse.py         # HorseService (advanced-alchemy)
│   ├── migrations/          # Alembic миграции
│   └── session.py           # Async сессия БД
├── schemas/
│   └── horse.py             # Pydantic схемы
├── shared/
│   ├── settings.py          # Настройки приложения
│   └── times.py             # Утилиты времени
└── web/
    ├── app.py               # FastAPI приложение
    ├── dependencies.py      # DI зависимости
    └── routers/
        └── horses.py        # API эндпоинты
docker/
├── Dockerfile
└── docker-compose.yml
```

## Миграции

```bash
# Создать новую миграцию
alembic revision --autogenerate -m "description"

# Применить все миграции
alembic upgrade head

# Откатить последнюю миграцию
alembic downgrade -1
```

## Лицензия

MIT
