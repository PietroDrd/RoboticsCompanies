#!/usr/bin/env python3

import yaml
import os

def generate_readme(data):
    readme_content = "# European Robotics Organizations Directory\n\n"
    readme_content += "[TOC]\n\n"

    # Generate Categories & Quick Links
    readme_content += "## Categories & Quick Links\n"
    for category_key, category_value in data['categories'].items():
        category_title = category_key.replace('_', ' ').title()
        emoji = "🏭" if category_key == "established_companies" else "🚀" if category_key == "growing_startups" else "🔬" if category_key == "research_centers" else "🎓"
        readme_content += f"- [{emoji} {category_title}](#{category_key.replace('_', '-')})\n"
        for subcategory_key in category_value.keys():
            subcategory_title = subcategory_key.replace('_', ' ').title()
            readme_content += f"  - [{subcategory_title}](#{subcategory_key.replace('_', '-')})\n"
    readme_content += "\n"

    # Generate content for each category and subcategory
    for category_key, category_value in data['categories'].items():
        category_title = category_key.replace('_', ' ').title()
        readme_content += f"## {category_title}\n\n"
        for subcategory_key, companies in category_value.items():
            subcategory_title = subcategory_key.replace('_', ' ').title()
            readme_content += f"### {subcategory_title}\n\n"
            readme_content += "| Company | Location | Specialization | Links |\n"
            readme_content += "|---------|----------|----------------|-------|\n"
            for company in companies:
                name = company.get('name', '')
                location = company.get('location', '')
                specialization = company.get('specialization', '')
                links = company.get('links', {})
                links_str = ' • '.join([f"[{key.capitalize()}]({url})" for key, url in links.items()])
                readme_content += f"| {name} | {location} | {specialization} | {links_str} |\n"
            readme_content += "\n"
    return readme_content

def main():
    # Read data from YAML file
    with open('robotics_data.yml', 'r') as file:
        data = yaml.safe_load(file)

    # Generate README content
    readme_content = generate_readme(data)

    # Write to README.md
    with open('README.md', 'w') as readme_file:
        readme_file.write(readme_content)

    print("README.md has been generated successfully.")

if __name__ == "__main__":
    main()
