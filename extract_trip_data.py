import glob
from tika import parser
from datetime import datetime
import pandas as pd

totals = []
dates = []
times = []
num_strings_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

for file in glob.glob("./*.pdf"):
    raw = parser.from_file(file)
    total = raw["content"][(raw["content"].find("Total") + 9):(raw["content"].find("Total") + 14)] # finding the total values
    total = total.replace(",", ".") # replacing decimal commas with points
    total = float(total) # converting totals from strings into floats
    totals.append(total)
    if raw["content"][(raw["content"].find("2022")) - 6] in num_strings_list: # finding the dates and times
        datetime_object = datetime.strptime(
            raw["content"][(raw["content"].find("2022") - 6):(raw["content"].find("2022") + 10)].strip(),
            "%d/%m/%Y %H:%M"
            )
    else:
        datetime_object = datetime.strptime(
            raw["content"][(raw["content"].find("2022") - 5):(raw["content"].find("2022") + 10)].strip(),
            "%d/%m/%Y %H:%M"
            )
    dates.append(datetime_object.strftime("%d/%m/%Y")) # extracting the date
    times.append(datetime_object.strftime("%H:%M")) # extracting the time

df = pd.DataFrame({"total": totals, "date": dates, "time": times})
df.to_excel("trip_data.xlsx", index=False)