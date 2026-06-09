#!/usr/bin/env python3
import os
import re

# Base path for the project
BASE_PATH = "/workspace/educatif-platform/educatif-platform"

# All subjects with their paths and display names
SUBJECTS = [
    ("Mathematiques/mathematiques.html", "Mathematiques/math.html", "Math"),
    ("Physique/physique.html", "Physique/physique.html", "Physique"),
    ("Electrique/electrique.html", "Electrique/electrique.html", "Électrique"),
    ("Mecanique/mecanique.html", "Mecanique/mecanique.html", "Mécanique"),
    ("Langues/Francais/francais.html", "Langues/Francais/francais.html", "Français"),
    ("Langues/Anglais/anglais.html", "Langues/Anglais/anglais.html", "Anglais"),
    ("Langues/Arabe/arabe.html", "Langues/Arabe/arabe.html", "Arabe"),
    ("Informatique/informatique.html", "Informatique/informatique.html", "Info"),
    ("Sciences-Humaines/Philosophie/philosophie.html", "Sciences-Humaines/Philosophie/philosophie.html", "Philo"),
]

def get_relative_path(current_file, target_file):
    """Calculate relative path from current file to target file"""
    current_dir = os.path.dirname(current_file)
    rel_path = os.path.relpath(target_file, current_dir)
    return rel_path

def get_depth(current_file):
    """Get the depth of the file from the base path"""
    rel_path = os.path.relpath(current_file, BASE_PATH)
    depth = rel_path.count(os.sep)
    return depth

def generate_nav_links(current_file, exclude_subject):
    """Generate navigation links excluding the current subject"""
    depth = get_depth(current_file)
    prefix = "../" * depth if depth > 0 else ""

    nav_items = ['<a href="' + prefix + 'index.html">Accueil</a>']

    for _, subject_path, display_name in SUBJECTS:
        subject_file = os.path.join(BASE_PATH, subject_path)
        rel_path = get_relative_path(current_file, subject_file)
        if display_name != exclude_subject:
            nav_items.append('<a href="' + rel_path + '">' + display_name + '</a>')

    return '\n                '.join(nav_items)

def update_file(filepath):
    """Update a single HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Determine depth and paths
    depth = get_depth(filepath)
    prefix = "../" * depth
    img_prefix = prefix if prefix else ""

    # Get filename to determine subject
    filename = os.path.basename(filepath)
    dirname = os.path.basename(os.path.dirname(filepath))

    # Determine exclude subject based on file location
    exclude_subject = None

    # Subject page patterns (e.g., mathematiques.html, physique.html)
    subject_match = re.match(r'^([a-zA-Z-]+)\.html$', filename)
    if subject_match:
        subject_name = subject_match.group(1).lower()
        subject_map = {
            'mathematiques': 'Math', 'math': 'Math',
            'physique': 'Physique',
            'electrique': 'Électrique',
            'mecanique': 'Mécanique',
            'francais': 'Français',
            'anglais': 'Anglais',
            'arabe': 'Arabe',
            'informatique': 'Info',
            'philosophie': 'Philo',
            'arts': 'Arts',
            'histoire': 'Histoire',
            'geographie': 'Geographie',
            'sciences': 'Sciences',
        }
        exclude_subject = subject_map.get(subject_name)
    else:
        # Lesson page - determine subject from directory
        dir_subject_map = {
            'Mathematiques': 'Math',
            'Physique': 'Physique',
            'Electrique': 'Électrique',
            'Mecanique': 'Mécanique',
            'Langues': None,  # Will need to check subdirectory
            'Informatique': 'Info',
            'Sciences-Humaines': None,
            'Arts': 'Arts',
            'Sciences': 'Sciences',
        }

        if dirname == 'Langues':
            subdir = os.path.basename(os.path.dirname(filepath))
            if subdir == 'Francais':
                exclude_subject = 'Français'
            elif subdir == 'Anglais':
                exclude_subject = 'Anglais'
            elif subdir == 'Arabe':
                exclude_subject = 'Arabe'
        elif dirname == 'Sciences-Humaines':
            subdir = os.path.basename(os.path.dirname(filepath))
            if subdir == 'Philosophie':
                exclude_subject = 'Philo'
            elif subdir == 'Histoire':
                exclude_subject = 'Histoire'
            elif subdir == 'Geographie':
                exclude_subject = 'Geographie'
        else:
            exclude_subject = dir_subject_map.get(dirname)

    # Generate new navigation
    nav_links = generate_nav_links(filepath, exclude_subject)

    # Update header logo section
    old_header_pattern = r'<a href="[^"]*" class="logo">\s*<div class="logo-icon">📚</div>\s*<span>[^<]*</span>\s*</a>'
    new_header = f'''<a href="{prefix}index.html" class="logo">
                <img src="{img_prefix}imgs/badri.png" alt="Logo" class="logo-image">
                <span class="logo-text">From Bac-2-Fac</span>
            </a>'''
    content = re.sub(old_header_pattern, new_header, content)

    # Also check for logo with img tag but wrong path
    old_logo_pattern = r'<a href="[^"]*" class="logo">\s*<img src="[^"]*logo\.png"[^>]*>\s*<span class="logo-text">[^<]*</span>\s*</a>'
    content = re.sub(old_logo_pattern, new_header, content)

    # Update navigation
    nav_pattern = r'<nav class="nav-links">.*?</nav>'
    new_nav = f'''<nav class="nav-links">
                {nav_links}
            </nav>'''
    content = re.sub(nav_pattern, new_nav, content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return True

def main():
    """Main function to update all HTML files"""
    html_files = []

    for root, dirs, files in os.walk(BASE_PATH):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))

    # Skip Shared directory
    html_files = [f for f in html_files if 'Shared' not in f]

    print(f"Found {len(html_files)} HTML files to update")

    for filepath in sorted(html_files):
        try:
            update_file(filepath)
            rel_path = os.path.relpath(filepath, BASE_PATH)
            print(f"✓ Updated: {rel_path}")
        except Exception as e:
            rel_path = os.path.relpath(filepath, BASE_PATH)
            print(f"✗ Error updating {rel_path}: {e}")

if __name__ == "__main__":
    main()