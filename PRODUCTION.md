# Company Scraper API - Production Deployment Guide

## Overview

This document provides instructions for deploying the Company Scraper API microservice at companycheck.wearefum.web.id.

## Architecture

The service is containerized using Docker and can be deployed using Docker Compose. It provides a REST API to scrape company information from companieshouse.id.

## Quick Start

For a complete setup with reverse proxy, you should deploy the application to `/opt/companycheck` and use the provided setup script:

1. Create the application directory:
```bash
sudo mkdir -p /opt/companycheck
sudo chown $USER:$USER /opt/companycheck
```

2. Copy all project files to the directory:
```bash
cp -r /Users/chumisfum/scappercompany/* /opt/companycheck/
```

3. Navigate to the directory:
```bash
cd /opt/companycheck
```

4. Make the setup script executable and run it:
```bash
chmod +x setup.sh
./setup.sh
```

This will start the service with Nginx reverse proxy at companycheck.wearefum.web.id.

## Deployment Methods

### Method 1: Using Docker Compose with Nginx Reverse Proxy (Recommended)

This method runs both your application and Nginx in containers, providing a complete solution.

1. Ensure Docker and Docker Compose are installed on your server
2. Upload all project files to your server:
   - Dockerfile
   - docker-compose-with-nginx.yml
   - docker-compose.yml
   - nginx.conf
   - setup.sh
   - app.py
   - company_client.py
   - requirements.txt

3. Run the setup script:
```bash
./setup.sh
```

Or run manually:
```bash
docker-compose -f docker-compose-with-nginx.yml up -d --build
```

### Method 2: Using System-level Reverse Proxy

If you prefer to use a system-level reverse proxy like Nginx installed directly on your server:

1. Deploy just the application:
```bash
docker-compose up -d --build
```

2. Configure your system Nginx as a reverse proxy:

Create `/etc/nginx/sites-available/companycheck`:
```nginx
server {
    listen 80;
    server_name companycheck.wearefum.web.id;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:
```bash
ln -s /etc/nginx/sites-available/companycheck /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
```

## Environment Variables

The application supports the following environment variables:

- `FLASK_ENV`: Set to "production" for production
- `PORT`: Port number to run the service on (default: 5000)
- `SEARCH_BASE_URL`: Base URL for search queries (default: https://companieshouse.id/search?term=)
- `BASE_DOMAIN`: Base domain for URL resolution (default: https://companieshouse.id)
- `RATE_LIMIT`: Time in seconds to wait between requests (default: 1)
- `REQUEST_TIMEOUT`: Timeout in seconds for HTTP requests (default: 10)
- `USER_AGENT`: User-Agent header for HTTP requests (default: Chrome browser)

## SSL/TLS Setup

For HTTPS, after your domain is pointing to your server, you can set up SSL with Certbot:

### With Container Setup
1. Update your nginx.conf to include SSL configuration after obtaining the certificate
2. Use the Certbot Docker method mentioned in the setup.sh script

### With System-level Nginx
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d companycheck.wearefum.web.id
```

## Health Checks

The service provides a health check endpoint:
- `GET /health` - Returns 200 with {"status": "healthy"} if the service is running

## API Usage

### Search Company
- `GET /company/search?name=<company_name>`
- Example: `GET /company/search?name=PT.%20Buka%20Bumi%20Konstruksi`

This returns a JSON object with the company information or an error message.

## Monitoring and Logging

Logs are output to stdout/stderr and can be accessed using:
```bash
docker-compose -f docker-compose-with-nginx.yml logs -f company-scraper
```

Or for just the app:
```bash
docker-compose -f docker-compose-with-nginx.yml logs -f
```

## Scaling

To scale the service (when not using the nginx proxy container):
```bash
docker-compose up -d --scale company-scraper=<number_of_instances>
```

## Security Considerations

1. **Rate Limiting**: Built-in rate limiting to be respectful to target website
2. **Input Validation**: The service validates input parameters
3. **Environment Variables**: Sensitive configuration is externalized
4. **Non-root User**: Container runs as non-root user
5. **Resource Limits**: Docker Compose includes resource limits
6. **Container Isolation**: Services run in isolated containers

## Backup and Recovery

- Regularly backup any persistent data
- Keep Docker images in a registry for quick redeployment
- Maintain infrastructure as code for reproducible deployments

## Troubleshooting

### Common Issues

1. **Domain Not Resolving**: Ensure companycheck.wearefum.web.id points to your server's IP address
2. **Rate Limiting**: If rate-limited by the source site, increase the `RATE_LIMIT` environment variable
3. **Timeout Errors**: If experiencing timeouts, increase the `REQUEST_TIMEOUT` environment variable
4. **Connection Issues**: Verify network connectivity to companieshouse.id from your server

### Debugging

Check container logs:
```bash
docker-compose -f docker-compose-with-nginx.yml logs company-scraper
```

Exec into the application container for inspection:
```bash
docker-compose -f docker-compose-with-nginx.yml exec company-scraper /bin/bash
```

Exec into the Nginx container:
```bash
docker-compose -f docker-compose-with-nginx.yml exec nginx /bin/sh
```

### Testing the Service

Test the health endpoint:
```bash
curl http://companycheck.wearefum.web.id/health
```

Test a company search:
```bash
curl "http://companycheck.wearefum.web.id/company/search?name=TEST_COMPANY_NAME"
```

## Updating the Service

To update the service:
1. Pull the latest code to your server
2. Rebuild and restart: `docker-compose -f docker-compose-with-nginx.yml up -d --build`

## Legal Considerations

This application scrapes data from external websites. Ensure you:
- Comply with the target website's terms of service
- Respect robots.txt and rate limiting
- Use the service responsibly and ethically