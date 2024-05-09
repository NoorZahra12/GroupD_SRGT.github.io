import tkinter as tk
from tkinter import ttk

class Items:
    def __init__(self, itemCode, itemName, chasisNo, engineNo, group, brand, country, quantity, cost, date):
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
    
    def showDetails(self):
        details = f"Item Code: {self.itemCode}\n"
        details += f"Item Name: {self.itemName}\n"
        details += f"Chasis No: {self.chasisNo}\n"
        details += f"Engine No: {self.engineNo}\n"
        details += f"Group: {self.group}\n"
        details += f"Brand: {self.brand}\n"
        details += f"Country: {self.country}\n"
        details += f"Quantity: {self.quantity}\n"
        details += f"Cost: {self.cost}\n"
        details += f"Date: {self.date}\n"
        return details

def add_item():
    item_data = [entry.get() for entry in entry_widgets]
    item = Items(*item_data)
    items_list.append(item)
    item_string = f"{item.itemName} | {item.itemCode} | {item.brand}"
    item_listbox.insert(tk.END, item_string)
    add_button.config(text="Added", state=tk.DISABLED)
    root.after(2000, lambda: reset_button(add_button, "Add Item"))

def delete_item():
    if item_listbox.curselection():
        index = item_listbox.curselection()[0]
        del items_list[index]
        item_listbox.delete(index)
        delete_button.config(text="Deleted", state=tk.DISABLED)
        root.after(2000, lambda: reset_button(delete_button, "Delete Item"))

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
        save_button.config(text="Saved", state=tk.DISABLED)
        root.after(2000, lambda: reset_button(save_button, "Save Changes"))

def reset_button(button, text):
    button.config(text=text, state=tk.NORMAL)

def show_selected_item(event):
    if item_listbox.curselection():
        index = item_listbox.curselection()[0]
        item = items_list[index]
        for i, attribute in enumerate(attributes):
            entry_widgets[i].delete(0, tk.END)  # Clear previous entry
            entry_widgets[i].insert(0, getattr(item, attribute))


root = tk.Tk()
root.title("Item Management System")

# left frame for list
left_frame = ttk.Frame(root, padding="10")
left_frame.grid(row=0, column=0, sticky="nsew")

# right frame for notebook
right_frame = ttk.Frame(root, padding="10")
right_frame.grid(row=0, column=1, sticky="nsew")

# listbox inside the left frame
item_listbox = tk.Listbox(left_frame, borderwidth=2, relief="sunken")
item_listbox.pack(fill="both", expand=True)
item_listbox.bind("<<ListboxSelect>>", show_selected_item)

# notebook inside the right frame
notebook = ttk.Notebook(right_frame)
notebook.pack(fill="both", expand=True)

# tab for managing items
add_tab = ttk.Frame(notebook)
notebook.add(add_tab, text="Item")

# labels and entry widgets for item details in the tab
attributes = ["itemCode", "itemName", "chasisNo", "engineNo", "group", "brand", "country", "quantity", "cost", "date"]
entry_widgets = []
for i, attribute in enumerate(attributes):
    ttk.Label(add_tab, text=attribute.capitalize()+":").grid(row=i, column=0, sticky="e", pady=2)
    entry = ttk.Entry(add_tab, width=30)
    entry.grid(row=i, column=1, padx=5, pady=2)
    entry_widgets.append(entry)

# 3 buttons for add, clear, and delete
add_button = ttk.Button(add_tab, text="Add Item", command=add_item)
add_button.grid(row=len(attributes), column=0, pady=10, padx=5)

delete_button = ttk.Button(add_tab, text="Delete Item", command=delete_item)
delete_button.grid(row=len(attributes), column=1, pady=10, padx=5)

save_button = ttk.Button(add_tab, text="Save Changes", command=save_changes)
save_button.grid(row=len(attributes), column=2, pady=10, padx=5)

items_list = []

root.mainloop()
