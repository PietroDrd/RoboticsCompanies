import yaml
import copy
import os

# Load existing YAML data
with open('robotics_companies.yaml', 'r') as f:
    data = yaml.safe_load(f)

# Function to get user input for a new entry
def get_new_entry():
    entry = {}
    # Ask for the category and subcategory
    categories = list(data['categories'].keys())
    print("Available categories:")
    for i, category in enumerate(categories):
        print(f"{i+1}. {category}")
    cat_choice = int(input("Select a category (number): ")) - 1
    category = categories[cat_choice]

    subcategories = list(data['categories'][category].keys())
    print(f"Available subcategories in '{category}':")
    for i, subcat in enumerate(subcategories):
        print(f"{i+1}. {subcat}")
    subcat_choice = int(input("Select a subcategory (number): ")) - 1
    subcategory = subcategories[subcat_choice]

    # Now, ask for entry details
    entry['name'] = input("Enter company name: ")
    entry['location'] = input("Enter company location: ")
    entry['specialization'] = input("Enter specialization: ")

    # Links
    entry['links'] = {}
    entry['links']['website'] = input("Enter website URL: ")
    entry['links']['careers'] = input("Enter careers URL: ")
    entry['links']['linkedin'] = input("Enter LinkedIn URL: ")

    return category, subcategory, entry

# Function to check if entry is complete
def is_entry_complete(entry):
    required_fields = ['name', 'location', 'specialization', 'links']
    for field in required_fields:
        if not entry.get(field):
            return False
    link_fields = ['website', 'careers', 'linkedin']
    for link_field in link_fields:
        if not entry['links'].get(link_field):
            return False
    return True

# Get new entry from user
category, subcategory, entry = get_new_entry()

# Check if entry is complete
if not is_entry_complete(entry):
    # Save incomplete entry to temporary yaml file
    temp_file = 'incomplete_entries.yaml'
    if os.path.exists(temp_file):
        with open(temp_file, 'r') as f:
            incomplete_entries = yaml.safe_load(f)
    else:
        incomplete_entries = []
    incomplete_entries.append(entry)
    with open(temp_file, 'w') as f:
        yaml.dump(incomplete_entries, f)
    print("Entry is incomplete. Please provide the missing details.")

    # Ask the user to input it again (only once)
    category, subcategory, entry = get_new_entry()

    if not is_entry_complete(entry):
        print("Entry is still incomplete. Exiting.")
        exit()
else:
    print("Entry is complete.")

# Add the new entry to the existing data
# Ensure that we do not ruin the existing YAML data
updated_data = copy.deepcopy(data)

# Add the new entry in the correct spot and category
updated_data['categories'][category][subcategory].append(entry)

# Save the updated data back to the YAML file
with open('robotics_companies.yaml', 'w') as f:
    yaml.dump(updated_data, f, sort_keys=False)

print("New entry added successfully.")
