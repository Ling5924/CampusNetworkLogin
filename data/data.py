import json
import os


def build_data():
    data_path = os.path.join(os.getcwd(), r"config.json")
    with open(data_path, 'r', encoding="utf-8") as f:
        conf = json.load(f)
        data = []
        for x in conf:
            data.append((x['username'], x['password'], x['route_info'], x['wifi_name']))
    return data