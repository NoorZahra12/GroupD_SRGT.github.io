import tkinter as tk
from tkinter import ttk
import json
import requests

class Items:
    def __init__(self, itemCode, itemName, chasisNo, engineNo, group, brand, country, quantity, cost, date, p=0.0, sp=0.0):
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


class Sales:
    def __init__(self, name):
        self.name = name

def add_item():
    item_data = [entry.get() for entry in entry_widgets]
    if len(item_data) < 12:
        item_data.extend(["0", "0.00"])
    item = Items(*item_data)
    items_list.append(item)
    item_string = f"{item.itemName} | {item.itemCode} | {item.brand}"
    item_listbox.insert(tk.END, item_string)
    update_json()


def delete_item():
    selected_index = item_listbox.curselection()
    if selected_index:
        del items_list[selected_index[0]]
        update_listbox()
        save_to_json()

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


def fetch_exchange_rate():
    try:
        response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
        data = response.json()
        return data['rates']
    except Exception as e:
        print(f"Error fetching exchange rates: {e}")
        return {}

def calculate_selling_price():
    try:
        erates = fetch_exchange_rate()
        cost = float(cost_entry.get())
        profit_margin = float(profit_combobox.get())
        
        # Get the exchange rate for USD
        usd_rate = erates['USD']
        # Convert the cost to USD
        cost_usd = cost / usd_rate
        # Calculate the selling price in USD
        selling_price_usd = cost_usd * (1 + profit_margin / 100)
        # Display the selling price in USD
        selling_price_num.config(text=f"{selling_price_usd:.2f}")
    except ValueError:
        selling_price_num.config(text="Invalid input")
    except Exception as e:
        selling_price_num.config(text=f"Error: {e}")



def update_listbox():
    item_listbox.delete(0, tk.END)
    for item in items_list:
        item_listbox.insert(tk.END, f"{item.itemName} | {item.itemCode} | {item.brand}")

def load_from_json():
    try:
        with open("stock.json", "r") as file:
            data = json.load(file)
            for item_data in data:
                # Replace missing attributes with default values
                item_data_with_defaults = {attr: item_data.get(attr, '') for attr in attributes}
                item = Items(**item_data_with_defaults)
                items_list.append(item)
                item_string = f"{item.itemName} | {item.itemCode} | {item.brand}"
                item_listbox.insert(tk.END, item_string)
    except FileNotFoundError:
        print("Stock JSON file not found.")


def update_json():
    try:
        with open('stock.json', 'w') as json_file:
            data = []
            for item in items_list:
                item_data = vars(item)
                # Replace empty strings with default values before saving
                for attr in attributes:
                    if not item_data[attr]:
                        item_data[attr] = ''
                data.append(item_data)
            json.dump(data, json_file)
    except Exception as e:
        print(f"Error updating JSON file: {e}")


def show_selected_item(event):
    if item_listbox.curselection():
        index = item_listbox.curselection()[0]
        item = items_list[index]
        for i, attribute in enumerate(attributes):
            entry_widgets[i].delete(0, tk.END)  # Clear previous entry
            entry_widgets[i].insert(0, getattr(item, attribute))


def filter_items(event=None):
    search_query = search_entry.get().lower()
    item_listbox.delete(0, tk.END)
    found_items = []
    for item in items_list:
        if search_query in item["itemName"].lower() or \
        search_query in item["itemCode"].lower() or \
        search_query in item["brand"].lower():
            found_items.append(f"{item['itemName']} | {item['itemCode']} | {item['brand']}")
    if found_items:
        for found_item in found_items:
            item_listbox.insert(tk.END, found_item)
    else:
        item_listbox.insert(tk.END, "No matching results found.")

root = tk.Tk()
root.title("Item Management System")
root.geometry("750x400")

# Notebook structure
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

item_tab = ttk.Frame(notebook)
notebook.add(item_tab, text="Items")

# Left frame
left_frame = ttk.Frame(item_tab, padding="10")
left_frame.grid(row=0, column=0, sticky="nsew")
left_frame.rowconfigure(1, weight=1)

search_frame = ttk.Frame(left_frame)
search_frame.grid(row=0, column=0, sticky="nsew")

search_label = ttk.Label(search_frame, text="Search:")
search_label.grid(row=0, column=0, padx=5, pady=5)

search_entry = ttk.Entry(search_frame)
search_entry.grid(row=0, column=1, padx=5, pady=5)

search_btn = ttk.Button(search_frame, text="search")
search_btn.grid(row=0,column=2)

item_listbox = tk.Listbox(left_frame, borderwidth=1, relief="sunken")
item_listbox.grid(row=1, column=0, sticky="nsew")
item_listbox.bind("<<ListboxSelect>>", show_selected_item)

scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=item_listbox.yview)
scrollbar.grid(row=1, column=1, sticky="ns")
item_listbox.config(yscrollcommand=scrollbar.set)

# Right frame
right_frame = ttk.Frame(item_tab, padding="10")
right_frame.grid(row=0, column=1, sticky="nsew")

attributes = ["itemCode", "itemName", "chasisNo", "engineNo", "group", "brand", "country", "quantity", "cost", "date"]
entry_widgets = []

for i, attribute in enumerate(attributes):
    ttk.Label(right_frame, text=attribute.capitalize() + ":").grid(row=i, column=0, sticky="e", padx=5, pady=2)
    entry = ttk.Entry(right_frame, width=30)
    entry.grid(row=i, column=1, padx=5, pady=2)
    entry_widgets.append(entry)

cost_entry = entry_widgets[8]

profit_label = ttk.Label(right_frame, text="Profit Margin (%):")
profit_label.grid(row=len(attributes), column=0, padx=5, pady=2)

profit_combobox = ttk.Combobox(right_frame, values=list(range(1, 101)))
profit_combobox.grid(row=len(attributes), column=1, padx=5, pady=2)

selling_price_label = ttk.Label(right_frame, text="Selling Price:")
selling_price_label.grid(row=len(attributes)+1, column=0, padx=5, pady=2)

selling_price_num = ttk.Label(right_frame, text="0.00")
selling_price_num.grid(row=len(attributes)+1, column=1, padx=5, pady=2)


# 3 buttons
itemDetail3btnFrame = ttk.Frame(right_frame)
add_button = ttk.Button(itemDetail3btnFrame, text="Add", command=add_item)
add_button.grid(row=len(attributes)+2, column=0, padx=5, pady=5)

delete_button = ttk.Button(itemDetail3btnFrame, text="Delete", command=delete_item)
delete_button.grid(row=len(attributes)+2, column=1, padx=5, pady=5)

save_button = ttk.Button(itemDetail3btnFrame, text="Save Changes", command=save_changes)
save_button.grid(row=len(attributes)+2, column=2, padx=5, pady=5)

# Sales tab for managing sales made
sales_tab = ttk.Frame(notebook)
notebook.add(sales_tab, text="Sales")

# Calculate tab
calc_tab = ttk.Frame(notebook)
notebook.add(calc_tab, text="Calculate")

# Recycle Bin tab
bin_tab = ttk.Frame(notebook)
notebook.add(bin_tab, text="Recycle Bin")

# Analysis tab
analysis_tab = ttk.Frame(notebook)
notebook.add(analysis_tab, text="Analysis")


# Initialize items list
items_list = []
load_from_json()

root.mainloop()