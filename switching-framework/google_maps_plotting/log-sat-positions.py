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
# It also checks path loss and received power


import requests
import sched
import time
from datetime import datetime
import math

# this is an example of how to import matlab in python for channel model computations
import matlab.engine
eng = matlab.engine.start_matlab()

s = sched.scheduler(time.time, time.sleep)


# n2yo
API_KEY = "XYZ"  # register for a key at n2yo.com
trail = "&apiKey=" + API_KEY
base_url = "https://api.n2yo.com/rest/v1/satellite/"
id = 28376  # AURA
log_file = "n2yo-output.txt"

# parameters
threshold = -194  # dBW, ITU
obs_lat = 42.338123  # ground station
obs_lon = -71.088927  # ground station
obs_alt = 10
freq = 240.0
ptx = 23.0
max_gain = 50.0


def print_trigger_time(trigger_time):
    print("Time now: %s -- Time scheduled: %s" % (time.time(), trigger_time))
    print("Time now %s " % (datetime.now().strftime("%Y%m%d-%H:%M:%S")))
    print("Time sched %s" % (datetime.utcfromtimestamp(
        trigger_time).strftime("%Y%m%d-%H:%M:%S")))


def trigger_240_to_120(trigger_time):
    print("Pass - switching")
    print_trigger_time(trigger_time)


def trigger_120_to_240(trigger_time):
    print("End pass - switching")
    print_trigger_time(trigger_time)


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


def get_prx_bw(positions):
    # need altitude and elevation angles
    # pathloss = [10] * len(positions)
    # pathloss[20:60] = [20] * (60 - 20)

    prx_bw = []
    pathloss = []

    print_true = True

    for pos in positions:
        alt = float(pos['sataltitude'])
        elevation = float(pos['elevation'])
        # TODO here compute the received power based on altitute and elevation
        # the original framework uses an ITU-based model, other models can be 
        # plugged in as well
        pathloss_val = 0
        pathloss.append(pathloss_val)  # TODO update 0 with a meaningful value
        prx_val = ptx + max_gain - pathloss_val - 10 * math.log10(3e6)
        prx_bw.append(prx_val)

        if print_true:
            print("alt %f el %f prx_bw %f" % (alt, elevation, prx_bw[0]))
            print_true = False

    return (prx_bw, pathloss)


def periodic_check(prev_switch_status, end_pass_time, first_time_run):
    print("periodic_check Time now: %s -- Time end: %s" %
          (time.time(), end_pass_time))
    print("periodic_check Time now %s " %
          (datetime.now().strftime("%Y%m%d-%H:%M:%S")))
    print("periodic_check Time end %s" % (datetime.utcfromtimestamp(
        end_pass_time).strftime("%Y%m%d-%H:%M:%S")))
    # need to schedule this every 5 minutes
    positions = get_positions()
    prx_bw, pathloss = get_prx_bw(positions)

    interference_positions = [(prx_bw_val > threshold)
                              for prx_bw_val in prx_bw]

    with open(log_file, 'a') as f:
        for index, interf in enumerate(interference_positions):
            str_to_print = str(time.time()) + ", "
            str_to_print += str(datetime.now().strftime("%Y%m%d-%H:%M:%S")) + ", "
            str_to_print += str(positions[index]) + ", "
            str_to_print += str(prx_bw[index]) + ", "
            str_to_print += str(pathloss[index]) + ", "
            str_to_print += str(interference_positions[index]) + "\n"
            f.write(str_to_print)

    positions_to_switch_120_to_240 = []
    utc_time_to_switch_120_to_240 = []
    positions_to_switch_240_to_120 = []
    utc_time_to_switch_240_to_120 = []

    for index, interf in enumerate(interference_positions):
        if index == 0:
            if interf != prev_switch_status:
                if interf == 1:
                    positions_to_switch_240_to_120.append(positions[index])
                    utc_time_to_switch_240_to_120.append(
                        positions[index]['timestamp'])
                else:
                    positions_to_switch_120_to_240.append(positions[index])
                    utc_time_to_switch_120_to_240.append(
                        positions[index]['timestamp'])
        else:
            if interf != interference_positions[index - 1]:
                if interf == 1:
                    positions_to_switch_240_to_120.append(positions[index])
                    utc_time_to_switch_240_to_120.append(
                        positions[index]['timestamp'])
                else:
                    positions_to_switch_120_to_240.append(positions[index])
                    utc_time_to_switch_120_to_240.append(
                        positions[index]['timestamp'])

    for time_val in utc_time_to_switch_120_to_240:
        s.enterabs(time_val, 0, trigger_120_to_240, (time_val,))
    for time_val in utc_time_to_switch_240_to_120:
        s.enterabs(time_val, 0, trigger_240_to_120, (time_val,))

    s.enterabs(time.time() + 300, 0, periodic_check,
               (interference_positions[-1], end_pass_time, False))
    if(first_time_run):
        s.run()


def main():
    print(API_KEY)

    # /radiopasses/{id}/{observer_lat}/{observer_lng}/{observer_alt}/{days}/{min_elevation}
    request_api = "/radiopasses/"
    days = 2
    min_elevation = 0
    response = requests.get(base_url + request_api + str(id)
                            + "/" + str(obs_lat) + "/" + str(obs_lon)
                            + "/" + str(obs_alt)
                            + "/" + str(days)
                            + "/" + str(min_elevation)
                            + trail)
    print(response.json())
    passes_dict = response.json()
    print(passes_dict)
    s.run()

    periodic_check(0, 0, True)


if __name__ == '__main__':
    main()
