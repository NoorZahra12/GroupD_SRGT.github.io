import tkinter as tk
import json

def display_stock_json():
    # Open the stock.json file for reading
    with open("stock.json", "r") as file:
        # Load the JSON data into a Python data structure
        data = json.load(file)
        # Create a Tkinter window to display the JSON data
        root = tk.Tk()
        root.title("stock.json Contents")
        # Create a text widget to display the JSON data
        text_widget = tk.Text(root)
        text_widget.pack()

        # Iterate over the items in the JSON data and assign IDs
        for i, item in enumerate(data):
            item['itemId'] = f'product_id_num{i}'
        
        # Insert the modified JSON data into the text widget
        text_widget.insert(tk.END, json.dumps(data, indent=4))
        # Run the Tkinter event loop
        root.mainloop()

# Call the function to display stock.json
display_stock_json()
