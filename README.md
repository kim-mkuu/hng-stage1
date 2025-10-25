# RESTful API String Analyzer

## Build a RESTful API service that analyzes strings and stores their computed properties

A RESTful API that analyzes strings and computes their properties including length, palindrome detection, unique character count, word count, SHA-256 hash, and character frequency mapping. Supports advanced filtering and natural language queries.

## 🚀 Features

- **Comprehensive String Analysis**: Computes length, palindrome status, unique characters, word count, SHA-256 hash, and character frequency
- **CRUD Operations**: Create, retrieve, list, and delete analyzed strings
- **Advanced Filtering**: Filter by palindrome status, length range, word count, and character presence
- **Natural Language Queries**: Query using plain English (e.g., "palindromic strings longer than 10 characters")
- **Duplicate Prevention**: Automatic detection and rejection of duplicate strings (409 Conflict)
- **RESTful Design**: Proper HTTP status codes and JSON responses
- **URL-Safe**: Handles special characters and spaces in string values
- **Production Ready**: Configured with Gunicorn, PostgreSQL support, and WhiteNoise for static files

## 📋 Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git
- virtualenv (recommended)

## 🛠 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/kim-mkuu/hng-stage1.git
cd hng-stage1
```

### 2. Create Virtual Environment

**On macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies 

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Core Dependencies

```txt
asgiref==3.10.0
dj-database-url==3.0.1
Django==5.2.7
django-filter==25.2
djangorestframework==3.16.1
gunicorn==23.0.0
packaging==25.0
psycopg2-binary==2.9.11
python-decouple==3.8
python-dotenv==1.1.1
sqlparse==0.5.3
tzdata==2025.2
whitenoise==6.11.0
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Add the following variables to `.env`:

```env
SECRET_KEY=your-django-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### Environment Variables In-Detail

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SECRET_KEY` | Django secret key for cryptographic signing | Yes | Fallback for dev |
| `DEBUG` | Enable/disable debug mode | No | True |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | No | `*` |
| `DATABASE_URL` | Database connection string | No | SQLite |

**Note:** Generate a secure SECRET_KEY using:

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

The API will be available at: `http://127.0.0.1:8000`

**Note:** If your browser automatically adds a trailing slash and returns 404, clear your browser cache or use `curl` for testing.

## 📁 Project Structure

```txt
hng-stage1/
├── config/                 # Django project configuration
│   ├── settings.py        # Main settings with environment variables
│   ├── urls.py            # Root URL configuration
│   └── wsgi.py            # WSGI entry point
├── strings/               # Main application
│   ├── models.py          # String model with computed fields
│   ├── serializers.py     # DRF serializers for validation
│   ├── views.py           # API view classes
│   ├── urls.py            # App-specific URL patterns
│   └── utils.py           # String analysis utility functions
├── .env                   # Environment variables (not in git)
├── .env.example           # Example environment file
├── .gitignore             # Git ignore rules
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── Procfile               # Deployment configuration (Gunicorn)
├── runtime.txt            # Python version specification
└── README.md              # Project documentation
```

## 🌐 API Endpoints

**Base URL:** `http://127.0.0.1:8000` (Development) | `https://your-domain.com` (Production)

### 1. Create/Analyze String

**Endpoint:** `POST /strings`

**Request:**

```json
{
  "value": "hello world"
}
```

**Response (201 Created):**

```json
{
  "id": "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9",
  "value": "hello world",
  "properties": {
    "length": 11,
    "is_palindrome": false,
    "unique_characters": 8,
    "word_count": 2,
    "sha256_hash": "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9",
    "character_frequency_map": {
      "h": 1, "e": 1, "l": 3, "o": 2, " ": 1, "w": 1, "r": 1, "d": 1
    }
  },
  "created_at": "2025-10-23T10:00:00Z"
}
```

**Error Responses:**

- **409 Conflict:** String already exists
- **400 Bad Request:** Missing "value" field
- **422 Unprocessable Entity:** Value is not a string

### 2. Get Specific String

**Endpoint:** `GET /strings/{string_value}`

**Example:** `GET /strings/hello%20world`

**Response (200 OK):** Same structure as create response

**Error Response:**

- **404 Not Found:** String does not exist

### 3. List All Strings with Filtering

**Endpoint:** `GET /strings`

**Query Parameters:**

- `is_palindrome` (boolean): `true` or `false`
- `min_length` (integer): Minimum string length
- `max_length` (integer): Maximum string length
- `word_count` (integer): Exact word count
- `contains_character` (string): Single character to search for

**Examples:**

```bash
GET /strings?is_palindrome=true
GET /strings?min_length=5&max_length=20
GET /strings?word_count=2&contains_character=a
```

**Response (200 OK):**

```json
{
  "data": [...],
  "count": 5,
  "filters_applied": {
    "is_palindrome": true,
    "min_length": 5
  }
}
```

**Error Response:**

- **400 Bad Request:** Invalid query parameter values or types

### 4. Natural Language Filtering

**Endpoint:** `GET /strings/filter-by-natural-language?query={text}`

**Supported Queries:**

- "all single word palindromic strings"
- "strings longer than 10 characters"
- "strings containing the letter z"
- "palindromic strings"
- "palindromic strings that contain the first vowel"

**Example:** `GET /strings/filter-by-natural-language?query=palindromic%20strings`

**Response (200 OK):**

```json
{
  "data": [...],
  "count": 3,
  "interpreted_query": {
    "original": "palindromic strings",
    "parsed_filters": {
      "is_palindrome": true
    }
  }
}
```

**Error Responses:**

- **400 Bad Request:** Missing query parameter
- **422 Unprocessable Entity:** Conflicting filters detected

### 5. Delete String

**Endpoint:** `DELETE /strings/{string_value}`

**Example:** `DELETE /strings/hello%20world`

**Response:** `204 No Content`

**Error Response:**

- **404 Not Found:** String does not exist

### Status Codes

| Code | Description |
|------|-------------|
| 200 | OK - Request succeeded |
| 201 | Created - Resource created successfully |
| 204 | No Content - Deletion successful |
| 400 | Bad Request - Invalid request data or query parameters |
| 404 | Not Found - Resource doesn't exist |
| 409 | Conflict - Duplicate string detected |
| 422 | Unprocessable Entity - Invalid data type or conflicting filters |


## 🧪 Testing

### Comprehensive Endpoint Testing

#### 1. Test POST /strings (Create)

```bash
# 201 Created - Success
curl -X POST http://127.0.0.1:8000/strings \
  -H "Content-Type: application/json" \
  -d '{"value":"test string"}'

# 409 Conflict - Duplicate
curl -X POST http://127.0.0.1:8000/strings \
  -H "Content-Type: application/json" \
  -d '{"value":"test string"}'

# 400 Bad Request - Missing value field
curl -X POST http://127.0.0.1:8000/strings \
  -H "Content-Type: application/json" \
  -d '{}'

# 422 Unprocessable Entity - Non-string value
curl -X POST http://127.0.0.1:8000/strings \
  -H "Content-Type: application/json" \
  -d '{"value":123}'
```

#### 2. Test GET /strings/{string_value}

```bash
# 200 OK - Existing string
curl http://127.0.0.1:8000/strings/test%20string

# 404 Not Found - Non-existent
curl http://127.0.0.1:8000/strings/nonexistent
```

#### 3. Test GET /strings (Filtering)

```bash
# Create test data first
curl -X POST http://127.0.0.1:8000/strings -H "Content-Type: application/json" -d '{"value":"racecar"}'
curl -X POST http://127.0.0.1:8000/strings -H "Content-Type: application/json" -d '{"value":"hello world"}'
curl -X POST http://127.0.0.1:8000/strings -H "Content-Type: application/json" -d '{"value":"a very long string with more than ten characters"}'

# 200 OK - No filters
curl http://127.0.0.1:8000/strings

# 200 OK - With filters
curl "http://127.0.0.1:8000/strings?is_palindrome=true"
curl "http://127.0.0.1:8000/strings?min_length=5&max_length=20"
curl "http://127.0.0.1:8000/strings?word_count=2"

# 400 Bad Request - Invalid parameter
curl "http://127.0.0.1:8000/strings?min_length=abc"
```

#### 4. Test Natural Language Filtering

```bash
# Create palindrome test data
curl -X POST http://127.0.0.1:8000/strings -H "Content-Type: application/json" -d '{"value":"mom"}'
curl -X POST http://127.0.0.1:8000/strings -H "Content-Type: application/json" -d '{"value":"zebra"}'

# 200 OK - Valid queries
curl "http://127.0.0.1:8000/strings/filter-by-natural-language?query=all%20single%20word%20palindromic%20strings"
curl "http://127.0.0.1:8000/strings/filter-by-natural-language?query=strings%20longer%20than%2010%20characters"
curl "http://127.0.0.1:8000/strings/filter-by-natural-language?query=strings%20containing%20the%20letter%20z"
curl "http://127.0.0.1:8000/strings/filter-by-natural-language?query=palindromic%20strings"

# 400 Bad Request - Missing query
curl "http://127.0.0.1:8000/strings/filter-by-natural-language"

# 422 Unprocessable Entity - Conflicting filters (if implemented)
curl "http://127.0.0.1:8000/strings/filter-by-natural-language?query=strings%20longer%20than%20100%20and%20shorter%20than%2010"
```

#### 5. Test DELETE /strings/{string_value}

```bash
# Create string to delete
curl -X POST http://127.0.0.1:8000/strings -H "Content-Type: application/json" -d '{"value":"delete me"}'

# 204 No Content - Success
curl -X DELETE http://127.0.0.1:8000/strings/delete%20me

# Verify deletion - 404 Not Found
curl http://127.0.0.1:8000/strings/delete%20me

# 404 Not Found - Already deleted
curl -X DELETE http://127.0.0.1:8000/strings/delete%20me
```

## 🚢 Deployment

### Leapcell Deployment

1. **Prepare Project Files**

Ensure you have:

- `Procfile`: `web: gunicorn config.wsgi --log-file -`
- `runtime.txt`: `python-3.11`
- `requirements.txt`: All dependencies listed

2. **Push to GitHub**

```bash
git add .
git commit -m "Prepare for Leapcell deployment"
git push origin main
```

3. **Deploy on Leapcell**

- Go to [leapcell.io](https://leapcell.io)
- Sign up/Login
- Click "New Project"
- Connect your GitHub repository
- Select `hng-stage1` repo
- Leapcell auto-detects Django project

4. **Configure Environment Variables**

In Leapcell dashboard, set:

```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app.leapcell.io
```

5. **Deploy**

Click "Deploy" - Leapcell automatically:

- Installs dependencies from `requirements.txt`
- Runs database migrations
- Starts Gunicorn server

6. **Verify Deployment**

```bash
curl https://your-app.leapcell.io/strings
```

## 🔍 Implementation Details

### String Properties Calculation

**utils.py** implements exact property calculations per specification:

- `length`: Total character count including spaces/punctuation
- `is_palindrome`: Case-insensitive comparison (does NOT strip spaces)
- `unique_characters`: Distinct character count (includes spaces)
- `word_count`: Using `value.split()` (collapses multiple spaces)
- `sha256_hash`: Lowercase hex digest of UTF-8 encoded string
- `character_frequency_map`: Counts all characters including spaces

### URL Routing Order

**strings/urls.py** maintains critical routing order:

1. `strings/filter-by-natural-language` (most specific)
2. `strings/<path:string_value>` (dynamic path)
3. `strings` (base endpoint)

This prevents the dynamic path from catching `filter-by-natural-language` as a string value.

### Database Configuration

Uses `dj-database-url` for flexible database configuration:

- **Local:** SQLite (default)
- **Production:** PostgreSQL (via DATABASE_URL env variable)

No manual configuration needed - automatically switches based on environment.

## 🐛 Troubleshooting

### Common Issues

**1. Port 8000 already in use:**

```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9

# Or use a different port
python manage.py runserver 8080
```

**2. SECRET_KEY not found error:**

- Ensure `.env` file exists in project root
- Verify `SECRET_KEY` is set in `.env`
- Check that `python-dotenv` is installed

**3. Migration errors:**

```bash
# Reset database (development only)
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
```

**4. Module not found:**

```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**5. Invalid query parameter error (400):**

- Ensure boolean values are lowercase: `is_palindrome=true` (not `True`)
- Integer values must be valid numbers
- URL encode special characters in string values

**6. String not found (404) when it exists:**

- Check URL encoding: spaces should be `%20`
- Ensure string value matches exactly (case-sensitive)

**7. Browser adds trailing slash causing 404:**

- Clear browser cache
- Use `curl` or API client instead of browser
- `APPEND_SLASH = False` is set in settings.py

**8. Empty results for natural language query:**

- Returns 200 OK with empty data array (not an error)
- Ensure test data exists that matches the query
- Example: "strings containing the letter z" requires strings with 'z'

## 👤 Author

- kim-mkuu

## 📝 License

MIT
