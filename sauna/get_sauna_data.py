import requests
import json
from datetime import datetime
import pandas as pd

headers = {
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
}

data = {"query": "{ allSaunas { name, current_seats, max_seats } }"}

json_data = json.dumps(data)

res = requests.post("https://lorauna.app/api", data=json_data, headers=headers)
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

json_data = res.json()
sauna_data = []
for sauna in json_data["data"]["allSaunas"]:
    if sauna["max_seats"] == 0:
        continue
    sauna_data.append(sauna)
    sauna_data[-1]["timestamp"] = timestamp
new_df = pd.DataFrame(sauna_data)

df = pd.read_csv("sauna_data.csv")
df = df.append(sauna_data)
df.to_csv("sauna_data.csv", index=False)
