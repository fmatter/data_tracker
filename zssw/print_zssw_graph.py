import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
import numpy as np

# import pandas_bokeh

df = pd.read_csv("zssw_data.csv", parse_dates=["date"])

df["time"] = df["date"].dt.time

df["daydate"] = df["date"].dt.date
df["day"] = df["date"].dt.weekday


daydic = {
    0: "Määnti",
    1: "Zysti",
    2: "Midwuch",
    3: "Donnsti",
    4: "Fryti",
    5: "Samsti",
    6: "Sunnti",
}
df["Tag"] = df.apply(lambda x: daydic[x["day"]], axis=1)

datefmt = "%Y-%m-%d"
timefmt = "%H:%M:%S"
fullfmt = datefmt + " " + timefmt
# filter earlier closing times
ten_to_eight_start = datetime.strptime("2021-07-05", datefmt)
ten_to_eight_stop = datetime.strptime("2021-08-06", datefmt)
# df = df[~((df["date"] > ten_to_eight) & (df["date"]) & (df["time"] > datetime(2016, 1, 1, 20, 15).time()))]
df = df[(ten_to_eight_start > df["date"]) | (df["date"] > ten_to_eight_stop)]
# start at HS2021
hs21 = datetime.strptime("2021-09-20", datefmt)
df = df[hs21 < df["date"]]

print(df)

# filter mornings
df = df[df["time"] > datetime(2016, 1, 1, 6, 45).time()]
# filter evenings
df = df[df["time"] < datetime(2016, 1, 1, 22, 15).time()]


def by_date(dataframe, year, month, day):
    the_date = datetime(year, month, day).date()
    dataframe = dataframe[dataframe["daydate"] == the_date]
    dataframe = dataframe[["count", "time"]]
    dataframe.set_index("time", inplace=True)
    dataframe.plot()
    plt.show()


def by_day(dataframe, name="single_day"):
    dataframe = dataframe[["count", "time"]]
    dataframe = dataframe.groupby(by="time").mean()
    dataframe["time"] = dataframe.index
    # dataframe.index = dataframe.apply(lambda x: datetime.combine(today, x["time"]), axis=1)
    dataframe.drop(columns=["time"], inplace=True)
    dataframe.plot()
    plt.savefig(name + ".png")
    plt.clf()


# weekday statistics
weekday = df[~df["Tag"].isin(["Samsti", "Sunnti"])]
by_day(weekday, "Wuchetääg")
# weekend statistics
for key, day in daydic.items():
    samsti = df[df["Tag"] == day]
    by_day(samsti, f"{key+1}_{day}")

today = datetime.today().date()
thisday = df[df["daydate"] == today]
thisday.set_index("date", inplace=True)
thisday["count"].plot()
plt.savefig("Today.png")
plt.clf()

piv = pd.pivot_table(df, index=["time"], columns=["Tag"], values=["count"])
ax = piv.plot(figsize=(20, 10), x_compat=True)
plt.savefig("Overall.png")
