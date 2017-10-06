# -*- coding: utf-8 -*-

import requests, json

""" TODO
    - All string value metrics commented out because potsdb does not 
      support annotations.
"""

class DarkSkyMetrics:
    """ Get some data from DarkSky about weather """

    root_url = "https://api.darksky.net"

    def __init__(self, key, latlongs):
        self.key = key
        self.latlongs = latlongs
        self.metrics = []

    def get_forecast(self, name, lat, lng):
        """ Get the forecast from DarkSky """

        qstring = "exclude=minutely,hourly"
        url = self.root_url + "/forecast/" + self.key + "/" + str(lat) + "," + str(lng) + "?" + qstring
        req = requests.get(url)

        if req.status_code == 200:
            dat = req.json()

            current_conditions = dat.get('currently')

            # Current conditions
            if current_conditions:
                #self.metrics.append(('weather_summary', dat['currently']['summary'], { 'location': name, }))
                if current_conditions.get('nearestStormDistance'):
                    self.metrics.append(('weather_nearestStormDistance', current_conditions['nearestStormDistance'], { 'location': name, }))
                if current_conditions.get('precipProbability'):
                    self.metrics.append(('weather_precipProbability', current_conditions['precipProbability'], { 'location': name, }))
                if current_conditions.get('temperature'):
                    self.metrics.append(('weather_temperature', current_conditions['temperature'], { 'location': name, }))
                if current_conditions.get('humidity'):
                    self.metrics.append(('weather_humidity', current_conditions['humidity'], { 'location': name, }))
                if current_conditions.get('windSpeed'):
                    self.metrics.append(('weather_windSpeed', current_conditions['windSpeed'], { 'location': name, }))
                if current_conditions.get('windBearing'):
                    self.metrics.append(('weather_windBearing', current_conditions['windBearing'], { 'location': name, }))
                if current_conditions.get('pressure'):
                    self.metrics.append(('weather_pressure', current_conditions['pressure'], { 'location': name, }))

            # Get weather alerts
            # TODO: Support multiple alerts.  Is that even doable?
            #if dat.get('alerts'):
            #    self.metrics.append(('weather_alert_title', dat['alerts'][0]['title'], { 'location': name, }))
            #    self.metrics.append(('weather_alert_description', dat['alerts'][0]['description'], { 'location': name, }))

        else:
            print("DarkSky: Error: HTTP request failed with code %s" % req.status_code)

    def get_all(self):
        """ Get all forecasts """
        
        for loc in self.latlongs:
            self.get_forecast(loc['name'], loc['lat'], loc['lng'])

        return self.metrics

def run(conf):
    """ Get all metrics """
    if not conf['location_json']:
        print('DarkSkyMetrics: Warning: location_json is undefined')
        return

    latlongs = []
    with open(conf['location_json']) as fil:
        location_json = json.load(fil)
        for loc in location_json:
            latlongs.append({'name': loc['name'], 'lat': loc['lat'], 'lng': loc['lng']})

    dsm = DarkSkyMetrics(conf['api_key'], latlongs)

    results = []
    results += dsm.get_all()
    return results

