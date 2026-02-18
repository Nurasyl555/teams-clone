# 🚀 Quick Start Guide - Teams Clone

## Для Team Lead (Участник 1)

### 1. Инициализация Git репозитория

```bash
# Перейти в директорию проекта
cd teams-clone-project

# Запустить скрипт инициализации Git
chmod +x git_setup.sh
./git_setup.sh

# Создать репозиторий на GitHub
# Потом добавить remote
git remote add origin <your-repository-url>
git push -u origin teams-clone-project
```

### 2. Настройка локального окружения

```bash
# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# Установить зависимости
pip install -r requirements/dev.txt

# Применить миграции (пока их нет, но позже)
python manage.py migrate

# Создать суперпользователя
python manage.py createsuperuser

# Запустить сервер
python manage.py runserver
```

### 3. Проверка что все работает

Откройте в браузере:
- http://127.0.0.1:8000/admin/ - должен открыться admin panel
- http://127.0.0.1:8000/api/docs/ - должна открыться Swagger документация

---

## Для других участников команды

### 1. Клонирование репозитория

```bash
# Клонировать проект
git clone <repository-url>
cd teams-clone-project

# Проверить что вы на правильной ветке
git branch
# Должно показать: teams-clone-project
```

### 2. Настройка окружения

```bash
# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Установить зависимости
pip install -r requirements/dev.txt

# Применить миграции
python manage.py migrate
```

### 3. Создание своей ветки

```bash
# Участник 2 (Teams)
git checkout -b feature/teams

# Участник 3 (Channels)
git checkout -b feature/channels

# Участник 4 (Messages)
git checkout -b feature/messages
```

### 4. Начало работы над своей задачей

**Пример для Участника 2 (Teams):**

```bash
# Создать Django приложение
python manage.py startapp teams apps/teams

# Добавить в INSTALLED_APPS (settings/base.py)
LOCAL_APPS = [
    'apps.teams',
]

# Создать модели в apps/teams/models.py
# Создать serializers в apps/teams/serializers.py
# Создать views в apps/teams/views.py
# Создать urls в apps/teams/urls.py

# Создать миграции
python manage.py makemigrations

# Применить миграции
python manage.py migrate

# Зарегистрировать в admin (apps/teams/admin.py)

# Тестировать endpoints
python manage.py runserver
```

### 5. Commit и Push

```bash
# Добавить изменения
git add .

# Коммит
git commit -m "Add Teams app with CRUD endpoints"

# Запушить в свою ветку
git push origin feature/teams

# Создать Pull Request на GitHub
```

---

## Важные файлы для каждого участника

### Участник 1 (Users/Auth)
- `apps/users/models.py` - Custom User Model
- `apps/users/serializers.py` - User Serializers
- `apps/users/views.py` - Auth Views (Register, Login, etc.)
- `apps/users/urls.py` - URL patterns
- `apps/users/permissions.py` - Custom Permissions

### Участник 2 (Teams)
- `apps/teams/models.py` - Team Model
- `apps/teams/serializers.py` - Team Serializers
- `apps/teams/views.py` - Team ViewSets
- `apps/teams/urls.py` - URL patterns
- `apps/teams/permissions.py` - IsOwner, IsMember permissions

### Участник 3 (Channels)
- `apps/channels/models.py` - Channel Model
- `apps/channels/serializers.py` - Channel Serializers
- `apps/channels/views.py` - Channel ViewSets
- `apps/channels/urls.py` - URL patterns
- `apps/channels/permissions.py` - Channel Permissions

### Участник 4 (Messages)
- `apps/messages/models.py` - Message Model
- `apps/messages/serializers.py` - Message Serializers
- `apps/messages/views.py` - Message ViewSets
- `apps/messages/urls.py` - URL patterns
- `apps/messages/permissions.py` - IsAuthorOrReadOnly permission

---

## Чеклист перед созданием Pull Request

- [ ] Код работает без ошибок
- [ ] Созданы все необходимые endpoints
- [ ] Добавлены serializers
- [ ] Настроены permissions
- [ ] Модели зарегистрированы в admin
- [ ] Добавлена документация (docstrings)
- [ ] Протестированы все endpoints в Postman/Thunder Client
- [ ] Сделаны screen recordings для Corporoom
- [ ] Код отформатирован и читаемый

---

## Полезные команды

```bash
# Создать новое приложение
python manage.py startapp app_name apps/app_name

# Создать миграции
python manage.py makemigrations

# Применить миграции
python manage.py migrate

# Запустить сервер
python manage.py runserver

# Создать суперпользователя
python manage.py createsuperuser

# Django shell
python manage.py shell

# Показать SQL миграций
python manage.py sqlmigrate app_name migration_number

# Проверить проблемы
python manage.py check
```

---

## Тестирование API

### Использование Postman/Thunder Client

1. **Register (POST /api/auth/register/)**
```json
{
    "email": "test@example.com",
    "password": "password123",
    "first_name": "Test",
    "last_name": "User"
}
```

2. **Login (POST /api/auth/login/)**
```json
{
    "email": "test@example.com",
    "password": "password123"
}
```

3. **Использовать токен в Headers:**
```
Authorization: Bearer <your_access_token>
```

---

## Troubleshooting

### Проблема: ModuleNotFoundError
**Решение:** Убедитесь что виртуальное окружение активировано

### Проблема: No migrations to apply
**Решение:** Сначала запустите `makemigrations`, потом `migrate`

### Проблема: Permission denied при запуске git_setup.sh
**Решение:** Запустите `chmod +x git_setup.sh`

### Проблема: Port already in use
**Решение:** Запустите сервер на другом порту: `python manage.py runserver 8001`

---

## Контакты

Вопросы пишите в Telegram группу команды! 💬
