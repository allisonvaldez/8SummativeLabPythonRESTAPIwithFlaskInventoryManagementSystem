# needed for Unit tests for the Inventory Management System API start with imports

import pytest
import json
from unittest.mock import patch, MagicMock
from app import app, inventory

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def reset_inventory():
    inventory.clear()
    inventory.extend([
        {"id": 1, "name": "Apple Juice", "quantity": 50, "price": 2.99, "barcode": ""},
        {"id": 2, "name": "Granola Bar",  "quantity": 120, "price": 1.49, "barcode": ""},
        {"id": 3, "name": "Olive Oil",    "quantity": 30,  "price": 8.99, "barcode": ""},
    ])

def test_homepage_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.get_json()

def test_get_all_inventory(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 3

def test_get_item_by_id(client):
    response = client.get("/inventory/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1
    assert data["name"] == "Apple Juice"

def test_get_item_not_found(client):
    response = client.get("/inventory/999")
    assert response.status_code == 404
    assert "error" in response.get_json()

def test_create_item(client):
    payload  = {"name": "Orange Juice", "quantity": 25, "price": 3.49}
    response = client.post("/inventory", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Orange Juice"
    assert "id" in data

def test_create_item_missing_fields(client):
    response = client.post("/inventory", json={"name": "Missing Fields"})
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_update_item(client):
    response = client.patch("/inventory/1", json={"quantity": 75, "price": 3.49})
    assert response.status_code == 200
    data = response.get_json()
    assert data["quantity"] == 75
    assert data["price"] == 3.49
    assert data["name"] == "Apple Juice"

def test_update_item_not_found(client):
    response = client.patch("/inventory/999", json={"quantity": 10})
    assert response.status_code == 404

def test_delete_item(client):
    response = client.delete("/inventory/1")
    assert response.status_code == 204
    assert client.get("/inventory/1").status_code == 404

def test_delete_item_not_found(client):
    response = client.delete("/inventory/999")
    assert response.status_code == 404

def test_search_items(client):
    response = client.get("/inventory/search/juice")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) >= 1
    assert all("juice" in item["name"].lower() for item in data)

def test_search_items_not_found(client):
    response = client.get("/inventory/search/xyz123notreal")
    assert response.status_code == 404

def test_fetch_external_product_found(client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "status": 1,
        "product": {"product_name": "Test Juice", "brands": "Test Brand", "quantity": "500ml", "nutriscore_grade": "b"}
    }
    with patch("app.http_requests.get", return_value=mock_response):
        response = client.get("/external/1234567890")
        assert response.status_code == 200
        data = response.get_json()
        assert data["name"] == "Test Juice"
        assert data["brand"] == "Test Brand"

def test_fetch_external_product_not_found(client):
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": 0}
    with patch("app.http_requests.get", return_value=mock_response):
        response = client.get("/external/0000000000")
        assert response.status_code == 404
        assert "error" in response.get_json()

def test_add_from_external(client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "status": 1,
        "product": {"product_name": "Mocked Cereal", "brands": "Mock Brand"}
    }
    with patch("app.http_requests.get", return_value=mock_response):
        response = client.post("/external/add/9876543210", json={"quantity": 10, "price": 4.99})
        assert response.status_code == 201
        data = response.get_json()
        assert data["name"] == "Mocked Cereal"
        assert data["quantity"] == 10
        assert data["price"] == 4.99
        assert "id" in data