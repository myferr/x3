import os
import shutil
import glob

# Define paths
project_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.dirname(project_dir)
backup_dir = os.path.join(parent_dir, 'temp_backup')
data_dir = os.path.join(project_dir, 'data')
backup_data_dir = os.path.join(backup_dir, 'data')

# --- 1. Create backup directory ---
if os.path.exists(backup_dir):
    shutil.rmtree(backup_dir)
os.makedirs(backup_data_dir)

print("Backing up data...")

# --- 2. Backup .env file ---
env_file = os.path.join(project_dir, '.env')
if os.path.exists(env_file):
    shutil.copy(env_file, backup_dir)
    print("  - .env file backed up.")

# --- 3. Backup all .json files from data directory ---
json_files = glob.glob(os.path.join(data_dir, '*.json'))
if json_files:
    for f in json_files:
        shutil.copy(f, backup_data_dir)
    print(f"  - Backed up {len(json_files)} JSON files from data/.")
else:
    print("  - No JSON files found in data/ to back up.")

print("\nUpdating repository...")

# --- 4. Go to parent directory and remove old project folder ---
os.chdir(parent_dir)
shutil.rmtree(project_dir)
print("- Removed old project directory.")

# --- 5. Clone the new repository ---
repo_url = "https://github.com/myferr/x3.git"
os.system(f"git clone {repo_url} x3")
print("- Cloned fresh repository.")

# Change into the new project directory
os.chdir(project_dir)

# --- 6. Restore .env file ---
backup_env_file = os.path.join(backup_dir, '.env')
if os.path.exists(backup_env_file):
    shutil.move(backup_env_file, project_dir)
    print("\nRestoring data...")
    print("  - .env file restored.")

# --- 7. Restore all .json files ---
restored_data_dir = os.path.join(project_dir, 'data')
backup_json_files = glob.glob(os.path.join(backup_data_dir, '*.json'))
if backup_json_files:
    if not os.path.exists(restored_data_dir):
        os.makedirs(restored_data_dir)
    for f in backup_json_files:
        shutil.move(f, restored_data_dir)
    print(f"  - Restored {len(backup_json_files)} JSON files to data/.")

# --- 8. Clean up backup directory ---
shutil.rmtree(backup_dir)
print("- Cleaned up backup directory.")

print("\nUpdate complete.")