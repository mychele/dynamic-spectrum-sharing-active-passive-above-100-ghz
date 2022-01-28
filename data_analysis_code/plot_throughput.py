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


# This script plots throughput over time


import numpy as np
import tikzplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import math
import pickle


agc_sel = "without-agc"
mcs_sel = "bpsk-1-5"

start_times = {}
start_times["without-agc"] = {}
start_times["without-agc"]["bpsk-1-5"] = [3686494015.035700, 3686494045.032000, 3686494075.026400, 3686494105.031400, 3686494135.035300,
                                          3686494165.030100, 3686494195.033900, 3686494225.028200, 3686494255.033900, 3686494285.028400, 3686494315.031600, 3686494345.030300]
start_times_centr = {}
start_times_centr["without-agc"] = {}
start_times_centr["without-agc"]["bpsk-1-5"] = [3686679300.5883, 3686679330.6497, 3686679360.6915, 3686679390.7422, 3686679420.8116,
                                                3686679450.8648, 3686679480.9038, 3686679510.9563, 3686679541.0069, 3686679571.0486, 3686679601.0873, 3686679631.2005]


decimation_factor = 10

fig, ax = plt.subplots()
ax.grid(True)
color = 'tab:red'
color_2 = 'tab:blue'
ax.set_xlabel('time UTC (s)')
ax.set_ylabel('throughput [Mbps]', color=color)
ax.tick_params(axis='y', labelcolor=color)


campaign_folder = "distributed"
with open(campaign_folder + ".p", "rb") as pf:
    t = pickle.load(pf)

    time_dict = t[0]
    throughput_dict = t[1]

    time_support = time_dict[agc_sel][mcs_sel]
    throughput = throughput_dict[agc_sel][mcs_sel]

    time_support_to_plot = []
    throughput_to_plot = []

    start_index = time_support.index(start_times[agc_sel][mcs_sel][0])
    time_support_to_plot.extend(
        [val for index, val in enumerate(time_support) if (index % decimation_factor == 0 and index < start_index)])

    throughput_to_plot.extend(
        [val for index, val in enumerate(throughput) if (index % decimation_factor == 0 and index < start_index)])

    for vec_index, time_entry in enumerate(start_times[agc_sel][mcs_sel]):
        start_index = time_support.index(time_entry)
        try:
            index_next = time_support.index(
                start_times[agc_sel][mcs_sel][vec_index + 1])
        except IndexError:
            index_next = start_index + 40

        time_support_to_plot.extend(
            [val for index, val in enumerate(time_support) if (index >= start_index and index < start_index + 20)])

        throughput_to_plot.extend(
            [val for index, val in enumerate(throughput) if (index >= start_index and index < start_index + 20)])

        time_support_to_plot.extend(
            [val for index, val in enumerate(time_support) if (index >= start_index + 20 and index < index_next and index % decimation_factor == 0)])

        throughput_to_plot.extend(
            [val for index, val in enumerate(throughput) if (index >= start_index + 20 and index < index_next and index % decimation_factor == 0)])

    ax.plot([entry - start_times[agc_sel][mcs_sel][0] for entry in time_support_to_plot],
            throughput_to_plot, color=color)


campaign_folder = "centralized"
with open(campaign_folder + ".p", "rb") as pf:
    t = pickle.load(pf)

    time_dict = t[0]
    throughput_dict = t[1]

    time_support = time_dict[agc_sel][mcs_sel]
    throughput = throughput_dict[agc_sel][mcs_sel]

    time_support_to_plot = []
    throughput_to_plot = []

    start_index = time_support.index(start_times_centr[agc_sel][mcs_sel][0])
    time_support_to_plot.extend(
        [val for index, val in enumerate(time_support) if (index % decimation_factor == 0 and index < start_index)])

    throughput_to_plot.extend(
        [val for index, val in enumerate(throughput) if (index % decimation_factor == 0 and index < start_index)])

    for vec_index, time_entry in enumerate(start_times_centr[agc_sel][mcs_sel]):
        start_index = time_support.index(time_entry)
        try:
            index_next = time_support.index(
                start_times_centr[agc_sel][mcs_sel][vec_index + 1])
        except IndexError:
            index_next = start_index + 40

        time_support_to_plot.extend(
            [val for index, val in enumerate(time_support) if (index >= start_index and index < start_index + 20)])

        throughput_to_plot.extend(
            [val for index, val in enumerate(throughput) if (index >= start_index and index < start_index + 20)])

        time_support_to_plot.extend(
            [val for index, val in enumerate(time_support) if (index >= start_index + 20 and index < index_next and index % decimation_factor == 0)])

        throughput_to_plot.extend(
            [val for index, val in enumerate(throughput) if (index >= start_index + 20 and index < index_next and index % decimation_factor == 0)])

    ax.plot([entry - start_times_centr[agc_sel][mcs_sel][0] for entry in time_support_to_plot],
            throughput_to_plot, color=color_2)


tikzplotlib.save('throughput-time-bpsk-1-5.tex')
plt.show()
