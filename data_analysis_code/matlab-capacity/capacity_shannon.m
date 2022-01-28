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

function [capacity] = capacity_shannon(bandwidth_max_support,k,T0,NF_mixer,P_rx)

noise_power = 10 * log10(k * bandwidth_max_support * 10^9 * T0) + NF_mixer;
snr = P_rx - noise_power;
capacity = bandwidth_max_support .* (10.^9) .* log2(1 + 10.^(snr/10)) / (10.^9);

end

