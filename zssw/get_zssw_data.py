from bs4 import BeautifulSoup
import urllib.request
from datetime import datetime
import csv

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

fp = urllib.request.urlopen(
    "https://www.zssw.unibe.ch/usp/zms/templates/crowdmonitoring/_display-spaces-zssw.php"
)
mybytes = fp.read()
tent = mybytes.decode("utf8")
fp.close()

soup = BeautifulSoup(tent, "html.parser")
count_div = soup.find_all("div", {"class": "go-stop-display_footer"})[0]
count, max_count = count_div.text.split(" von ")

with open("zssw_data.csv", "a") as fd:
    writer = csv.writer(fd)
    writer.writerow([count, max_count, timestamp])
