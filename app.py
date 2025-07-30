from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/get_image', methods=['POST'])
def get_image():
    try:
        data = request.get_json()
        product_name = data.get("product_name", "")

        if not product_name:
            return jsonify({"error": "Product name is required"}), 400

        return jsonify({"message": f"Received product name: {product_name}"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
