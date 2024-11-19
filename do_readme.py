#!/usr/bin/env python3

import yaml
import os

def generate_readme(data):
    readme_content = "# European Robotics Organizations Directory\n\n"
    readme_content += "[TOC]\n\n"

    # Generate Categories & Quick Links
    readme_content += "## Categories & Quick Links\n"
    for category_key, category_value in data.get('categories', {}).items():
        category_title = category_key.replace('_', ' ').title()
        emoji = "🏭" if category_key == "established_companies" else \
                "🚀" if category_key == "growing_startups" else \
                "🔬" if category_key == "research_centers" else \
                "🎓" if category_key == "university_labs" else \
                "🔧"
        readme_content += f"- [{emoji} {category_title}](#{category_key.replace('_', '-')})\n"

        if isinstance(category_value, dict):  # Nested subcategories
            for subcategory_key in category_value.keys():
                subcategory_title = subcategory_key.replace('_', ' ').title()
                readme_content += f"  - [{subcategory_title}](#{subcategory_key.replace('_', '-')})\n"
    readme_content += "\n"

    # Generate content for each category and subcategory
    for category_key, category_value in data.get('categories', {}).items():
        category_title = category_key.replace('_', ' ').title()
        readme_content += f"## {category_title}\n\n"

        if isinstance(category_value, dict):  # Handle subcategories
            for subcategory_key, companies in category_value.items():
                subcategory_title = subcategory_key.replace('_', ' ').title()
                readme_content += f"### {subcategory_title}\n\n"
                readme_content += generate_table(companies)
        elif isinstance(category_value, list):  # Flat list
            readme_content += generate_table(category_value)

    # Add Resources Section
    if 'resources' in data:
        readme_content += "## Resources\n\n"
        for resource_key, resources in data['resources'].items():
            resource_title = resource_key.replace('_', ' ').title()
            readme_content += f"### {resource_title}\n\n"
            readme_content += "| Name | Link |\n"
            readme_content += "|------|------|\n"
            for resource in resources:
                name = resource.get('name', '')
                url = resource.get('url', '')
                readme_content += f"| {name} | [Link]({url}) |\n"
            readme_content += "\n"

    return readme_content

def generate_table(companies):
    """
    Generate Markdown table for a list of companies or entries.
    """
    if not companies:
        return "No entries available.\n\n"

    table = "| Name | Location | Specialization | Links |\n"
    table += "|------|----------|----------------|-------|\n"
    for company in companies:
        name = company.get('name', company.get('institution', ''))
        location = company.get('location', '')
        specialization = company.get('specialization', company.get('focus_areas', ''))
        links = company.get('links', {})
        links_str = ' • '.join([f"[{key.capitalize()}]({url})" for key, url in links.items()])
        table += f"| {name} | {location} | {specialization} | {links_str} |\n"
    table += "\n"
    return table

def main():
    # Read data from YAML file
    yaml_file = 'robotics_data.yml'
    if not os.path.exists(yaml_file):
        print(f"Error: {yaml_file} not found.")
        return

    with open(yaml_file, 'r') as file:
        try:
            data = yaml.safe_load(file)
            if not data:
                print("Error: YAML file is empty or invalid.")
                return
        except yaml.YAMLError as e:
            print(f"Error parsing YAML: {e}")
            return

    # Generate README content
    readme_content = generate_readme(data)

    # Write to README.md with UTF-8 encoding
    with open('README.md', 'w', encoding='utf-8') as readme_file:
        readme_file.write(readme_content)

    print("README.md has been generated successfully.")
    

if __name__ == "__main__":
    main()
