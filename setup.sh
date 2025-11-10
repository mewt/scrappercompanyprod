#!/bin/bash

echo "Setting up Company Scraper API at companycheck.wearefum.web.id"

# Build and start the services
echo "Building and starting Docker services..."
docker-compose -f docker-compose-with-nginx.yml up -d --build

echo "Waiting for services to start..."
sleep 30

echo "Services are now running!"
echo "Your API is available at: http://companycheck.wearefum.web.id"
echo ""
echo "To set up SSL/HTTPS, run the following commands after confirming your domain resolves to this server:"
echo "1. docker run -it --rm --name certbot \\"
echo "     -v \"$(pwd)/ssl:/etc/letsencrypt\" \\"
echo "     -v \"$(pwd)/nginx.conf:/etc/nginx/nginx.conf\" \\"
echo "     -p 80:80 -p 443:443 \\"
echo "     certbot/certbot certonly --standalone -d companycheck.wearefum.web.id"
echo ""
echo "2. Update nginx.conf to include SSL configuration"
echo ""
echo "API endpoints:"
echo " - Health check: http://companycheck.wearefum.web.id/health"
echo " - Company search: http://companycheck.wearefum.web.id/company/search?name=COMPANY_NAME"