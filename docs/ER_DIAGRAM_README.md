# 🎨 ER Diagram Package - Teams Clone

## 📦 Что в этом пакете

Я создал для вас **полный набор документации** по структуре базы данных для проекта Teams Clone:

### 📄 Файлы для создания визуальной диаграммы

| Файл | Назначение | Использование |
|------|-----------|---------------|
| **ER_DIAGRAM_DBML.txt** | Код для dbdiagram.io | Скопировать → вставить на dbdiagram.io → получить красивую диаграмму |
| **ER_DIAGRAM_MERMAID.md** | Код для Mermaid | Использовать на mermaid.live или в GitHub/GitLab |

### 📚 Документация

| Файл | Содержание |
|------|-----------|
| **ER_DIAGRAM_DETAILED.md** | Полное описание всех моделей с примерами кода Python |
| **DATABASE_CHEAT_SHEET.md** | Краткая шпаргалка для каждого участника команды |
| **HOW_TO_CREATE_DIAGRAM.md** | Инструкции как создать визуальную диаграмму (5 способов) |

---

## 🚀 Быстрый старт

### Вариант 1: Создать визуальную диаграмму за 2 минуты

1. Откройте: https://dbdiagram.io/
2. Нажмите "Go to App"
3. Создайте "New Diagram"
4. **Удалите** весь текст слева
5. Откройте файл **ER_DIAGRAM_DBML.txt**
6. **Скопируйте всё** из файла
7. **Вставьте** в редактор dbdiagram.io
8. **БУМ!** 💥 Диаграмма готова!
9. Экспортируйте в PNG: Export → PNG

**Результат:** Красивая визуальная диаграмма для презентации

---

### Вариант 2: Для разработчиков

Откройте файл **DATABASE_CHEAT_SHEET.md** - там вся информация которая нужна для написания кода:
- Все поля для каждой модели
- Все связи (ForeignKey, ManyToMany)
- Примеры кода
- Чеклисты

**Результат:** Вся команда знает что писать

---

## 📊 Структура базы данных

```
4 основные модели + 2 связующие таблицы = 6 таблиц

┌─────────┐
│  USER   │ ─── Custom User Model (email login)
└─────────┘
     │
     ├──── owns ──────► TEAM
     ├──── member ─────► TEAM (M:N via TeamMembership)
     ├──── writes ─────► MESSAGE
     └──── member ─────► CHANNEL (M:N via ChannelMembership, private only)

TEAM ──── contains ──────► CHANNEL
CHANNEL ─ contains ──────► MESSAGE
MESSAGE ─ replies to ────► MESSAGE (self-reference)
```

---

## 👥 Распределение по участникам

### Участник 1 (Team Lead)
**Модель:** User  
**Файлы:** `apps/users/`  
**Что читать:** DATABASE_CHEAT_SHEET.md → раздел "Участник 1"

### Участник 2
**Модели:** Team, TeamMembership  
**Файлы:** `apps/teams/`  
**Что читать:** DATABASE_CHEAT_SHEET.md → раздел "Участник 2"

### Участник 3
**Модели:** Channel, ChannelMembership  
**Файлы:** `apps/channels/`  
**Что читать:** DATABASE_CHEAT_SHEET.md → раздел "Участник 3"

### Участник 4
**Модель:** Message  
**Файлы:** `apps/messages/`  
**Что читать:** DATABASE_CHEAT_SHEET.md → раздел "Участник 4"

---

## 🎯 Что каждый должен сделать

### 1. Прочитать свою часть
Откройте **DATABASE_CHEAT_SHEET.md** и найдите свой раздел

### 2. Понять связи
Посмотрите **ER_DIAGRAM_DETAILED.md** → раздел "Визуализация связей"

### 3. Создать визуальную диаграмму (для Team Lead)
Используйте **ER_DIAGRAM_DBML.txt** на dbdiagram.io

### 4. Начать писать код
Используя информацию из DATABASE_CHEAT_SHEET.md:
- Создайте модели
- Добавьте связи (ForeignKey, ManyToMany)
- Создайте миграции
- Зарегистрируйте в admin

---

## ⚠️ Важные правила для избежания конфликтов

### 1. Порядок создания моделей
```
1️⃣ User (Участник 1) - ПЕРВЫМ!
2️⃣ Team (Участник 2) - зависит от User
3️⃣ Channel (Участник 3) - зависит от Team
4️⃣ Message (Участник 4) - зависит от Channel и User
```

### 2. related_name должны быть уникальными
```python
# ✅ ПРАВИЛЬНО
owner = ForeignKey(User, related_name='owned_teams')
members = ManyToManyField(User, related_name='teams')

# ❌ НЕПРАВИЛЬНО (конфликт!)
owner = ForeignKey(User, related_name='teams')
members = ManyToManyField(User, related_name='teams')
```

### 3. Всегда указывайте on_delete
```python
# Для всех ForeignKey:
team = ForeignKey(Team, on_delete=models.CASCADE)
```

---

## 📋 Детальная информация по моделям

### User Model
```python
Основные поля:
- email (UNIQUE, USERNAME_FIELD)
- password
- first_name, last_name
- is_active, is_staff, is_superuser
- date_joined, last_login

Связи:
- owned_teams (1:N)
- teams (M:N via TeamMembership)
- private_channels (M:N via ChannelMembership)
- messages (1:N)
```

### Team Model
```python
Основные поля:
- name
- description
- created_at, updated_at

Связи:
- owner → User (ForeignKey)
- members ↔ User (ManyToMany via TeamMembership)
- channels (1:N)
```

### Channel Model
```python
Основные поля:
- name
- description
- is_private
- created_at, updated_at

Связи:
- team → Team (ForeignKey)
- members ↔ User (ManyToMany via ChannelMembership, if private)
- messages (1:N)
```

### Message Model
```python
Основные поля:
- content
- created_at, updated_at

Связи:
- author → User (ForeignKey)
- channel → Channel (ForeignKey)
- parent_message → Message (ForeignKey to self, nullable)
```

---

## 🛠️ Инструменты для визуализации

1. **dbdiagram.io** ⭐ - РЕКОМЕНДУЕТСЯ для презентации
2. **mermaid.live** - для документации
3. **Django Extensions** - автоматическая генерация из кода
4. **Draw.io** - ручное рисование
5. **ASCII** - простая текстовая диаграмма

**Инструкции:** См. файл **HOW_TO_CREATE_DIAGRAM.md**

---

## 📸 Пример результата (dbdiagram.io)

После вставки кода из ER_DIAGRAM_DBML.txt вы получите:

```
┌─────────────────┐         ┌─────────────────┐
│     users       │────────>│     teams       │
│  • id (PK)      │  owner  │  • id (PK)      │
│  • email (UK)   │         │  • name         │
│  • password     │         │  • owner_id FK  │
└─────────────────┘         └─────────────────┘
        │                            │
        │ M:N                        │ 1:N
        ▼                            ▼
┌──────────────────┐        ┌─────────────────┐
│  team_members    │        │    channels     │
│  • team_id FK    │        │  • id (PK)      │
│  • user_id FK    │        │  • team_id FK   │
└──────────────────┘        │  • is_private   │
                            └─────────────────┘
                                     │ 1:N
                                     ▼
                            ┌─────────────────┐
                            │    messages     │
                            │  • id (PK)      │
                            │  • channel_id FK│
                            │  • author_id FK │
                            │  • parent_msg FK│
                            └─────────────────┘
```

---

## ✅ Чеклист для команды

### Team Lead (Участник 1)
- [ ] Создать визуальную диаграмму на dbdiagram.io
- [ ] Экспортировать в PNG
- [ ] Поделиться диаграммой с командой
- [ ] Создать User Model

### Вся команда
- [ ] Прочитать DATABASE_CHEAT_SHEET.md (свой раздел)
- [ ] Понять связи между моделями
- [ ] Создать свои модели в правильном порядке
- [ ] Проверить related_name на уникальность
- [ ] Создать миграции
- [ ] Зарегистрировать в admin
- [ ] Протестировать связи

---

## 📞 Полезные ссылки

- **dbdiagram.io:** https://dbdiagram.io/
- **Mermaid Live:** https://mermaid.live/
- **Django Models Docs:** https://docs.djangoproject.com/en/5.0/topics/db/models/

---

## 🎓 Для защиты проекта

### Что показать преподавателю:

1. **Визуальную диаграмму** (из dbdiagram.io)
2. **Описание связей** (из ER_DIAGRAM_DETAILED.md)
3. **Реальные модели в коде**
4. **Работающий admin panel** с данными

### Что объяснить:

- Какие модели есть и зачем
- Какие связи между ними (1:N, M:N)
- Почему использовали related_name
- Зачем нужны through tables

---

## 💡 Советы

1. **Сначала создайте диаграмму** - это поможет всем понять структуру
2. **Держите DATABASE_CHEAT_SHEET.md открытым** - там вся нужная информация
3. **Создавайте модели по порядку** - User → Team → Channel → Message
4. **Проверяйте related_name** - они должны быть уникальными
5. **Тестируйте в admin panel** - добавьте тестовые данные

---

## 🎯 Итого

✅ У вас есть **3 формата** ER диаграммы (DBML, Mermaid, подробное описание)  
✅ У вас есть **подробная документация** для каждого участника  
✅ У вас есть **инструкции** как создать визуальную диаграмму  
✅ У вас есть **шпаргалка** с кодом для быстрого старта  

**Всё готово для начала работы! 🚀**

---

## ❓ Вопросы?

Если что-то непонятно:
1. Откройте **HOW_TO_CREATE_DIAGRAM.md** - там 5 разных способов
2. Откройте **ER_DIAGRAM_DETAILED.md** - там примеры кода
3. Откройте **DATABASE_CHEAT_SHEET.md** - там краткая информация
4. Спросите в Telegram группе команды

**Удачи с проектом! 🎉**
