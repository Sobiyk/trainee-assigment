# Управление баннерами
![Static Badge](https://img.shields.io/badge/python-3.11-black?style=plastic&logo=python&labelColor=black&color=blue) ![Static Badge](https://img.shields.io/badge/fastapi-black?style=plastic&logo=fastapi&labelColor=black&color=blue)

#### Шаблон наполнения .env файла
```
DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/db_name"
SECRET="SECRET"
FIRST_SUPERUSER_EMAIL='user@example.com'
FIRST_SUPERUSER_PASSWORD='password'
FIRST_SUPERUSER_ROLE='admin'
```

#### Для заупска с помощью docker:
Соберите docker контейнеры
```
docker-compose up -d --build
```
Выполните миграции
```
docker-compose exec web alembic upgrade head
```
Заполните БД данными
```
docker-compose exec db psql -U postgres
\c banners
\copy feature(id, name) from '/docker-entrypoint-initdb.d/feature.csv' delimiter ';' CSV HEADER;
\copy tag(id, name) from '/docker-entrypoint-initdb.d/tag.csv' delimiter ';' CSV HEADER;
```
Перезапустите сервер
```
docker-compose exec -d web uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
### [Документация](http://localhost:8004/docs) с описанием эндпоинтов, примерами запросов и ответов

#### Для заупска локально:
```
py -3.11 -m venv venv
```
```
python -m pip install --upgrade pip
```
```
pip install -r requriments.txt
```
```
alembic upgrade head
```
```
uvicorn app.main:app --reload
```

### Также скачать документацию отдельно можно [здесь](https://disk.yandex.ru/d/toJ0oTJhmJcwgg)