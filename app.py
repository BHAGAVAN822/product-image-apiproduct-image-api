from flask import Flask, request, jsonify
import requests
import base64
import xmlrpc.client

app = Flask(__name__)

# Google Custom Search API
API_KEY = "YOUR_GOOGLE_API_KEY"
CSE_ID = "YOUR_CSE_ID"

# Odoo Credentials
ODOO_URL = "https://your-odoo-domain.com"
ODOO_DB = "your-database"
ODOO_USERNAME = "your-username"
ODOO_PASSWORD = "your-password"

@app.route('/fetch_and_update_image', methods=['POST'])
def fetch_and_update_image():
    try:
        data = request.get_json()
        product_name = data.get("name")
        product_id = data.get("id")

        if not product_name or not product_id:
            return jsonify({"status": "error", "message": "Product name or ID missing"}), 400

        # Fetch image from Google
        url = f"https://www.googleapis.com/customsearch/v1?q={product_name}&cx={CSE_ID}&key={API_KEY}&searchType=image"
        response = requests.get(url)

        if response.status_code != 200:
            return jsonify({"status": "error", "message": "Failed to fetch image"}), 500

        results = response.json()
        if "items" not in results:
            return jsonify({"status": "error", "message": "No image found"}), 404

        image_url = results["items"][0]["link"]
        image_response = requests.get(image_url)
        image_base64 = base64.b64encode(image_response.content).decode('utf-8')

        # Connect to Odoo
        common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
        uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
        models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')

        # Update product image
        models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'product.template', 'write',
            [[product_id], {'image_1920': image_base64}]
        )

        return jsonify({"status": "success", "message": f"Image updated for product: {product_name}"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
