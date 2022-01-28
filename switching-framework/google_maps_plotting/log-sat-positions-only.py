# Copyright 2021, Michele Polese <michele.polese@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation;
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


# This script logs the positions of NASA Aura using n2yo information

import requests
import sched
import time
from datetime import datetime
import math

s = sched.scheduler(time.time, time.sleep)

# n2yo
API_KEY = "XYZ"  # register for a key at n2yo.com
trail = "&apiKey=" + API_KEY
base_url = "https://api.n2yo.com/rest/v1/satellite/"
id = 28376  # AURA
log_file = "n2yo-output.txt"


def get_positions():
    # /positions/{id}/{observer_lat}/{observer_lng}/{observer_alt}/{seconds}
    request_api = "/positions/"
    seconds_future = 300  # number of positions, one for each s, max 300

    response = requests.get(base_url + request_api + str(id)
                            + "/" + str(obs_lat) + "/" + str(obs_lon)
                            + "/" + str(obs_alt)
                            + "/" + str(seconds_future)
                            + trail)
    # print(response.json())
    return response.json()['positions']


def periodic_check(first_time_run):
    print("periodic_check Time now: %s" %
          (time.time()))
    print("periodic_check Time now %s " %
          (datetime.now().strftime("%Y%m%d-%H:%M:%S")))
    # need to schedule this every 5 minutes
    positions = get_positions()

    with open(log_file, 'a') as f:
        for index, interf in enumerate(positions):
            str_to_print = str(time.time()) + ", "
            str_to_print += str(datetime.now().strftime("%Y%m%d-%H:%M:%S")) + ", "
            str_to_print += str(positions[index]) + "\n"
            f.write(str_to_print)

    s.enterabs(time.time() + 300, 0, periodic_check,
               (False,))
    if(first_time_run):
        s.run()


def main():
    print(API_KEY)
    s.run()
    periodic_check(True)


if __name__ == '__main__':
    main()
