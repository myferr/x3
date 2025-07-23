import json
import os

DATA_DIR = "data"
USER_DATA_FILE = os.path.join(DATA_DIR, "users.json")
COOLDOWN_DATA_FILE = os.path.join(DATA_DIR, "cooldowns.json")
COOLDOWN_FILE = "cooldown.json"

# Operator role persistence
OP_ROLE_FILE = os.path.join(DATA_DIR, "operator_role.json")

def save_operator_role(guild_id, role_id):
    data = {}
    if os.path.exists(OP_ROLE_FILE):
        with open(OP_ROLE_FILE, "r") as f:
            data = json.load(f)
    data[guild_id] = role_id
    with open(OP_ROLE_FILE, "w") as f:
        json.dump(data, f)

def load_operator_role(guild_id):
    if not os.path.exists(OP_ROLE_FILE):
        return None
    with open(OP_ROLE_FILE, "r") as f:
        data = json.load(f)
    return data.get(guild_id)
import json
import os

DATA_DIR = "data"
USER_DATA_FILE = os.path.join(DATA_DIR, "users.json")
COOLDOWN_DATA_FILE = os.path.join(DATA_DIR, "cooldowns.json")
COOLDOWN_FILE = "cooldown.json"

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

def get_or_create_user_data(user_id):
    users = load_user_data()
    if user_id not in users:
        users[user_id] = {
            "bait": {"worm": 0, "magic_bait": 0},
            "rods": [],
            "equipped_rod": None,
            "fish": [],
            "balance": 0,
            "deposit": 0,
            "sold_fish": []
        }
    
    if "money" in users[user_id]:
        users[user_id]["balance"] += users[user_id]["money"]
        del users[user_id]["money"]

    if "equipped_rod" not in users[user_id]:
        users[user_id]["equipped_rod"] = None

    bait = users[user_id].get("bait")
    if not isinstance(bait, dict):
        users[user_id]["bait"] = {"worm": 0, "magic_bait": 0}
    else:
        if "worm" not in bait:
            bait["worm"] = 0
        if "magic_bait" not in bait:
            bait["magic_bait"] = 0

    save_user_data(users)
    return users

def save_user_data(data):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_cooldown_data():
    with open(COOLDOWN_DATA_FILE, "r") as f:
        return json.load(f)

def save_cooldown_data(data):
    with open(COOLDOWN_DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_fish_cooldown():
    if not os.path.exists(COOLDOWN_FILE):
        return 0.3
    with open(COOLDOWN_FILE, "r") as f:
        return json.load(f).get("fish_cooldown", 0.3)

def save_fish_cooldown(seconds):
    with open(COOLDOWN_FILE, "w") as f:
        json.dump({"fish_cooldown": seconds}, f)
