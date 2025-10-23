# RESTful API string analyzer

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

## 📋 Prerequisites

- Python 3.8 or higher
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

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
touch .env
```

Add the following variables to `.env`:

```env
SECRET_KEY=your-django-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

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

## 📦 Dependencies

### Installing Dependencies

All dependencies are listed in `requirements.txt`. Install them using:

```bash
pip install -r requirements.txt
```

### Core Dependencies

```env
Django>=4.2.0
djangorestframework>=3.14.0
python-dotenv>=1.0.0
```

For production deployment, also install:

```bash
pip install gunicorn psycopg2-binary
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

### 2. Get Specific String

**Endpoint:** `GET /strings/{string_value}`

**Example:** `GET /strings/hello%20world`

**Response (200 OK):** Same structure as create response

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

### 4. Natural Language Filtering

**Endpoint:** `GET /strings/filter-by-natural-language?query={text}`

**Supported Queries:**

- "all single word palindromic strings"
- "strings longer than 10 characters"
- "strings containing the letter z"
- "palindromic strings"

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

### 5. Delete String

**Endpoint:** `DELETE /strings/{string_value}`

**Example:** `DELETE /strings/hello%20world`

**Response:** `204 No Content`

### Status Codes

| Code | Description |
|------|-------------|
| 200 | OK - Request succeeded |
| 201 | Created - Resource created successfully |
| 204 | No Content - Deletion successful |
| 400 | Bad Request - Invalid request data or query parameters |
| 404 | Not Found - Resource doesn't exist |
| 409 | Conflict - Duplicate string detected |
| 422 | Unprocessable Entity - Invalid data type (value must be string) |

## 🔧 Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SECRET_KEY` | Django secret key for cryptographic signing | Yes | - |
| `DEBUG` | Enable/disable debug mode | No | True |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | No | `*` |

## 🚢 Deployment

### Railway Deployment

1. Push code to GitHub repository
2. Sign up at [railway.app](https://railway.app)
3. Create new project from GitHub repo
4. Add environment variables in Railway dashboard:
   - `SECRET_KEY` 
   - `DEBUG=False`
   - `ALLOWED_HOSTS=your-domain.railway.app`
5. Railway will auto-deploy on push

### Environment Variables for Production

```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## 🧪 Testing

### Test with cURL

**Create a string:**

```bash
curl -X POST http://127.0.0.1:8000/strings \
  -H "Content-Type: application/json" \
  -d '{"value": "racecar"}'
```

**Get all strings:**

```bash
curl http://127.0.0.1:8000/strings
```

**Filter palindromes:**

```bash
curl "http://127.0.0.1:8000/strings?is_palindrome=true"
```

**Natural language query:**

```bash
curl "http://127.0.0.1:8000/strings/filter-by-natural-language?query=palindromic%20strings"
```

**Delete string:**

```bash
curl -X DELETE http://127.0.0.1:8000/strings/racecar
```

**Test duplicate (should return 409):**

```bash
curl -X POST http://127.0.0.1:8000/strings \
  -H "Content-Type: application/json" \
  -d '{"value": "racecar"}'
```

### Test with Postman/Insomnia

1. Import endpoints listed above
2. Set `Content-Type: application/json` header for POST requests
3. Test each endpoint with various inputs
4. Verify status codes match specification

## 📁 Project Structure

```txt
string-analyzer-api/
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
├── Procfile               # Deployment configuration
└── README.md              # Project documentation
```

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

## 👤 Author

- kim-mkuu

## 📝 License

MIT
