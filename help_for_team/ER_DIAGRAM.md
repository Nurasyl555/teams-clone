# ER Diagram - Teams Clone Project

## Database Structure

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           TEAMS CLONE DATABASE                           │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────────┐
│       User           │
├──────────────────────┤
│ id (PK)              │
│ email (UNIQUE)       │
│ password             │
│ first_name           │
│ last_name            │
│ is_active            │
│ is_staff             │
│ is_superuser         │
│ date_joined          │
│ last_login           │
└──────────────────────┘
         │
         │ 1:N (owner)
         ├─────────────────┐
         │                 │
         ▼                 │
┌──────────────────────┐   │
│       Team           │   │
├──────────────────────┤   │
│ id (PK)              │   │
│ name                 │   │
│ description          │   │
│ owner (FK → User)    │◄──┘
│ created_at           │
│ updated_at           │
└──────────────────────┘
         │
         │ N:M (members)
         ├──────────────────┐
         │                  │
         │                  ▼
         │         ┌──────────────────────┐
         │         │   TeamMembership     │ (Through table)
         │         ├──────────────────────┤
         │         │ team (FK → Team)     │
         │         │ user (FK → User)     │
         │         │ joined_at            │
         │         └──────────────────────┘
         │
         │ 1:N (channels)
         ├─────────────────┐
         │                 │
         ▼                 │
┌──────────────────────┐   │
│      Channel         │   │
├──────────────────────┤   │
│ id (PK)              │   │
│ name                 │   │
│ description          │   │
│ team (FK → Team)     │◄──┘
│ is_private           │
│ created_at           │
│ updated_at           │
└──────────────────────┘
         │
         │ N:M (members, for private channels)
         ├──────────────────┐
         │                  │
         │                  ▼
         │         ┌──────────────────────────┐
         │         │  ChannelMembership       │ (Through table)
         │         ├──────────────────────────┤
         │         │ channel (FK → Channel)   │
         │         │ user (FK → User)         │
         │         │ joined_at                │
         │         └──────────────────────────┘
         │
         │ 1:N (messages)
         ├─────────────────┐
         │                 │
         ▼                 │
┌──────────────────────┐   │
│      Message         │   │
├──────────────────────┤   │
│ id (PK)              │   │
│ content              │   │
│ author (FK → User)   │◄──┼─────┐ 1:N (author)
│ channel (FK → Chan.) │◄──┘     │
│ parent_message       │◄────────┘ Self-referencing
│   (FK → Message)     │           (for threads/replies)
│ created_at           │
│ updated_at           │
└──────────────────────┘


## Relationships Summary

1. **User ←→ Team**
   - One-to-Many: User (owner) can own multiple Teams
   - Many-to-Many: User can be member of multiple Teams

2. **Team ←→ Channel**
   - One-to-Many: Team has multiple Channels
   - One Channel belongs to one Team

3. **User ←→ Channel**
   - Many-to-Many: User can be member of multiple private Channels
   - Through: ChannelMembership table

4. **Channel ←→ Message**
   - One-to-Many: Channel has multiple Messages
   - One Message belongs to one Channel

5. **User ←→ Message**
   - One-to-Many: User (author) can write multiple Messages
   - One Message has one author

6. **Message ←→ Message** (Self-referencing)
   - One-to-Many: Message can have multiple replies
   - Reply Message references parent Message

## Models Fields Details

### User Model
- **Primary Key:** id (AutoField)
- **Unique Field:** email (used for login instead of username)
- **Authentication:** password (hashed)
- **Profile:** first_name, last_name
- **Status:** is_active, is_staff, is_superuser
- **Timestamps:** date_joined, last_login

### Team Model
- **Primary Key:** id (AutoField)
- **Basic Info:** name, description
- **Owner:** ForeignKey to User (the creator)
- **Members:** ManyToManyField to User (team participants)
- **Timestamps:** created_at, updated_at

### Channel Model
- **Primary Key:** id (AutoField)
- **Basic Info:** name, description
- **Parent:** ForeignKey to Team
- **Privacy:** is_private (boolean)
- **Members:** ManyToManyField to User (for private channels only)
- **Timestamps:** created_at, updated_at

### Message Model
- **Primary Key:** id (AutoField)
- **Content:** content (TextField)
- **Author:** ForeignKey to User
- **Location:** ForeignKey to Channel
- **Threading:** parent_message (ForeignKey to self, nullable)
- **Timestamps:** created_at, updated_at

## Indexes (для оптимизации)

```python
# Suggested indexes for models:

# Team
class Meta:
    indexes = [
        models.Index(fields=['owner']),
        models.Index(fields=['-created_at']),
    ]

# Channel
class Meta:
    indexes = [
        models.Index(fields=['team']),
        models.Index(fields=['is_private']),
    ]

# Message
class Meta:
    indexes = [
        models.Index(fields=['channel', '-created_at']),
        models.Index(fields=['author']),
        models.Index(fields=['parent_message']),
    ]
```

## Constraints

1. **User.email** must be unique
2. **Team.owner** cannot be null
3. **Channel.team** cannot be null
4. **Message.author** cannot be null
5. **Message.channel** cannot be null

## Cascade Behaviors

- When **User** is deleted → Set owner to NULL or prevent deletion if they own teams
- When **Team** is deleted → Delete all Channels in that team
- When **Channel** is deleted → Delete all Messages in that channel
- When **User** (author) is deleted → Handle messages (keep with anonymous or delete)

## Visual Diagram Tools

Для создания визуальной диаграммы можно использовать:

1. **dbdiagram.io** - онлайн редактор
2. **draw.io** - для схем
3. **Django Extensions** - команда `graph_models`
   ```bash
   pip install django-extensions pyparsing pydot
   python manage.py graph_models -a -o er_diagram.png
   ```
4. **DBeaver** - если используете PostgreSQL
5. **Mermaid** - для Markdown диаграмм

## Пример для dbdiagram.io

```dbml
Table User {
  id int [pk, increment]
  email varchar [unique, not null]
  password varchar [not null]
  first_name varchar
  last_name varchar
  is_active boolean
  is_staff boolean
  is_superuser boolean
  date_joined datetime
  last_login datetime
}

Table Team {
  id int [pk, increment]
  name varchar [not null]
  description text
  owner_id int [ref: > User.id]
  created_at datetime
  updated_at datetime
}

Table TeamMembership {
  id int [pk, increment]
  team_id int [ref: > Team.id]
  user_id int [ref: > User.id]
  joined_at datetime
}

Table Channel {
  id int [pk, increment]
  name varchar [not null]
  description text
  team_id int [ref: > Team.id]
  is_private boolean
  created_at datetime
  updated_at datetime
}

Table ChannelMembership {
  id int [pk, increment]
  channel_id int [ref: > Channel.id]
  user_id int [ref: > User.id]
  joined_at datetime
}

Table Message {
  id int [pk, increment]
  content text [not null]
  author_id int [ref: > User.id]
  channel_id int [ref: > Channel.id]
  parent_message_id int [ref: > Message.id]
  created_at datetime
  updated_at datetime
}
```
