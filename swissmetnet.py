import requests
import csv
import itertools
import shutil
import argparse
import os.path


parser = argparse.ArgumentParser(description="SwissMetNet Script")
parser.add_argument("-v", "--version", action="version", version="SwissMetNet Script 0.1")
datagroup = parser.add_mutually_exclusive_group()
parser.add_argument("station", help="Measurement station, See: http://data.geo.admin.ch/ch.meteoschweiz.swissmetnet/info/VQHA69_EN.txt")
datagroup.add_argument("-temperature", help="Air temperature 2 m above ground - °C", action="store_true")
datagroup.add_argument("-sunshine", help="Sunshine duration; ten minutes total - min", action="store_true")
datagroup.add_argument("-precipitation", help="Precipitation; ten minutes total - mm", action="store_true")
datagroup.add_argument("-winddirection", help="Wind direction; ten minutes mean - °", action="store_true")
datagroup.add_argument("-windspeed", help="Wind speed; ten minutes mean - km/h", action="store_true")
datagroup.add_argument("-gustpeak", help="Gust peak (one second); maximum - km/h", action="store_true")
datagroup.add_argument("-airhumidity", help="Relative air humidity 2 m above ground; current value - Percent", action="store_true")
datagroup.add_argument("-pressureqnh", help="Pressure reduced to sea level according to standard atmosphere (QNH); current value - hPa", action="store_true")
datagroup.add_argument("-pressureqfe", help="Pressure at station level (QFE); current value - hPa", action="store_true")
datagroup.add_argument("-pressureqff", help="Pressure reduced to sea level (QFF); current value - hPa", action="store_true")
datagroup.add_argument("-timestamp", help="UTC timestamp of the measurement - YYYYMMDD", action="store_true")
parser.add_argument("-withunits", help="Print the value with units", action="store_true")
parser.add_argument("-file", help="Get data from a specified file")
arg = parser.parse_args()


# Check if a file has been specified
if arg.file is not None:

    # Check if file exists and load the data
    if os.path.exists(arg.file):
        dataset = open(arg.file, "r", encoding="utf-8")

    # Print an error instead
    else:
        print("Error: The file: " + arg.file + " does not exist.")
        quit()


# Otherwise get fresh data and save it
else:
    dataurl = "http://data.geo.admin.ch/ch.meteoschweiz.swissmetnet/VQHA69.csv"
    datarequest = requests.get(dataurl, stream=True)
    with open("smn_current.csv", "wb") as datafile:
        shutil.copyfileobj(datarequest.raw, datafile)

    # Load the data
    dataset = open("smn_current.csv", "r", encoding="utf-8")


# Remove the first two lines of the data
dataset2 = itertools.islice((dataset), 2, None)


# Read the data
datasetcsv = csv.DictReader(dataset2, delimiter="|")
for datasets in datasetcsv:

    # Look for the selected station
    if datasets["stn"] == arg.station:

        # Check the values of this station
        if arg.temperature:
            if arg.withunits and datasets["tre200s0"] != "-":
                print(datasets["tre200s0"] + " °C")
            elif datasets["tre200s0"] != "-":
                print(datasets["tre200s0"])
            else:
                print("Error: No valid data found")

        elif arg.sunshine:
            if arg.withunits and datasets["sre000z0"] != "-":
                print(datasets["sre000z0"] + " min")
            elif datasets["sre000z0"] != "-":
                print(datasets["sre000z0"])
            else:
                print("Error: No valid data found")

        elif arg.precipitation:
            if arg.withunits and datasets["rre150z0"] != "-":
                print(datasets["rre150z0"] + " mm")
            elif datasets["rre150z0"] != "-":
                print(datasets["rre150z0"])
            else:
                print("Error: No valid data found")

        elif arg.winddirection:
            if arg.withunits and datasets["dkl010z0"] != "°":
                print(datasets["dkl010z0"] + " min")
            elif datasets["dkl010z0"] != "-":
                print(datasets["dkl010z0"])
            else:
                print("Error: No valid data found")

        elif arg.windspeed:
            if arg.withunits and datasets["fu3010z0"] != "-":
                print(datasets["fu3010z0"] + " km/h")
            elif datasets["fu3010z0"] != "-":
                print(datasets["fu3010z0"])
            else:
                print("Error: No valid data found")

        elif arg.gustpeak:
            if arg.withunits and datasets["fu3010z1"] != "-":
                print(datasets["fu3010z1"] + " km/h")
            elif datasets["fu3010z1"] != "-":
                print(datasets["fu3010z1"])
            else:
                print("Error: No valid data found")

        elif arg.airhumidity:
            if arg.withunits and datasets["ure200s0"] != "-":
                print(datasets["ure200s0"] + " %")
            elif datasets["ure200s0"] != "-":
                print(datasets["ure200s0"])
            else:
                print("Error: No valid data found")

        elif arg.pressureqnh:
            if arg.withunits and datasets["pp0qnhs0"] != "-":
                print(datasets["pp0qnhs0"] + " hPa")
            elif datasets["pp0qnhs0"] != "-":
                print(datasets["pp0qnhs0"])
            else:
                print("Error: No valid data found")

        elif arg.pressureqfe:
            if arg.withunits and datasets["prestas0"] != "-":
                print(datasets["prestas0"] + " hPa")
            elif datasets["prestas0"] != "-":
                print(datasets["prestas0"])
            else:
                print("Error: No valid data found")

        elif arg.pressureqff:
            if arg.withunits and datasets["pp0qffs0"] != "-":
                print(datasets["pp0qffs0"] + " hPa")
            elif datasets["pp0qffs0"] != "-":
                print(datasets["pp0qffs0"])
            else:
                print("Error: No valid data found")

        elif arg.timestamp:
            print(datasets["time"])

        else:
            print("Error: No parameter selected")