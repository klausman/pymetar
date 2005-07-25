#!/usr/bin/python -tt
# -*- coding: iso-8859-15 -*-

__version__="1.0"

import pymetar
import sys

#print "pymet v%s using pymetar lib v%s"%(__version__,pymetar.__version__)

if len(sys.argv)<2 or sys.argv[1]=="--help":
    sys.stderr.write("Usage: %s <station id>\n"% sys.argv[0])
    sys.stderr.write("Station IDs can be found at: http://www.nws.noaa.gov/tg/siteloc.shtml\n")
    sys.exit(1)
elif (sys.argv[1] == "--version"):
    print "pmw v%s using pymetar lib v%s"%(__version__,pymetar.__version__)
    sys.exit(0)
else:
    station=sys.argv[1]

try:
    rf=pymetar.ReportFetcher(station)
    rep=rf.FetchReport()
except Exception, e:
    sys.stderr.write("Something went wrong when fetching the report.\n")
    sys.stderr.write("These usually are transient problems if the station ")
    sys.stderr.write("ID is valid. \nThe error encountered was:\n")
    sys.stderr.write(str(e)+"\n")
    sys.exit(1)

rp=pymetar.ReportParser()
pr=rp.ParseReport(rep)

print "Weather report for %s (%s) as of %s" %\
    (pr.getStationName(), station, pr.getISOTime())
print "Values of \"None\" indicate that the value is missing from the report."
print "Temperature: %s C / %s F" %\
    (pr.getTemperatureCelsius(), pr.getTemperatureFahrenheit())
print "Rel. Humidity: %s%%" % (pr.getHumidity())
if pr.getWindSpeed() is not None:
    print "Wind speed: %0.2f m/s" % (pr.getWindSpeed())
else:
    print "Wind speed: None"
    
print "Wind direction: %s deg (%s)" %\
    (pr.getWindDirection(), pr.getWindCompass())
if pr.getPressure() is not None:
    print "Pressure: %s hPa" % (int(pr.getPressure()))
else:
    print "Pressure: None"

print "Dew Point: %s C / %s F" %\
    (pr.getDewPointCelsius(), pr.getDewPointFahrenheit())
print "Weather:",pr.getWeather()
print "Sky Conditions:",pr.getSkyConditions()
    
