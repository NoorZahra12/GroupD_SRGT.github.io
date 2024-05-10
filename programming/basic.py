import tkinter as tk
from tkinter import ttk
import json
import requests

class Items:
    def __init__(self, itemCode, itemName, chasisNo, engineNo, group, brand, country, quantity, cost, date, profit, sellingPrice):
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
        self.profit = profit
        self.sellingPrice = sellingPrice


class Sales:
    def __init__(self, name):
        self.name = name

def add_item():
    item_data = [entry.get() for entry in entry_widgets]
    if len(item_data) < 12:
        item_data.extend(["0", "0.0", "0.0"])  # Add default values for profit and selling price
    item = Items(*item_data)
    
    # Check if both cost and profit are provided
    if item.cost and item.profit:
        cost = float(item.cost)
        profit = float(item.profit)
        calculate_selling_price_and_save(len(items_list), cost, profit)
    # Check if both cost and selling price are provided
    elif item.cost and item.sellingPrice:
        cost = float(item.cost)
        selling_price = float(item.sellingPrice)
        # Calculate profit
        profit = ((selling_price - cost) / cost) * 100
        item.profit = f"{profit:.1f}"  # Format profit to have 1 decimal point
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
        
        # Check if both cost and profit are provided
        if modified_item.cost and modified_item.profit:
            cost = float(modified_item.cost)
            profit = float(modified_item.profit)
            calculate_selling_price_and_save(index, cost, profit)
        # Check if both cost and selling price are provided
        elif modified_item.cost and modified_item.sellingPrice:
            cost = float(modified_item.cost)
            selling_price = float(modified_item.sellingPrice)
            # Calculate profit
            profit = ((selling_price - cost) / cost) * 100
            items_list[index].profit = f"{profit:.1f}"  # Format profit to have 1 decimal point
        
        update_json()

def calculate_selling_price_and_save(index, cost, profit):
    # Calculate the selling price
    selling_price = cost * (1 + profit / 100)
    # Save the calculated selling price to the item
    items_list[index].sellingPrice = f"{selling_price:.1f}"  # Format selling price to have 1 decimal point


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
        # Get the cost from the cost entry
        cost = float(entry_widgets[8].get())
        # Get the profit margin from the profit margin entry
        profit_margin = float(entry_widgets[-1].get())
        
        # Calculate the selling price
        erates = fetch_exchange_rate()
        usd_rate = erates['USD']
        cost_usd = cost / usd_rate
        selling_price_usd = cost_usd * (1 + profit_margin / 100)
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
            entry_widgets[i].delete(0, tk.END)
            entry_widgets[i].insert(0, getattr(item, attribute))


def searching(event=None):
    search_query = search_entry.get().lower()
    item_listbox.delete(0, tk.END)
    found_items = []
    for item in items_list:
        if search_query in item.itemName.lower() or search_query in item.itemCode.lower() or search_query in item.brand.lower():
            found_items.append(f"{item.itemName} | {item.itemCode} | {item.brand}")
    if found_items:
        for found_item in found_items:
            item_listbox.insert(tk.END, found_item)
    else:
        item_listbox.insert(tk.END, "No matching results found.")

def reset_list():
    # Clear the search entry
    search_entry.delete(0, tk.END)
    # Reload all items in the listbox
    update_listbox()


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

search_btn = ttk.Button(search_frame, text="search", command=searching)
search_btn.grid(row=0,column=2)

reset_button = ttk.Button(search_frame, text="X", command=reset_list, width=3)
reset_button.grid(row=0, column=3)


item_listbox = tk.Listbox(left_frame, borderwidth=1, relief="sunken")
item_listbox.grid(row=1, column=0, sticky="nsew")
item_listbox.bind("<<ListboxSelect>>", show_selected_item)

scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=item_listbox.yview)
scrollbar.grid(row=1, column=1, sticky="ns")
item_listbox.config(yscrollcommand=scrollbar.set)

# Right frame
right_frame = ttk.Frame(item_tab, padding="10")
right_frame.grid(row=0, column=1, sticky="nsew")

attributes = ["itemCode", "itemName", "chasisNo", "engineNo", "group", "brand", "country", "quantity", "cost", "date","profit","sellingPrice"]
entry_widgets = []

for i, attribute in enumerate(attributes):
    ttk.Label(right_frame, text=attribute.capitalize() + ":").grid(row=i, column=0, sticky="e", padx=5, pady=2)
    entry = ttk.Entry(right_frame, width=30)
    entry.grid(row=i, column=1, padx=5, pady=2)
    entry_widgets.append(entry)

cost_entry = entry_widgets[8]
profit_entry = entry_widgets[10]
sellingPrice_entry = entry_widgets[11]


# 3 buttons
itemDetail3btnFrame = ttk.Frame(right_frame)
itemDetail3btnFrame.grid(row=len(attributes)+2, columnspan=3, padx=5, pady=5)

add_button = ttk.Button(itemDetail3btnFrame, text="Add", command=add_item)
add_button.grid(row=0, column=0)

delete_button = ttk.Button(itemDetail3btnFrame, text="Delete", command=delete_item)
delete_button.grid(row=0, column=1, padx=10)

save_button = ttk.Button(itemDetail3btnFrame, text="Save Changes", command=save_changes)
save_button.grid(row=0, column=2)

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