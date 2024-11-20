import yaml
from datetime import datetime

def generate_readme(data_file, output_file):
    # Load YAML data
    with open(data_file, 'r') as file:
        data = yaml.safe_load(file)

    # Initialize README content
    readme = "# European Robotics Organizations Directory\n\n"

    # Categories mapping for ordering
    category_titles = {
        "established_companies": "🏭 Established Companies",
        "growing_startups": "🚀 Growing Startups",
        "research_centers": "🔬 Research Centers",
        "university_labs": "🎓 University Laboratories",
        "additional_resources": "📚 Additional Resources",
        "components": "🔧 Components",
        "specialized_applications": "✨ Specialized Applications"
    }

    # Generate content by category
    for category, title in category_titles.items():
        if category in data:
            readme += f"## {title}\n\n"
            for subcategory, entries in data[category].items():
                # Subcategories sorted by name
                readme += f"### {subcategory.replace('_', ' ').title()}\n\n"
                entries = sorted(entries, key=lambda x: x.get("name", ""))
                for entry in entries:
                    readme += f"- **{entry['name']}** ({entry.get('location', 'N/A')})\n"
                    readme += f"  - **Specialization**: {entry.get('specialization', entry.get('focus_areas', 'N/A'))}\n"
                    if "links" in entry:
                        links = " • ".join(
                            [f"[{key.capitalize()}]({value})" for key, value in entry["links"].items()]
                        )
                        readme += f"  - **Links**: {links}\n"
                    readme += "\n"

    # Additional Resources
    if "additional_resources" in data:
        readme += "## 📚 Additional Resources\n\n"
        for resource_type, resources in data["additional_resources"].items():
            readme += f"### {resource_type.replace('_', ' ').title()}\n\n"
            for resource in resources:
                readme += f"- **{resource['name']}**: {resource['url']}\n"
            readme += "\n"

    # Footer
    readme += "---\n\n"
    readme += f"*Note: This directory is maintained as part of the robotics community initiative. Last updated: {datetime.now().strftime('%B %Y')}. For corrections or additions, please submit a pull request.*\n"

    # Write to the output file
    with open(output_file, 'w') as file:
        file.write(readme)

    print(f"README file generated: {output_file}")

# Specify input and output files
data_file = "robotics_data.yml"  # Replace with your YAML file path
output_file = "README.md"  # Replace with your desired output file path

# Generate README
generate_readme(data_file, output_file)
