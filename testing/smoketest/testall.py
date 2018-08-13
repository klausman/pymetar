#!/usr/bin/python3 -tt

import pymetar
import sys
import os

if __name__ == "__main__":
    if len(sys.argv) > 1:
        repdir=sys.argv[1]
    else:
        repdir=("reports")

    if len(sys.argv) > 2:
        reports = sys.argv[2:]
    else:
        reports = os.listdir(repdir)

    reports.sort()
    count=0
    rf=pymetar.ReportFetcher()

    for reportfile in reports:
        station = reportfile[:-4]
        sys.stdout.write("%s " % (station))
        sys.stdout.flush()

        fd = open("%s/%s" % (repdir, reportfile))
        try:
            report = fd.read().encode()
        except UnicodeDecodeError:
            continue
        fd.close()

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
        a=pr.getPressuremmHg()
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

        pr._clearallfields()

        count += 1
    
        sys.stdout.write("...ok\n")

    sys.stderr.write("%s station reports check out ok\n" % (count))


