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

        fd = open("%s/%s" % (repdir, reportfile))
        try:
            report = fd.read().encode()
        except UnicodeDecodeError:
            continue
        fd.close()

        repo = rf.MakeReport(station, report)
        rp = pymetar.ReportParser()
        pr = rp.ParseReport(repo)
        
        a=pr.getCloudtype()
        if a != None:
            print("%s: %s"% (station, a))

        count += 1

    sys.stderr.write("%s station reports check out ok\n" % (count))



