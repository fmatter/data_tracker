import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, time

df = pd.read_csv("sauna_data.csv", parse_dates=["timestamp"])
df["date"] = df["timestamp"].dt.date
df["time"] = df["timestamp"].dt.time
df["weekday"] = df["timestamp"].dt.weekday
df["ratio"] = df["current_seats"] / df["max_seats"]

daydic = {
    0: "Määnti",
    1: "Zysti",
    2: "Midwuch",
    3: "Donnsti",
    4: "Fryti",
    5: "Samsti",
    6: "Sunnti",
}
df["Tag"] = df.apply(lambda x: daydic[x["weekday"]], axis=1)

today = datetime.today().date()
thisday = df[df["date"] == today]
thisday = thisday[["current_seats", "time"]]
thisday.rename(columns={"current_seats": "Lüt"}, inplace=True)
thisday.index = thisday["time"]
thisday.drop(columns=["time"], inplace=True)
thisday.plot()
plt.savefig("Today.png")
plt.clf()


def by_day(df, day=0):
    name = daydic[day]
    temp_df = df[df["weekday"] == day]
    temp_df = temp_df[["ratio", "time"]]
    temp_df = temp_df.groupby(by="time").mean()
    temp_df["time"] = temp_df.index
    temp_df.drop(columns=["time"], inplace=True)
    temp_df.plot()
    plt.savefig(name + ".png")
    plt.clf()


now = datetime.now().weekday()
by_day(df, now)

from datetime import datetime, time

start = time(11, 30, 0)
end = time(21, 30, 0)


def get_current():
    now = datetime.now()
    if now.weekday() != 2:
        if start < now.time() < end:
            return True
    return False


def sauna_markdown(row):
    if get_current():
        text = f"### Jitz grad: {int(row.current_seats)}/{int(row.max_seats)} ({row.Tag}, {row.timestamp}"
    else:
        text = "Nid offe."
    return f"""{text}

### Hütige Vrlouf:
![Graph](Today.png)

### E durschnittleche {row.Tag}:
![Graph]({row.Tag}.png)"""


f = open("README.md", "w")
f.write(sauna_markdown(df.iloc[-1]))
f.close()
