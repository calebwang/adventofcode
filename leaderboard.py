import json
import time
from collections import defaultdict
from datetime import datetime
import math

inp = json.load(open("leaderboard.json"))

members = inp["members"]
days = defaultdict(lambda: defaultdict(list))

start_dt = datetime(2021, 11, 29, 21)
start_ts = int(start_dt.timestamp())
sec_per_day = 3600 * 24


def format_time(seconds):
    days = math.floor(seconds / sec_per_day)
    return ("{}d ".format(days) if days > 0 else "") + time.strftime('%H:%M:%S', time.gmtime(seconds))

for mem_id, member in members.items():
    for day, entry in member['completion_day_level'].items():
        if '1' in entry:
            raw_time = days[day][member['name']].append(entry['1']['get_star_ts'])
        if '2' in entry:
            days[day][member['name']].append(entry['2']['get_star_ts'])

for day in sorted(days, key=lambda d: int(d)):
    print("Day", day)
    release_ts = start_ts + int(day) * sec_per_day
    entry = days[day]
    sorted_members = sorted(entry, key=lambda m: entry[m][1] if len(entry[m]) > 1 else float('inf'))
    for member in sorted_members:
        times = entry[member]
        relative_times = [time - release_ts for time in times]
        print("{:20s}: {:11s} | {:11s}".format(
            member,
            format_time(relative_times[0]),
            format_time(relative_times[1]) if len(relative_times) > 1 else 'n/a'
        ))
    print("=======")

