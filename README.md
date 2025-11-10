# Company Scraper API

A Flask-based web API that scrapes company information from companieshouse.id.

## Overview

This project provides a simple API that allows you to search for Indonesian company information by name. It uses web scraping techniques to retrieve data from companieshouse.id and returns it in a structured JSON format.

## Educational Purpose

**Note**: This project is created for educational purposes only. It demonstrates web scraping techniques, API development with Flask, and proper handling of HTTP requests. Please use responsibly and be aware that web scraping may be subject to terms of service and legal restrictions. I don't guarantee anything regarding the functionality or legal compliance of this code.

## Features

- RESTful API endpoint to search for company data
- Extracts key company information including registered name, legal entity type, business number, registered address, and city
- Handles error cases when a company is not found
- Standardized name matching for more flexible searching
- Production-ready deployment with Docker and Docker Compose
- Health check endpoint for monitoring
- Configurable rate limiting to be respectful to the target website
- Comprehensive logging

## Files

- `app.py`: Main Flask application with the API endpoint
- `company_client.py`: Web scraping logic for extracting company data
- `requirements.txt`: Python dependencies
- `Dockerfile`: Docker configuration for containerization
- `docker-compose.yml`: Docker Compose configuration for easy deployment
- `README.md`: This file
- `PRODUCTION.md`: Production deployment guide
- `.gitignore`: Specifies files and directories to ignore in git

## Local Development

To run the Flask application locally:

```bash
pip install -r requirements.txt
python app.py
```

Then make a GET request to:

```
http://localhost:5000/company/search?name=PT.%20Buka%20Bumi%20Konstruksi
```

## API Endpoints

### Search Company
`GET /company/search?name={company_name}`

- `name`: The name of the company to search for

Returns a JSON object with company information or an error message if not found.

### Health Check
`GET /health`

Returns a JSON object with service health status.

## Dependencies

This project uses:
- Flask: for the web API framework
- requests: for making HTTP requests
- BeautifulSoup: for parsing HTML content
- time: for rate limiting
- gunicorn: for production WSGI server

## Production Deployment

For production deployment information, see [PRODUCTION.md](PRODUCTION.md).

To run with Docker:

```bash
docker build -t company-scraper .
docker run -p 5000:5000 company-scraper
```

Or with Docker Compose:

```bash
docker-compose up -d
```

## Configuration

The application can be configured using environment variables:

- `FLASK_ENV`: Set to "production" for production mode (default: production)
- `PORT`: Port number to run the service on (default: 5000)
- `SEARCH_BASE_URL`: Base URL for search queries (default: https://companieshouse.id/search?term=)
- `BASE_DOMAIN`: Base domain for URL resolution (default: https://companieshouse.id)
- `RATE_LIMIT`: Time in seconds to wait between requests (default: 1)
- `REQUEST_TIMEOUT`: Timeout in seconds for HTTP requests (default: 10)
- `USER_AGENT`: User-Agent header for HTTP requests

## Note

This project implements rate limiting to be respectful to the target website. Please use responsibly and comply with the target website's terms of service.

For production deployment details, refer to [PRODUCTION.md](PRODUCTION.md).