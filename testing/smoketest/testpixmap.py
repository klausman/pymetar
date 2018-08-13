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

        fd = open("%s/%s" % (repdir,reportfile))
        try:
            report = fd.read().encode()
        except UnicodeDecodeError:
            continue
        fd.close()

        repo = rf.MakeReport(station, report)
        
        rp = pymetar.ReportParser()
        pr = rp.ParseReport(repo)
        
        a=pr.getPixmap()
        b=pr.getCloudinfo()
        c=pr.getConditions()

        print(a, b, c)

        count += 1

    sys.stderr.write("%s station report pixmaps check out ok\n" % (count))


