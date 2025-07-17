import json
import os

CONFIG_FILE = "settings.json"

DEFAULT_CONFIG = {
    "access_key": "XU0OWIYTUILRQIQY4XLS",
    "secret_key": "lok9QWZXjHp53GhhZqycFQVQeQpdjw0z1tJrT2m1",
    "endpoint": "obsv3.zong-hpcc-isb.zongcloud.com.pk",
    "bucket": "imranbucket",
    "upload_folder": "uploads"
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
