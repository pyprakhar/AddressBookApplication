# Address Book API

This is a minimal Address Book application built with **FastAPI** and **SQLite**.

The API allows users to:
- Create, update, and delete addresses
- Store address coordinates (latitude & longitude)
- Validate address data
- Retrieve addresses within a given distance from a location

FastAPI's built-in Swagger UI is used for API documentation and testing.

---

## Project Structure

```
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
├── crud/
│   └── address.py        # Database operations
├── main.py               # Application entry point
├── init_db.py            # Database initialization script
├── readme.md
└── requirements.txt
```

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd address_book_application
```

### 2. Create Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
```bash
# Copy the example .env file
cp .env.example .env
# The database URL is already configured in .env
```

### 5. Initialize the Database
```bash
python init_db.py
```
This will create the SQLite database file (`address_book.db`) and all necessary tables.

**Note:** The database is also automatically created when you start the application, but running this script ensures it exists before deployment.

### 6. Run the Application
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

Swagger UI documentation at `http://localhost:8000/docs`

---

## API Endpoints

### Create Address
`POST /addresses/`
```json
{
  "name": "JamesYard",
  "street": "123 Main St",
  "city": "New York",
  "state": "NY",
  "country": "USA",
  "latitude": 40.7128,
  "longitude": -74.0060
}
{
"name": "Office",
"street": "456 Park Ave",
"city": "New York",
"state": "NY",
"country": "USA",
"latitude": 40.7306,
"longitude": -73.9352
}
```

### Get All Addresses
`GET /addresses/`


### Delete All Addresses
`DELETE /addresses/`
```
This is for quick cleanup of DB records
```
### Get Nearby Addresses
`GET /addresses/nearby?latitude=40.7128&longitude=-74.0060&distance_km=5`
```
In output the JamesYard Address should come, the nearby address

```
### Update Address
`PUT /addresses/{address_id}`

### Delete Address
`DELETE /addresses/{address_id}`

### Health Check
`GET /health_check/db`

---

## Features

- ✅ CRUD operations for addresses
- ✅ Geolocation support (latitude & longitude)
- ✅ Find nearby addresses within a specified distance
- ✅ Duplicate address prevention (same name, latitude, longitude)
- ✅ Automatic database creation on startup
- ✅ Database health check endpoint
- ✅ Comprehensive error handling
- ✅ API documentation with Swagger UI
