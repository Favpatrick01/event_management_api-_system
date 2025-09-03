
# Event Management System API

A FastAPI-powered API for managing users, events, speakers, and event registrations.

## Features
- User registration and management
- Event creation, update, and deletion
- Register users for events and mark attendance
- Manage event speakers


## Usage
Run the development server:
```bash
uvicorn main:app --reload

---


## API Endpoints
## User Management

| Method   | Endpoint      | Description               |
| -------- | ------------- | ------------------------- |
| `GET`    | `/users`      | Get all users             |
| `GET`    | `/users/{id}` | Get a specific user by ID |
| `POST`   | `/users`      | Create a new user         |
| `PUT`    | `/users/{id}` | Update an existing user   |
| `PATCH`  | `/users/{id}` | Deactivate a user         |
| `DELETE` | `/users/{id}` | Delete a user             |

## Event Management 

| Method   | Endpoint                         | Description                                    |
| -------- | -------------------------------- | ---------------------------------------------- |
| `GET`    | `/events`                        | Get all events                                 |
| `POST`   | `/events?user_id={user_id}`      | Create a new event (only for registered users) |
| `PUT`    | `/events/{id}?user_id={user_id}` | Update event (only owner)                      |
| `PATCH`  | `/events/{id}?user_id={user_id}` | Close registration for an event (only owner)   |
| `DELETE` | `/events/{id}?user_id={user_id}` | Delete event (only owner)                      |


## Speaker Management

| Method   | Endpoint                                   | Description                     |
| -------- | ------------------------------------------ | ------------------------------- |
| `GET`    | `/speakers`                                | Get all speakers                |
| `GET`    | `/speakers/{name}`                         | Get speaker by name             |
| `POST`   | `/speakers?user_id={user_id}`              | Add a new speaker               |
| `PUT`    | `/speakers/{speaker_id}?user_id={user_id}` | Update a speaker (only creator) |
| `DELETE` | `/speakers/{speaker_id}?user_id={user_id}` | Delete a speaker (only creator) |


## Registration Management

| Method  | Endpoint                                    | Description                               |
| ------- | ------------------------------------------- | ----------------------------------------- |
| `POST`  | `/registrations/events/{event_id}/register` | Register a user for an event              |
| `PATCH` | `/registrations/{registration_id}/attend`   | Mark attendance for a registration        |
| `GET`   | `/registrations?user_id={user_id}`          | Get all registrations for a specific user |
| `GET`   | `/registrations`                            | Get all registrations in the system       |

## Project Structure

EMS/
├── database.py           # In-memory database
├── main.py               # FastAPI app entry point
├── routers/              # API route handlers
│   ├── event.py
│   ├── registration.py
│   ├── speaker.py
│   └── user.py
├── schemas/              # Pydantic models
│   ├── event.py
│   ├── registration.py
│   ├── speaker.py
│   └── user.py
├── services/             # Business logic layer
│   ├── event.py
│   ├── registration.py
│   ├── speaker.py
│   └── user.py
└── README.md             # Project documentation




