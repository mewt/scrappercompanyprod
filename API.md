# Company Scraper API - Production Documentation

## Overview

A production-ready Flask-based API that scrapes Indonesian company information from [companieshouse.id](https://companieshouse.id) with Docker support, comprehensive logging, health monitoring, and environment-based configuration.

## API Specification

The complete API specification is available in [Swagger/OpenAPI format](./swagger.json).

View it with:
- [Swagger Editor](https://editor.swagger.io/) - Online editor
- [Swagger UI](https://swagger.io/tools/swagger-ui/) - Local hosting
- Import into Postman or Insomnia

## Quick Start

### Using Docker

```bash
# Clone the repository
git clone https://github.com/mewt/scrappercompanyprod.git
cd scrappercompanyprod

# Start with Docker Compose
docker-compose up -d

# Or with Nginx reverse proxy
docker-compose -f docker-compose-with-nginx.yml up -d
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## API Endpoints

### 1. Health Check

```http
GET /health
```

**Purpose:** Monitor service health for load balancers and monitoring tools

**Example Response:**
```json
{
  "status": "healthy"
}
```

### 2. Search Company

```http
GET /company/search?name={company_name}
```

**Parameters:**
- `name` (required): Company name to search for (URL-encoded)

**Example Request:**
```bash
curl "http://localhost:5000/company/search?name=PT.%20Buka%20Bumi%20Konstruksi"
```

**Example Response:**
```json
{
  "Registered Name": "PT. Buka Bumi Konstruksi",
  "Legal Entity Type": "Limited Liability Company",
  "Business Number": "1218057",
  "Registered Address": "Gold Coast Office Tower Liberty Lantai 3 GH, Jalan Pantai Indah Kapuk",
  "City": "NORTH JAKARTA"
}
```

## Error Responses

| Status Code | Description | Example Response |
|------------|-------------|------------------|
| 200 | Success | Company data JSON |
| 400 | Missing parameter | `{"error": "Missing 'name' parameter"}` |
| 503 | Company not found | `{"error": "Could not find information for 'Company'"}` |
| 500 | Server error | `{"error": "Internal error occurred..."}` |

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `5000` | Server port |
| `SEARCH_BASE_URL` | `https://companieshouse.id/search?term=` | Search URL |
| `BASE_DOMAIN` | `https://companieshouse.id` | Base domain |
| `RATE_LIMIT` | `1` | Seconds between requests |
| `REQUEST_TIMEOUT` | `10` | Request timeout (seconds) |
| `USER_AGENT` | Chrome 100 | HTTP User-Agent header |
| `FLASK_ENV` | `production` | Flask environment |

### Example .env file

```env
PORT=5000
RATE_LIMIT=1
REQUEST_TIMEOUT=10
FLASK_ENV=production
```

## Response Fields

| Field | Description | Example |
|-------|-------------|---------|
| Registered Name | Official company name | "PT. Buka Bumi Konstruksi" |
| Legal Entity Type | Company type | "Limited Liability Company" |
| Business Number | Registration number (NIB) | "1218057" |
| Registered Address | Official address | "Gold Coast Office Tower..." |
| City | Registration city | "NORTH JAKARTA" |

## Features

### Production Features

- **Health Check Endpoint**: `/health` for monitoring
- **Structured Logging**: Comprehensive request/response logging
- **Environment Configuration**: All settings via env vars
- **Docker Support**: Complete containerization
- **Nginx Reverse Proxy**: Production-ready with SSL support
- **Rate Limiting**: Configurable delays between requests
- **Error Handling**: Comprehensive exception handling
- **Resource Limits**: Memory (512M) and CPU (0.5) constraints

### Name Matching

Flexible name matching that standardizes inputs:
- Removes periods (.) and commas (,)
- Converts to lowercase
- Trims whitespace

Examples that all match:
- `PT. Buka Bumi Konstruksi`
- `PT Buka Bumi Konstruksi`
- `PT., Buka Bumi Konstruksi`

## Deployment

### Basic Docker Deployment

```bash
docker-compose up -d --build
```

### With Nginx (Production)

```bash
chmod +x setup.sh
./setup.sh
```

Or manually:
```bash
docker-compose -f docker-compose-with-nginx.yml up -d --build
```

### Monitoring

Check service health:
```bash
curl http://localhost:5000/health
```

View logs:
```bash
docker-compose logs -f
```

## Data Source

Data is scraped from [companieshouse.id](https://companieshouse.id) for educational purposes. Please use responsibly and comply with the website's terms of service.

## See Also

- [Production Guide](./PRODUCTION.md) - Detailed production deployment instructions
- [Swagger Specification](./swagger.json) - Complete API specification