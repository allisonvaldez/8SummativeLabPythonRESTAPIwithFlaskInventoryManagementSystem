# cli.py — for the Inventory Management System commands start with importing utilities and dependencies

import requests
import json

# Create base URL
base_url = "http://127.0.0.1:5555"

# Create function to display an item
def print_item(item):
    print(f"  ID:       {item.get('id')}")
    print(f"  Name:     {item.get('name')}")
    print(f"  Quantity: {item.get('quantity')}")
    print(f"  Price:    ${item.get('price'):.2f}")
    if item.get("barcode"):
        print(f"  Barcode:  {item.get('barcode')}")
    if item.get("brand"):
        print(f"  Brand:    {item.get('brand')}")
    print()

# Create function to display instructions
def print_menu():
    print("\n\nInventory Management System:")
    print("0. To view all inventory")
    print("1. To view item by ID")
    print("2. To add a new item")
    print("3. To update an inventory item")
    print("4. To delete an inventory item")
    print("5. To search for an item by name")
    print("6. To find a product via OpenFoodFacts (by a barcode)")
    print("7. To add a product from OpenFoodFacts to existinh inventory")
    print("88. To exit the program...")
    print("\n\n")

# Create function to display view items
def view_all():
    response = requests.get(f"{base_url}/inventory")
    
    items = response.json()
    
    # Control flow
    if not items:
        print("No items in the inventory.")
        return
    print(f"\n\n Inventory ({len(items)} items)")

    for item in items:
        print_item(item)

# Create function to view by id
def view_by_id():

    item_id = input("Enter item ID: ").strip()
    
    response = requests.get(f"{base_url}/inventory/{item_id}")
    
    # Controll flow
    if response.status_code == 404:
        print(f"Item {item_id} not found.")
        return
    print("\n\nItem:")
    print_item(response.json())

# Create function to add an item
def add_item():
    print("\n\nAdd a new item:")
    name     = input("Name: ").strip()
    quantity = int(input("Quantity: ").strip())
    price    = float(input("Price: $").strip())
    barcode  = input("Barcode (optional, press Enter to skip): ").strip()
    payload  = {"name": name, "quantity": quantity, "price": price, "barcode": barcode}
    response = requests.post(f"{base_url}/inventory", json=payload)
    if response.status_code == 201:
        print("\n\nItem added!")
        print_item(response.json())
    else:
        print(f"Error: {response.json().get('error')}")

# Create function to update an item
def update_item():
    
    item_id  = input("Enter item ID to update: ").strip()
    
    print("Enter a new item and it's value (press Enter to skip):")
    name     = input("New name: ").strip()
    quantity = input("New quantity: ").strip()
    price    = input("New price: $").strip()
    payload  = {}
    if name:     payload["name"]     = name
    if quantity: payload["quantity"] = int(quantity)
    if price:    payload["price"]    = float(price)
    response = requests.patch(f"{base_url}/inventory/{item_id}", json=payload)
    if response.status_code == 200:
        print("\n\nItem updated.")
        print_item(response.json())
    else:
        print(f"Error: {response.json().get('error')}")

# Create function to delete an item
def delete_item():
    
    item_id = input("Enter item ID to delete: ").strip()
    
    confirm = input(f"Are you sure you want to delete item {item_id}? (y/n): ").strip().lower()
    
    #Control flow
    if confirm != "y":
        print("Delete cancelled.")
        return
    
    response = requests.delete(f"{base_url}/inventory/{item_id}")
    
    if response.status_code == 204:
        print(f"Item {item_id} deleted successfully.")
    else:
        print(f"Error: {response.json().get('error')}")

# Create function to search for an item
def search_items():
    name     = input("Enter search term: ").strip()
    response = requests.get(f"{base_url}/inventory/search/{name}")

    # Control flow
    if response.status_code == 404:
        print(f"No item found that matches that '{name}'.")
        return
    
    results = response.json()
    print(f"\n\nFound Results: ({len(results)} items found)")
    for item in results:
        print_item(item)

# Create function to get api's item
def fetch_external():
    barcode  = input("Enter a product's barcode: ").strip()
    response = requests.get(f"{base_url}/external/{barcode}")

    #Control flow
    if response.status_code == 404:
        print("Product not found on OpenFoodFacts.")
        return
    
    if response.status_code != 200:
        print(f"Error: {response.json().get('error')}")
        return
    
    print("\n\nOpenFoodFacts's Item:")
    data = response.json()
    print(f"  Name:       {data.get('name')}")
    print(f"  Brand:      {data.get('brand')}")
    print(f"  Quantity:   {data.get('quantity')}")
    print(f"  Nutriscore: {data.get('nutriscore')}")

# Create function to add an item from the API provided 
def add_from_external():
    barcode  = input("Enter product's barcode: ").strip()
    quantity = int(input("How many would you like to add: ").strip())
    price    = float(input("Price: $").strip())
    payload  = {"quantity": quantity, "price": price}
    response = requests.post(f"{base_url}/external/add/{barcode}", json=payload)
    
    # Control flow
    if response.status_code == 201:
        print("\nProduct added to inventory from OpenFoodFacts!")
        print_item(response.json())
    else:
        print(f"Error: {response.json().get('error')}")

# Create function the main to put it all together
def main():
    print("Starting CLI on port 5555.")

    # Control flow
    while True:
        print_menu()
        choice = input("Choose an option: ").strip()
        if   choice == "0": view_all()
        elif choice == "1": view_by_id()
        elif choice == "2": add_item()
        elif choice == "3": update_item()
        elif choice == "4": delete_item()
        elif choice == "5": search_items()
        elif choice == "6": fetch_external()
        elif choice == "7": add_from_external()
        elif choice == "88":
            print("Bye!")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()