import yaml

# Define the function to add or update an entry
def update_robotics_companies(yaml_file, category, subcategory, new_entry):
    try:
        # Load the YAML file
        with open(yaml_file, 'r') as file:
            data = yaml.safe_load(file)
        
        # Navigate to the required category and subcategory
        if category not in data['categories']:
            data['categories'][category] = {}
        if subcategory not in data['categories'][category]:
            data['categories'][category][subcategory] = []

        # Check if the entry already exists
        updated = False
        for company in data['categories'][category][subcategory]:
            if company['name'] == new_entry['name']:
                company.update(new_entry)
                updated = True
                break
        
        # Add the entry if it doesn't exist
        if not updated:
            data['categories'][category][subcategory].append(new_entry)
        
        # Write back to the YAML file
        with open(yaml_file, 'w') as file:
            yaml.dump(data, file, sort_keys=False)
        
        print(f"Entry {'updated' if updated else 'added'} successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
new_company = {
    "name": "New Robotics Company",
    "location": "USA",
    "specialization": "Autonomous systems",
    "links": {
        "website": "https://newroboticscompany.com",
        "careers": "https://newroboticscompany.com/careers",
        "linkedin": "https://www.linkedin.com/company/new-robotics-company/"
    }
}

# Call the function
yaml_file_path = "robotics_data.yml"  # Path to your YAML file
update_robotics_companies(yaml_file_path, "established_companies", "industrial_manufacturing", new_company)
