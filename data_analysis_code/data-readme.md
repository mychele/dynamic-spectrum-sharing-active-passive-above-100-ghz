This code has been used to elaborate and plot the data collected for the paper 

> M. Polese, V. Ariyarathna, P. Sen, J. Siles, F. Restuccia, T. Melodia and J. M. Jornet, "Dynamic Spectrum Sharing Between Active and Passive Users Above 100 GHz", submitted, 2021.

Please reference the paper if you use the code or data from the dataset. The data can be found at [this link](http://hdl.handle.net/2047/D20427338).

The `distributed.p` and `centralized.p` pickle file contains the following entries (as a tuple):
- `time_th` and `val_th` are the time support and values for the measured throughput. They are dictionaries with keys `[agc_val][mcs_val]`.
- `time_crc` and `val_crc` are the time support and values for the measured CRC feedback. They are dictionaries with keys `[agc_val][mcs_val]`.
- `time_evm` and `val_evm` are the time support and values for the measured EVM. They are dictionaries with keys `[agc_val][mcs_val]`.
- `mcs_list` is the list of modulation and coding schemes with valid keys for the pickle file (a subset of `bpsk-1-5`, `qpsk-1-4`, `qpsk-1-2`, `qpsk-3-4`, `16qam-1-2`, `16qam-3-4`).
- `agc_list` is the list of automatic gain control configurations with valid keys for the pickle file (`without_agc` and `with_agc`).

Four MATLAB .fig files feature the data and figures for the amplitude and phase noise analysis:
- `120_network_amp_noise_800MHz.fig` contains noise samples for the noise amplitude analysis of LB;
- `240_network_amp_noise_800MHz.fig` contains noise samples for the noise amplitude analysis of UB;
- `120_ph_noise_network.fig` contains noise samples for the phase noise analysis of LB;
- `240_ph_noise_network.fig` contains noise samples for the phase noise analysis of UB;