import re
from datetime import timedelta

interval_regex = re.compile(r'((?P<hours>\d+?)hr)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?')

# Thanks to http://stackoverflow.com/questions/4628122/how-to-construct-a-timedelta-object-from-a-simple-string
def parse_time(time_str):
    parts = interval_regex.match(time_str)
    if not parts:
        return
    parts = parts.groupdict()
    time_params = {}
    for (name, param) in parts.items():
        if param:
            time_params[name] = int(param)
    return timedelta(**time_params)
