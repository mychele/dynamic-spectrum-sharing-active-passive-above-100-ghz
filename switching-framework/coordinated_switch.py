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

import requests
import sched
import time
from datetime import datetime

s = sched.scheduler(time.time, time.sleep)

# SPDT switch
# https://www.minicircuits.com/softwaredownload/Prog_Manual-2-Switch.pdf
switch_url = "http://192.168.1.104/"  # update with the IP of the SPDT switch
switch_command = "SETA="


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
    call_switch(1)


def trigger_120_to_240(trigger_time):
    print("End pass - switching")
    print_trigger_time(trigger_time)
    call_switch(0)


def main():
    # modify these lists with proper time
    # you can use the generate_utc_time to generate properly
    # formatted entries based on time.now() + delta
    time_240_to_120 = [1603551411, 1603551471,
                       1603551531, 1603551591, 1603551651]
    time_120_to_240 = [val + 30 for val in time_240_to_120]

    for time_val in time_240_to_120:
        print(time_val)
        s.enterabs(time_val, 0, trigger_240_to_120,
                   (time_val,))

    for time_val in time_120_to_240:
        print(time_val)
        s.enterabs(time_val, 0, trigger_120_to_240,
                   (time_val,))
    s.run()


if __name__ == '__main__':
    main()
