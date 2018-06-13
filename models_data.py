#######################################################
# File containing model names and sensitivity estimates


Mods = ["GFDL-CM3", "GFDL-ESM2G", "GFDL-ESM2M", "CCSM4", "IPSL-CM5A-LR", "HadGEM2-ES", "GISS-E2-R", "MPI-ESM-LR", "MIROC5", "CSIRO-Mk3-6-0", "inmcm4", "FGOALS-s2", "bcc-csm1-1", "CNRM-CM5", "BNU-ESM", "MRI-CGCM3", "NorESM1-M", "CanESM2"]
m = len( Mods )

coeffs1 = np.zeros( (3, m - 1) ) #The Forster et al estimates
coeffs2 = np.zeros( (2, m - 2) ) #The Geoffroy et al estimates

coeffs1[0] = [0.7, 1.29, 1.38, 1.23, 0.75, 0.64, 1.79, 1.13, 1.52, 0.63, 1.43, 0.92, 1.14, 1.14, 1.25, 1.11, 1.04] #\beta_F
coeffs1[1] = [3.97, 2.39, 2.44, 2.89, 4.13, 4.59, 2.11, 3.63, 2.72, 4.08, 2.08, 4.17, 2.82, 3.25, 2.6, 2.8, 3.69] #ECS
coeffs1[2] =  [ -0.48, 0.26, 0.33, 0.16, -0.7, -0.37, 0.48, 0.04, 0.51, -0.23, 0.12, 0.48, 0.07, 0.2,  0.09, 0.11, -0.13 ] #\beta_F, C
coeffs2[0] = [ 1.38, 1.4, 0.79, 0.61, 2.03, 1.21, 1.58, 0.68, 1.56, 0.87, 1.28,  1.12, 0.92, 1.31, 1.15, 1.06 ] #\beta_F
coeffs2[1] = [ 2.5, 3., 4.25, 5.5, 2.25, 3.9, 2.8, 5.1, 1.9, 4.5, 2.9, 3.2, 3.9, 2.7, 3.25, 3.9] #ECS


