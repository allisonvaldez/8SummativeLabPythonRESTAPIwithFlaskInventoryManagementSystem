# File for Flask app start with importing utilities and dependencies
import os
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import requests as http_requests
from inventory import get_inventory_data

app = Flask(__name__)
CORS(app)

# Get the data from inventory.py for in memory list new items are appended here
inventory_data = get_inventory_data()

# Get the next id using a generator expression
def next_id():
    return max(item["id"] for item in inventory_data) + 1 if inventory_data else 1

# Define home route with decorator and simple welcome message
@app.route("/", methods=["GET"])
def home():
    return make_response(jsonify({"message": "Welcome to the site"}), 200)

# Define GET /inventory route with decorator
@app.route("/inventory", methods=["GET"])
def get_inventory():
    return make_response(jsonify(inventory_data), 200)

# Define GET /inventory/<int:id> route with decorator
@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    item = next((i for i in inventory_data if i["id"] == item_id), None)

    # Control flow
    if item is None:
        # FIX 3: was 400 (Bad Request) — should be 404 (Not Found) for missing items
        return make_response(jsonify({"error": "Try again the item doesn't exist"}), 404)
    return make_response(jsonify(item), 200)

# Define POST /inventory route with decorator
@app.route("/inventory", methods=["POST"])
def create_inventory_item():
    data = request.get_json()

    # Control flow
    if not data or "name" not in data or "quantity" not in data or "price" not in data:
        return make_response(jsonify({"error": "Missing required entry fields"}), 400)
    
    new_inventory_item = {
        "id":       next_id(),
        "name":     data["name"],
        "quantity": data["quantity"],
        "price":    data["price"],
        "barcode":  data.get("barcode", ""),
    }

    inventory_data.append(new_inventory_item)

    return make_response(jsonify(new_inventory_item), 201)

# Define PATCH /inventory/<id> route with decorator
@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_inventory_item(item_id):
    item = next((i for i in inventory_data if i["id"] == item_id), None)

    if item is None:
        return make_response(jsonify({"error": f"Item with id {item_id} not found"}), 404)

    data = request.get_json()

    # Control flow — only update fields provided in the request body
    for field in ["name", "quantity", "price", "barcode"]:
        if field in data:
            item[field] = data[field]
    
    return make_response(jsonify(item), 200)


# Define DELETE /inventory/<id> route with decorator
@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_inventory_item(item_id):
    global inventory_data
    item = next((i for i in inventory_data if i["id"] == item_id), None)

    # Control flow
    if item is None:
        return make_response(jsonify({"error": f"Item with id {item_id} not found"}), 404)
    inventory_data = [i for i in inventory_data if i["id"] != item_id]

    return make_response("", 204)


# Define GET /inventory/search/<name> route with decorator
@app.route("/inventory/search/<string:name>", methods=["GET"])
def search_inventory_item(name):
    results = [i for i in inventory_data if name.lower() in i["name"].lower()]

    # Control flow
    if not results:
        return make_response(jsonify({"message": f"No item found with the named: {name}"}), 404)
    return make_response(jsonify(results), 200)

# Define GET /external/<barcode> route with decorator from Open Food Facts API
@app.route("/external/<barcode>", methods=["GET"])
def fetch_external_inventory_item(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    try:
        response = http_requests.get(url, timeout=5)
        data = response.json()
        if data.get("status") == 0:
            return make_response(jsonify({"error": f"Product with barcode {barcode} not found"}), 404)
        product = data.get("product", {})
        result = {
            "barcode":    barcode,
            "name":       product.get("product_name", "Unknown"),
            "brand":      product.get("brands", "Unknown"),
            "quantity":   product.get("quantity", "Unknown"),
            "nutriscore": product.get("nutriscore_grade", "N/A"),
        }
        return make_response(jsonify(result), 200)
    except http_requests.exceptions.RequestException as e:
        return make_response(jsonify({"error": f"Failed to reach OpenFoodFacts: {str(e)}"}), 503)

# Define POST /external/add/<barcode> route with decorator from Open Food Facts API
@app.route("/external/add/<barcode>", methods=["POST"])
def add_from_external(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    try:
        response = http_requests.get(url, timeout=5)
        data = response.json()
        if data.get("status") == 0:
            return make_response(jsonify({"error": f"Product with barcode {barcode} not found"}), 404)
        product = data.get("product", {})
        body = request.get_json() or {}
        new_item = {
            "id":       next_id(),
            "name":     product.get("product_name", "Unknown Product"),
            "quantity": body.get("quantity", 0),
            "price":    body.get("price", 0.00),
            "barcode":  barcode,
            "brand":    product.get("brands", "Unknown"),
        }
        inventory_data.append(new_item)
        return make_response(jsonify(new_item), 201)
    except http_requests.exceptions.RequestException as e:
        return make_response(jsonify({"error": f"Failed to reach OpenFoodFacts: {str(e)}"}), 503)

if __name__ == "__main__":
    app.run(port=5555, debug=True)