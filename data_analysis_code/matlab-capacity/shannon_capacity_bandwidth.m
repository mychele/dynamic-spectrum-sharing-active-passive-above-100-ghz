% Copyright 2021, Michele Polese <michele.polese@gmail.com>
%
% This program is free software; you can redistribute it and/or modify
% it under the terms of the GNU General Public License version 3 as
% published by the Free Software Foundation;
%
% This program is distributed in the hope that it will be useful,
% but WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
% GNU General Public License for more details.
%
% You should have received a copy of the GNU General Public License
% along with this program; if not, write to the Free Software
% Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

% test Shannon capacity with and without sharing


k = 1.380658e-23; %[J/K] - boltzmann constant
T0 = 296; %[K] - reference temperature
NF_mixer = 8.5; % [dB]
P_rx = -23; %  dBm;

bandwidth_max_support = 0.8:0.8:32; % GHz
capacity = capacity_shannon(bandwidth_max_support,k,T0,NF_mixer,P_rx);

bw_no_sharing_single = 3.5; % GHz, 231.5-235
capacity_no_sharing_single_max = capacity_shannon(bw_no_sharing_single,k,T0,NF_mixer,P_rx);
capacity_no_sharing_single_max_vec = min(capacity, capacity_no_sharing_single_max);

bw_no_sharing_combined = 6.5; % GHz, 231.5-235 + 238-241
capacity_no_sharing_combined_max = capacity_shannon(bw_no_sharing_combined,k,T0,NF_mixer,P_rx);
capacity_no_sharing_combined_max_vec = min(capacity, capacity_no_sharing_combined_max);

bw_sharing_not_prohibited_single = 17; % GHz, 209-226
capacity_sharing_single_max = capacity_shannon(bw_sharing_not_prohibited_single,k,T0,NF_mixer,P_rx);
capacity_sharing_single_max_vec = min(capacity, capacity_sharing_single_max);

bw_sharing_not_prohibited_combined = 26.5; % GHz, 209-226 + 231.5-241
capacity_sharing_combined_max = capacity_shannon(bw_sharing_not_prohibited_combined,k,T0,NF_mixer,P_rx);
capacity_sharing_combined_max_vec = min(capacity, capacity_sharing_combined_max);

bw_sharing_prohib = 32; % GHz, 209-241

figure, hold on
grid on
plot(bandwidth_max_support, capacity)
plot(bandwidth_max_support, capacity_no_sharing_single_max_vec)
plot(bandwidth_max_support, capacity_no_sharing_combined_max_vec)
plot(bandwidth_max_support, capacity_sharing_single_max_vec)
plot(bandwidth_max_support, capacity_sharing_combined_max_vec)
xlabel('Bandwidth [GHz]')
ylabel('Shannon capacity [Gbps]')
