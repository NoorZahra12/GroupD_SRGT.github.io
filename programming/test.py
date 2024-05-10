import json
# Load items from JSON file
try:
    with open("stock.json", "r") as file:
        items_list = json.load(file)
except FileNotFoundError:
    print("Stock JSON file not found.")
    items_list = []  # Initialize an empty list

# Populate listbox with items from JSON file
for item in items_list:
    # Provide default values for missing keys
    item_name = item.get('itemName', 'N/A')
    item_code = item.get('itemCode', 'N/A')
    brand = item.get('brand', 'N/A')
    item_listbox.insert(tk.END, f"{item_name} | {item_code} | {brand}")
