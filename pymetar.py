# -*- coding: utf8 -*-
# pylint: disable-msg=C0103 # Disable naming style messages
# Pymetar (c) 2002-2018 Tobias Klausmann
"""
PyMETAR is a python module and command line tool designed to fetch Metar
reports from the NOAA (https://www.noaa.gov) and allow access to the
included weather information.
"""
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA."""
#
import re

import urllib.request  # noqa: E402
import urllib.error    # noqa: E402
import urllib.parse    # noqa: E402

__author__ = "klausman-pymetar@schwarzvogel.de"

__version__ = "1.4"

CLOUD_RE_STR = (r"^(CAVOK|CLR|SKC|BKN|SCT|FEW|OVC|NSC)([0-9]{3})?"
                r"(TCU|CU|CB|SC|CBMAM|ACC|SCSL|CCSL|ACSL)?$")
COND_RE_STR = (r"^[-+]?(VC|MI|BC|PR|TS|BL|SH|DR|FZ)?(DZ|RA|SN|SG|IC|PE|"
               r"GR|GS|UP|BR|FG|FU|VA|SA|HZ|PY|DU|SQ|SS|DS|PO|\+?FC)$")


class EmptyReportException(Exception):
    """This gets thrown when the ReportParser gets fed an empty report"""


class EmptyIDException(Exception):
    """This gets thrown when the ReportFetcher is called with an empty ID"""


class NetworkException(Exception):
    """This gets thrown when a network error occurs"""


class GarbledReportException(Exception):
    """This gets thrown when the report is not valid ASCII or Unicode"""

# What a boring list to type !
#
# It seems the NOAA doesn't want to return plain text, but considering the
# format of their response, this is not to save bandwidth :-)


_WEATHER_CONDITIONS = {
    "DZ": ("Drizzle", "rain", {
           "": "Moderate drizzle",
           "-": "Light drizzle",
           "+": "Heavy drizzle",
           "VC": "Drizzle in the vicinity",
           "MI": "Shallow drizzle",
           "BC": "Patches of drizzle",
           "PR": "Partial drizzle",
           "TS": ("Thunderstorm", "storm"),
           "BL": "Windy drizzle",
           "SH": "Showers",
           "DR": "Drifting drizzle",
           "FZ": "Freezing drizzle",
           }),
    "RA": ("Rain", "rain", {
           "": "Moderate rain",
           "-": "Light rain",
           "+": "Heavy rain",
           "VC": "Rain in the vicinity",
           "MI": "Shallow rain",
           "BC": "Patches of rain",
           "PR": "Partial rainfall",
           "TS": ("Thunderstorm", "storm"),
           "BL": "Blowing rainfall",
           "SH": "Rain showers",
           "DR": "Drifting rain",
           "FZ": "Freezing rain",
           }),
    "SN": ("Snow", "snow", {
           "": "Moderate snow",
           "-": "Light snow",
           "+": "Heavy snow",
           "VC": "Snow in the vicinity",
           "MI": "Shallow snow",
           "BC": "Patches of snow",
           "PR": "Partial snowfall",
           "TS": ("Snowstorm", "storm"),
           "BL": "Blowing snowfall",
           "SH": "Snowfall showers",
           "DR": "Drifting snow",
           "FZ": "Freezing snow",
           }),
    "SG": ("Snow grains", "snow", {
           "": "Moderate snow grains",
           "-": "Light snow grains",
           "+": "Heavy snow grains",
           "VC": "Snow grains in the vicinity",
           "MI": "Shallow snow grains",
           "BC": "Patches of snow grains",
           "PR": "Partial snow grains",
           "TS": ("Snowstorm", "storm"),
           "BL": "Blowing snow grains",
           "SH": "Snow grain showers",
           "DR": "Drifting snow grains",
           "FZ": "Freezing snow grains",
           }),
    "IC": ("Ice crystals", "snow", {
           "": "Moderate ice crystals",
           "-": "Few ice crystals",
           "+": "Heavy ice crystals",
           "VC": "Ice crystals in the vicinity",
           "BC": "Patches of ice crystals",
           "PR": "Partial ice crystals",
           "TS": ("Ice crystal storm", "storm"),
           "BL": "Blowing ice crystals",
           "SH": "Showers of ice crystals",
           "DR": "Drifting ice crystals",
           "FZ": "Freezing ice crystals",
           }),
    "PE": ("Ice pellets", "snow", {
           "": "Moderate ice pellets",
           "-": "Few ice pellets",
           "+": "Heavy ice pellets",
           "VC": "Ice pellets in the vicinity",
           "MI": "Shallow ice pellets",
           "BC": "Patches of ice pellets",
           "PR": "Partial ice pellets",
           "TS": ("Ice pellets storm", "storm"),
           "BL": "Blowing ice pellets",
           "SH": "Showers of ice pellets",
           "DR": "Drifting ice pellets",
           "FZ": "Freezing ice pellets",
           }),
    "GR": ("Hail", "rain", {
           "": "Moderate hail",
           "-": "Light hail",
           "+": "Heavy hail",
           "VC": "Hail in the vicinity",
           "MI": "Shallow hail",
           "BC": "Patches of hail",
           "PR": "Partial hail",
           "TS": ("Hailstorm", "storm"),
           "BL": "Blowing hail",
           "SH": "Hail showers",
           "DR": "Drifting hail",
           "FZ": "Freezing hail",
           }),
    "GS": ("Small hail", "rain", {
           "": "Moderate small hail",
           "-": "Light small hail",
           "+": "Heavy small hail",
           "VC": "Small hail in the vicinity",
           "MI": "Shallow small hail",
           "BC": "Patches of small hail",
           "PR": "Partial small hail",
           "TS": ("Small hailstorm", "storm"),
           "BL": "Blowing small hail",
           "SH": "Showers of small hail",
           "DR": "Drifting small hail",
           "FZ": "Freezing small hail",
           }),
    "UP": ("Precipitation", "rain", {
           "": "Moderate precipitation",
           "-": "Light precipitation",
           "+": "Heavy precipitation",
           "VC": "Precipitation in the vicinity",
           "MI": "Shallow precipitation",
           "BC": "Patches of precipitation",
           "PR": "Partial precipitation",
           "TS": ("Unknown thunderstorm", "storm"),
           "BL": "Blowing precipitation",
           "SH": "Showers, type unknown",
           "DR": "Drifting precipitation",
           "FZ": "Freezing precipitation",
           }),
    "BR": ("Mist", "fog", {
           "": "Moderate mist",
           "-": "Light mist",
           "+": "Thick mist",
           "VC": "Mist in the vicinity",
           "MI": "Shallow mist",
           "BC": "Patches of mist",
           "PR": "Partial mist",
           "BL": "Mist with wind",
           "DR": "Drifting mist",
           "FZ": "Freezing mist",
           }),
    "FG": ("Fog", "fog", {
           "": "Moderate fog",
           "-": "Light fog",
           "+": "Thick fog",
           "VC": "Fog in the vicinity",
           "MI": "Shallow fog",
           "BC": "Patches of fog",
           "PR": "Partial fog",
           "BL": "Fog with wind",
           "DR": "Drifting fog",
           "FZ": "Freezing fog",
           }),
    "FU": ("Smoke", "fog", {
           "": "Moderate smoke",
           "-": "Thin smoke",
           "+": "Thick smoke",
           "VC": "Smoke in the vicinity",
           "MI": "Shallow smoke",
           "BC": "Patches of smoke",
           "PR": "Partial smoke",
           "TS": ("Smoke w/ thunders", "storm"),
           "BL": "Smoke with wind",
           "DR": "Drifting smoke",
           }),
    "VA": ("Volcanic ash", "fog", {
           "": "Moderate volcanic ash",
           "+": "Thick volcanic ash",
           "VC": "Volcanic ash in the vicinity",
           "MI": "Shallow volcanic ash",
           "BC": "Patches of volcanic ash",
           "PR": "Partial volcanic ash",
           "TS": ("Volcanic ash w/ thunders", "storm"),
           "BL": "Blowing volcanic ash",
           "SH": "Showers of volcanic ash",
           "DR": "Drifting volcanic ash",
           "FZ": "Freezing volcanic ash",
           }),
    "SA": ("Sand", "fog", {
           "": "Moderate sand",
           "-": "Light sand",
           "+": "Heavy sand",
           "VC": "Sand in the vicinity",
           "BC": "Patches of sand",
           "PR": "Partial sand",
           "BL": "Blowing sand",
           "DR": "Drifting sand",
           }),
    "HZ": ("Haze", "fog", {
           "": "Moderate haze",
           "-": "Light haze",
           "+": "Thick haze",
           "VC": "Haze in the vicinity",
           "MI": "Shallow haze",
           "BC": "Patches of haze",
           "PR": "Partial haze",
           "BL": "Haze with wind",
           "DR": "Drifting haze",
           "FZ": "Freezing haze",
           }),
    "PY": ("Sprays", "fog", {
           "": "Moderate sprays",
           "-": "Light sprays",
           "+": "Heavy sprays",
           "VC": "Sprays in the vicinity",
           "MI": "Shallow sprays",
           "BC": "Patches of sprays",
           "PR": "Partial sprays",
           "BL": "Blowing sprays",
           "DR": "Drifting sprays",
           "FZ": "Freezing sprays",
           }),
    "DU": ("Dust", "fog", {
           "": "Moderate dust",
           "-": "Light dust",
           "+": "Heavy dust",
           "VC": "Dust in the vicinity",
           "BC": "Patches of dust",
           "PR": "Partial dust",
           "BL": "Blowing dust",
           "DR": "Drifting dust",
           }),
    "SQ": ("Squall", "storm", {
           "": "Moderate squall",
           "-": "Light squall",
           "+": "Heavy squall",
           "VC": "Squall in the vicinity",
           "PR": "Partial squall",
           "TS": "Thunderous squall",
           "BL": "Blowing squall",
           "DR": "Drifting squall",
           "FZ": "Freezing squall",
           }),
    "SS": ("Sandstorm", "fog", {
           "": "Moderate sandstorm",
           "-": "Light sandstorm",
           "+": "Heavy sandstorm",
           "VC": "Sandstorm in the vicinity",
           "MI": "Shallow sandstorm",
           "PR": "Partial sandstorm",
           "TS": ("Thunderous sandstorm", "storm"),
           "BL": "Blowing sandstorm",
           "DR": "Drifting sandstorm",
           "FZ": "Freezing sandstorm",
           }),
    "DS": ("Duststorm", "fog", {
           "": "Moderate duststorm",
           "-": "Light duststorm",
           "+": "Heavy duststorm",
           "VC": "Duststorm in the vicinity",
           "MI": "Shallow duststorm",
           "PR": "Partial duststorm",
           "TS": ("Thunderous duststorm", "storm"),
           "BL": "Blowing duststorm",
           "DR": "Drifting duststorm",
           "FZ": "Freezing duststorm",
           }),
    "PO": ("Dustwhirls", "fog", {
           "": "Moderate dustwhirls",
           "-": "Light dustwhirls",
           "+": "Heavy dustwhirls",
           "VC": "Dustwhirls in the vicinity",
           "MI": "Shallow dustwhirls",
           "BC": "Patches of dustwhirls",
           "PR": "Partial dustwhirls",
           "BL": "Blowing dustwhirls",
           "DR": "Drifting dustwhirls",
           }),
    "+FC": ("Tornado", "storm", {
            "": "Moderate tornado",
            "+": "Raging tornado",
            "VC": "Tornado in the vicinity",
            "PR": "Partial tornado",
            "TS": "Thunderous tornado",
            "BL": "Tornado",
            "DR": "Drifting tornado",
            "FZ": "Freezing tornado",
            }),
    "FC": ("Funnel cloud", "fog", {
           "": "Moderate funnel cloud",
           "-": "Light funnel cloud",
           "+": "Thick funnel cloud",
           "VC": "Funnel cloud in the vicinity",
           "MI": "Shallow funnel cloud",
           "BC": "Patches of funnel cloud",
           "PR": "Partial funnel cloud",
           "BL": "Funnel cloud w/ wind",
           "DR": "Drifting funnel cloud",
           }),
}

CLOUDTYPES = {
    "ACC": "altocumulus castellanus",
    "ACSL": "standing lenticular altocumulus",
    "CB": "cumulonimbus",
    "CBMAM": "cumulonimbus mammatus",
    "CCSL": "standing lenticular cirrocumulus",
    "CU": "cumulus",
    "SCSL": "standing lenticular stratocumulus",
    "SC": "stratocumulus",
    "TCU": "towering cumulus"
}


def metar_to_iso8601(metardate):
    """Convert a metar date to an ISO8601 date."""
    if metardate is not None:
        (date, hour) = metardate.split()[:2]
        (year, month, day) = date.split('.')
        # assuming tz is always 'UTC', aka 'Z'
        return ("%s-%s-%s %s:%s:00Z" %
                (year, month, day, hour[:2], hour[2:4]))


def _parse_lat_long(latlong):
    """
    Parse Lat or Long in METAR notation into float values. N and E
    are +, S and W are -. Expects one positional string and returns
    one float value.
    """
    # I know, I could invert this if and put
    # the rest of the function into its block,
    # but I find it to be more readable this way
    if latlong is None:
        return None

    cap_inp = latlong.upper().strip()
    elements = cap_inp.split('-')
    # Extract N/S/E/W
    compass_dir = elements[-1][-1]
    # get rid of compass direction
    elements[-1] = elements[-1][:-1]
    elements = [int(i) for i in elements]
    coords = 0.0
    elen = len(elements)
    if elen > 2:
        coords = coords + float(elements[2]) / 3600.0

    if elen > 1:
        coords = coords + float(elements[1]) / 60.0

    coords = coords + float(elements[0])

    if compass_dir in 'WS':
        coords = -1.0 * coords

    return coords


class WeatherReport:
    """Incorporates both the unparsed textual representation of the
    weather report and the parsed values as soon as they are filled
    in by ReportParser."""

    def _clearallfields(self):
        """Clear all fields values."""
        # until finished, report is invalid
        self.valid = 0
        # Clear all
        self.givenstationid = None
        self.fullreport = None
        self.temp = None
        self.tempf = None
        self.windspeed = None
        self.windspeedmph = None
        self.winddir = None
        self.vis = None
        self.dewp = None
        self.dewpf = None
        self.humid = None
        self.press = None
        self.pressmmHg = None
        self.code = None
        self.weather = None
        self.sky = None
        self.fulln = None
        self.cycle = None
        self.windcomp = None
        self.rtime = None
        self.pixmap = None
        self.latitude = None
        self.longitude = None
        self.altitude = None
        self.stat_city = None
        self.stat_country = None
        self.reporturl = None
        self.latf = None
        self.longf = None
        self.cloudinfo = None
        self.conditions = None
        self.w_chill = None
        self.w_chillf = None
        self.cloudtype = None

    def __init__(self, MetarStationCode=None):
        """Clear all fields and fill in wanted station id."""
        self._clearallfields()
        self.givenstationid = MetarStationCode

    def getFullReport(self):
        """ Return the complete weather report.  """
        return self.fullreport

    def getTemperatureCelsius(self):
        """
        Return the temperature in degrees Celsius.
        """
        return self.temp

    def getTemperatureFahrenheit(self):
        """
        Return the temperature in degrees Fahrenheit.
        """
        return self.tempf

    def getDewPointCelsius(self):
        """
        Return dewpoint in degrees Celsius.
        """
        return self.dewp

    def getDewPointFahrenheit(self):
        """
        Return dewpoint in degrees Fahrenheit.
        """
        return self.dewpf

    def getWindSpeed(self):
        """
        Return the wind speed in meters per second.
        """
        return self.windspeed

    def getWindSpeedMilesPerHour(self):
        """
        Return the wind speed in miles per hour.
        """
        return self.windspeedmph

    def getWindSpeedBeaufort(self):
        """
        Return the wind speed in the Beaufort scale
        cf. https://en.wikipedia.org/wiki/Beaufort_scale
        """
        if self.windspeed is not None:
            return round((self.windspeed / 0.8359648) ** (2 / 3.0))

    def getWindSpeedKnots(self):
        """
        Return the wind speed in knots
        """
        if self.windspeed is not None:
            return self.windspeed * 1.94384449

    def getWindDirection(self):
        """
        Return wind direction in degrees.
        """
        return self.winddir

    def getWindCompass(self):
        """
        Return wind direction as compass direction
        (e.g. NE or SSE)
        """
        return self.windcomp

    def getVisibilityKilometers(self):
        """
        Return visibility in km.
        """
        return self.vis

    def getVisibilityMiles(self):
        """
        Return visibility in miles.
        """
        if self.vis is not None:
            return self.vis / 1.609344

    def getHumidity(self):
        """
        Return relative humidity in percent.
        """
        return self.humid

    def getPressure(self):
        """
        Return pressure in hPa.
        """
        return self.press

    def getPressuremmHg(self):
        """
        Return pressure in mmHg.
        """
        return self.pressmmHg

    def getRawMetarCode(self):
        """
        Return the encoded weather report.
        """
        return self.code

    def getWeather(self):
        """
        Return short weather conditions
        """
        return self.weather

    def getSkyConditions(self):
        """
        Return sky conditions
        """
        return self.sky

    def getStationName(self):
        """
        Return full station name
        """
        return self.fulln

    def getStationCity(self):
        """
        Return city-part of station name
        """
        return self.stat_city

    def getStationCountry(self):
        """
        Return country-part of station name
        """
        return self.stat_country

    def getCycle(self):
        """
        Return cycle value.
        The cycle value is not the frequency or delay between
        observations but the "time slot" in which the observation was made.
        There are 24 cycle slots every day which usually last from N:45 to
        N+1:45. The cycle from 23:45 to 0:45 is cycle 0.
        """
        return self.cycle

    def getStationPosition(self):
        """
        Return latitude, longitude and altitude above sea level of station
        as a tuple. Some stations don't deliver altitude, for those, None
        is returned as altitude.  The lat/longs are expressed as follows:
        xx-yyd
        where xx is degrees, yy minutes and d the direction.
        Thus 51-14N means 51 degrees, 14 minutes north.  d may take the
        values N, S for latitues and W, E for longitudes. Latitude and
        Longitude may include seconds.  Altitude is always given as meters
        above sea level, including a trailing M.
        Schipohl Int. Airport Amsterdam has, for example:
        ('52-18N', '004-46E', '-2M')
        Moenchengladbach (where I live):
        ('51-14N', '063-03E', None)
        If you need lat and long as float values, look at
        getStationPositionFloat() instead
        """
        # convert self.altitude to string for consistency
        return (self.latitude, self.longitude, "%s" % self.altitude)

    def getStationPositionFloat(self):
        """
        Return latitude and longitude as float values in a
        tuple (lat, long, alt).
        """
        return (self.latf, self.longf, self.altitude)

    def getStationLatitude(self):
        """
        Return the station's latitude in dd-mm[-ss]D format :
        dd : degrees
        mm : minutes
        ss : seconds
        D : direction (N, S, E, W)
        """
        return self.latitude

    def getStationLatitudeFloat(self):
        """
        Return latitude as a float
        """
        return self.latf

    def getStationLongitude(self):
        """
        Return the station's longitude in dd-mm[-ss]D format :
        dd : degrees
        mm : minutes
        ss : seconds
        D : direction (N, S, E, W)
        """
        return self.longitude

    def getStationLongitudeFloat(self):
        """
        Return Longitude as a float
        """
        return self.longf

    def getStationAltitude(self):
        """
        Return the station's altitude above the sea in meters.
        """
        return self.altitude

    def getReportURL(self):
        """
        Return the URL from which the report was fetched.
        """
        return self.reporturl

    def getTime(self):
        """
        Return the time when the observation was made.  Note that this
        is *not* the time when the report was fetched by us
        Format:  YYYY.MM.DD HHMM UTC
        Example: 2002.04.01 1020 UTC
        """
        return self.rtime

    def getISOTime(self):
        """
        Return the time when the observation was made in ISO 8601 format
        (e.g. 2002-07-25 15:12:00Z)
        """
        return metar_to_iso8601(self.rtime)

    def getPixmap(self):
        """
        Return a suggested pixmap name, without extension, depending on
        current weather.
        """
        return self.pixmap

    def getCloudinfo(self):
        """
        Return a tuple consisting of the parsed cloud information and a
        suggest pixmap name
        """
        return self.cloudinfo

    def getConditions(self):
        """
        Return a tuple consisting of the parsed sky conditions and a
        suggested pixmap name
        """
        return self.conditions

    def getWindchill(self):
        """
        Return wind chill in degrees Celsius
        """
        # https://en.wikipedia.org/wiki/Wind_chill - North American wind chill
        # index
        if self.w_chill is None:
            if (self.temp and self.temp <= 10 and
                    self.windspeed and (self.windspeed * 3.6) > 4.8):

                self.w_chill = (13.12 + 0.6215 * self.temp -
                                11.37 * (self.windspeed * 3.6) ** 0.16 +
                                0.3965 * self.temp *
                                (self.windspeed * 3.6) ** 0.16)
        return self.w_chill

    def getWindchillF(self):
        """
        Return wind chill in degrees Fahrenheit
        """
        # https://en.wikipedia.org/wiki/Wind_chill - North American wind chill
        # index
        if self.w_chillf is None:
            if (self.tempf and self.tempf <= 50 and
                    self.windspeedmph and self.windspeedmph >= 3):

                self.w_chillf = (35.74 + 0.6215 * self.tempf -
                                 35.75 * self.windspeedmph ** 0.16 +
                                 0.4275 * self.tempf *
                                 self.windspeedmph ** 0.16)
            else:
                self.w_chillf = self.tempf

        return self.w_chillf

    def getCloudtype(self):
        """
        Return cloud type information
        """
        return self.cloudtype


class ReportParser:

    """Parse raw METAR data from a WeatherReport object into actual
    values and return the object with the values filled in."""

    def __init__(self, MetarReport=None):
        """Set attribute Report as specified on instantation."""
        self.Report = MetarReport

    def extractCloudInformation(self):
        """
        Extract cloud information. Return None or a tuple (sky type as a
        string of text, cloud type (if any)  and suggested pixmap name)
        """
        matches = self.match_WeatherPart(CLOUD_RE_STR)
        skytype = None
        ctype = None
        pixmap = None
        for wcloud in matches:
            if wcloud is not None:
                stype = wcloud[:3]
                if stype in ("CLR", "SKC", "CAV", "NSC"):
                    skytype = "Clear sky"
                    pixmap = "sun"
                elif stype == "BKN":
                    skytype = "Broken clouds"
                    pixmap = "suncloud"
                elif stype == "SCT":
                    skytype = "Scattered clouds"
                    pixmap = "suncloud"
                elif stype == "FEW":
                    skytype = "Few clouds"
                    pixmap = "suncloud"
                elif stype == "OVC":
                    skytype = "Overcast"
                    pixmap = "cloud"
                if ctype is None:
                    ctype = CLOUDTYPES.get(wcloud[6:], None)

        return (skytype, ctype, pixmap)

    def extractSkyConditions(self):
        """
        Extract sky condition information from the encoded report. Return
        a tuple containing the description of the sky conditions as a
        string and a suggested pixmap name for an icon representing said
        sky condition.
        """
        matches = self.match_WeatherPart(COND_RE_STR)
        for wcond in matches:
            if len(wcond) > 3 and wcond.startswith(('+', '-')):
                wcond = wcond[1:]

            if wcond.startswith(('+', '-')):
                pphen = 1
            elif len(wcond) < 4:
                pphen = 0
            else:
                pphen = 2
            squal = wcond[:pphen]
            sphen = wcond[pphen: pphen + 4]
            phenomenon = _WEATHER_CONDITIONS.get(sphen, None)
            if phenomenon is not None:
                (name, pixmap, phenomenon) = phenomenon
                pheninfo = phenomenon.get(squal, name)
                if not isinstance(pheninfo, type(())):
                    return (pheninfo, pixmap)
                else:
                    # contains pixmap info
                    return pheninfo

    def match_WeatherPart(self, regexp):
        """
        Return the matching part of the encoded Metar report.
        regexp: the regexp needed to extract this part.
        Return the first matching string or None.
        WARNING: Some Metar reports may contain several matching
        strings, only the first one is taken into account!
        """
        matches = []
        # FIXME This mixes direct access to the "code" attribute and the accessor function "getRawMetarCode" which just returns "code".
        if self.Report.code is not None:
            myre = re.compile(regexp)
            for wpart in self.Report.getRawMetarCode().split():
                match = myre.match(wpart)
                if match:
                    matches.append(match.group())
        return matches

    def ParseReport(self, MetarReport=None):
        """Take report with raw info only and return it with in
        parsed values filled in. Note: This function edits the
        WeatherReport object you supply!"""
        if self.Report is None and MetarReport is None:
            raise EmptyReportException(
                "No report given on init and ParseReport().")
        elif MetarReport is not None:
            self.Report = MetarReport

        try:
            lines = self.Report.fullreport.decode().split("\n")
        except UnicodeDecodeError:
            raise GarbledReportException(
                "Report is not valid ASCII or Unicode.")

        for line in lines:
            try:
                header, data = line.split(":", 1)
            except ValueError:
                header = data = line

            header = header.strip()
            data = data.strip()

            # The station id inside the report
            # As the station line may contain additional sets of (),
            # we have to search from the rear end and flip things around
            if header.find("(" + self.Report.givenstationid + ")") != -1:
                id_offset = header.find("(" + self.Report.givenstationid + ")")
                loc = data[:id_offset]
                coords = data[id_offset:]
                try:
                    loc = loc.strip()
                    rloc = loc[::-1]
                    rcoun, rcity = rloc.split(",", 1)
                except ValueError:
                    rcity = ""
                    rcoun = ""
                    coords = data
                try:
                    lat, lng, alt = coords.split()[1:4]
                    alt = int(alt[:-1])  # cut off 'M' for meters
                except ValueError:
                    try:
                        (lat, lng) = coords.split()[1:3]
                    except ValueError:
                        # The lat/long is completely hooped, nothing we can do.
                        (lat, lng) = (None, None)
                    alt = None
                # A few jokers out there think O==0
                if lat and "O" in lat:
                    lat = lat.replace("O", "0")
                if lng and "O" in lng:
                    lng = lng.replace("O", "0")

                self.Report.stat_city = rcity.strip()[::-1]
                self.Report.stat_country = rcoun.strip()[::-1]
                self.Report.fulln = loc
                self.Report.latitude = lat
                self.Report.longitude = lng
                self.Report.latf = _parse_lat_long(lat)
                self.Report.longf = _parse_lat_long(lng)
                self.Report.altitude = alt

            # The line containing date and time of the report
            # We have to make sure that the station ID is *not*
            # in this line to avoid trying to parse the ob: line
            elif " UTC" in data and self.Report.givenstationid not in data:
                rtime = data.split("/")[1]
                self.Report.rtime = rtime.strip()

            # temperature

            elif header == "Temperature":
                fnht, cels = data.split(None, 3)[0:3:2]
                self.Report.tempf = float(fnht)
                # The string we have split is "(NN C)", hence the slice
                self.Report.temp = float(cels[1:])

            # wind chill

            elif header == "Windchill":
                fnht, cels = data.split(None, 3)[0:3:2]
                self.Report.w_chillf = float(fnht)
                # The string we have split is "(NN C)", hence the slice
                self.Report.w_chill = float(cels[1:])

            # wind dir and speed

            elif header == "Wind":
                if "Calm" in data:
                    self.Report.windspeed = 0.0
                    self.Report.windspeedkt = 0.0
                    self.Report.windspeedmph = 0.0
                    self.Report.winddir = None
                    self.Report.windcomp = None
                elif "Variable" in data:
                    speed = data.split(" ", 3)[2]
                    self.Report.windspeed = (float(speed) * 0.44704)
                    self.Report.windspeedkt = int(data.split(" ", 5)[4][1:])
                    self.Report.windspeedmph = int(speed)
                    self.Report.winddir = None
                    self.Report.windcomp = None
                else:
                    fields = data.split(" ", 9)[0:9]
                    comp = fields[2]
                    deg = fields[3]
                    speed = fields[6]
                    speedkt = fields[8][1:]
                    self.Report.winddir = int(deg[1:])
                    self.Report.windcomp = comp.strip()
                    self.Report.windspeed = (float(speed) * 0.44704)
                    self.Report.windspeedkt = (int(speedkt))
                    self.Report.windspeedmph = int(speed)

            # visibility

            elif header == "Visibility":
                for visgroup in data.split():
                    try:
                        self.Report.vis = float(visgroup) * 1.609344
                        break
                    except ValueError:
                        self.Report.vis = None
                        break

            # dew point

            elif header == "Dew Point":
                fnht, cels = data.split(None, 3)[0:3:2]
                self.Report.dewpf = float(fnht)
                # The string we have split is "(NN C)", hence the slice
                self.Report.dewp = float(cels[1:])

            # humidity

            elif header == "Relative Humidity":
                h = data.split("%", 1)[0]
                self.Report.humid = int(h)

            # pressure

            elif header == "Pressure (altimeter)":
                press = data.split(" ", 1)[0]
                self.Report.press = float(press) * 33.863886
                # 1 in = 25.4 mm => 1 inHg = 25.4 mmHg
                self.Report.pressmmHg = float(press) * 25.4000

            # shot weather desc. ("rain", "mist", ...)

            elif header == "Weather":
                self.Report.weather = data

            # short desc. of sky conditions

            elif header == "Sky conditions":
                self.Report.sky = data

            # the encoded report itself

            elif header == "ob":
                self.Report.code = data.strip()

            # the cycle value ("time slot")

            elif header == "cycle":
                try:
                    self.Report.cycle = int(data)
                except ValueError:
                    # cycle value is missing or garbled, assume cycle 0
                    # TODO: parse the date/time header if it isn't too involved
                    self.Report.cycle = 0

        # cloud info
        cloudinfo = self.extractCloudInformation()
        (cloudinfo, cloudtype, cloudpixmap) = cloudinfo

        conditions = self.extractSkyConditions()
        if conditions is not None:
            (conditions, condpixmap) = conditions
        else:
            (conditions, condpixmap) = (None, None)

        # Some people might want to always use sky or cloud info specifially
        self.Report.cloudinfo = (cloudinfo, cloudpixmap)
        self.Report.conditions = (conditions, condpixmap)

        # fill the weather information
        self.Report.weather = self.Report.weather or conditions or cloudinfo

        # Pixmap guessed from general conditions has priority
        # over pixmap guessed from clouds
        self.Report.pixmap = condpixmap or cloudpixmap

        # Cloud type (Cumulonimbus etc.)
        if self.Report.cloudtype is None:
            self.Report.cloudtype = cloudtype

        # report is complete
        self.Report.valid = 1

        return self.Report


class ReportFetcher:

    """Fetches a report from a given METAR id, optionally taking into
       account a different baseurl and using environment var-specified
       proxies."""

    def __init__(self, MetarStationCode=None,
                 baseurl="https://tgftp.nws.noaa.gov/data/observations/"
                         "metar/decoded/"):
        """Set stationid attribute and base URL to fetch report from"""
        self.stationid = MetarStationCode
        self.baseurl = baseurl

    def MakeReport(self, StationID, RawReport):
        """
        Take a string (RawReport) and a station code and turn it
        into an object suitable for ReportParser
        """
        self.reporturl = "%s%s.TXT" % (self.baseurl, StationID)
        self.fullreport = RawReport
        report = WeatherReport(StationID)
        report.reporturl = self.reporturl
        report.fullreport = self.fullreport
        self.report = report  # Caching it for GetReport()

        return report

    def FetchReport(self, StationCode=None, proxy=None):
        """
        Fetch a report for a given station ID from the baseurl given
        upon creation of the ReportFetcher instance.
        If proxy is not None, a proxy URL of the form
        protocol://user:password@host.name.tld:port/
        is expected, for example:
        http://squid.somenet.com:3128/
        If no proxy is specified, the environment variable http_proxy
        is inspected. If it isn't set, a direct connection is tried.
        """
        if self.stationid is None and StationCode is None:
            raise EmptyIDException(
                "No ID given on init and FetchReport().")
        elif StationCode is not None:
            self.stationid = StationCode

        self.stationid = self.stationid.upper()
        self.reporturl = "%s%s.TXT" % (self.baseurl, self.stationid)

        if proxy:
            p_dict = {'http': proxy}
            p_handler = urllib.request.ProxyHandler(p_dict)
            opener = urllib.request.build_opener(
                p_handler, urllib.request.HTTPHandler)
            urllib.request.install_opener(opener)
        else:
            urllib.request.install_opener(
                urllib.request.build_opener(urllib.request.ProxyHandler,
                                            urllib.request.HTTPHandler))

        try:
            fn = urllib.request.urlopen(self.reporturl)
        except urllib.error.HTTPError as why:
            raise NetworkException(why)

        # Dump entire report in a variable
        self.fullreport = fn.read()

        if fn.status != 200:
            raise NetworkException(
                "Could not fetch METAR report: %s" % (fn.status))

        report = WeatherReport(self.stationid)
        report.reporturl = self.reporturl
        report.fullreport = self.fullreport
        self.report = report  # Caching it for GetReport()

        return report

    def GetReport(self):
        """Get a previously fetched report again"""
        return self.report
