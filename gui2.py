import tkinter as tk
from tkinter import messagebox, filedialog
import yaml
import os

attempts = 0

def update_yaml():
    global attempts
    attempts += 1

    # Get user inputs
    yaml_file = file_path_var.get()
    category = category_var.get()
    subcategory = subcategory_var.get()
    
    name = name_var.get()
    location = location_var.get()
    specialization = specialization_var.get()
    website = website_var.get()
    careers = careers_var.get()
    linkedin = linkedin_var.get()
    
    if not yaml_file or not category or not subcategory or not name:
        messagebox.showerror("Input Error", "Please fill all fields and load a YAML file.")
        return
    
    # Assemble new entry
    new_entry = {
        'name': name,
        'location': location,
        'specialization': specialization,
        'links': {
            'website': website,
            'careers': careers,
            'linkedin': linkedin
        }
    }
    
    # Check if the entry is complete
    if not is_entry_complete(new_entry):
        # Save incomplete entry to temporary yaml file
        temp_file = 'incomplete_entries.yaml'
        if os.path.exists(temp_file):
            with open(temp_file, 'r') as f:
                incomplete_entries = yaml.safe_load(f)
                if incomplete_entries is None:
                    incomplete_entries = []
        else:
            incomplete_entries = []
        incomplete_entries.append(new_entry)
        with open(temp_file, 'w') as f:
            yaml.dump(incomplete_entries, f)
        
        if attempts < 2:
            messagebox.showwarning("Incomplete Entry", "Entry is incomplete. Please provide the missing details and try again.")
            return
        else:
            messagebox.showerror("Incomplete Entry", "Entry is still incomplete after second attempt. Exiting.")
            attempts = 0  # reset attempts
            return
        
    # Entry is complete
    try:
        # Load the YAML file
        with open(yaml_file, 'r') as file:
            data = yaml.safe_load(file)
            if data is None:
                data = {}
    except FileNotFoundError:
        data = {}

    # Navigate to category and subcategory
    if 'categories' not in data:
        data['categories'] = {}
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
    attempts = 0  # reset attempts after success
    # Clear the input fields
    category_var.set('')
    subcategory_var.set('')
    name_var.set('')
    location_var.set('')
    specialization_var.set('')
    website_var.set('')
    careers_var.set('')
    linkedin_var.set('')

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("YAML Files", "*.yml;*.yaml"), ("All Files", "*.*")])
    if file_path:
        file_path_var.set(file_path)

def is_entry_complete(entry):
    required_fields = ['name', 'location', 'specialization', 'links']
    for field in required_fields:
        if field not in entry or not entry[field]:
            return False
    link_fields = ['website', 'careers', 'linkedin']
    for link_field in link_fields:
        if link_field not in entry['links'] or not entry['links'][link_field]:
            return False
    return True

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

# Company Details
name_var = tk.StringVar()
tk.Label(root, text="Company Name:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
tk.Entry(root, textvariable=name_var, width=50).grid(row=3, column=1, padx=5, pady=5, sticky="w")

location_var = tk.StringVar()
tk.Label(root, text="Location:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
tk.Entry(root, textvariable=location_var, width=50).grid(row=4, column=1, padx=5, pady=5, sticky="w")

specialization_var = tk.StringVar()
tk.Label(root, text="Specialization:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
tk.Entry(root, textvariable=specialization_var, width=50).grid(row=5, column=1, padx=5, pady=5, sticky="w")

# Links
website_var = tk.StringVar()
tk.Label(root, text="Website URL:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
tk.Entry(root, textvariable=website_var, width=50).grid(row=6, column=1, padx=5, pady=5, sticky="w")

careers_var = tk.StringVar()
tk.Label(root, text="Careers URL:").grid(row=7, column=0, padx=5, pady=5, sticky="w")
tk.Entry(root, textvariable=careers_var, width=50).grid(row=7, column=1, padx=5, pady=5, sticky="w")

linkedin_var = tk.StringVar()
tk.Label(root, text="LinkedIn URL:").grid(row=8, column=0, padx=5, pady=5, sticky="w")
tk.Entry(root, textvariable=linkedin_var, width=50).grid(row=8, column=1, padx=5, pady=5, sticky="w")

# Buttons
tk.Button(root, text="Update YAML", command=update_yaml).grid(row=9, column=1, pady=10, sticky="e")

root.mainloop()
