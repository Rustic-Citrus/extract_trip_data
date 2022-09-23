import glob
from tika import parser
from datetime import datetime
import pandas as pd

totals = []
dates = []
times = []

for file in glob.glob("./*.pdf"):
    raw = parser.from_file(file)
    total = raw["content"][(raw["content"].find("Total") + 9):(raw["content"].find("Total") + 14)]
    total = total.replace(",", ".")
    total = float(total)
    totals.append(total)
    datetime_object = datetime.strptime(raw["content"][(raw["content"].find("2022") - 6):(raw["content"].find("2022") + 10)].strip(),"%d/%m/%Y %H:%M")
    dates.append(datetime_object.strftime("%d/%m/%Y"))
    times.append(datetime_object.strftime("%H:%M"))

df = pd.DataFrame({"total": totals, "date": dates, "time": times})
df.to_excel("uber_trip_data.xlsx", index=False)