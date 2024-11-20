import tkinter as tk
from tkinter import messagebox, filedialog
import yaml

def update_yaml():
    # Get user inputs
    yaml_file = file_path_var.get()
    category = category_var.get()
    subcategory = subcategory_var.get()
    company_data = text_input.get("1.0", tk.END).strip()
    
    if not yaml_file or not category or not subcategory or not company_data:
        messagebox.showerror("Input Error", "Please fill all fields and load a YAML file.")
        return
    
    try:
        # Parse the pasted YAML-like data
        new_entry = yaml.safe_load(company_data)
        if not isinstance(new_entry, dict) or 'name' not in new_entry:
            messagebox.showerror("Data Error", "Invalid company data. Ensure it is a valid YAML structure.")
            return
        
        # Load the YAML file
        with open(yaml_file, 'r') as file:
            data = yaml.safe_load(file)
        
        # Navigate to category and subcategory
        if category not in data['categories']:
            data['categories'][category] = {}
        if subcategory not in data['categories'][category]:
            data['categories'][category][subcategory] = []
        
        # Check if the entry already exists and update or append
        updated = False
        for company in data['categories'][category][subcategory]:
            if company['name'] == new_entry['name']:
                company.update(new_entry)
                updated = True
                break
        if not updated:
            data['categories'][category][subcategory].append(new_entry)
        
        # Write back to the YAML file
        with open(yaml_file, 'w') as file:
            yaml.dump(data, file, sort_keys=False)
        
        messagebox.showinfo("Success", f"Entry {'updated' if updated else 'added'} successfully.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("YAML Files", "*.yml"), ("All Files", "*.*")])
    if file_path:
        file_path_var.set(file_path)

# GUI Setup
root = tk.Tk()
root.title("YAML Robotics Company Updater")

# File selection
file_path_var = "robotics_data.yml"

# Category
category_var = tk.StringVar()
tk.Label(root, text="Category:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
tk.Entry(root, textvariable=category_var, width=30).grid(row=1, column=1, padx=5, pady=5, sticky="w")

# Subcategory
subcategory_var = tk.StringVar()
tk.Label(root, text="Subcategory:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
tk.Entry(root, textvariable=subcategory_var, width=30).grid(row=2, column=1, padx=5, pady=5, sticky="w")

# Text input for company data
tk.Label(root, text="Company Data (YAML format):").grid(row=3, column=0, padx=5, pady=5, sticky="nw")
text_input = tk.Text(root, width=60, height=15)
text_input.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky="w")

# Buttons
tk.Button(root, text="Update YAML", command=update_yaml).grid(row=4, column=1, pady=10, sticky="e")

root.mainloop()
