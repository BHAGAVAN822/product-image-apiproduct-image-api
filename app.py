from flask import Flask, request, jsonify
import requests
import base64

app = Flask(__name__)

@app.route('/get_image', methods=['POST'])
def get_image():
    try:
        data = request.get_json()
        product_name = data.get("product_name")
        if not product_name:
            return jsonify({"status": "error", "message": "Product name is required"}), 400

        # Google Custom Search API
        API_KEY = "AIzaSyDGeFtEPIZ-JqKRNLMpKJCd39VHRaIsLZk"
        CSE_ID = "90547fd845737490d"
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

        return jsonify({"status": "success", "image_base64": image_base64})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
