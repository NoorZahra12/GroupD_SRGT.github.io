import tkinter as tk
from tkinter import ttk
import json
import requests
import tkinter.messagebox as messagebox


class Items:
    next_item_id = 0
    def __init__(self, itemCode, itemName, chasisNo, engineNo, group, brand, country, quantity, cost, date, profit, sellingPrice):
        self.itemId = f'product_id_num{Items.next_item_id}'
        Items.next_item_id += 1

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
# class Sales:
#     next_customer_id = 0
#     def __init__(self, CSname,):
#         self.itemId = f'product_id_num{Items.next_customer_id}'
#         Items.next_customer_id += 1
        
#         self.name = name























def add_item():
    # Check if both cost and profit are provided
    if entry_widgets[8].get() and entry_widgets[10].get():
        cost = float(entry_widgets[8].get())
        profit = float(entry_widgets[10].get())
        # Calculate selling price
        selling_price = cost * (1 + profit / 100)
        # Update selling price entry widget
        entry_widgets[11].delete(0, tk.END)
        entry_widgets[11].insert(0, f"{selling_price:.1f}")

    # Check if both cost and selling price are provided
    elif entry_widgets[8].get() and entry_widgets[11].get():
        cost = float(entry_widgets[8].get())
        selling_price = float(entry_widgets[11].get())
        # Calculate profit
        profit = ((selling_price - cost) / cost) * 100
        # Update profit entry widget
        entry_widgets[10].delete(0, tk.END)
        entry_widgets[10].insert(0, f"{profit:.1f}")

    item = Items(*[entry.get() for entry in entry_widgets])
    items_list.append(item)
    item_string = f"{item.itemName} | {item.itemCode} | {item.brand}"
    item_listbox.insert(tk.END, item_string)
    update_json()
def delete_item():
    selected_index = item_listbox.curselection()
    if selected_index:
        # Add the deleted item to bin.json
        deleted_item = items_list[selected_index[0]]
        add_to_bin(deleted_item)
        
        # Remove the item from items_list
        del items_list[selected_index[0]]
        update_listbox()
        update_json()
def add_to_bin(deleted_item):
    # Open bin.json for appending
    with open("bin.json", "a") as bin_file:
        # Write the deleted item to bin.json
        json.dump(deleted_item.__dict__, bin_file)
        bin_file.write('\n')
def display_bin_json():
    # Open the bin.json file for reading
    with open("bin.json", "r") as bin_file:
        # Load the JSON data into a Python data structure
        bin_data = [json.loads(line) for line in bin_file]
def show_bin_item_details(event):
    selected_index = bin_listbox.curselection()
    if selected_index:
        details_text.delete("1.0", tk.END)
        selected_item = bin_data[selected_index[0]]
        details_text.insert(tk.END, json.dumps(selected_item, indent=4))
# Function to display deleted items in the bin_listbox
def display_deleted_items():
    # Clear the listbox before adding items
    bin_listbox.delete(0, tk.END)
    # Load deleted items from bin.json
    with open("bin.json", "r") as bin_file:
        deleted_items = json.load(bin_file)
    # Populate the listbox with item names
    for item in deleted_items:
        bin_listbox.insert(tk.END, item["itemName"])
def save_changes():
    selection = item_listbox.curselection()
    if selection:
        index = selection[0]
        for i, attribute in enumerate(attributes):
            setattr(items_list[index], attribute, entry_widgets[i].get())
        if entry_widgets[8].get() and entry_widgets[10].get():
            cost = float(entry_widgets[8].get())
            profit = float(entry_widgets[10].get())
            # Calculate selling price
            selling_price = cost * (1 + profit / 100)
            # Update selling price entry widget
            entry_widgets[11].delete(0, tk.END)
            entry_widgets[11].insert(0, f"{selling_price:.1f}")

        # Check if both cost and selling price are provided
        elif entry_widgets[8].get() and entry_widgets[11].get():
            cost = float(entry_widgets[8].get())
            selling_price = float(entry_widgets[11].get())
            # Calculate profit
            profit = ((selling_price - cost) / cost) * 100
            # Update profit entry widget
            entry_widgets[10].delete(0, tk.END)
            entry_widgets[10].insert(0, f"{profit:.1f}")
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
def display_item_id():
    if item_listbox.curselection():
        index = item_listbox.curselection()[0]
        item_id = items_list[index].itemId
        messagebox.showinfo("Selected Item ID", f"The ID of the selected item is: {item_id}")
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
def search_item(event=None):
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
def search_bin():
    search_query = search_entry.get().lower()
    bin_listbox.delete(0, tk.END)
    found_items = []
    for item in items_list:
        if search_query in item.itemName.lower() or search_query in item.itemCode.lower() or search_query in item.brand.lower():
            found_items.append(f"{item.itemName} | {item.itemCode} | {item.brand}")
    if found_items:
        for found_item in found_items:
            bin_listbox.insert(tk.END, found_item)
    else:
        bin_listbox.insert(tk.END, "No matching results found.")
def reset_list():
    # Clear the search entry
    search_entry.delete(0, tk.END)
    # Reload all items in the listbox
    update_listbox()











root = tk.Tk()
root.title("SRGT Management System")
root.geometry("750x400")
# Notebook structure
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)





















##### ITEM TAB ######
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
search_btn = ttk.Button(search_frame, text="search", command=search_item)
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
# 4 buttons
itemDetail_btnFrame = ttk.Frame(right_frame)
itemDetail_btnFrame.grid(row=len(attributes)+2, columnspan=3, padx=5, pady=5)
add_button = ttk.Button(itemDetail_btnFrame, text="Add", command=add_item)
add_button.grid(row=0, column=0, padx=5)
delete_button = ttk.Button(itemDetail_btnFrame, text="Delete", command=delete_item)
delete_button.grid(row=0, column=1, padx=5)
save_button = ttk.Button(itemDetail_btnFrame, text="Save Changes", command=save_changes)
save_button.grid(row=0, column=2, padx=5)
get_id_button = ttk.Button(itemDetail_btnFrame, text="Get ID", command=display_item_id)
get_id_button.grid(row=0, column=3, padx=5)













# Recycle bin tab
bin_tab = ttk.Frame(notebook)
notebook.add(bin_tab, text="Recycle Bin")
# Button frame
btn_frame = ttk.Frame(bin_tab)
btn_frame.pack(pady=10)






















# # Sales tab for managing sales made
# sales_tab = ttk.Frame(notebook)
# notebook.add(sales_tab, text="Sales")

# Calculate tab
calc_tab = ttk.Frame(notebook)
notebook.add(calc_tab, text="Calculate")




# # Analysis tab
# analysis_tab = ttk.Frame(notebook)
# notebook.add(analysis_tab, text="Analysis")

# Initialize items list
items_list = []
load_from_json()

root.mainloop()