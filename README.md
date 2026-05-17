# Inventory Management System
A Flask-based REST API for managing retail inventory with full CRUD operations, OpenFoodFacts external API integration, a CLI interface, and a unit test suite.

---

## Installation and Setup

### Prerequisites
- Python 3.8+
- pip

### Install Dependencies
```bash
pip install flask flask-cors requests pytest
```

### Run the Flask Server
```bash
python app.py
```
Server starts at `http://127.0.0.1:5555`

### Run the CLI (in a second terminal while server is running)
```bash
python cli.py
```

### Run the Test Suite
```bash
python -m pytest tests/ -v
```

---

## Project Structure
```
inventory_system/
├── app.py              # Flask REST API — all routes and logic
├── cli.py              # Command line interface for employees
├── README.md           # Project documentation
└── tests/
    └── test_app.py     # Unit tests with pytest and unittest.mock
```

---

## API Endpoint Details

| Method | Route | Description | Status Codes |
|--------|-------|-------------|--------------|
| GET | `/` | Welcome message and endpoint list | 200 |
| GET | `/inventory` | Return all inventory items | 200 |
| GET | `/inventory/<id>` | Return one item by ID | 200, 404 |
| POST | `/inventory` | Add a new item | 201, 400 |
| PATCH | `/inventory/<id>` | Update an existing item | 200, 404 |
| DELETE | `/inventory/<id>` | Remove an item | 204, 404 |
| GET | `/inventory/search/<name>` | Search items by name | 200, 404 |
| GET | `/external/<barcode>` | Lookup product on OpenFoodFacts | 200, 404, 503 |
| POST | `/external/add/<barcode>` | Fetch from OpenFoodFacts and add to inventory | 201, 404, 503 |

---

## Example Usage

### View all inventory
```bash
curl http://127.0.0.1:5555/inventory
```

### Add a new item manually
```bash
curl -X POST http://127.0.0.1:5555/inventory \
  -H "Content-Type: application/json" \
  -d '{"name": "Coconut Water", "quantity": 40, "price": 2.49}'
```

### Update an item
```bash
curl -X PATCH http://127.0.0.1:5555/inventory/1 \
  -H "Content-Type: application/json" \
  -d '{"quantity": 75, "price": 3.99}'
```

### Delete an item
```bash
curl -X DELETE http://127.0.0.1:55555/inventory/1
```

### Search by name
```bash
curl http://127.0.0.1:5555/inventory/search/juice
```

### Lookup product on OpenFoodFacts by barcode
```bash
curl http://127.0.0.1:5555/external/0048151623426
```

### Add product from OpenFoodFacts to inventory
```bash
curl -X POST http://127.0.0.1:5555/external/add/0048151623426 \
  -H "Content-Type: application/json" \
  -d '{"quantity": 20, "price": 3.99}'
```

---

## CLI Commands

Run `python cli.py` then choose from the menu:

| Option | Action |
|--------|--------|
| 0 | View all inventory |
| 1 | View item by ID |
| 2 | Add new item manually |
| 3 | Update an item |
| 4 | Delete an item |
| 5 | Search items by name |
| 6 | Fetch product from OpenFoodFacts (view only) |
| 7 | Add product from OpenFoodFacts to inventory |
| 88 | Exit |

---

## Testing

Tests use `pytest` and `unittest.mock` to simulate external API responses without hitting the internet.

```bash
python -m pytest tests/ -v
```

Test coverage includes:
- GET, POST, PATCH, DELETE for `/inventory`
- 404 handling for all routes
- Search functionality
- OpenFoodFacts external API
- Adding from external API to inventory

---
