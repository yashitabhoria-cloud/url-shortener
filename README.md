# FastAPI URL Shortener

A backend URL shortener API built with FastAPI. It supports creating short URLs, custom short codes, click tracking, expiration times, persistent SQLite storage, API key authentication, pagination, update/delete operations, and configurable rate limiting.

## Features

- Create shortened URLs
- Redirect short URLs to original URLs
- Support custom short codes
- Validate duplicate and invalid custom short codes
- Track click counts
- View URL statistics
- Support optional expiration times
- Reject expired short URLs
- Delete short URLs
- Update destination URLs
- List shortened URLs with pagination
- Store data persistently using SQLite
- Use in-memory storage for tests
- Protect private endpoints with API key authentication
- Load configuration from environment variables
- Apply configurable rate limiting to protected routes
- Automated tests using pytest

## Tech Stack

- Python
- FastAPI
- Pydantic
- SQLite
- pytest
- python-dotenv
- Uvicorn

## Project Structure

```txt
.
├── main.py
├── config.py
├── rate_limiter.py
├── schemas.py
├── interfaces.py
├── storage.py
├── sqlite_storage.py
├── database.py
├── services.py
├── utils.py
├── requirements.txt
├── .gitignore
└── tests/
    ├── conftest.py
    ├── test_main.py
    └── test_services.py
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd <your-project-folder>
```

### 2. Create and activate a virtual environment

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

Create a file named `.env` in the project root.

Example:

```env
API_KEY=dev-secret-key
RATE_LIMIT_REQUESTS=5
RATE_LIMIT_WINDOW_SECONDS=60
```

### 5. Run the application

```bash
uvicorn main:app --reload
```

The API will be available at:

```txt
http://127.0.0.1:8000
```

Interactive API documentation is available at:

```txt
http://127.0.0.1:8000/docs
```

## API Authentication

Protected routes require an API key in the request header:

```txt
X-API-Key: dev-secret-key
```

Public redirect routes do not require an API key.

## API Endpoints

### Create a short URL

```http
POST /shorten
```

Requires API key.

Example request body:

```json
{
  "url": "https://www.google.com"
}
```

Example with custom short code:

```json
{
  "url": "https://www.google.com",
  "custom_code": "google"
}
```

Example with expiration:

```json
{
  "url": "https://www.google.com",
  "expires_at": "2030-01-01T00:00:00Z"
}
```

### Redirect to original URL

```http
GET /{short_code}
```

Public endpoint. Does not require API key.

Example:

```txt
http://127.0.0.1:8000/google
```

### Get URL statistics

```http
GET /stats/{short_code}
```

Requires API key.

Returns information such as:

- Original URL
- Short code
- Click count
- Creation time
- Expiration time
- Expiration status

### Delete a short URL

```http
DELETE /{short_code}
```

Requires API key.

### Update a short URL

```http
PATCH /{short_code}
```

Requires API key.

Example request body:

```json
{
  "url": "https://www.youtube.com"
}
```

### List shortened URLs

```http
GET /urls?limit=10&offset=0
```

Requires API key.

Supports pagination using:

- `limit`
- `offset`

## Example curl Commands

Create a short URL:

```bash
curl -X POST "http://127.0.0.1:8000/shorten" ^
-H "Content-Type: application/json" ^
-H "X-API-Key: dev-secret-key" ^
-d "{\"url\":\"https://www.google.com\",\"custom_code\":\"google\"}"
```

Get stats:

```bash
curl -X GET "http://127.0.0.1:8000/stats/google" ^
-H "X-API-Key: dev-secret-key"
```

Update a URL:

```bash
curl -X PATCH "http://127.0.0.1:8000/google" ^
-H "Content-Type: application/json" ^
-H "X-API-Key: dev-secret-key" ^
-d "{\"url\":\"https://www.youtube.com\"}"
```

Delete a URL:

```bash
curl -X DELETE "http://127.0.0.1:8000/google" ^
-H "X-API-Key: dev-secret-key"
```

List URLs:

```bash
curl -X GET "http://127.0.0.1:8000/urls?limit=10&offset=0" ^
-H "X-API-Key: dev-secret-key"
```

## Running Tests

Run all tests with:

```bash
python -m pytest
```

## Status Codes

Common responses:

- `200 OK` - Request succeeded
- `307 Temporary Redirect` - Short URL redirected successfully
- `400 Bad Request` - Invalid custom code or invalid expiration time
- `401 Unauthorized` - Missing or invalid API key
- `404 Not Found` - Short code not found
- `409 Conflict` - Custom short code already exists
- `410 Gone` - Short URL has expired
- `422 Unprocessable Entity` - Invalid request body or query parameters
- `429 Too Many Requests` - Rate limit exceeded

## What I Learned

This project demonstrates backend development concepts including:

- REST API design
- FastAPI route handling
- Request and response validation with Pydantic
- Dependency injection
- Service-layer architecture
- Repository pattern
- SQLite persistence
- Environment-based configuration
- API key authentication
- Rate limiting
- Error handling with HTTP status codes
- Automated testing with pytest
- Git-based development workflow