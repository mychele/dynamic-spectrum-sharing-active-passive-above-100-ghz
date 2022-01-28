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


# Translate n2yo output to Google Maps input


import numpy as np
import tikzplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import math
import pickle
import time
from datetime import datetime


# generate log_file with log-sat-positions*.py
log_file = "n2yo-output.txt"
google_js_file = "html_js/lat-lng-multiple-11-24.js"


def main():
    time_visits = []
    latitude_visits = []
    longitude_visits = []
    altitute_visits = []
    elevation_visits = []

    google_format_strings_list = []
    google_format_strings_thresholds_list = []

    el_to_log = False
    google_format_strings = []
    google_format_strings_thresholds = []

    with open(log_file, 'r') as f:
        for line in f:
            strings = line.split(", ")
            el_string = strings[-1]
            el = float(el_string.split(": ")[1].split("}")[0])
            if el >= 0:
                elevation_visits.append(el)
                lat_string = strings[2]
                lat = float(lat_string.split(": ")[1])
                latitude_visits.append(lat)
                lon = float(strings[5].split(": ")[1])
                longitude_visits.append(lon)
                alt = float(strings[7].split(": ")[1])
                altitute_visits.append(alt)
                time_visits.append(strings[0])
                el_to_log = True
                google_format_strings.append(
                    "{ lat: " + str(lat) + ", lng: " + str(lon) + " },\n")

                if el >= 9.3:
                    google_format_strings_thresholds.append(
                        "{ lat: " + str(lat) + ", lng: " + str(lon) + " },\n")

            if el_to_log is True and el < 0:
                google_format_strings_list.append(google_format_strings)
                google_format_strings_thresholds_list.append(
                    google_format_strings_thresholds)
                el_to_log = False
                google_format_strings = []
                google_format_strings_thresholds = []

    with open(google_js_file, "w") as f:
        pass_index = 0
        for entry in google_format_strings_list:
            f.write("const flightPlanCoordinates_" +
                    str(pass_index) + " = [\n")
            for loc in entry:
                f.write(loc)
            f.write("];\n")
            pass_index += 1
        f.write("const pass_index = " + str(pass_index) + ";\n")

        pass_index = 0
        for entry in google_format_strings_thresholds_list:
            f.write("const flightPlanCoordinatesAbove_" +
                    str(pass_index) + " = [\n")
            for loc in entry:
                f.write(loc)
            f.write("];\n")
            pass_index += 1
        f.write("const pass_index_above = " + str(pass_index) + ";\n")


if __name__ == '__main__':
    main()
