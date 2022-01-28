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


# This script triggers a switch on the SPDT device at URL switch_url
# based on n2yo information


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

# SPDT switch
# https://www.minicircuits.com/softwaredownload/Prog_Manual-2-Switch.pdf
switch_url = "http://192.168.1.104/"  # update with the IP of the SPDT switch
switch_command = "SETA="

# parameters
threshold = -194  # dBW, ITU
obs_lat = 42.338123  # ground station
obs_lon = -71.088927  # ground station
obs_alt = 10
freq = 240.0
ptx = 23.0
max_gain = 50.0
log_file = "positions-prx.txt"


def call_switch(state):
    r = requests.get(url=switch_url + switch_command + str(state))
    print(r.json())


def print_trigger_time(trigger_time):
    print("Time now: %s -- Time scheduled: %s" % (time.time(), trigger_time))
    print("Time now %s " % (datetime.now().strftime("%Y%m%d-%H:%M:%S")))
    print("Time sched %s" % (datetime.utcfromtimestamp(
        trigger_time).strftime("%Y%m%d-%H:%M:%S")))


def trigger_240_to_120(trigger_time):
    print("Pass - switching")
    print_trigger_time(trigger_time)
    call_switch(0)


def trigger_120_to_240(trigger_time):
    print("End pass - switching")
    print_trigger_time(trigger_time)
    call_switch(1)


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
    prx_bw = []

    print_true = True

    for pos in positions:
        alt = float(pos['sataltitude'])
        elevation = float(pos['elevation'])
        # TODO here compute the received power based on altitute and elevation
        # the original framework uses an ITU-based model, other models can be 
        # plugged in as well
        prx_bw.append(0)  # TODO update 0 with a meaningful value

        if print_true:
            print("alt %f el %f prx_bw %f" % (alt, elevation, prx_bw[0]))
            print_true = False

    return prx_bw


def periodic_check(prev_switch_status, end_pass_time):
    print("periodic_check Time now: %s -- Time end: %s" %
          (time.time(), end_pass_time))
    print("periodic_check Time now %s " %
          (datetime.now().strftime("%Y%m%d-%H:%M:%S")))
    print("periodic_check Time end %s" % (datetime.utcfromtimestamp(
        end_pass_time).strftime("%Y%m%d-%H:%M:%S")))

    # need to schedule this every 5 minutes
    positions = get_positions()
    prx_bw = get_prx_bw(positions)

    interference_positions = [(prx_bw_val > threshold)
                              for prx_bw_val in prx_bw]

    # log
    with open(log_file, 'w') as f:
        for index, interf in enumerate(interference_positions):
            str_to_print = str(time.time()) + ", "
            str_to_print += str(datetime.now().strftime("%Y%m%d-%H:%M:%S")) + ", "
            str_to_print += str(positions[index]) + ", "
            str_to_print += str(prx_bw[index]) + ", "
            str_to_print += str(interference_positions[index]) + "\n"
            f.write(str_to_print)

    positions_to_switch_120_to_240 = []
    utc_time_to_switch_120_to_240 = []
    positions_to_switch_240_to_120 = []
    utc_time_to_switch_240_to_120 = []

    # create lists with switching times
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

    # schedule switch events
    for time_val in utc_time_to_switch_120_to_240:
        s.enterabs(time_val, 0, trigger_120_to_240, (time_val,))
    for time_val in utc_time_to_switch_240_to_120:
        s.enterabs(time_val, 0, trigger_240_to_120, (time_val,))

    # schedule this method again
    if (time.time() < end_pass_time):
        s.enterabs(time.time() + 300, 0, periodic_check,
                   (interference_positions[-1], end_pass_time,))


def run_check_interference(start_pass_time, end_pass_time):
    # start the periodic check
    periodic_check(0, end_pass_time)


def main():
    print(API_KEY)

    # get passes
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

    # schedule a check event for each pass
    num_pass = passes_dict['info']['passescount']
    for pass_index in range(num_pass):
        print(pass_index)
        start_pass_time = passes_dict['passes'][pass_index]['startUTC']
        end_pass_time = passes_dict['passes'][pass_index]['endUTC']
        print("Start %s -- end %s %s" %
              (start_pass_time, end_pass_time, datetime.utcfromtimestamp(start_pass_time).strftime("%Y%m%d-%H:%M:%S")))

        # schedule precise checks during passes
        s.enterabs(start_pass_time, 0, run_check_interference,
                   (start_pass_time, end_pass_time,))

    s.run()


if __name__ == '__main__':
    main()
