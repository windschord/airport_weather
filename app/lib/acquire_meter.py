# -*- coding:utf-8 -*-
import urllib.parse
import urllib.request
from xml.etree import ElementTree
import dateutil.parser

from app import app
from app.model.meter import Meter
from app.model.meter_sky_condition import MeterSkyCondition


__author__ = 'windschord.com'


class AcquireMeter(object):
    def __init__(self):
        self.URL = 'http://www.aviationweather.gov/adds/dataserver_current/httpparam?'

    def execute(self, station, hours):
        res = self.__request_awc(station.name, hours)
        return self.__parse_xml(station, res)

    def __request_awc(self, station_name, hours):
        values = {'dataSource': 'metars',
                  'requestType': 'retrieve',
                  'format': 'xml',
                  'stationString': station_name,
                  'hoursBeforeNow': hours}

        data = urllib.parse.urlencode(values)
        req = urllib.request.Request(self.URL + data)
        app.logger.debug('req: %s' % req.get_full_url())

        response = urllib.request.urlopen(req)
        the_page = response.read()
        app.logger.debug('res: %s' % the_page)
        return the_page

    def __parse_xml(self, station, xml_data):
        ret = []
        root = ElementTree.fromstring(xml_data)
        for d in list(root.find('data')):
            time = dateutil.parser.parse(d.find('observation_time').text)
            air_temp = d.find('temp_c').text
            dewpoint = d.find('dewpoint_c').text
            wind_dir = d.find('wind_dir_degrees').text
            wind_speed = d.find('wind_speed_kt').text
            visibility = d.find('visibility_statute_mi').text
            altimeter = d.find('altim_in_hg').text

            if d.find('sea_level_pressure_mb'):
                sea_level_press = d.find('sea_level_pressure_mb').text
            else:
                sea_level_press = None

            sky_condition = []
            for sc in d.iter('sky_condition'):
                sky_cover = sc.attrib['sky_cover']
                cloud_base_ft_agl = sc.attrib['cloud_base_ft_agl']
                sky_condition.append(MeterSkyCondition(sky_cover, cloud_base_ft_agl))

            flight_category = d.find('flight_category').text
            elevation_m = d.find('elevation_m').text

            ret.append(Meter(station.id, time, air_temp, dewpoint, wind_dir,
                             wind_speed, visibility, altimeter, sky_condition,
                             flight_category, elevation_m, sea_level_press))
        app.logger.debug(ret)
        return ret