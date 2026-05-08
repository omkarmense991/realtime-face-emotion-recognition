# src/recognition/database.py

import os
import json


class FaceDatabase:
    def __init__(self, db_path="data/faces"):
        self.db_path = db_path

        os.makedirs(self.db_path, exist_ok=True)

    def save_embeddings(self, name, embeddings):
        """
        Save multiple embeddings for a user.
        """

        file_path = os.path.join(self.db_path, f"{name}.json")

        data = {"name": name, "embeddings": embeddings}

        with open(file_path, "w") as f:
            json.dump(data, f)

    def load_all_embeddings(self):
        """
        Load all user embeddings.
        """

        database = {}

        for file in os.listdir(self.db_path):

            if file.endswith(".json"):

                file_path = os.path.join(self.db_path, file)

                with open(file_path, "r") as f:
                    data = json.load(f)

                    database[data["name"]] = data["embeddings"]

        return database
