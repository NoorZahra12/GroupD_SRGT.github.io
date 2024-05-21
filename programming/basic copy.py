import tkinter as tk
from tkinter import ttk
import json
import requests
import tkinter.messagebox as messagebox




class Sales:
    next_customer_id = 0
    def __init__(self, CSname,):
        self.itemId = f'product_id_num{Items.next_customer_id}'
        Items.next_customer_id += 1
        
        self.name = name









root = tk.Tk()
root.title("SRGT Management System")
root.geometry("750x400")
# Notebook structure
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)





##### ITEM TAB ######
sales_tab = ttk.Frame(notebook)
notebook.add(sales_tab, text="Sales")
# Left frame
left_frame = ttk.Frame(sales_tab, padding="10")
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
right_frame = ttk.Frame(sales_tab, padding="10")
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