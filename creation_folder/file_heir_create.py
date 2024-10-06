import os

# Define the file hierarchy
structure = {
    'lib_manage': {
        'static': {
            'css': ['style.css'],
            'js': ['script.js'],
            'images': ['logo.png']
        },
        'templates': [
            'base.html',
            'index.html',
            'users.html',
            'racks.html',
            'books.html',
            'requests.html',
            'issues.html',
            'reservations.html',
            'fines.html',
            'bookrack.html'
        ],
        '.env': None,
        'app.py': None,
        'requirements.txt': None
    }
}

# Function to create files and directories
def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            # Create directory
            os.makedirs(path, exist_ok=True)
            # Recursively create subdirectories
            create_structure(path, content)
        elif isinstance(content, list):
            # Create files in directory
            for file_name in content:
                with open(os.path.join(path, file_name), 'w') as f:
                    pass  # Create an empty file
        elif content is None:
            # Create an empty file
            with open(path, 'w') as f:
                pass

# Create the file hierarchy
base_path = os.getcwd()  # Current working directory
create_structure(base_path, structure)

print("File hierarchy created successfully!")
