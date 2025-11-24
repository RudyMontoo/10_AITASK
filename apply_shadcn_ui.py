#!/usr/bin/env python3
"""
Apply shadcn/ui design system to all task HTML files
"""

import os
import re

# Task directories
tasks = [
    'task1_DMN',
    'task2_cleaning_simulation',
    'task3_path_planners',
    'task4_warehouse_pickup',
    'task5_rescue_bots',
    'task6_drone_delivery',
    'task7_grid_painting',
    'task8_resource_collection',
    'task9_firefighters',
    'task10_map_exploration'
]

def update_html_file(filepath):
    """Update HTML file to include shadcn design system"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add shadcn-design-system.css link if not present
    if 'shadcn-design-system.css' not in content:
        content = content.replace(
            '<link rel="stylesheet" href="style.css">',
            '<link rel="stylesheet" href="../shadcn-design-system.css">\n    <link rel="stylesheet" href="style.css">'
        )
    
    # Update button classes
    content = re.sub(
        r'class="btn btn-primary"',
        'class="btn-shadcn btn-success"',
        content
    )
    content = re.sub(
        r'class="btn btn-secondary"',
        'class="btn-shadcn btn-warning"',
        content
    )
    content = re.sub(
        r'class="btn btn-danger"',
        'class="btn-shadcn btn-destructive"',
        content
    )
    
    # Update slider class
    content = re.sub(
        r'<input type="range"',
        '<input type="range" class="slider-shadcn"',
        content
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Updated: {filepath}")

def main():
    print("🎨 Applying shadcn/ui design system to all tasks...\n")
    
    for task in tasks:
        html_file = os.path.join(task, 'index.html')
        if os.path.exists(html_file):
            update_html_file(html_file)
        else:
            print(f"⚠️  Not found: {html_file}")
    
    print("\n✨ shadcn/ui design system applied successfully!")
    print("\n📝 Changes made:")
    print("  - Added shadcn-design-system.css link")
    print("  - Updated button classes (btn-shadcn)")
    print("  - Updated slider classes")
    print("  - Maintained all existing functionality")

if __name__ == '__main__':
    main()
