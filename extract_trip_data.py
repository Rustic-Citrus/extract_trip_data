import glob
from PyPDF2 import PdfReader
from datetime import datetime
import pandas as pd

totals = []
dates = []
times = []
num_strings_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

for file in glob.glob("./*.pdf"):
    pdf = PdfReader(file) # parsing the pdf
    txt = pdf.pages[0].extract_text() # extracting text from pdf
    total = txt[(txt.find("Total") + 9):(txt.find("Total") + 14)] # finding the total values
    total = total.replace(",", ".") # replacing decimal commas with points
    total = float(total) # converting totals from strings into floats
    totals.append(total)
    if txt[(txt.find("2022")) - 6] in num_strings_list: # finding the dates and times
        datetime_object = datetime.strptime(
            txt[(txt.find("2022") - 6):(txt.find("2022") + 10)].strip(),
            "%d/%m/%Y %H:%M"
            )
    else:
        datetime_object = datetime.strptime(
            txt[(txt.find("2022") - 5):(txt.find("2022") + 10)].strip(),
            "%d/%m/%Y %H:%M"
            )
    dates.append(datetime_object.strftime("%d/%m/%Y")) # extracting the date
    times.append(datetime_object.strftime("%H:%M")) # extracting the time

df = pd.DataFrame({"total": totals, "date": dates, "time": times})
df.to_excel("trip_data.xlsx", index=False)