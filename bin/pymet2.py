#!/usr/bin/python -tt
# -*- coding: iso-8859-15 -*-

__version__="2.1"

import pymetar
import sys

print("pymet v%s using pymetar lib v%s"%(__version__,pymetar.__version__))

if len(sys.argv)<2:
    station="NZCM"
else:
    station=sys.argv[1]

rf=pymetar.ReportFetcher(station)
rep=rf.FetchReport()
rp=pymetar.ReportParser()
pr=rp.ParseReport(rep)

print("--------- Full report ---------")
print(pr.fullreport)
print("------- End full report -------")

print("-------- Parsed Values --------")
for k in list(pr.__dict__.keys()):
 if k != "fullreport":
  print("%s: %s"%(k,pr.__dict__[k]))
print("------ End Parsed Values ------")

print("----- Report getFunctions -----")
print("getTemperatureCelsius():",pr.getTemperatureCelsius())
print("getTemperatureFahrenheit():",pr.getTemperatureFahrenheit())
print("getDewPointCelsius():",pr.getDewPointCelsius())
print("getDewPointFahrenheit():",pr.getDewPointFahrenheit())
print("getWindSpeed():",pr.getWindSpeed())
print("getWindSpeedMilesPerHour():",pr.getWindSpeedMilesPerHour())
print("getWindDirection():",pr.getWindDirection())
print("getWindCompass():",pr.getWindCompass())
print("getVisibilityKilometers():",pr.getVisibilityKilometers())
print("getVisibilityMiles():",pr.getVisibilityMiles())
print("getHumidity():",pr.getHumidity())
print("getPressure():",pr.getPressure())
print("getRawMetarCode():",pr.getRawMetarCode())
print("getWeather():",pr.getWeather())
print("getSkyConditions():",pr.getSkyConditions())
print("getStationName():",pr.getStationName())
print("getStationCity():",pr.getStationCity())
print("getStationCountry():",pr.getStationCountry())
print("getCycle():",pr.getCycle())
print("getStationPosition():",pr.getStationPosition())
print("getStationPositionFloat():",pr.getStationPositionFloat())
print("getStationLatitude():",pr.getStationLatitude())
print("getStationLatitudeFloat():",pr.getStationLatitudeFloat())
print("getStationLongitude():",pr.getStationLongitude())
print("getStationLongitudeFloat():",pr.getStationLongitudeFloat())
print("getStationAltitude():",pr.getStationAltitude())
print("getReportURL():",pr.getReportURL())
print("getTime():",pr.getTime())
print("getISOTime():",pr.getISOTime())
print("getPixmap():",pr.getPixmap())
print("getCloudtype():",pr.getCloudtype())
print("getWindchill():",pr.getWindchill())
print("getWindchillF():",pr.getWindchillF())
print("getCloudinfo():",pr.getCloudinfo())
print("getConditions():",pr.getConditions())

print("--- End Report getFunctions ---")

