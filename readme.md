# Address Book API

This is a minimal Address Book application built with **FastAPI** and **SQLite**.

The API allows users to:
- Create, update, and delete addresses
- Store address coordinates (latitude & longitude)
- Validate address data
- Retrieve addresses within a given distance from a location

FastAPI’s built-in Swagger UI is used for API documentation and testing.

---

## Project Structure

```text
app/
├── api/
│   └── address.py        # API routes
├── database/
│   └── db.py             # Database connection and session
├── model/
│   ├── models.py         # SQLAlchemy models
│   └── schema.py         # Pydantic schemas
├── utils/
│   └── nearby_address.py # Distance calculation logic
├── main.py               # Application entry point
├── readme.md
└── requirements.txt
