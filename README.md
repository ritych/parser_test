# Sales Analysis Service

## Краткое описание
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean leo sapien, rutrum at lacus id, 
porttitor interdum neque. Cras metus sapien, luctus vitae tortor et, commodo egestas nisl. 
Quisque hendrerit mollis ex eget pharetra. Praesent scelerisque diam id turpis consectetur 
accumsan. Sed tristique mauris turpis, sed scelerisque ligula pellentesque eget. Suspendisse 
a egestas ante. Nunc eu leo varius, aliquam lorem at, mollis nulla. Cras pulvinar ut elit 
eget hendrerit. Donec eleifend laoreet urna, id tempus leo. In vulputate consectetur sapien, 
eget commodo est euismod vel. 

## Структура проекта:

```shell
parser-service
├── app
│   ├── dal
│   │   ├── __init__.py
│   │   └── example.py
│   ├── database
│   │   ├── __init__.py
│   │   └── session.py
│   ├── loggers
│   │   └── __init__.py
│   ├── models
│   │   ├── __init__.py
│   │   └── model.py
│   ├── routers
│   │   ├── __init__.py
│   │   └── template_router.py
│   ├── schemas
│   │   ├── __init__.py
│   │   └── template_schema.py
│   ├── services
│   │   ├── __init__.py
│   │   └── template_service.py
│   ├── tasks
│   │   │   ├── __init__.py
│   │   │   └── task.py
│   └── main.py
├── migrations
│   ├── versions
│   ├── env.py
│   ├── README
│   └── script.py.mako
├── tests
│   └── __init__.py
├── alembic.ini
├── docker-compose.yaml
├── Dockerfile
├── entrypoint.sh
├── README.md
└── requirements.txt

```

- `app`: Содержит логику работу микросервиса
- `dal/`: это слой в архитектуре программного обеспечения, который отвечает за
  взаимодействие с базой данных.
  Он изолирует бизнес-логику приложения от деталей работы с данными
- `database/`: Содержит конфигурацию engine и сессии соединения с базой данных
- `logging/`: это набор функций и классов, которые позволяют регистрировать
  события, происходящие во время работы кода.
- `models/`: Содержит файлы с моделями ORM
- `routes/`: Содержит файлы с определением маршрутов
- `schemas/`: Pydantic-модели
- `services/`: Содержит файлы с бизнес-логикой
- `migrations/`: Миграции базы данных
- `tests/`: Содержит модульные тесты
- `.env`: Файл конфигурации переменных среды
- `.gitignore`: Указывает, какие файлы и папки не должны отслеживаться VCS
- `alembic.ini`: Содержит конфигурацию Alembic для управления версиями базы
  данных
- `docker-compose.yaml`: Определяет конфигурацию для запуска нескольких
  контейнеров
- `Dockerfile`: Содержит инструкции для собрки Docker-образа
- `entrypoint.sh`: Скрипт, используемый для инициализации контейнера и запуска
  основного процесса приложения
- `README.md`: Содержит описание проекта, инструкции по установки и
  использованию
- `requirements.txt`: Файл с зависимостями проекта

## Установка

1. Клонируйте репозиторий.
2. Убедитесь, что у вас установлен Docker и Docker Compose.
3. Настройте переменные окружения в `.env`.
4. Не забудьте указать в `.env` ключ OPENAI
4. Запустите сервис:

```bash
docker-compose up --build
