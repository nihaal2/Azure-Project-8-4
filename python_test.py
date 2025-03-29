import os
import xml.etree.ElementTree as ET

# Path to the force-app directory and package.xml file
force_app_path = 'force-app/main/default'
package_xml_path = 'manifest/package.xml'

# Function to get all components in force-app directory
def get_force_app_components(path):
    components = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.xml'):
                component_path = os.path.relpath(os.path.join(root, file), path)
                components.append(component_path)
    return components

# Function to get all components listed in package.xml
def get_package_xml_components(path):
    tree = ET.parse(path)
    root = tree.getroot()
    namespaces = {'sf': 'http://soap.sforce.com/2006/04/metadata'}
    components = []
    for member in root.findall('.//sf:members', namespaces):
        components.append(member.text.replace('/', os.sep) + '.xml')
    return components

# Get components from force-app and package.xml
force_app_components = get_force_app_components(force_app_path)
package_xml_components = get_package_xml_components(package_xml_path)

# Find components in force-app not in package.xml
missing_in_package_xml = set(force_app_components) - set(package_xml_components)

# Print missing components
if missing_in_package_xml:
    print("Components in force-app not in package.xml:")
    for component in missing_in_package_xml:
        print(component)
    exit(1)  # Exit with error code if there are missing components
else:
    print("All components in force-app are included in package.xml.")
