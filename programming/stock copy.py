import tkinter as tk
from tkinter import ttk
import json
import requests

class Items:
    def __init__(self, itemCode, itemName, chasisNo, engineNo, group, brand, country, quantity, cost, date, p="default_p_value", sp="default_sp_value"):
        self.itemCode = itemCode
        self.itemName = itemName
        self.chasisNo = chasisNo
        self.engineNo = engineNo
        self.group = group
        self.brand = brand
        self.country = country
        self.quantity = quantity
        self.cost = cost
        self.date = date
        self.p = p
        self.sp = sp

def fetch_exchange_rate():
    try:
        response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
        data = response.json()
        return data['rates']
    except Exception as e:
        print(f"Error fetching exchange rates: {e}")
        return {}

def calculate_selling_price(profit_margin_combobox):
    try:
        # Get the index of the last added item
        last_index = len(items_list) - 1
        cost = float(entry_widgets[attributes.index("cost")].get())
        profit_margin = float(profit_margin_combobox.get())  # Get profit margin from Combobox
        selling_price = cost * (1 + profit_margin / 100)  # Calculate selling price
        
        # Update the selling price label for the last added item
        selling_price_labels[last_index].config(text=f"Selling price: {selling_price:.2f}")
        
    except (ValueError, IndexError):
        selling_price_label.config(text="Invalid input or no item added")


def add_item():
    item_data = [entry.get() for entry in entry_widgets]
    item = Items(*item_data)
    items_list.append(item)
    item_string = f"{item.itemName} | {item.itemCode} | {item.brand}"
    item_listbox.insert(tk.END, item_string)
    
    # Create a new selling price label for the new item and store it in the dictionary
    selling_price_label = ttk.Label(add_tab, text="Selling price: 0.00")
    selling_price_label.grid(row=len(attributes) + len(items_list), columnspan=3, pady=5)
    selling_price_labels[len(items_list) - 1] = selling_price_label
    
    update_json()

def delete_item():
    if item_listbox.curselection():
        index = item_listbox.curselection()[0]
        del items_list[index]
        item_listbox.delete(index)
        update_json()

def save_changes():
    selection = item_listbox.curselection()
    if selection:
        index = selection[0]
        for i, attribute in enumerate(attributes):
            setattr(items_list[index], attribute, entry_widgets[i].get())
        modified_item = items_list[index]
        item_string = f"{modified_item.itemName} | {modified_item.itemCode} | {modified_item.brand}"
        item_listbox.delete(index)
        item_listbox.insert(index, item_string)
        update_json()

def show_selected_item(event):
    if item_listbox.curselection():
        index = item_listbox.curselection()[0]
        item = items_list[index]
        for i, attribute in enumerate(attributes):
            entry_widgets[i].delete(0, tk.END)  # Clear previous entry
            entry_widgets[i].insert(0, getattr(item, attribute))

def update_json():
    with open('stock.json', 'w') as json_file:
        json.dump([vars(item) for item in items_list], json_file)

def load_json():
    try:
        with open('stock.json', 'r') as json_file:
            data = json.load(json_file)
            for item_data in data:
                item = Items(**item_data)
                items_list.append(item)
                item_string = f"{item.itemName} | {item.itemCode} | {item.brand}"
                item_listbox.insert(tk.END, item_string)
    except FileNotFoundError:
        pass

root = tk.Tk()
root.title("Item Management System")
root.geometry("650x450")

left_frame = ttk.Frame(root, padding="10")
left_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

right_frame = ttk.Frame(root, padding="10")
right_frame.grid(row=0, column=2, sticky="nsew")

item_listbox = tk.Listbox(left_frame, borderwidth=1, relief="sunken")
item_listbox.pack(fill="both", expand=True)
item_listbox.bind("<<ListboxSelect>>", show_selected_item)

notebook = ttk.Notebook(right_frame)
notebook.pack(fill="both", expand=True)

add_tab = ttk.Frame(notebook)
notebook.add(add_tab, text="Item")

attributes = ["itemCode", "itemName", "chasisNo", "engineNo", "group", "brand", "country", "quantity", "cost", "date"]
entry_widgets = []

for i, attribute in enumerate(attributes):
    ttk.Label(add_tab, text=attribute.capitalize()+":").grid(row=i, column=0, sticky="e", pady=2)
    entry = ttk.Entry(add_tab, width=30)
    entry.grid(row=i, column=1, padx=5, pady=2)
    entry_widgets.append(entry)

profit_label = ttk.Label(add_tab, text="Profit Margin (%):")
profit_label.grid(row=len(attributes), column=0, pady=2)

profit_margin = ttk.Combobox(add_tab, values=list(range(1, 101)))
profit_margin.current(49)  # Set default value to 50
profit_margin.grid(row=len(attributes), column=1, padx=5, pady=2)

calc_button = ttk.Button(add_tab, text="Calculate", command=lambda: calculate_selling_price(profit_margin))
calc_button.grid(row=len(attributes), column=2, pady=2)

selling_price_label = ttk.Label(add_tab, text="Selling price: 0.00")
selling_price_label.grid(row=len(attributes)+2, columnspan=3, pady=10)

# 3 buttons for add, delete, and save changes
add_button = ttk.Button(add_tab, text="Add Item", command=add_item)
add_button.grid(row=len(attributes)+3, column=0, pady=10, padx=5)

delete_button = ttk.Button(add_tab, text="Delete Item", command=delete_item)
delete_button.grid(row=len(attributes)+3, column=1)

save_button = ttk.Button(add_tab, text="Save Changes", command=save_changes)
save_button.grid(row=len(attributes)+3, column=2, pady=10, padx=5)

items_list = []
load_json()

root.mainloop()
