# Задачи для Corporoom - Teams Clone Project

## Epic 1: Project Setup & Infrastructure
**Ответственный:** Участник 1 (Team Lead)

### Sprint 1 - Week 7

#### Task 1.1: Настройка проекта и Git
**Статус:** In Progress
**Приоритет:** High
**Subtasks:**
- [ ] Создать Git репозиторий
- [ ] Создать branch: teams-clone-project
- [ ] Настроить .gitignore
- [ ] Создать структуру проекта
- [ ] Запушить начальный коммит

**Screen Recording:** Прикрепить видео настройки Git и создания структуры

---

## Epic 2: Authentication & Users
**Ответственный:** Участник 1 (Team Lead)

### Sprint 1 - Week 7

#### Task 2.1: Custom User Model
**Статус:** To Do
**Приоритет:** High
**Subtasks:**
- [ ] Backend: Создать apps/users/ приложение
- [ ] Backend: Создать Custom User Model (email как main field)
- [ ] Backend: Создать UserManager
- [ ] Backend: Настроить AUTH_USER_MODEL в settings
- [ ] Backend: Создать и применить миграции

**Screen Recording:** Прикрепить видео создания модели и миграций

#### Task 2.2: User Serializers
**Статус:** To Do
**Приоритет:** High
**Subtasks:**
- [ ] Backend: Создать UserSerializer
- [ ] Backend: Создать UserRegistrationSerializer
- [ ] Backend: Создать UserLoginSerializer
- [ ] Backend: Добавить валидацию полей

**Screen Recording:** Прикрепить видео создания serializers

#### Task 2.3: JWT Authentication Endpoints
**Статус:** To Do
**Приоритет:** High
**Subtasks:**
- [ ] Backend: POST /api/auth/register/ - регистрация
- [ ] Backend: POST /api/auth/login/ - вход
- [ ] Backend: POST /api/auth/refresh/ - обновление токена
- [ ] Backend: POST /api/auth/logout/ - выход
- [ ] Backend: GET /api/auth/me/ - текущий пользователь

**Screen Recording:** Прикрепить видео тестирования endpoints в Postman/Thunder Client

#### Task 2.4: Permissions & Admin
**Статус:** To Do
**Приоритет:** Medium
**Subtasks:**
- [ ] Backend: Настроить custom permissions
- [ ] Backend: Зарегистрировать User в admin panel
- [ ] Backend: Создать тестовых пользователей

**Screen Recording:** Прикрепить видео работы с admin panel

#### Task 2.5: Documentation
**Статус:** To Do
**Приоритет:** Medium
**Subtasks:**
- [ ] Backend: Настроить drf-spectacular для всех endpoints
- [ ] Backend: Добавить docstrings
- [ ] Backend: Проверить документацию в Swagger

**Screen Recording:** Прикрепить видео Swagger документации

---

## Epic 3: Teams/Workspaces
**Ответственный:** Участник 2

### Sprint 1 - Week 7

#### Task 3.1: Team Model
**Статус:** To Do
**Приоритет:** High
**Subtasks:**
- [ ] Backend: Создать apps/teams/ приложение
- [ ] Backend: Создать Team Model (name, description, owner, members)
- [ ] Backend: Создать и применить миграции

**Screen Recording:** Прикрепить видео создания модели

#### Task 3.2: Team Serializers
**Статус:** To Do
**Приоритет:** High
**Subtasks:**
- [ ] Backend: Создать TeamSerializer
- [ ] Backend: Создать TeamCreateSerializer
- [ ] Backend: Добавить вложенный UserSerializer для members

**Screen Recording:** Прикрепить видео создания serializers

#### Task 3.3: Team CRUD Endpoints
**Статус:** To Do
**Приоритет:** High
**Subtasks:**
- [ ] Backend: GET /api/teams/ - список команд
- [ ] Backend: POST /api/teams/ - создание команды
- [ ] Backend: GET /api/teams/{id}/ - детали команды
- [ ] Backend: PUT/PATCH /api/teams/{id}/ - обновление команды
- [ ] Backend: DELETE /api/teams/{id}/ - удаление команды

**Screen Recording:** Прикрепить видео тестирования CRUD операций

#### Task 3.4: Team Members Management
**Статус:** To Do
**Приоритет:** High
**Subtasks:**
- [ ] Backend: POST /api/teams/{id}/members/ - добавить участника
- [ ] Backend: DELETE /api/teams/{id}/members/{user_id}/ - удалить участника

**Screen Recording:** Прикрепить видео управления участниками

#### Task 3.5: Permissions & Filtering
**Статус:** To Do
**Приоритет:** Medium
**Subtasks:**
- [ ] Backend: Создать IsTeamOwner permission
- [ ] Backend: Создать IsTeamMember permission
- [ ] Backend: Добавить фильтрацию по owner, members
- [ ] Backend: Настроить admin panel

**Screen Recording:** Прикрепить видео работы permissions и фильтров

#### Task 3.6: Documentation
**Статус:** To Do
**Приоритет:** Medium
**Subtasks:**
- [ ] Backend: Настроить drf-spectacular
- [ ] Backend: Добавить docstrings
- [ ] Backend: Проверить в Swagger

**Screen Recording:** Прикрепить видео документации

---

## Epic 4: Channels
**Ответственный:** Участник 3

### Sprint 1 - Week 7

#### Task 4.1: Channel Model
**Статус:** To Do
**Приоритет:** High
**Subtasks:**
- [ ] Backend: Создать apps/channels/ приложение
- [ ] Backend: Создать Channel Model (name, team, is_private, members)
- [ ] Backend: Создать и применить миграции

**Screen Recording:** Прикрепить видео создания модели

#### Task 4.2: Channel Serializers
**Статус:** To Do
**Приоритет:** High
**Subtasks:**
- [ ] Backend: Создать ChannelSerializer
- [ ] Backend: Создать ChannelCreateSerializer
- [ ] Backend: Добавить вложенные serializers

**Screen Recording:** Прикрепить видео создания serializers

#### Task 4.3: Channel CRUD Endpoints
**Статус:** To Do
**Приоритет:** High
**Subtasks:**
- [ ] Backend: GET /api/channels/ - список каналов
- [ ] Backend: POST /api/channels/ - создание канала
- [ ] Backend: GET /api/channels/{id}/ - детали канала
- [ ] Backend: PUT/PATCH /api/channels/{id}/ - обновление канала
- [ ] Backend: DELETE /api/channels/{id}/ - удаление канала

**Screen Recording:** Прикрепить видео тестирования CRUD

#### Task 4.4: Permissions & Filtering
**Статус:** To Do
**Приоритет:** Medium
**Subtasks:**
- [ ] Backend: Создать IsTeamMember permission для channels
- [ ] Backend: Добавить фильтрацию по team_id
- [ ] Backend: Настроить admin panel

**Screen Recording:** Прикрепить видео permissions и фильтров

#### Task 4.5: Documentation
**Статус:** To Do
**Приоритет:** Medium
**Subtasks:**
- [ ] Backend: Настроить drf-spectacular
- [ ] Backend: Добавить docstrings
- [ ] Backend: Проверить в Swagger

**Screen Recording:** Прикрепить видео документации

---

## Epic 5: Messages
**Ответственный:** Участник 4

### Sprint 1 - Week 7

#### Task 5.1: Message Model
**Статус:** To Do
**Приоритет:** High
**Subtasks:**
- [ ] Backend: Создать apps/messages/ приложение
- [ ] Backend: Создать Message Model (content, author, channel, parent_message)
- [ ] Backend: Создать и применить миграции

**Screen Recording:** Прикрепить видео создания модели

#### Task 5.2: Message Serializers
**Статус:** To Do
**Приоритет:** High
**Subtasks:**
- [ ] Backend: Создать MessageSerializer
- [ ] Backend: Создать MessageCreateSerializer
- [ ] Backend: Добавить вложенные serializers (author, channel)

**Screen Recording:** Прикрепить видео создания serializers

#### Task 5.3: Message CRUD Endpoints
**Статус:** To Do
**Приоритет:** High
**Subtasks:**
- [ ] Backend: GET /api/messages/ - список сообщений
- [ ] Backend: POST /api/messages/ - создание сообщения
- [ ] Backend: GET /api/messages/{id}/ - детали сообщения
- [ ] Backend: PUT/PATCH /api/messages/{id}/ - обновление сообщения
- [ ] Backend: DELETE /api/messages/{id}/ - удаление сообщения

**Screen Recording:** Прикрепить видео тестирования CRUD

#### Task 5.4: Permissions & Filtering
**Статус:** To Do
**Приоритет:** Medium
**Subtasks:**
- [ ] Backend: Создать IsAuthorOrReadOnly permission
- [ ] Backend: Добавить фильтрацию по channel_id
- [ ] Backend: Настроить admin panel

**Screen Recording:** Прикрепить видео permissions и фильтров

#### Task 5.5: Documentation
**Статус:** To Do
**Приоритет:** Medium
**Subtasks:**
- [ ] Backend: Настроить drf-spectacular
- [ ] Backend: Добавить docstrings
- [ ] Backend: Проверить в Swagger

**Screen Recording:** Прикрепить видео документации

---

## Epic 6: Final Integration & Testing
**Ответственные:** Вся команда

### Sprint 1 - Week 7

#### Task 6.1: ER Diagram
**Статус:** To Do
**Приоритет:** High
**Ответственный:** Участник 1
**Subtasks:**
- [ ] Создать ER диаграмму всех моделей
- [ ] Показать связи между моделями
- [ ] Добавить в документацию

**Screen Recording:** Прикрепить скриншот диаграммы

#### Task 6.2: Database Seeding
**Статус:** To Do
**Приоритет:** High
**Ответственный:** Вся команда
**Subtasks:**
- [ ] Создать management command для заполнения БД
- [ ] Добавить тестовых пользователей (10-20)
- [ ] Добавить тестовые команды (5-10)
- [ ] Добавить тестовые каналы (10-15)
- [ ] Добавить тестовые сообщения (50-100)

**Screen Recording:** Прикрепить видео заполнения БД

#### Task 6.3: Integration Testing
**Статус:** To Do
**Приоритет:** High
**Ответственный:** Вся команда
**Subtasks:**
- [ ] Протестировать все endpoints
- [ ] Проверить работу permissions
- [ ] Проверить фильтрацию
- [ ] Проверить JWT авторизацию

**Screen Recording:** Прикрепить видео полного тестирования

#### Task 6.4: Final Documentation Review
**Статус:** To Do
**Приоритет:** Medium
**Ответственный:** Участник 1
**Subtasks:**
- [ ] Проверить Swagger документацию
- [ ] Обновить README
- [ ] Подготовить презентацию для защиты

**Screen Recording:** Прикрепить видео Swagger UI

---

## Дедлайны

- **Week 7 (Practice + Lectures):** Все задачи должны быть завершены
- **Defense:** Week 7-8

## Важные замечания

1. Каждый участник работает в своей ветке (feature/...)
2. Все изменения только через Pull Requests
3. Обязательно прикреплять screen recordings к каждой задаче
4. Минимум 10 endpoints в проекте (у нас будет 22+)
5. База данных должна быть заполнена тестовыми данными
