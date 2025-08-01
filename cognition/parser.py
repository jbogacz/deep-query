import json


class Parser:
    def parse(self, file_path: str) -> dict | list[dict]:
        with open(file_path, "r") as file:
            content = file.read()
        # Implement your parsing logic here
        try:
            data = json.loads(content)
            if isinstance(data, list):
                return data
            else:
                return [data]
        except json.JSONDecodeError:
            print(f"Error parsing JSON from {file_path}")
            return []
