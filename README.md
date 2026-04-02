# Типовой шаблон FastAPI проекта

## Окружение

Python

alembic

sqlalchemy

fastapi

pydantic

asyncpg

celery

## Описание

## Первый запуск и развертывание

### Запуск приложения

#### Создать .env файл на основе ``.env.example``

#### Запуск окружения

``` bash
docker-compose -f docker-compose.dev.yml up -d --build --force-recreate
```

#### Установка зависимостей

``` bash
pip install -r requirements.dev.txt
```

#### Применение миграций

``` bash
python -m db upgrade head
```

#### Создание конфигурации запуска

Создать python конфигурацию, указав запуск скрипта /{full_root_path}/main_app.py с рабочей директорией full_root_path

### Хранение состояния

Миграции применяются при старте сервера.

Создание миграций

```
python -m db revision --autogenerate 
```

Откат всех миграций

```
python -m db  downgrade base 
```

Применение миграций

```
python -m db upgrade head
```

История миграций

```
python -m db history
```

Откат одной миграции

```
python -m db downgrade -1
```

### Запуск тестов

```
pytest -m "not integration" -vv