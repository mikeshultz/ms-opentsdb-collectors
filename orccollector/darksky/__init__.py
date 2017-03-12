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

            # Current conditions
            if dat.get('currently'):
                #self.metrics.append(('weather_summary', dat['currently']['summary'], { 'location': name, }))
                self.metrics.append(('weather_nearestStormDistance', dat['currently']['nearestStormDistance'], { 'location': name, }))
                self.metrics.append(('weather_precipProbability', dat['currently']['precipProbability'], { 'location': name, }))
                self.metrics.append(('weather_temperature', dat['currently']['temperature'], { 'location': name, }))
                self.metrics.append(('weather_humidity', dat['currently']['humidity'], { 'location': name, }))
                self.metrics.append(('weather_windSpeed', dat['currently']['windSpeed'], { 'location': name, }))
                self.metrics.append(('weather_windBearing', dat['currently']['windBearing'], { 'location': name, }))
                self.metrics.append(('weather_pressure', dat['currently']['pressure'], { 'location': name, }))

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

