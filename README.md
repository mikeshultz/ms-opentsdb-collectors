# orccollector

Handy OpenTSDB collectors.

## Configuration

Make sure to add `/etc/orc.ini` or `~/.orc.ini` using the following as a sample:

    [default]
    interval    = 10s

    [otsdb]
    host        = localhost
    port        = 4242
    qsize       = 1000
    host_tag    = True
    mps         = 100
    check_host  = True

    [sensu]
    api_url     = http://localhost:3000

Each module must have it's own section in the ini with its own 
configuration.  See the "[Modules](#modules)" section for more information.

## Install

`python setup.py install`

## Run

`orccollector` runs as a constant loop.  You can run it standalone with 
just the command `orccollector`.  Alternatively, you can configure 
supervisord to watch over the process.

### supervisord

Example configuration for supervisord.

    [program:orccollector]
    command=orccollector
    stdout_logfile=/var/log/orccollector.log
    stderr_logfile=/var/log/orccollector.error.log
    stdout_logfile_maxbytes=5MB
    stderr_logfile_maxbytes=5MB

## Modules

### Sensu

The sensu module collects information on client health and puts it into 
OpenTSDB as the `sensu_status` metric.  Configure the Sensu API base URL
in the `[sensu]` section in the ini file.

#### Config

    [sensu]
    api_url     = http://localhost:3000

### DarkSky

[DarkSky](https://darksky.net/dev/) provides weather information via a 
RESTful API.  You can make up to 1000 calls per day to their API at no 
charge.

#### Config 

    [darksky]
    api_key       = 0123456789abcdef
    location_json = /path/to/weather_locations.json
    interval    = 30m

**NOTE**: Make sure to pay attention to the interval so you don't go 
above the amount of API calls you intend.  24 hours has 1440 seconds in 
it so a call per second will hit that limit.