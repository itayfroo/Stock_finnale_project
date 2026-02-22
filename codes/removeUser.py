import os
import json
class RemoveUser:
    def __init__(self, username) -> None:
        self.name = username
        self.delete_user(self.name)
        self.delete_user(f"{self.name}_info")

    def delete_user(self, content):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        file_path = os.path.join(project_root, "texts", "users.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as json_file:
                data = json.load(json_file)
                if content in data:
                    del data[content]
            with open(file_path, "w") as json_file:
                json.dump(data, json_file)
        else:
            print("JSON file does not exist.")