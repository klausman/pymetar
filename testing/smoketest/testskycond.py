#!/usr/bin/python3 -tt

import pymetar
import sys
import os

conds=set([None, 'Moderate haze', 'Partial haze', 'Haze in the vicinity', 'Drifting haze', 'Patches of haze', 'Haze with wind', 'Shallow haze', 'Thick haze', 'Light haze', 'Freezing haze', 'Moderate smoke', 'Partial smoke', 'Smoke in the vicinity', 'Drifting smoke', 'Patches of smoke', 'Smoke with wind', 'Shallow smoke', 'Thick smoke', 'Thin smoke', 'Smoke w/ thunders', 'storm', 'Moderate funnel cloud', 'Partial funnel cloud', 'Funnel cloud in the vicinity', 'Drifting funnel cloud', 'Patches of funnel cloud', 'Funnel cloud w/ wind', 'Shallow funnel cloud', 'Thick funnel cloud', 'Light funnel cloud', 'Moderate drizzle', 'Drizzle in the vicinity', 'Patches of drizzle', 'Windy drizzle', 'Light drizzle', 'Freezing drizzle', 'Drifting drizzle', 'Partial drizzle', 'Heavy drizzle', 'Shallow drizzle', 'Thunderstorm', 'storm', 'Showers', 'Moderate tornado', 'Partial tornado', 'Tornado in the vicinity', 'Tornado', 'Freezing tornado', 'Raging tornado', 'Drifting tornado', 'Thunderous tornado', 'Moderate mist', 'Partial mist', 'Mist in the vicinity', 'Drifting mist', 'Patches of mist', 'Mist with wind', 'Shallow mist', 'Thick mist', 'Light mist', 'Freezing mist', 'Moderate fog', 'Partial fog', 'Fog in the vicinity', 'Drifting fog', 'Patches of fog', 'Fog with wind', 'Shallow fog', 'Thick fog', 'Light fog', 'Freezing fog', 'Moderate dust', 'Partial dust', 'Dust', 'Dust in the vicinity', 'Patches of dust', 'Blowing dust', 'Drifting dust', 'Heavy dust', 'Light dust', 'Moderate duststorm', 'Partial duststorm', 'Duststorm in the vicinity', 'Drifting duststorm', 'Blowing duststorm', 'Shallow duststorm', 'Heavy duststorm', 'Light duststorm', 'Thunderous duststorm', 'storm', 'Freezing duststorm', 'Moderate sprays', 'Partial sprays', 'Sprays in the vicinity', 'Drifting sprays', 'Patches of sprays', 'Blowing sprays', 'Shallow sprays', 'Heavy sprays', 'Light sprays', 'Freezing sprays', 'Moderate rain', 'Rain in the vicinity', 'Patches of rain', 'Blowing rainfall', 'Light rain', 'Freezing rain', 'Drifting rain', 'Partial rainfall', 'Heavy rain', 'Shallow rain', 'Thunderstorm', 'storm', 'Rain showers', 'Moderate ice pellets', 'Ice pellets in the vicinity', 'Patches of ice pellets', 'Blowing ice pellets', 'Few ice pellets', 'Freezing ice pellets', 'Drifting ice pellets', 'Partial ice pellets', 'Heavy ice pellets', 'Shallow ice pellets', 'Ice pellets storm', 'storm', 'Showers of ice pellets', 'Moderate dustwhirls', 'Partial dustwhirls', 'Dustwhirls in the vicinity', 'Drifting dustwhirls', 'Patches of dustwhirls', 'Blowing dustwhirls', 'Shallow dustwhirls', 'Heavy dustwhirls', 'Light dustwhirls', 'Moderate volcanic ash', 'Volcanic ash in the vicinity', 'Patches of volcanic ash', 'Blowing volcanic ash', 'Freezing volcanic ash', 'Drifting volcanic ash', 'Partial volcanic ash', 'Thick volcanic ash', 'Shallow volcanic ash', 'Volcanic ash w/ thunders', 'storm', 'Showers of volcanic ash', 'Moderate small hail', 'Small hail in the vicinity', 'Patches of small hail', 'Blowing small hail', 'Light small hail', 'Freezing small hail', 'Drifting small hail', 'Partial small hail', 'Heavy small hail', 'Shallow small hail', 'Small hailstorm', 'storm', 'Showers of small hail', 'Moderate hail', 'Hail in the vicinity', 'Patches of hail', 'Blowing hail', 'Light hail', 'Freezing hail', 'Drifting hail', 'Partial hail', 'Heavy hail', 'Shallow hail', 'Hailstorm', 'storm', 'Hail showers', 'Moderate ice crystals', 'Ice crystals in the vicinity', 'Patches of ice crystals', 'Blowing ice crystals', 'Freezing ice crystals', 'Drifting ice crystals', 'Partial ice crystals', 'Heavy ice crystals', 'Few ice crystals', 'Ice crystal storm', 'storm', 'Showers of ice crystals', 'Moderate sandstorm', 'Partial sandstorm', 'Sandstorm in the vicinity', 'Drifting sandstorm', 'Blowing sandstorm', 'Shallow sandstorm', 'Heavy sandstorm', 'Light sandstorm', 'Thunderous sandstorm', 'storm', 'Freezing sandstorm', 'Moderate squall', 'Partial squall', 'Squall in the vicinity', 'Blowing squall', 'Drifting squall', 'Heavy squall', 'Light squall', 'Thunderous squall', 'Freezing squall', 'Moderate precipitation', 'Precipitation in the vicinity', 'Patches of precipitation', 'Blowing precipitation', 'Light precipitation', 'Freezing precipitation', 'Drifting precipitation', 'Partial precipitation', 'Heavy precipitation', 'Shallow precipitation', 'Unknown thunderstorm', 'storm', 'Showers, type unknown', 'Moderate snow', 'Snow in the vicinity', 'Patches of snow', 'Blowing snowfall', 'Light snow', 'Freezing snow', 'Drifting snow', 'Partial snowfall', 'Heavy snow', 'Shallow snow', 'Snowstorm', 'storm', 'Snowfall showers', 'Moderate sand', 'Partial sand', 'Sand in the vicinity', 'Sand', 'Patches of sand', 'Blowing sand', 'Drifting sand', 'Heavy sand', 'Light sand', 'Moderate snow grains', 'Snow grains in the vicinity', 'Patches of snow grains', 'Blowing snow grains', 'Light snow grains', 'Freezing snow grains', 'Drifting snow grains', 'Partial snow grains', 'Heavy snow grains', 'Shallow snow grains', 'Snowstorm', 'Snow grain showers'])


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
        
        a=pr.getConditions()
        if a[0] not in conds:
            print(a)
            sys.exit(-1)
        if a != None:
            print("%s: %s"% (station, a))

        count += 1

    sys.stderr.write("%s station reports check out ok\n" % (count))



