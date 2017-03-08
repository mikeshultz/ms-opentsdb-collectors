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
configuration.  See the "Modules" section for more information.

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

At this point, there's only one module, and that's sensu.

### Sensu

The sensu module collects information on client health and puts it into 
OpenTSDB as the `sensu_status` metric.  Configure the Sensu API base URL
in the `[sensu]` section in the ini file.

#### Config

    [sensu]
    api_url     = http://localhost:3000