import json
import os
import uuid

config_data = json.load(open(os.path.dirname(os.path.realpath(__file__)) + "/data/config.json"))

class Config:
    mongo_uri = config_data.get("mongo_uri")
    base_page_id = str(uuid.UUID(config_data.get("base_page_id")))