import os

from utils import get_datetime, set_datetime

# set path to Google Photos folder
dir = ""

success, total = 0, 0

for root, dirs, files in os.walk(dir):
    for file in files:
        file_path = os.path.join(root, file)
        conditions = os.path.isfile(file_path) and \
            not file_path.endswith(".json") and \
            not file.startswith(".") and \
            "Photos from 2022" not in file_path
        if conditions:
            total += 1
            result = get_datetime(file_path)
            if result:
                destination = f"./temp{root.replace(dir, '')}"
                try:
                    set_datetime(file_path, destination, result)
                    success += 1
                    print(f"🟢 {success}/{total}")
                except Exception as e:
                    print(f"🔴 {e}")
