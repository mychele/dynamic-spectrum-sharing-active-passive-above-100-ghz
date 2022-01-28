# Data and repo for the paper Dynamic Spectrum Sharing Between Active and Passive Users Above 100 GHz

The code in this repository has been used to generate, elaborate, and plot the data for the paper 

> M. Polese, V. Ariyarathna, P. Sen, J. Siles, F. Restuccia, T. Melodia and J. M. Jornet, "Dynamic Spectrum Sharing Between Active and Passive Users Above 100 GHz", submitted, 2021.

Please reference the paper if you use the code or data from the dataset. The data can be found at [this link](http://hdl.handle.net/2047/D20427338).

<!-- Please reference the paper if you use the code or data from the dataset: [bibtex entry](https://ece.northeastern.edu/wineslab/wines_bibtex/polese2021mobihoc.txt)
 -->

# Data structure

The data is organized into two pickle files for the throughput analysis, and four MATLAB files for the noise analysis. See [this file](data_analysis_code/data-readme.md) for more information.

# Source code structure

The source code for the switching framework can be found in the [switching-framework](switching-framework) folder. We provide Python scripts to query the [n2yo](https://n2yo.com) APIs, track the AURA satellite, and trigger switch commands to the SPDT switch of the dual-band backhaul prototype. The source code to elaborate the data and generate the paper figures is in the [data_analysis_code](data_analysis_code) folder.



