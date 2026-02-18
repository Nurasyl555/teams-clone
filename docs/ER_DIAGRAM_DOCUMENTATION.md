# Teams Clone - ER Diagram Documentation

## 📊 Database Models Overview

### 1️⃣ User (apps/users/)
**Main authentication model - email-based**

```python
class User(AbstractBaseUser, PermissionsMixin):
    # Primary fields
    id = BigAutoField (PK)
    email = EmailField (UNIQUE, required)
    password = CharField (hashed)
    first_name = CharField (max_length=50)
    last_name = CharField (max_length=50)
    phone = CharField (max_length=20, unique=True, blank=True, null=True)
    
    # Status fields
    is_active = BooleanField (default=True)
    is_staff = BooleanField (default=False)
    is_superuser = BooleanField (default=False)
    
    # Timestamps
    date_joined = DateTimeField (auto_now_add=True)
    last_login = DateTimeField (null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
```

**Relationships:**
- owns many Teams (ForeignKey from Team.owner)
- creates many Channels (ForeignKey from Channel.created_by)
- member of many Teams (through TeamMember)
- member of many Channels (through ChannelMember)
- sends many Messages (ForeignKey from Message.sender)

---

### 2️⃣ Team (apps/teams/)
**Workspace/organization container**

```python
class Team(models.Model):
    id = BigAutoField (PK)
    name = CharField (max_length=100, required)
    description = TextField (blank=True)
    owner = ForeignKey (User, on_delete=CASCADE, related_name='owned_teams')
    created_at = DateTimeField (auto_now_add=True)
    updated_at = DateTimeField (auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
```

**Relationships:**
- belongs to 1 User (owner) — ForeignKey to User
- has many Channels — reverse FK from Channel.team
- has many members through TeamMember

---

### 3️⃣ TeamMember (apps/teams/)
**Many-to-Many relationship between Team and User with extra fields**

```python
class TeamMember(models.Model):
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('admin', 'Admin'),
        ('member', 'Member'),
    ]
    
    id = BigAutoField (PK)
    team = ForeignKey (Team, on_delete=CASCADE, related_name='members')
    user = ForeignKey (User, on_delete=CASCADE, related_name='team_memberships')
    role = CharField (max_length=20, choices=ROLE_CHOICES, default='member')
    joined_at = DateTimeField (auto_now_add=True)
    
    class Meta:
        unique_together = ('team', 'user')
        ordering = ['joined_at']
```

**Relationships:**
- belongs to 1 Team — ForeignKey to Team
- belongs to 1 User — ForeignKey to User

---

### 4️⃣ Channel (apps/channels/)
**Communication channels within a team (like #general, #random)**

```python
class Channel(models.Model):
    id = BigAutoField (PK)
    name = CharField (max_length=100, required)
    description = TextField (blank=True)
    team = ForeignKey (Team, on_delete=CASCADE, related_name='channels')
    is_private = BooleanField (default=False)
    created_by = ForeignKey (User, on_delete=SET_NULL, null=True, related_name='created_channels')
    created_at = DateTimeField (auto_now_add=True)
    updated_at = DateTimeField (auto_now=True)
    
    class Meta:
        ordering = ['name']
        unique_together = ('team', 'name')
```

**Relationships:**
- belongs to 1 Team — ForeignKey to Team
- created by 1 User — ForeignKey to User
- has many members through ChannelMember
- contains many Messages — reverse FK from Message.channel

---

### 5️⃣ ChannelMember (apps/channels/)
**Many-to-Many relationship between Channel and User**

```python
class ChannelMember(models.Model):
    id = BigAutoField (PK)
    channel = ForeignKey (Channel, on_delete=CASCADE, related_name='memberships')
    user = ForeignKey (User, on_delete=CASCADE, related_name='channel_memberships')
    joined_at = DateTimeField (auto_now_add=True)
    
    class Meta:
        unique_together = ('channel', 'user')
        ordering = ['joined_at']
```

**Relationships:**
- belongs to 1 Channel — ForeignKey to Channel
- belongs to 1 User — ForeignKey to User

---

### 6️⃣ Message (apps/messages/)
**Messages sent in channels**

```python
class Message(models.Model):
    id = BigAutoField (PK)
    content = TextField (required)
    channel = ForeignKey (Channel, on_delete=CASCADE, related_name='messages')
    sender = ForeignKey (User, on_delete=CASCADE, related_name='sent_messages')
    is_edited = BooleanField (default=False)
    created_at = DateTimeField (auto_now_add=True)
    updated_at = DateTimeField (auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
```

**Relationships:**
- belongs to 1 Channel — ForeignKey to Channel
- belongs to 1 User (sender) — ForeignKey to User

---

## 🔗 Relationship Summary

```
User (1) ←→ (N) TeamMember ←→ (N) Team (1)
     ↓                              ↓
     owner                     contains
     ↓                              ↓
Team (1) ←───────────────────→ Channel (N)
                                   ↓
Channel (1) ←→ (N) ChannelMember ←→ User (N)
     ↓
     contains
     ↓
Message (N) ──→ sender: User (1)
```

**Key Points:**
1. **User** can own multiple Teams
2. **User** can be member of multiple Teams (through TeamMember)
3. **Team** contains multiple Channels
4. **Channel** belongs to one Team
5. **User** can join multiple Channels (through ChannelMember)
6. **Message** belongs to one Channel and one User (sender)

---

## 🛡️ Important Constraints

1. **User.email** — UNIQUE (used for authentication)
2. **Team + User** — unique pair in TeamMember
3. **Channel + User** — unique pair in ChannelMember
4. **Team + Channel.name** — unique pair (no duplicate channel names in same team)

---

## 🎯 How to Use This Diagram

### For Mermaid visualization:
1. Go to https://mermaid.live
2. Paste the content from `teams_clone_er_diagram.mermaid`
3. Export as PNG/SVG

### For other tools:
- Draw.io: Import as entity relationship diagram
- Lucidchart: Create diagram from text description
- dbdiagram.io: Convert to DBML format

---

## ✅ Data Flow Examples

### Example 1: Creating a new team
1. User creates Team (becomes owner)
2. TeamMember record created automatically (role='owner')
3. Default "General" Channel created in the Team

### Example 2: Sending a message
1. User must be ChannelMember of the Channel
2. Message created with sender=User, channel=Channel
3. Message appears in Channel's message list

### Example 3: Adding user to team
1. TeamMember record created (team, user, role)
2. User can now see team's public Channels
3. User needs to explicitly join Channels (ChannelMember)
