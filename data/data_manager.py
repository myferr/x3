
import json
import os

DATA_DIR = "data"
USER_DATA_FILE = os.path.join(DATA_DIR, "users.json")
COOLDOWN_DATA_FILE = os.path.join(DATA_DIR, "cooldowns.json")

def setup_data_files():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "w") as f:
            json.dump({}, f)
    if not os.path.exists(COOLDOWN_DATA_FILE):
        with open(COOLDOWN_DATA_FILE, "w") as f:
            json.dump({}, f)

def load_user_data():
    with open(USER_DATA_FILE, "r") as f:
        return json.load(f)

def save_user_data(data):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_cooldown_data():
    with open(COOLDOWN_DATA_FILE, "r") as f:
        return json.load(f)

def save_cooldown_data(data):
    with open(COOLDOWN_DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
