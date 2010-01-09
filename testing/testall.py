#!/usr/bin/python -tt

import pymetar
import sys

if __name__ == "__main__":
    fd = open("stations")
    count=0
    rf=pymetar.ReportFetcher()
    for line in fd:
        station = line.strip()
        sys.stderr.write("%s " % (station))
        sys.stderr.flush()

        fd2 = open("reports/%s.TXT" % station)
        report = fd2.read()
        fd2.close()

        repo = rf.MakeReport(station, report)
        
        rp = pymetar.ReportParser()
        pr = rp.ParseReport(repo)
        
        a=pr.getFullReport()
        a=pr.getTemperatureCelsius()
        a=pr.getTemperatureFahrenheit()
        a=pr.getDewPointCelsius()
        a=pr.getDewPointFahrenheit()
        a=pr.getWindSpeed()
        a=pr.getWindSpeedMilesPerHour()
        a=pr.getWindSpeedBeaufort()
        a=pr.getWindDirection()
        a=pr.getWindCompass()
        a=pr.getVisibilityKilometers()
        a=pr.getVisibilityMiles()
        a=pr.getHumidity()
        a=pr.getPressure()
        a=pr.getRawMetarCode()
        a=pr.getWeather()
        a=pr.getSkyConditions()
        a=pr.getStationName()
        a=pr.getStationCity()
        a=pr.getStationCountry()
        a=pr.getCycle()
        a=pr.getStationPosition()
        a=pr.getStationPositionFloat()
        a=pr.getStationLatitude()
        a=pr.getStationLatitudeFloat()
        a=pr.getStationLongitude()
        a=pr.getStationLongitudeFloat()
        a=pr.getStationAltitude()
        a=pr.getReportURL()
        a=pr.getTime()
        a=pr.getISOTime()
        a=pr.getPixmap()
        a=pr.getCloudinfo()
        a=pr.getConditions()
        a=pr.getWindchill()
        a=pr.getWindchillF()


        count += 1

    print "\n%s station reports check out ok" % (count)


