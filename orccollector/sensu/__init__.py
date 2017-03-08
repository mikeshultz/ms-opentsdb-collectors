# -*- coding: utf-8 -*-

import requests

class SensuMetrics:
    """ Get sensu metrics from its RESTful API """

    root_url = None
    metrics = []

    def __init__(self, root_url):
        self.root_url = root_url

    def clients(self):
        """ Get all basic hosts metrics """

        req = requests.get(self.root_url + "/clients")

        if req.status_code == 200:
            dat = req.json()
            for host in dat:
                self.metrics.append(('sensu_status', host['status'], {'host': host['name'], 'dc': host['dc']}))

    def metrics(self):
        """ Gets the metrics processed up until this point """
        self.metrics = []
        
        self.clients()

        if len(self.metrics) > 0:
            return self.metrics
        else:
            return None

def run(conf):
    """ Process sensu metrics """

    sm = SensuMetrics(conf['api_url'])
    results = []
    results += sm.metrics()
    return results