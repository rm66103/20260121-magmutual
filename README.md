# User API

A FastAPI application for querying user data from a CSV file, featuring semantic similarity search for professions using vector embeddings.

## Features

- **User Lookup**: Get specific users by ID
- **Filtered Queries**: Filter users by date range and profession (exact match)
- **Semantic Search**: Find users with similar professions using vector similarity search
- **CSV-based Data**: All user data stored in CSV format (no database required)
- **Vector Search**: Uses sentence-transformers and in-memory cosine similarity for semantic profession matching

## Project Structure

```
magmutual/
├── api/
│   ├── __init__.py
│   ├── main.py              # FastAPI app and route definitions
│   ├── csv_reader.py        # CSV reading and parsing utilities
│   ├── vector_search.py     # Vector similarity search for professions
│   └── data/
│       ├── users.csv        # Sample user data CSV
│       └── professions.db   # SQLite database for vector embeddings (auto-generated)
├── tests/
│   ├── __init__.py
│   ├── test_endpoints.py    # API endpoint tests
│   └── test_csv_reader.py   # CSV reading tests
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Setup

### Prerequisites

- Python 3.10.0
- pyenv (for virtual environment management)

### Installation

1. Activate your pyenv environment:
   ```bash
   pyenv activate magmutual
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Note: The first time you run the application, sentence-transformers will download the embedding model (`all-MiniLM-L6-v2`) from Hugging Face. This is a one-time download that will be cached locally.

### Running the Server

**Important**: Make sure you're in the project root directory (`magmutual/`) when running the server.

Start the FastAPI development server:

```bash
# Make sure you're in the magmutual directory
cd /Users/mcm66103/Documents/python/magmutual

# Activate your pyenv environment
eval "$(pyenv init -)"
pyenv activate magmutual

# Run the server (use python -m for better module path handling)
python -m uvicorn api.main:app --reload
```

Alternatively, you can use uvicorn directly (must be in project root):

```bash
uvicorn api.main:app --reload
```

The API will be available at `http://localhost:8000`

**Note**: If you get a `ModuleNotFoundError: No module named 'api'`, make sure you're running the command from the `magmutual/` directory (the directory containing the `api/` folder).


### API Documentation

FastAPI automatically generates interactive API documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### GET `/`

Root endpoint with API information.

**Response:**
```json
{
  "message": "User API",
  "endpoints": {
    "GET /users/{user_id}": "Get a specific user by ID",
    "GET /users": "Get users with optional filters",
    "GET /users/search": "Semantic search for users by profession"
  }
}
```

### GET `/users/{user_id}`

Get a specific user by ID.

**Parameters:**
- `user_id` (path): User ID to retrieve

**Response:**
```json
{
  "id": "1",
  "name": "John Doe",
  "email": "john.doe@example.com",
  "profession": "Software Engineer",
  "created_date": "2023-01-15",
  "age": 30,
  "location": "New York, NY",
  "phone": "555-1234"
}
```

**Error Responses:**
- `404`: User not found

### GET `/users`

Get a list of users with optional filters.

**Query Parameters:**
- `start_date` (optional): Filter users created on/after this date (format: YYYY-MM-DD)
- `end_date` (optional): Filter users created on/before this date (format: YYYY-MM-DD)
- `profession` (optional): Filter by exact profession match (case-insensitive)

**Examples:**
```bash
# Get all users
GET /users

# Get users created after January 1, 2023
GET /users?start_date=2023-01-01

# Get users created between dates
GET /users?start_date=2023-01-01&end_date=2023-06-30

# Get users with specific profession
GET /users?profession=Software Engineer

# Combine filters
GET /users?start_date=2023-01-01&profession=Doctor
```

**Response:**
```json
[
  {
    "id": "1",
    "name": "John Doe",
    "email": "john.doe@example.com",
    "profession": "Software Engineer",
    "created_date": "2023-01-15",
    "age": 30,
    "location": "New York, NY",
    "phone": "555-1234"
  }
]
```

### GET `/users/search`

Semantic search for users by profession using vector similarity.

**Query Parameters:**
- `profession` (required): Profession text to search for semantically
- `limit` (optional): Maximum number of results to return (default: 10, max: 100)

**Examples:**
```bash
# Search for "programmer" - will find Software Engineer, Software Developer, etc.
GET /users/search?profession=programmer

# Search with custom limit
GET /users/search?profession=doctor&limit=5
```

**Response:**
```json
[
  {
    "id": "1",
    "name": "John Doe",
    "email": "john.doe@example.com",
    "profession": "Software Engineer",
    "created_date": "2023-01-15",
    "age": 30,
    "location": "New York, NY",
    "phone": "555-1234",
    "similarity_score": 0.9234
  }
]
```

The results are ordered by similarity score (higher = more similar). The `similarity_score` field indicates how semantically similar the user's profession is to your search query.

**How it works:**
1. Your query profession is converted to a vector embedding
2. The system searches for professions with similar embeddings
3. Results are ranked by cosine similarity
4. Full user records are returned with similarity scores

## CSV File Format

The `api/data/users.csv` file should contain the following columns:

- `id`: Unique identifier (string)
- `name`: Full name (string)
- `email`: Email address (string)
- `profession`: Job title/profession (string)
- `created_date`: Date in ISO format YYYY-MM-DD (string)
- `age`: Age as integer (string, will be parsed)
- `location`: City/state (string)
- `phone`: Phone number (string)

Example:
```csv
id,name,email,profession,created_date,age,location,phone
1,John Doe,john.doe@example.com,Software Engineer,2023-01-15,30,"New York, NY",555-1234
```

## Running Tests

Run the test suite:

```bash
pytest
```

Run with verbose output:

```bash
pytest -v
```

Run specific test file:

```bash
pytest tests/test_endpoints.py
pytest tests/test_csv_reader.py
```

## Technical Details

### Vector Search

The semantic search feature uses:
- **sentence-transformers**: Generates embeddings from profession text
  - Model: `all-MiniLM-L6-v2` (384 dimensions)
  - Runs locally, no API keys required
  - Models download automatically on first use
- **In-memory storage**: Embeddings are stored in memory (no database required)
- **scipy**: Uses cosine similarity for matching professions
  - Simple, fast, and works on all platforms
  - No SQLite extensions needed

### Data Flow

1. CSV data is loaded into memory on application startup
2. Profession embeddings are generated and stored in memory
3. API endpoints query the in-memory CSV data and/or in-memory embeddings
4. Results are returned as JSON

### Performance

- CSV data is cached in memory after first load
- Vector embeddings are generated once at startup
- Semantic search queries are fast (typically < 100ms for small datasets)

## Future Enhancements

This project is organized to support a future React frontend application. The API structure is designed to be consumed by a separate frontend application.

## License

This project is for demonstration purposes.
