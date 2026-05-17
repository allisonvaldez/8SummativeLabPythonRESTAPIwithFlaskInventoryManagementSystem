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
    return max(item["id"] for e in inventory_data) + 1 if inventory_data else 1

# Define home route with decorator and simple welcome message
@app.route("/", methods=["GET"])
def home():
    return make_response(jsonify({"message": "Welcome to the site"}), 200)

# Define GET /inventory route with decorator
@app.route("/inventory", methods=["GET"])
def get_inventory():
    return make_response(jsonify(inventory_data), 200)

# Define GET /inventory/<int:id> route with decorator
@app.route("/inventory/<int:id>", methods=["GET"])
def get_inventory_item(item_id):
    item = next((i for i in inventory_data if i["id"] == item_id), None)

    # Control flow
    if item is None:
        return make_response(jsonify({"error": "Try again the item doesn't exist"}), 400)
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
def update_inventory_item():
    item = next((i for i in inventory_data if i["id"] == item_id), None)

    # Control flow
    for field in ["name", "id", "quantity", "price", "barcode"]:
        if field in inventory_data:
            item[field] = data[field]
    
    return make_response(jsonify(inventory_item), 200)
