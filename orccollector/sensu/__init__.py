# -*- coding: utf-8 -*-
import sys
import requests

class SensuMetrics:
    """ Get sensu metrics from its RESTful API """

    root_url = None
    metrics = []

    def __init__(self, root_url):
        self.root_url = root_url

    def clients(self):
        """ Get all basic hosts metrics """

        try:
            req = requests.get(self.root_url + "/clients")
        except requests.exceptions.ConnectionError as e:
            req = None
            print(str(e), file=sys.stderr)
        except Exception as e:
            print("Unknown error making a request to the Sensu API", file=sys.stderr)
            print(str(e), file=sys.stderr)

        if req and req.status_code == 200:
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
            return []

def run(conf):
    """ Process sensu metrics """

    sm = SensuMetrics(conf['api_url'])
    results = []
    results += sm.metrics()
    return results