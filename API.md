# API Documentation

Base URL: `https://your-app-url`

Authentication: Bearer token in `Authorization` header.

---

## Auth

### POST /auth/register

Register a new user.

**Request:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "secret123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response 201:**
```json
{
  "id": "64a...",
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "user"
}
```

---

### POST /auth/login

**Request:**
```json
{
  "username": "johndoe",
  "password": "secret123"
}
```

**Response 200:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

---

### GET /auth/me

🔒 Requires auth.

**Response 200:**
```json
{
  "id": "64a...",
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "profile_pic": "",
  "phone": "",
  "bio": "",
  "role": "user",
  "is_active": true
}
```

---

## Users

🔒 All endpoints require auth.

### GET /users/

List all users (max 100).

**Response 200:**
```json
[
  {
    "id": "64a...",
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "profile_pic": "",
    "phone": "",
    "bio": "",
    "role": "user",
    "is_active": true
  }
]
```

---

### GET /users/{id}

**Response 200:** Single user object.

---

### POST /users/

**Request:** Same as `/auth/register`.

---

### PUT /users/{id}

**Request:** Partial update (only include fields to change).
```json
{
  "bio": "Updated bio",
  "phone": "123-456-7890"
}
```

---

## Items

🔒 All endpoints require auth.

### GET /items/

List all items (max 100).

**Response 200:**
```json
[]
```
