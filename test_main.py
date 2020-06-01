zone = pytz.timezone("Australia/Adelaide")
local_time = pytz.utc.localize(utc_time).astimezone(zone)