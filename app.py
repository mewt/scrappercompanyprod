import os
import logging
from flask import Flask, jsonify, request
from company_client import extract_company_data, check_company_exists  # Import the scraper functions

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for monitoring
    """
    return jsonify({"status": "healthy"}), 200

# Check company exists endpoint (lightweight)
@app.route('/company/check', methods=['GET'])
def check_company():
    """
    Lightweight endpoint to check if a company exists.
    Only performs search, does NOT scrape detail page.
    Much faster than /company/search (2-5 seconds vs 30+ seconds).
    
    Usage: GET /company/check?name=PT.%20Buka%20Bumi%20Konstruksi
    
    Returns:
        200: {"exists": true, "name": "...", "url": "..."} - Company found
        404: {"exists": false} - Company not found
        400: {"error": "Missing 'name' parameter"} - Invalid request
    """
    logger.info("Received company check request")
    
    # Get the company name dynamically from the URL query string
    company_name = request.args.get('name')
    
    # Validate input
    if not company_name:
        error_msg = "Missing 'name' parameter in the request."
        logger.warning(error_msg)
        return jsonify({"error": error_msg}), 400
    
    # Call the check function (lightweight, no detail scraping)
    try:
        result = check_company_exists(company_name)
    except Exception as e:
        logger.error(f"Error checking company existence for '{company_name}': {str(e)}")
        return jsonify({"error": f"Internal error occurred while checking '{company_name}'"}), 500
    
    # Handle response
    if result is None:
        logger.info(f"Company '{company_name}' not found")
        return jsonify({"exists": False}), 404
        
    logger.info(f"Company '{company_name}' found")
    # Return success with company info
    return jsonify(result), 200

# Define the API endpoint
@app.route('/company/search', methods=['GET'])
def search_company():
    """
    API endpoint to search for company data.
    Usage: GET /company/search?name=PT.%20Buka%20Bumi%20Konstruksi
    """
    logger.info("Received company search request")

    # Get the company name dynamically from the URL query string
    company_name = request.args.get('name')

    # Validate input
    if not company_name:
        error_msg = "Missing 'name' parameter in the request."
        logger.warning(error_msg)
        return jsonify({"error": error_msg}), 400

    # Call the scraper function with the dynamic input
    try:
        company_info = extract_company_data(company_name)
    except Exception as e:
        logger.error(f"Error extracting company data for '{company_name}': {str(e)}")
        return jsonify({"error": f"Internal error occurred while processing request for '{company_name}'."}), 500

    # Handle success or failure
    if company_info is None:
        error_msg = f"Could not find or extract information for '{company_name}'. Please verify the company name."
        logger.warning(error_msg)
        return jsonify({"error": error_msg}), 503

    logger.info(f"Successfully retrieved company data for '{company_name}'")
    
    # Return the extracted data as JSON
    return jsonify(company_info)

if __name__ == '__main__':
    print("Starting Flask API server...")
    # Get port from environment variable, default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Run in production mode (debug=False)
    app.run(host='0.0.0.0', port=port, debug=False)