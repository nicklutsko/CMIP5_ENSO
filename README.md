# CMIP5_ENSO

This readme contains a description of the files deposited in this directory. These files were used to perform the analysis in the study "The Relationship Between Cloud Radiative Effect and Surface Temperature Variability at ENSO Frequencies in CMIP5 Models" submitted to GRL by Nick Lutsko in 2018.

Please note that the code in this directory comes without any warranty, without even the implied warranty of merchantibility or fitness for a particular purpose.

The directory contains three folders:

-The folder Bony_decomp contains the scripts used to bin the data by the \omega_500 velocities. w500_bin.py includes the function to do the binning, and bin_data.py is a wrapper to load the data and loop over the models. bin_CF_data.py bins the cloud fraction data. tropical_mean_temps.py calculates tropical-mean temperatures and ENSO_index.py calculates the Nino3.4 index. \\
-The folder frequency_regr contains the scripts used to perform the frequency-dependent regressions. multi_taper_analysis.py includes the function to do the regressions, and frequency_regressions.py is a wrapper to load the data and loop over the models. \\
-The folder analysis contains the scripts to make the figures. plot_histogram.py makes Figure 1, plot_regressions.py can be used to plot the results of the frequency dependent regressions (i.e., to make Figures 2 and 3 and Supplementary Figures 1 and 3). plot_correlations.py plots the r^2 values for the regressions between the frequency-dependent regression co-efficients and the sensitivity estimates, as well as scatter plots of the co-efficients versus the sensitivity estimates (i.e., Figure 4 and Supplementary Figures 4, 5 and 6). Finally lag_correlations.py performs the lag-correlations to make Supplementary Figure 2.

The file "models_data.py" contains the model names and sensitivity estimates from Geoffroy et al (2013) and Forster et al (2013).

Because the CMIP5 data files are very large they are not included in this folder, and it is assumed that they have been processed to only include the first 500 years of each simulation.
