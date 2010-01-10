#!/usr/bin/python -tt

import pymetar
import sys

if __name__ == "__main__":
    fd = open("stations")
    count=0
    rf=pymetar.ReportFetcher()
    for line in fd:
        station = line.strip()
        sys.stdout.write("%s " % (station))
        sys.stdout.flush()

        fd2 = open("reports/%s.TXT" % station)
        report = fd2.read()
        fd2.close()

        repo = rf.MakeReport(station, report)
        
        rp = pymetar.ReportParser()
        pr = rp.ParseReport(repo)
        
        a=pr.getPixmap()
        b=pr.getCloudinfo()
        c=pr.getConditions()

        print a, b, c

        count += 1

    sys.stderr.write("%s station report pixmaps check out ok\n" % (count))


