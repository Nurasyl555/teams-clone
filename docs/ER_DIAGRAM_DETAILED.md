# 📊 ER Diagram - Teams Clone Database

## 🎯 Краткое описание

**Проект:** Teams Clone (клон Microsoft Teams)  
**Количество моделей:** 4 основных + 2 связующих (Many-to-Many)  
**Всего таблиц в БД:** 6

---

## 📋 Модели и их поля

### 1️⃣ User (Custom User Model)
**Приложение:** `apps/users/`  
**Таблица:** `users`  
**Ответственный:** Участник 1

```python
class User(AbstractBaseUser, PermissionsMixin):
    # Основные поля
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)  # ⚠️ MAIN LOGIN FIELD
    password = models.CharField(max_length=128)  # Hashed
    
    # Профиль
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    
    # Статус
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    # Временные метки
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
```

**Связи:**
- `1:N` → Team (как owner)
- `M:N` → Team (как member через TeamMembership)
- `M:N` → Channel (как member через ChannelMembership для приватных каналов)
- `1:N` → Message (как author)

---

### 2️⃣ Team (Команда/Workspace)
**Приложение:** `apps/teams/`  
**Таблица:** `teams`  
**Ответственный:** Участник 2

```python
class Team(models.Model):
    # Основные поля
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    
    # Связи
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_teams'
    )
    members = models.ManyToManyField(
        User,
        through='TeamMembership',
        related_name='teams'
    )
    
    # Временные метки
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['owner']),
            models.Index(fields=['-created_at']),
        ]
```

**Связи:**
- `N:1` → User (owner - кто создал команду)
- `M:N` → User (members - участники команды)
- `1:N` → Channel (команда имеет много каналов)

---

### 2.1️⃣ TeamMembership (Связующая таблица)
**Приложение:** `apps/teams/`  
**Таблица:** `team_members`  
**Ответственный:** Участник 2

```python
class TeamMembership(models.Model):
    # Основные поля
    id = models.AutoField(primary_key=True)
    
    # Связи
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Дополнительные поля
    joined_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(
        max_length=50,
        default='member',
        choices=[
            ('member', 'Member'),
            ('admin', 'Admin'),
        ]
    )
    
    class Meta:
        unique_together = ['team', 'user']
        indexes = [
            models.Index(fields=['team', 'user']),
        ]
```

---

### 3️⃣ Channel (Канал внутри команды)
**Приложение:** `apps/channels/`  
**Таблица:** `channels`  
**Ответственный:** Участник 3

```python
class Channel(models.Model):
    # Основные поля
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    
    # Связи
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='channels'
    )
    
    # Приватность
    is_private = models.BooleanField(default=False)
    members = models.ManyToManyField(
        User,
        through='ChannelMembership',
        related_name='private_channels',
        blank=True
    )
    
    # Временные метки
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['team']),
            models.Index(fields=['is_private']),
        ]
        unique_together = ['team', 'name']
```

**Связи:**
- `N:1` → Team (канал принадлежит одной команде)
- `M:N` → User (members - только для приватных каналов)
- `1:N` → Message (канал содержит много сообщений)

**Логика:**
- Если `is_private = False` → все участники команды видят канал
- Если `is_private = True` → только users в `members` видят канал

---

### 3.1️⃣ ChannelMembership (Связующая таблица)
**Приложение:** `apps/channels/`  
**Таблица:** `channel_members`  
**Ответственный:** Участник 3

```python
class ChannelMembership(models.Model):
    # Основные поля
    id = models.AutoField(primary_key=True)
    
    # Связи
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Дополнительные поля
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['channel', 'user']
        indexes = [
            models.Index(fields=['channel', 'user']),
        ]
```

**Примечание:** Используется только для приватных каналов

---

### 4️⃣ Message (Сообщение в канале)
**Приложение:** `apps/messages/`  
**Таблица:** `messages`  
**Ответственный:** Участник 4

```python
class Message(models.Model):
    # Основные поля
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    
    # Связи
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    
    # Для реализации тредов/ответов
    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    
    # Временные метки
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['channel', '-created_at']),
            models.Index(fields=['author']),
            models.Index(fields=['parent_message']),
        ]
```

**Связи:**
- `N:1` → User (author - кто написал сообщение)
- `N:1` → Channel (в каком канале сообщение)
- `N:1` → Message (parent_message - для ответов/тредов)

**Логика тредов:**
- Если `parent_message = None` → это основное сообщение
- Если `parent_message = ID` → это ответ на сообщение

---

## 🔗 Визуализация связей

```
┌─────────────┐
│    USER     │
└─────────────┘
      │
      ├─── owns (1:N) ──────────────┐
      │                             │
      ├─── member_of (M:N) ─────┐   │
      │                         │   │
      ├─── writes (1:N) ───┐    │   │
      │                    │    │   │
      ▼                    │    │   ▼
┌─────────────┐            │    │ ┌─────────────┐
│   CHANNEL   │            │    └─│    TEAM     │
└─────────────┘            │      └─────────────┘
      │                    │            │
      ├─── contains (1:N) ─┼────────────┘ contains (1:N)
      │                    │
      ▼                    ▼
┌─────────────┐      ┌─────────────┐
│   MESSAGE   │◄────┤   MESSAGE   │ (self-reference)
└─────────────┘      └─────────────┘
                     parent_message
```

---

## 📊 Таблица связей

| От | Связь | К | Тип | Описание |
|---|---|---|---|---|
| User | owner | Team | 1:N | Один user может владеть многими teams |
| User | member | Team | M:N | User может быть в нескольких teams |
| Team | channels | Channel | 1:N | Team имеет много channels |
| User | member | Channel | M:N | User может быть в приватных channels |
| Channel | messages | Message | 1:N | Channel содержит много messages |
| User | author | Message | 1:N | User пишет много messages |
| Message | replies | Message | 1:N | Message может иметь ответы |

---

## 🎯 Для каждого участника команды

### Участник 1 - User Model
**Что создать:**
```python
# apps/users/models.py
- User (с email как USERNAME_FIELD)
- UserManager (для создания users)

# Не нужны дополнительные таблицы связи на этом этапе
```

### Участник 2 - Team Model
**Что создать:**
```python
# apps/teams/models.py
- Team
- TeamMembership (через through parameter)

# Связи:
- team.owner → User (ForeignKey)
- team.members → User (ManyToMany через TeamMembership)
```

### Участник 3 - Channel Model
**Что создать:**
```python
# apps/channels/models.py
- Channel
- ChannelMembership (через through parameter)

# Связи:
- channel.team → Team (ForeignKey)
- channel.members → User (ManyToMany через ChannelMembership)
```

### Участник 4 - Message Model
**Что создать:**
```python
# apps/messages/models.py
- Message

# Связи:
- message.author → User (ForeignKey)
- message.channel → Channel (ForeignKey)
- message.parent_message → Message (ForeignKey to self)
```

---

## ⚠️ Важные моменты для избежания конфликтов

### 1. related_name
Используйте уникальные `related_name` для избежания конфликтов:

```python
# ✅ ПРАВИЛЬНО
owner = models.ForeignKey(User, related_name='owned_teams')
members = models.ManyToManyField(User, related_name='teams')

# ❌ НЕПРАВИЛЬНО (конфликт)
owner = models.ForeignKey(User, related_name='teams')
members = models.ManyToManyField(User, related_name='teams')
```

### 2. on_delete behavior
```python
# User удаляется → что происходит с Team?
owner = models.ForeignKey(User, on_delete=models.CASCADE)  # Team удаляется
# или
owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # owner → NULL

# Рекомендуется: CASCADE для всех связей
```

### 3. Порядок миграций
```
1. User (apps/users) - первым!
2. Team (apps/teams) - зависит от User
3. Channel (apps/channels) - зависит от Team
4. Message (apps/messages) - зависит от Channel и User
```

### 4. Индексы
Добавляйте индексы на часто используемые поля:
```python
class Meta:
    indexes = [
        models.Index(fields=['team']),
        models.Index(fields=['-created_at']),
    ]
```

---

## 🛠️ Инструменты для визуализации

1. **dbdiagram.io** - используйте файл `ER_DIAGRAM_DBML.txt`
2. **mermaid.live** - используйте файл `ER_DIAGRAM_MERMAID.md`
3. **Django Extensions:**
   ```bash
   pip install django-extensions pyparsing pydot
   python manage.py graph_models -a -o er_diagram.png
   ```

---

## ✅ Чеклист для каждой модели

- [ ] Все поля определены
- [ ] related_name уникальны
- [ ] on_delete указан для всех ForeignKey
- [ ] Добавлены Meta indexes
- [ ] created_at / updated_at (где нужно)
- [ ] `__str__()` метод определен
- [ ] Модель зарегистрирована в admin.py

---

Эта диаграмма поможет всей команде работать без конфликтов! 🚀
