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


# Analyze throughput and plot switching times


import numpy as np
import tikzplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import math
import pickle

start_times = {}
start_times["with-agc"] = {}
start_times["without-agc"] = {}

start_times["with-agc"]["bpsk-1-5"] = [3686498500.031300, 3686498530.031800, 3686498560.014500, 3686498590.022600, 3686498620.014700,
                                       3686498650.024200, 3686498680.024300, 3686498710.027000, 3686498740.027200, 3686498770.028000, 3686498800.028100, 3686498830.029600]
start_times["with-agc"]["qpsk-1-4"] = [3686499054.031800, 3686499084.025000, 3686499114.023600, 3686499144.036300, 3686499174.026000,
                                       3686499204.025200, 3686499234.027500, 3686499264.028200, 3686499294.029500, 3686499324.028100, 3686499354.029700, 3686499384.030400]
start_times["with-agc"]["qpsk-1-2"] = [3686499601.034100, 3686499631.025700, 3686499661.027100, 3686499691.026900, 3686499721.028100,
                                       3686499751.027200, 3686499781.027900, 3686499811.029100, 3686499841.028500, 3686499871.031600, 3686499901.030000, 3686499931.033300]
start_times["with-agc"]["qpsk-3-4"] = [3686500145.035700, 3686500175.038800, 3686500205.026500, 3686500235.028600, 3686500265.030200,
                                       3686500295.028200, 3686500325.029300, 3686500355.029500, 3686500385.031800, 3686500415.032300, 3686500445.032200, 3686500475.032800]
start_times["with-agc"]["16qam-1-2"] = [3686500666.030500, 3686500696.031600, 3686500726.032700, 3686500756.033400, 3686500786.031500,
                                        3686500816.034200, 3686500846.035600, 3686500876.024800, 3686500906.027200, 3686500936.027700, 3686500966.029700, 3686500996.028200]
start_times["with-agc"]["16qam-3-4"] = [3686501289.037000, 3686501319.030500, 3686501349.030600, 3686501379.030600, 3686501409.031700,
                                        3686501439.032700, 3686501469.033000, 3686501499.033700, 3686501529.035200, 3686501559.035900, 3686501589.028900, 3686501619.039700]

start_times["without-agc"]["bpsk-1-5"] = [3686494015.035700, 3686494045.032000, 3686494075.026400, 3686494105.031400, 3686494135.035300,
                                          3686494165.030100, 3686494195.033900, 3686494225.028200, 3686494255.033900, 3686494285.028400, 3686494315.031600, 3686494345.030300]
start_times["without-agc"]["qpsk-1-4"] = [3686494756.036500, 3686494786.034800, 3686494816.034000, 3686494846.029300, 3686494876.031500,
                                          3686494906.028700, 3686494936.027000, 3686494966.036700, 3686494996.034200, 3686495026.034100, 3686495056.029300, 3686495086.026600]
start_times["without-agc"]["qpsk-1-2"] = [3686495411.030000, 3686495441.028700, 3686495471.037000, 3686495501.023200, 3686495531.032500,
                                          3686495561.032700, 3686495591.039500, 3686495621.028200, 3686495651.036500, 3686495681.033700, 3686495711.032900, 3686495741.031700]
start_times["without-agc"]["qpsk-3-4"] = [3686496008.035900, 3686496038.033600, 3686496068.032400, 3686496098.029600, 3686496128.027300,
                                          3686496158.026600, 3686496188.034900, 3686496218.034800, 3686496248.030500, 3686496278.030300, 3686496308.027600, 3686496338.025800]
start_times["without-agc"]["16qam-1-2"] = [3686496665.035100, 3686496695.034000, 3686496725.023400, 3686496755.035700, 3686496785.036100,
                                           3686496815.027100, 3686496845.023500, 3686496875.024800, 3686496905.024200, 3686496935.034200, 3686496965.024100, 3686496995.032100]
start_times["without-agc"]["16qam-3-4"] = [3686497239.034800, 3686497269.033300, 3686497299.034200, 3686497329.033700, 3686497359.021500,
                                           3686497389.031900, 3686497419.031800, 3686497449.033400, 3686497479.022800, 3686497509.030800, 3686497539.032600, 3686497569.034000]

end_times = {}
end_times["with-agc"] = {}
end_times["without-agc"] = {}

end_times["with-agc"]["bpsk-1-5"] = [3686498500.262300, 3686498530.263900, 3686498560.263500, 3686498590.262100, 3686498620.275700,
                                     3686498650.275800, 3686498680.264400, 3686498710.267100, 3686498740.267100, 3686498770.268000, 3686498800.267700, 3686498830.269700]
end_times["with-agc"]["qpsk-1-4"] = [3686499054.271900, 3686499084.274000, 3686499114.255200, 3686499144.264400, 3686499174.265500,
                                     3686499204.265300, 3686499234.267600, 3686499264.268500, 3686499294.267600, 3686499324.259700, 3686499354.261300, 3686499384.261000]
end_times["with-agc"]["qpsk-1-2"] = [3686499601.253700, 3686499631.254300, 3686499661.255300, 3686499691.257500, 3686499721.257700,
                                     3686499751.258800, 3686499781.258500, 3686499811.7281, 3686499841.269100, 3686499871.262200, 3686499901.261100, 3686499931.260400]
end_times["with-agc"]["qpsk-3-4"] = [3686500145.266800, 3686500175.266900, 3686500205.258100, 3686500235.259700, 3686500265.258300,
                                     3686500295.259400, 3686500325.260400, 3686500355.260600, 3686500385.260400, 3686500415.262900, 3686500445.313900, 3686500475.263900]
end_times["with-agc"]["16qam-1-2"] = [3686500666.279000, 3686500696.272200, 3686500726.272300, 3686500756.282000, 3686500786.262100,
                                      3686500816.273800, 3686500846.275700, 3686500876.276900, 3686500906.275800, 3686500936.267800, 3686500966.278400, 3686500996.319200]
end_times["with-agc"]["16qam-3-4"] = [3686501289.277600, 3686501319.270100, 3686501349.268700, 3686501379.270200, 3686501409.271800,
                                      3686501439.272200, 3686501469.273000, 3686501499.274200, 3686501529.275800, 3686501559.275000, 3686501589.286400, 3686501619.276800]

end_times["without-agc"]["bpsk-1-5"] = [3686494015.308200, 3686494045.301400, 3686494075.297400, 3686494105.292400, 3686494135.305100,
                                        3686494165.291600, 3686494195.283400, 3686494225.297200, 3686494255.283800, 3686494285.277400, 3686494315.283100, 3686494345.279400]
end_times["without-agc"]["qpsk-1-4"] = [3686494756.277100, 3686494786.274300, 3686494816.273600, 3686494846.272800, 3686494876.271600,
                                        3686494906.268800, 3686494936.268000, 3686494966.365100, 3686494996.264300, 3686495026.171300, 3686495056.269900, 3686495086.270100]
end_times["without-agc"]["qpsk-1-2"] = [3686495411.279600, 3686495441.269300, 3686495471.307000, 3686495501.262800, 3686495531.272000,
                                        3686495561.261300, 3686495591.258600, 3686495621.267300, 3686495651.315900, 3686495681.265300, 3686495711.261500, 3686495741.270800]
end_times["without-agc"]["qpsk-3-4"] = [3686496008.254400, 3686496038.243700, 3686496068.242500, 3686496098.238700, 3686496128.249500,
                                        3686496158.246200, 3686496188.245000, 3686496218.244400, 3686496248.240700, 3686496278.240400, 3686496308.240200, 3686496338.237900]
end_times["without-agc"]["16qam-1-2"] = [3686496665.253700, 3686496695.255600, 3686496725.293400, 3686496755.276300, 3686496785.243200,
                                         3686496815.244200, 3686496845.293500, 3686496875.243900, 3686496905.243800, 3686496935.252900, 3686496965.243800, 3686496995.243200]
end_times["without-agc"]["16qam-3-4"] = [3686497239.253500, 3686497269.251900, 3686497299.252800, 3686497329.252200, 3686497359.252100,
                                         3686497389.254000, 3686497419.253400, 3686497449.253500, 3686497479.251900, 3686497509.301300, 3686497539.291700, 3686497569.252600]

start_times_centr = {}
start_times_centr["without-agc"] = {}

start_times_centr["without-agc"]["bpsk-1-5"] = [3686679300.5883, 3686679330.6497, 3686679360.6915, 3686679390.7422, 3686679420.8116,
                                                3686679450.8648, 3686679480.9038, 3686679510.9563, 3686679541.0069, 3686679571.0486, 3686679601.0873, 3686679631.2005]
start_times_centr["without-agc"]["qpsk-1-4"] = [3686679838.0569, 3686679868.1188, 3686679898.1588, 3686679928.2089, 3686679958.2503,
                                                3686679988.3115, 3686680018.3523, 3686680048.4049, 3686680078.4446, 3686680108.5151, 3686680138.5453, 3686680168.5886]
start_times_centr["without-agc"]["qpsk-1-2"] = [3686680328.3719, 3686680358.4137, 3686680388.4765, 3686680418.5051, 3686680448.5368,
                                                3686680478.6093, 3686680508.6704, 3686680538.7102, 3686680568.7512, 3686680598.7829, 3686680628.8436, 3686680658.8758]
start_times_centr["without-agc"]["qpsk-3-4"] = [3686680810.7087, 3686680840.7616, 3686680870.8032, 3686680900.8531, 3686680930.8947,
                                                3686680960.9337, 3686680990.9962, 3686681021.0264, 3686681051.0683, 3686681081.1190, 3686681111.1603, 3686681141.2112]

end_times_centr = {}
end_times_centr["without-agc"] = {}

end_times_centr["without-agc"]["bpsk-1-5"] = [3686679300.6183, 3686679330.6906, 3686679360.7215, 3686679390.7722, 3686679420.8426,
                                              3686679450.8948, 3686679480.9457, 3686679510.9863, 3686679541.0369, 3686679571.0876, 3686679601.1172, 3686679631.2305]
end_times_centr["without-agc"]["qpsk-1-4"] = [3686679838.0959, 3686679868.1467, 3686679898.1888, 3686679928.2299, 3686679958.2803,
                                              3686679988.3415, 3686680018.3913, 3686680048.4229, 3686680078.4836, 3686680108.5450, 3686680138.5753, 3686680168.6186]
end_times_centr["without-agc"]["qpsk-1-2"] = [3686680328.4139, 3686680358.4347, 3686680388.5155, 3686680418.5261, 3686680448.5787,
                                              3686680478.6272, 3686680508.7004, 3686680538.7192, 3686680568.7901, 3686680598.8039, 3686680628.8736, 3686680658.8937]
end_times_centr["without-agc"]["qpsk-3-4"] = [3686680810.7387, 3686680840.7916, 3686680870.8422, 3686680900.8830, 3686680930.9336,
                                              3686680960.9546, 3686680991.0352, 3686681021.0474, 3686681051.0993, 3686681081.1400, 3686681111.1993, 3686681141.2322]


# centralize 10/28
start_times_centr_indoor = {}
start_times_centr_indoor["without-agc"] = {}

start_times_centr_indoor["without-agc"]["bpsk-1-5"] = [3686755957.7496, 3686755987.7897, 3686756017.8301, 3686756047.8726,
                                                       3686756077.9113, 3686756107.9523, 3686756137.9940, 3686756168.0347, 3686756198.0746, 3686756228.1154, 3686756258.1483, 3686756288.1889]
start_times_centr_indoor["without-agc"]["qpsk-1-4"] = [3686756442.4919, 3686756472.5446, 3686756502.5738, 3686756532.6154,
                                                       3686756622.7295, 3686756652.7588, 3686756682.8013, 3686756712.8400, 3686756742.8813, 3686756772.9239, 3686756442.4919, 3686756472.5446]
start_times_centr_indoor["without-agc"]["qpsk-1-2"] = [3686756995.1696, 3686757025.2193, 3686757055.2604, 3686757085.3028,
                                                       3686757115.3421, 3686757145.3850, 3686757175.4265, 3686757205.4673, 3686757235.5085, 3686757265.5392, 3686757295.5798, 3686757325.6204]
start_times_centr_indoor["without-agc"]["qpsk-3-4"] = [3686757509.5355, 3686757539.5665, 3686757569.6181, 3686757599.6592,
                                                       3686757629.6879, 3686757659.7294, 3686757689.7703, 3686757719.8111, 3686757749.8528, 3686757779.8924, 3686757809.9247, 3686757839.9648]

end_times_centr_indoor = {}
end_times_centr_indoor["without-agc"] = {}

end_times_centr_indoor["without-agc"]["bpsk-1-5"] = [3686755957.7886, 3686755987.8107, 3686756017.8601, 3686756047.8906,
                                                     3686756077.9413, 3686756107.9822, 3686756138.0840, 3686756168.0647, 3686756198.1046, 3686756228.1454, 3686756258.1783, 3686756288.2189]
end_times_centr_indoor["without-agc"]["qpsk-1-4"] = [3686756442.5219, 3686756472.5655, 3686756502.6038, 3686756532.6364,
                                                     3686756622.7576, 3686756652.8008, 3686756682.8313, 3686756712.8610, 3686756742.9113, 3686756772.9539, 3686756442.5339, 3686756472.5746]
end_times_centr_indoor["without-agc"]["qpsk-1-2"] = [3686756995.2206, 3686757025.2523, 3686757055.3024, 3686757085.3238,
                                                     3686757115.3840, 3686757145.4150, 3686757175.4655, 3686757205.4973, 3686757235.5385, 3686757265.5781, 3686757295.6198, 3686757325.6374]
end_times_centr_indoor["without-agc"]["qpsk-3-4"] = [3686757509.5745, 3686757539.5875, 3686757569.6481, 3686757599.6772,
                                                     3686757629.7299, 3686757659.7503, 3686757689.8122, 3686757719.8291, 3686757749.8918, 3686757779.9224, 3686757809.9637, 3686757839.9858]

# distributed 10/28
start_times_distr_indoor = {}
start_times_distr_indoor["without-agc"] = {}

end_times_distr_indoor = {}
end_times_distr_indoor["without-agc"] = {}

start_times_distr_indoor["without-agc"]["bpsk-1-5"] = [3686759127.0326, 3686759157.0242, 3686759187.0244, 3686759217.0251,
                                                       3686759247.0275, 3686759277.0274, 3686759307.0295, 3686759337.0314, 3686759367.0318, 3686759397.0311, 3686759427.0235, 3686759457.0237]
end_times_distr_indoor["without-agc"]["bpsk-1-5"] = [3686759128.2741, 3686759158.2658, 3686759188.2656, 3686759218.2558,
                                                     3686759248.2774, 3686759278.2573, 3686759308.2806, 3686759338.2816, 3686759368.2716, 3686759398.2733, 3686759428.2738, 3686759458.2628]
start_times_distr_indoor["without-agc"]["qpsk-1-4"] = [3686759623.0277, 3686759653.0307, 3686759683.0324, 3686759713.0326,
                                                       3686759743.0313, 3686759773.0216, 3686759803.0227, 3686759833.0255, 3686759863.0259, 3686759893.0266, 3686759923.0263, 3686759953.0289]
end_times_distr_indoor["without-agc"]["qpsk-1-4"] = [3686759624.2667, 3686759654.2791, 3686759684.2819, 3686759714.2605,
                                                     3686759744.2818, 3686759774.2546, 3686759804.2738, 3686759834.2552, 3686759864.2862, 3686759894.2561, 3686759924.2777, 3686759954.2685]
start_times_distr_indoor["without-agc"]["qpsk-1-2"] = [3686760170.0351, 3686760200.0249, 3686760230.0265, 3686760260.0269,
                                                       3686760290.0299, 3686760320.0304, 3686760350.0313, 3686760380.0320, 3686760410.0336, 3686760440.0327, 3686760470.0238, 3686760500.0255]
end_times_distr_indoor["without-agc"]["qpsk-1-2"] = [3686760171.2866, 3686760201.2759, 3686760231.2957, 3686760261.2693,
                                                     3686760291.3099, 3686760321.2807, 3686760351.2913, 3686760381.2714, 3686760411.2938, 3686760441.2844, 3686760471.2936, 3686760501.2638]
start_times_distr_indoor["without-agc"]["qpsk-3-4"] = [3686760664.0294, 3686760694.0314, 3686760724.0305, 3686760754.0330,
                                                       3686760784.0346, 3686760814.0242, 3686760844.0252, 3686760874.0256, 3686760904.0078, 3686760934.0290, 3686760964.0304, 3686760994.0314]
end_times_distr_indoor["without-agc"]["qpsk-3-4"] = [3686760665.3312, 3686760695.2817, 3686760725.3021, 3686760755.2841,
                                                     3686760785.2942, 3686760815.2846, 3686760845.3150, 3686760875.2870, 3686760905.3085, 3686760935.2888, 3686760965.2995, 3686760995.2885]


mcs_list = ["bpsk-1-5", "qpsk-1-4", "qpsk-1-2",
            "qpsk-3-4", "16qam-1-2", "16qam-3-4"]  # , "16qam-7-8"]
mcs_list_centr = ["bpsk-1-5", "qpsk-1-4", "qpsk-1-2", "qpsk-3-4"]
agc_list = ["without-agc"]
agc_list_centr = ["without-agc"]


switch_duration = {}
for agc_val in agc_list:
  start_t_all_mcs = start_times[agc_val]
  end_t_all_mcs = end_times[agc_val]

  switch_duration[agc_val] = {}

  for mcs_val in mcs_list:
    start_t = start_t_all_mcs[mcs_val]
    end_t = end_t_all_mcs[mcs_val]
    duration = []
    for index, val in enumerate(start_t):
      duration.append(end_t[index] - start_t[index])

    switch_duration[agc_val][mcs_val] = duration

switch_duration_centr = {}
for agc_val in agc_list_centr:
  start_t_all_mcs = start_times_centr[agc_val]
  end_t_all_mcs = end_times_centr[agc_val]

  switch_duration_centr[agc_val] = {}

  for mcs_val in mcs_list_centr:
    start_t = start_t_all_mcs[mcs_val]
    end_t = end_t_all_mcs[mcs_val]
    duration = []
    for index, val in enumerate(start_t):
      duration.append(end_t[index] - start_t[index])

    switch_duration_centr[agc_val][mcs_val] = duration

switch_duration_centr_indoor = {}
for agc_val in agc_list_centr:
  start_t_all_mcs = start_times_centr_indoor[agc_val]
  end_t_all_mcs = end_times_centr_indoor[agc_val]

  switch_duration_centr_indoor[agc_val] = {}

  for mcs_val in mcs_list_centr:
    start_t = start_t_all_mcs[mcs_val]
    end_t = end_t_all_mcs[mcs_val]
    duration = []
    for index, val in enumerate(start_t):
      duration.append(end_t[index] - start_t[index])

    switch_duration_centr_indoor[agc_val][mcs_val] = duration

switch_duration_distr_indoor = {}
for agc_val in agc_list_centr:
  start_t_all_mcs = start_times_distr_indoor[agc_val]
  end_t_all_mcs = end_times_distr_indoor[agc_val]

  switch_duration_distr_indoor[agc_val] = {}

  for mcs_val in mcs_list_centr:
    start_t = start_t_all_mcs[mcs_val]
    end_t = end_t_all_mcs[mcs_val]
    duration = []
    for index, val in enumerate(start_t):
      duration.append(end_t[index] - start_t[index])

    switch_duration_distr_indoor[agc_val][mcs_val] = duration


def plot_campaign(campaign_folder, switch_duration, agc_list, mcs_list, start_times, end_times):
  with open(campaign_folder + ".p", "rb") as pf:
    t = pickle.load(pf)

    time_dict = t[0]
    throughput_dict = t[1]

  duration_all = {}
  for agc_val in agc_list:
    duration_all[agc_val] = []
    for entry in switch_duration[agc_val].values():
      duration_all[agc_val].extend(entry)
    print(len(duration_all[agc_val]))

  fig, ax = plt.subplots()
  ax.grid(True)
  num_bins = 200
  for agc_val in agc_list:
    counts, bin_edges = np.histogram(duration_all[agc_val], bins=num_bins)
    cdf = np.cumsum(counts)
    ax.plot(bin_edges[1:], cdf)

  ax.set_xlabel('switch duration [s]')
  ax.set_ylabel('CDF')
  ax.legend(agc_list)

  plt.show(block=False)

  # average throughput from when switch starts (-30) to when it ends
  avg_throughput = []
  max_throughput = []
  zero_throughput_duration = {}
  labels = []

  tot_samples = 0
  print("start")
  for agc_val in agc_list:
    zero_throughput_duration[agc_val] = {}
    for mcs_val in mcs_list:
      labels.append(agc_val + "-" + mcs_val)
      zero_throughput_duration[agc_val][mcs_val] = []
      th = throughput_dict[agc_val][mcs_val]
      time_v = time_dict[agc_val][mcs_val]

      # find entry related to first switch
      first_switch_time = start_times[agc_val][mcs_val][0]
      last_switch_time = end_times[agc_val][mcs_val][-1]

      past_30_s = first_switch_time - 30
      # find the closest element in time
      index_start = np.argmin(
          np.abs([val - past_30_s for val in time_v]))
      index_end = np.argmin(
          np.abs([val - last_switch_time for val in time_v]))

      print("len of th samples")
      print(len(th[index_start:index_end]))
      tot_samples += len(th[index_start:index_end])
      avg_throughput.append(np.mean(th[index_start:index_end]))
      max_throughput.append(np.max(th[index_start:index_end]))

      index = 0
      while index < len(th):
        th_val = th[index]
        start_time = time_v[index]
        end_time = time_v[index]
        # print("%f %f %f" % (index, th_val, end_time))
        while th_val < 1 and (index + 1) < len(th):  # zero throughput
          index = index + 1
          end_time = time_v[index]
          th_val = th[index]
        index = index + 1
        if (end_time - start_time) > 0:
          zero_throughput_duration[agc_val][mcs_val].append(
              end_time - start_time)

  print("end")
  print(tot_samples)
  duration_zeros_all = {}
  for agc_val in agc_list:
    duration_zeros_all[agc_val] = []
    for entry in zero_throughput_duration[agc_val].values():
      duration_zeros_all[agc_val].extend(entry)
    print(len(duration_zeros_all[agc_val]))

  fig, ax = plt.subplots()
  ax.grid(True)
  num_bins = 200
  for agc_val in agc_list:
    counts, bin_edges = np.histogram(
        duration_zeros_all[agc_val], bins=num_bins)
    cdf = np.cumsum(counts)
    ax.plot(bin_edges[1:], cdf)

  ax.set_xlabel('zero throughput duration [s]')
  ax.set_ylabel('CDF')
  ax.legend(agc_list)
  ax.set_xlim([0, 0.3])

  plt.show(block=False)

  fig, ax = plt.subplots()
  ax.grid(True)
  ax.bar(labels, max_throughput)
  ax.bar(labels, avg_throughput)
  ax.set_xlabel('Config')
  ax.tick_params(axis='x', rotation=70)
  ax.set_ylabel('Throughput [Mbps]')
  ax.legend(['Max', 'Average'])
  plt.show(block=False)

  tikzplotlib.save('throughput-average-max' + campaign_folder + '.tex')

  return duration_all


def main():
  duration_all = plot_campaign("distributed", switch_duration,
                               agc_list, mcs_list, start_times, end_times)
  duration_all_centr = plot_campaign("centralized", switch_duration_centr,
                                     agc_list_centr, mcs_list_centr, start_times_centr, end_times_centr)

  # duration_indoor_centr = plot_campaign("experiments-10-28-2020-centralized", switch_duration_centr_indoor,
  #               agc_list_centr, mcs_list_centr, start_times_centr_indoor, end_times_centr_indoor)
  # duration_indoor_distr = plot_campaign("experiments-10-28-2020-distributed", switch_duration_distr_indoor,
  #               agc_list_centr, mcs_list_centr, start_times_distr_indoor, end_times_distr_indoor)

  fig, ax = plt.subplots()
  ax.grid(True)
  num_bins = 200

  print("distr")
  print(len(duration_all["without-agc"]))
  print("centr")
  print(len(duration_all_centr["without-agc"]))

  counts, bin_edges = np.histogram(duration_all["without-agc"], bins=num_bins)
  cdf = np.cumsum(counts)
  ax.plot(bin_edges[1:], cdf / np.max(cdf))

  counts, bin_edges = np.histogram(
      duration_all_centr["without-agc"], bins=num_bins)
  cdf = np.cumsum(counts)
  ax.plot(bin_edges[1:], cdf / np.max(cdf))

  ax.set_xlabel('switch duration [s]')
  ax.set_ylabel('CDF')
  ax.legend(["Distr", "Centr"])
  tikzplotlib.save('switching_distribution.tex')
  plt.show()


if __name__ == '__main__':
  main()
