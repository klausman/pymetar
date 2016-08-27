# PyMETAR - a module to fetch and parse METAR reports

**NOTE:** If you're looking for information regarding Python 3 and PyMETAR, see
the end of this document.

**NOTE 2:** PyMETAR is in maintenance mode. That means I will only bugs or adapt
it to when NOAA changes URLs (again).

The National Oceanic and Atmospheric Administration (NOAA, http://www.noaa.gov/)
provides easy access to the weather reports generated by a large number of
weather stations (mostly at airports) worldwide. Those reports are called METAR
reports and are delivered as plain text files that look like this:

```
Duesseldorf, Germany (EDDL) 51-18N 006-46E 41M
Jul 26, 2002 - 03:50 AM EST / 2002.07.26 0850 UTC
Wind: from the SW (220 degrees) at 9 MPH (8 KT):0
Visibility: 3 mile(s):0
Sky conditions: mostly cloudy
Weather: mist
Temperature: 60 F (16 C)
Dew Point: 57 F (14 C)
Relative Humidity: 87%
Pressure (altimeter): 30.00 in. Hg (1016 hPa)
ob: EDDL 260850Z 22008KT 5000 BR SCT006 BKN012 16/14 Q1016 BECMG BKN015
cycle: 9
```

While this is convenient if you just want to quickly look up the data, there's
some effort involved in parsing all of this into a format that is digestible by
a program. Plus, you have to remember the base URL of the reports and fetch the
file.

This is what this library does. All you have to do is find the station you're
interested in at http://www.aviationweather.gov/metar and feed the 4-letter
station code to the MetarReport class.

On the user end, the library provides a large number of methods to fetch the
parsed information in a plethora of formats. Those functions are described in
the file `librarydoc.txt` which was in turn generated using PyDoc.

As of version 0.5, PyMETAR uses `urllib2` which in turn makes it easy to honor
the environment variable `http_proxy`. This simplifies use of a proxy
tremendously. Thanks go to Davide Di Blasi for both suggesting and implementing
this. The environment variable is easy to use: just set it to:

```
http://username:password@proxy.yourdomain.com:port 
```

As of version 0.11, you can also specify a proxy (with the same syntax) as an
argument to the fetching function. This is sometimes easier when using PyMETAR
in a web application environment (such as ZopeWeatherApplet by Jerome Alet). See
`librarydoc.txt` for details on how to accomplish that. 

You can also use IPs instead of hostnames, of course. When in doubt, ask your
proxy admin.

Due to some peculiarities in the METAR format, I can not rule out the
possibility that the library barfs on some less common types of reports. If you
encounter such a report, please save it and the error messages you get as
completely as possible and send them to me at `klausman-pymetar@schwarzvogel.de`
- Thanks a lot!

Of course you may send all the other bugs you encounter to me, too. As this is a
Python library, chances are that you are Python programmer and can provide a
patch. If you do so, please, by all means use spaces for indentation, four per
level, that makes merging the patch a lot easier.

## Python 3

PyMETAR does currently not support Python 3 (Python 2.4-2.7 should be fine.
Versions <2.4 are not officially supported but may work by chance). PyMETAR
_may_ work after being put through `2to3`, but you do so at your own risk.

I'm currently in the process of plotting out the future of PyMETAR, which
naturally includes thinking about Py3. The design of the whole library is now
over a decade years old. At this point, there is little that I can do in the
ways of changing the API gradually, so I'm thinking about releasing a totally
incompatible new library which will only share the basic purpose of PyMETAR. I
don't think that the current code can be refactored easily and I have meant to
try different approaches to the same problem (pylex, dispatcher code, state
machines and sundry other stuff). *If* I go that route, it will be Py3-only,
since that is the future. Also, I will create a better test suite/scaffolding.

If you want to join me in building and designing the "new PyMETAR", feel free to
join me on the mailing list.

Oh, and we need a new name or some other distinctive tag for the new code. And
no, it will not be pymetar-ng.