#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, time, configparser, potsdb, importlib
from datetime import timedelta
from orccollector.core.utils import interval_regex, parse_time

home_config = "~/.orc.ini"
sys_config = "/etc/orc.ini"

config = configparser.ConfigParser()
read_files = config.read([os.path.expanduser(home_config), sys_config])

last_checks = {}

""" Config santity checks """

# Make sure files were read
if len(read_files) < 1:
    print("orc-collector: Error: Could not find configuration.  Make sure you create %s or %s." % (home_config, sys_config))
    sys.exit(1)

""" Config parsing """

# Get the OTSDB connect args together
otsdb_kwargs = {
    "port": config.getint('otsdb', 'port', fallback=4242),
    "qsize": config.getint('otsdb', 'qsize', fallback=1000),
    "host_tag": config.get('otsdb', 'host_tag', fallback=True),
    "mps": config.getint('otsdb', 'mps', fallback=100),
    "check_host": config.getboolean('otsdb', 'check_host', fallback=True),
}
db = potsdb.Client(config.get('otsdb', 'host', fallback='localhost'), **otsdb_kwargs)

# Parse interval
INTERVAL = parse_time(config.get('default', 'interval', fallback=""))

""" Second round of config sanity checks """

# Make sure interval is set...
if not INTERVAL:
    print("orc-collector: Error: 'interval' setting is undefined.")
    sys.exit(2)

# ...and that it's valid
#if not interval_regex.match(INTERVAL):
#    print("orc-collector: Error: %s is not a valid interval configuration.  Should be in format XhrYmZs." % (INTERVAL))
#    sys.exit(2)

""" Util functions """

def process_metric(metric, value, tags = {}):
    # If we got results...
    if metric and value is not None:
        print("orc-collector: Info: Processing metric '%s' with value '%s'" % (metric, value))
        # ...put them into OpenTSDB
        db.send(metric, value, **tags)
    else:
        print("orc-collector: Warning: Metric is either undefined or has no value.  Not sending to OpenTSDB.")

""" Do the needful """
def collect():
    # Assume each config section is an enabled module
    for section in config.sections():
        if section != 'default' and section != 'otsdb':

            mod = None

            # Let's see if we can import it
            try:

                mod = importlib.import_module('orccollector.' + section)

            except ImportError:

                print("orc-collector: Warning: %s is not a valid module." % section)

            # If we did...
            if mod:

                # If there's an interval setting for this module, 
                # make sure we don't run it in a shorter time window
                if config.get(section, 'interval', fallback=None):
                    intv = parse_time(config.get(section, 'interval'))
                    
                    if last_checks.get(section):
                        
                        if (time.time() - last_checks[section]) < intv.total_seconds():
                            continue

                # Run it
                module_data = []
                module_data = mod.run(config[section])

                if type(module_data) == type([]):

                    if len(module_data) > 0:
                        for metric,value,tags in module_data:
                            process_metric(metric, value, tags)
                            last_checks[section] = time.time()
                    else:
                        print("orc-collector: Warning: Module returned no results")

                elif type(module_data) == type((None, None, None)):
                    process_metric(module_data[0], module_data[1], module_data[2])
                    last_checks[section] = time.time()

                else:

                    print("orc-collector: Warning: No idea what type of data the %s module is returning." % (section))

            # hm
            else:
                print("orc-collector: Warning: Unable to import module %s" % section)

def main():
    try:
        while True:
            # get start time
            before = time.time()

            # run the main junk
            collect()

            # get the time now
            after = time.time()

            # sleep if necessary to hit the next interval
            time.sleep((INTERVAL - timedelta(seconds=(after - before))).seconds)

    except KeyboardInterrupt:
        db.wait()
        sys.exit(0)

if __name__ == '__main__':
    main()

