# 📝 Database Schema Cheat Sheet

## Quick Reference для каждого участника

---

## 👤 Участник 1: USER Model

### Файл: `apps/users/models.py`

```python
class User(AbstractBaseUser, PermissionsMixin):
    # ПОЛЯ
    email              # EmailField, unique=True, USERNAME_FIELD
    password           # CharField (hashed)
    first_name         # CharField
    last_name          # CharField
    is_active          # BooleanField, default=True
    is_staff           # BooleanField, default=False
    is_superuser       # BooleanField, default=False
    date_joined        # DateTimeField, auto_now_add=True
    last_login         # DateTimeField, null=True
```

**Связи (через related_name с другими моделями):**
- `user.owned_teams` → все Teams где user - owner
- `user.teams` → все Teams где user - member
- `user.private_channels` → все приватные Channels
- `user.messages` → все Messages автора

**⚠️ Важно:**
- `USERNAME_FIELD = 'email'`
- Создать `UserManager` с `create_user()` и `create_superuser()`
- НЕ добавлять поле `username`!

---

## 🏢 Участник 2: TEAM Model

### Файл: `apps/teams/models.py`

```python
class Team(models.Model):
    # ПОЛЯ
    name               # CharField, max_length=200
    description        # TextField, blank=True, null=True
    created_at         # DateTimeField, auto_now_add=True
    updated_at         # DateTimeField, auto_now=True
    
    # СВЯЗИ
    owner              # ForeignKey → User
                       # on_delete=models.CASCADE
                       # related_name='owned_teams'
    
    members            # ManyToManyField → User
                       # through='TeamMembership'
                       # related_name='teams'
```

```python
class TeamMembership(models.Model):
    # ПОЛЯ
    joined_at          # DateTimeField, auto_now_add=True
    role               # CharField, default='member'
                       # choices: 'member', 'admin'
    
    # СВЯЗИ
    team               # ForeignKey → Team, on_delete=CASCADE
    user               # ForeignKey → User, on_delete=CASCADE
    
    # META
    unique_together = ['team', 'user']
```

**Endpoints (7 штук):**
1. `GET /api/teams/` - список команд
2. `POST /api/teams/` - создать команду
3. `GET /api/teams/{id}/` - детали команды
4. `PUT/PATCH /api/teams/{id}/` - обновить команду
5. `DELETE /api/teams/{id}/` - удалить команду
6. `POST /api/teams/{id}/members/` - добавить участника
7. `DELETE /api/teams/{id}/members/{user_id}/` - удалить участника

**Custom Permissions:**
- `IsTeamOwner` - только owner может редактировать/удалять
- `IsTeamMember` - только members могут просматривать

**Фильтрация:**
- По `owner` (мои команды)
- По `members` (команды где я участник)

---

## 📢 Участник 3: CHANNEL Model

### Файл: `apps/channels/models.py`

```python
class Channel(models.Model):
    # ПОЛЯ
    name               # CharField, max_length=200
    description        # TextField, blank=True, null=True
    is_private         # BooleanField, default=False
    created_at         # DateTimeField, auto_now_add=True
    updated_at         # DateTimeField, auto_now=True
    
    # СВЯЗИ
    team               # ForeignKey → Team
                       # on_delete=models.CASCADE
                       # related_name='channels'
    
    members            # ManyToManyField → User
                       # through='ChannelMembership'
                       # related_name='private_channels'
                       # blank=True (только для приватных)
```

```python
class ChannelMembership(models.Model):
    # ПОЛЯ
    joined_at          # DateTimeField, auto_now_add=True
    
    # СВЯЗИ
    channel            # ForeignKey → Channel, on_delete=CASCADE
    user               # ForeignKey → User, on_delete=CASCADE
    
    # META
    unique_together = ['channel', 'user']
```

**Endpoints (5 штук):**
1. `GET /api/channels/?team_id={id}` - список каналов
2. `POST /api/channels/` - создать канал
3. `GET /api/channels/{id}/` - детали канала
4. `PUT/PATCH /api/channels/{id}/` - обновить канал
5. `DELETE /api/channels/{id}/` - удалить канал

**Логика приватности:**
- Если `is_private = False`: все участники team видят канал
- Если `is_private = True`: только users в members видят канал

**Custom Permissions:**
- `IsTeamMember` - только участники team могут видеть каналы
- `IsChannelMember` - только members приватного канала могут видеть

**Фильтрация:**
- По `team_id` (обязательно!)
- По `is_private`

---

## 💬 Участник 4: MESSAGE Model

### Файл: `apps/messages/models.py`

```python
class Message(models.Model):
    # ПОЛЯ
    content            # TextField
    created_at         # DateTimeField, auto_now_add=True
    updated_at         # DateTimeField, auto_now=True
    
    # СВЯЗИ
    author             # ForeignKey → User
                       # on_delete=models.CASCADE
                       # related_name='messages'
    
    channel            # ForeignKey → Channel
                       # on_delete=models.CASCADE
                       # related_name='messages'
    
    parent_message     # ForeignKey → self (Message)
                       # on_delete=models.CASCADE
                       # null=True, blank=True
                       # related_name='replies'
```

**Endpoints (5 штук):**
1. `GET /api/messages/?channel_id={id}` - список сообщений
2. `POST /api/messages/` - создать сообщение
3. `GET /api/messages/{id}/` - детали сообщения
4. `PUT/PATCH /api/messages/{id}/` - обновить сообщение
5. `DELETE /api/messages/{id}/` - удалить сообщение

**Логика тредов:**
- Если `parent_message = null` → основное сообщение
- Если `parent_message = ID` → это ответ/thread

**Custom Permissions:**
- `IsAuthorOrReadOnly` - только автор может редактировать/удалять

**Фильтрация:**
- По `channel_id` (обязательно!)
- По `author`
- По `parent_message` (для получения тредов)

---

## 📊 Связи между моделями (ВАЖНО!)

```
User (1) ──owns──> (N) Team
User (M) ←─member─→ (N) Team          via TeamMembership

Team (1) ──has──> (N) Channel

User (M) ←─member─→ (N) Channel       via ChannelMembership (private only)

User (1) ──writes──> (N) Message
Channel (1) ──contains──> (N) Message

Message (1) ──replies──> (N) Message  (self-reference)
```

---

## ⚙️ Meta classes (добавьте во все модели)

```python
class Meta:
    # Ordering
    ordering = ['-created_at']  # или ['name'] для Channel
    
    # Indexes для производительности
    indexes = [
        models.Index(fields=['owner']),           # Team
        models.Index(fields=['team']),            # Channel
        models.Index(fields=['channel', '-created_at']),  # Message
    ]
    
    # Unique constraints
    unique_together = ['team', 'name']  # Channel: уникальное имя в team
```

---

## 🎯 Обязательные методы в моделях

```python
def __str__(self):
    return self.name  # или self.email для User
```

---

## 📋 Admin Registration (для ВСЕХ моделей)

```python
# apps/users/admin.py
from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_active']
    search_fields = ['email', 'first_name', 'last_name']
    list_filter = ['is_active', 'is_staff']
```

---

## ⚠️ Порядок создания (ВАЖНО!)

**1. Сначала:** User Model (Участник 1)
**2. Потом:** Team Model (Участник 2) - зависит от User
**3. Затем:** Channel Model (Участник 3) - зависит от Team
**4. Наконец:** Message Model (Участник 4) - зависит от Channel и User

---

## 🔧 Миграции

```bash
# После создания/изменения моделей:
python manage.py makemigrations
python manage.py migrate

# Проверка миграций:
python manage.py showmigrations

# Откат последней миграции:
python manage.py migrate app_name previous_migration_name
```

---

## ✅ Чеклист перед созданием Pull Request

**Модели:**
- [ ] Все поля определены с правильными типами
- [ ] related_name указаны и уникальны
- [ ] on_delete указан для всех ForeignKey
- [ ] Meta class с ordering и indexes
- [ ] `__str__()` метод определен
- [ ] Миграции созданы и применены

**Admin:**
- [ ] Модели зарегистрированы в admin.py
- [ ] list_display настроен
- [ ] search_fields и list_filter добавлены

**Serializers:**
- [ ] Созданы для всех моделей
- [ ] Указаны нужные fields
- [ ] Валидация добавлена где нужно

**Views:**
- [ ] ViewSet или APIView созданы
- [ ] Permissions настроены
- [ ] Queryset оптимизирован (select_related, prefetch_related)

**URLs:**
- [ ] Router зарегистрирован
- [ ] URLs подключены в settings/urls.py

**Documentation:**
- [ ] drf-spectacular @extend_schema добавлены
- [ ] Docstrings написаны

---

## 🚀 Полезные команды

```bash
# Django shell для тестирования
python manage.py shell

# Создать суперпользователя
python manage.py createsuperuser

# Запустить сервер
python manage.py runserver

# Проверить код на ошибки
python manage.py check
```

---

## 📞 Если застряли

1. Проверьте файл `ER_DIAGRAM_DETAILED.md` - там полные примеры кода
2. Посмотрите связи в `ER_DIAGRAM_DBML.txt`
3. Спросите в Telegram группе команды
4. Проверьте логи: `tail -f logs/django.log`

---

Держите эту шпаргалку под рукой! 📌
