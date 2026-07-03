# AI Collaboration Log

## AI Tools Used

- Cursor AI
- ChatGPT (GPT-5.5)

---

## Purpose

AI was used to accelerate development, generate boilerplate code, review implementation decisions, and improve the overall architecture while keeping the project aligned with the assignment requirements.

---

## Example Prompts

### Backend

```
Build and modify my existing uptime monitor backend.

Requirements:

- FastAPI
- SQLAlchemy
- PostgreSQL
- APScheduler
- Use FastAPI lifespan for scheduler startup/shutdown
- Validate URLs using Pydantic HttpUrl
- Prevent duplicate URLs
- Keep the existing project structure.
```

---

### Frontend

```
Generate a React frontend using Vite.

Requirements:

- Table showing monitored URLs
- URL input
- Add button
- Status badges
- Auto refresh every 5 seconds
- Axios for API calls
```

---

### Docker

```
Generate Dockerfiles and docker-compose.yml so the frontend, backend and PostgreSQL start using a single docker compose up command.
```

---

## AI Contributions

AI assisted with:

- FastAPI project structure
- SQLAlchemy models
- React UI generation
- Docker configuration
- Nginx reverse proxy configuration
- API integration
- Documentation suggestions

---

## Course Corrections

During development, AI suggested adding additional features such as:

- Alembic migrations
- URL history tracking
- Delete endpoint

After reviewing the assignment requirements, these suggestions were intentionally not implemented because the assignment explicitly requested a strict MVP. The implementation was kept focused on the required functionality.

Another improvement involved moving the APScheduler startup into FastAPI's lifespan event instead of starting it during module import, resulting in cleaner application lifecycle management.

---

## Verification

The completed application was verified by:

- Running the entire stack using Docker Compose.
- Adding a working URL (`https://example.com`) and confirming it reported an UP status.
- Adding an unreachable URL and confirming it reported a DOWN status after the scheduler executed.
- Confirming automatic UI refresh and backend API functionality through Swagger documentation.