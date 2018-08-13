#!/usr/bin/python -tt
# -*- coding: iso-8859-15 -*-

__version__ = "2.1"

import pymetar
import sys

print("pymet v%s using pymetar lib v%s" % (__version__, pymetar.__version__))

if len(sys.argv) < 2:
    station = "NZCM"
else:
    station = sys.argv[1]

rf = pymetar.ReportFetcher(station)
rep = rf.FetchReport()
rp = pymetar.ReportParser()
pr = rp.ParseReport(rep.decode())

print("--------- Full report ---------")
print(pr.fullreport)
print("------- End full report -------")

print("-------- Parsed Values --------")
for k in list(pr.__dict__.keys()):
    if k != "fullreport":
        print("%s: %s" % (k, pr.__dict__[k]))
print("------ End Parsed Values ------")

print("----- Report getFunctions -----")
print("getTemperatureCelsius(): %s" % (pr.getTemperatureCelsius()))
print("getTemperatureFahrenheit(): %s" % (pr.getTemperatureFahrenheit()))
print("getDewPointCelsius(): %s" % (pr.getDewPointCelsius()))
print("getDewPointFahrenheit(): %s" % (pr.getDewPointFahrenheit()))
print("getWindSpeed(): %s" % (pr.getWindSpeed()))
print("getWindSpeedMilesPerHour(): %s" % (pr.getWindSpeedMilesPerHour()))
print("getWindDirection(): %s" % (pr.getWindDirection()))
print("getWindCompass(): %s" % (pr.getWindCompass()))
print("getVisibilityKilometers(): %s" % (pr.getVisibilityKilometers()))
print("getVisibilityMiles(): %s" % (pr.getVisibilityMiles()))
print("getHumidity(): %s" % (pr.getHumidity()))
print("getPressure(): %s" % (pr.getPressure()))
print("getRawMetarCode(): %s" % (pr.getRawMetarCode()))
print("getWeather(): %s" % (pr.getWeather()))
print("getSkyConditions(): %s" % (pr.getSkyConditions()))
print("getStationName(): %s" % (pr.getStationName()))
print("getStationCity(): %s" % (pr.getStationCity()))
print("getStationCountry(): %s" % (pr.getStationCountry()))
print("getCycle(): %s" % (pr.getCycle()))
print("getStationPosition(): %s" % (repr(pr.getStationPosition())))
print("getStationPositionFloat(): %s" % (repr(pr.getStationPositionFloat())))
print("getStationLatitude(): %s" % (pr.getStationLatitude()))
print("getStationLatitudeFloat(): %s" % (pr.getStationLatitudeFloat()))
print("getStationLongitude(): %s" % (pr.getStationLongitude()))
print("getStationLongitudeFloat(): %s" % (pr.getStationLongitudeFloat()))
print("getStationAltitude(): %s" % (pr.getStationAltitude()))
print("getReportURL(): %s" % (pr.getReportURL()))
print("getTime(): %s" % (pr.getTime()))
print("getISOTime(): %s" % (pr.getISOTime()))
print("getPixmap(): %s" % (pr.getPixmap()))
print("getCloudtype(): %s" % (pr.getCloudtype()))
print("getWindchill(): %s" % (pr.getWindchill()))
print("getWindchillF(): %s" % (pr.getWindchillF()))
print("getCloudinfo(): %s" % (repr(pr.getCloudinfo())))
print("getConditions(): %s" % (repr(pr.getConditions())))

print("--- End Report getFunctions ---")
