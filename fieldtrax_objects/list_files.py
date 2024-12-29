import os

folder_path = r'C:\Users\smbab\fieldtrax\frontend'
excluded_extensions = ['.exe', '.dll', '.sys', '.pyc', '.bat', '.ps1',]  # Add the extensions you want to exclude
excluded_folders = ['site-packages', '.pytest_cache','node_modules','coverage','.pytest_cache', 'venv-fieldtrax', 'fieldtrax_objects', 'react-training','routerproj','testfolder,']  # Add the names of folders you want to exclude

for root, dirs, files in os.walk(folder_path):
    # Remove the excluded folders from the search
    dirs[:] = [d for d in dirs if d not in excluded_folders]
    for file in files:
        if not any(file.endswith(ext) for ext in excluded_extensions):
            print(os.path.join(root, file))
            
# folder_path = r'C:\Users\smbab\fieldtrax\frontend'
# excluded_extensions = ['.exe', '.dll', '.sys', '.pyc', '.bat', '.ps1',]  # Add the extensions you want to exclude
# excluded_folders = ['site-packages', '.pytest_cache','node_modules','coverage','.pytest_cache', 'venv-fieldtrax']  # Add the names of folders you want to exclude

# for root, dirs, files in os.walk(folder_path):
#     # Remove the excluded folders from the search
#     dirs[:] = [d for d in dirs if d not in excluded_folders]
#     for file in files:
#         if not any(file.endswith(ext) for ext in excluded_extensions):
#             print(os.path.join(root, file))