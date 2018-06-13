""""
Nicholas Lutsko -- EAPS department, MIT

Script for binning CMIP5 cloud fraction data by \omega_500 velocities. Assumes the netcdf files are labeled according to their model names.

Last updated -- June 13th 2018
"""

import numpy as np
import scipy.io as si #Easier than xarray because of weird dates
import scipy.signal as ss
import w500_bin 

Mods = ["GFDL-CM3", "GFDL-ESM2G", "GFDL-ESM2M", "CCSM4", "IPSL-CM5A-LR", "HadGEM2-ES", "GISS-E2-R", "MPI-ESM-LR", "MIROC5", "CSIRO-Mk3-6-0", "inmcm4", "FGOALS-s2", "bcc-csm1-1", "CNRM-CM5", "BNU-ESM", "MRI-CGCM3", "NorESM1-M", "CanESM2"]
m = len( Mods )

bins = np.arange( -100 , 105., 5. )
b = len( b )

opts = [ "wap", "cf"]
o = len( opts )

t = 500

###############################
# Some useful functions

def get_lats_lons( f ):
	#Only keep data between -30 and 30
	j = len( f1.variables[opts[0]][0, 0, 0] )
	l = len( f1.variables[opts[0]][0, 0] )

	lats = np.zeros( l )
	lats[:] = f1.variables['lat'][:]

	l1 = 0
	for m in range( l ):
		if lats[m] >= -30. and l1 == 0:
			l1 = m
		elif lats[m] >= 30.:
			l2 = m
			break
	
	return l1, l2, j

def sdat(c, F):
	#For saving data
        data = open(F, "w")
        print "Saving in:", F
        np.save(data, c)
        data.close()
        return 0

def seasonal_cycle_3( data ):
	#Calculate seasonal cycle
	d1, d2, d3 = np.shape( data )
	sc = np.zeros( ( (12, d2, d3) ) )

	for i in range( 12 ):
		for j in range( d1 ):
			if j % 12 == i:
				sc[i, :, :] += data[j, :, :] / float( d1 ) * 12.
	return sc 

def remove_sc_3(data):
	#Remove seasonal cycle from data
	d1, d2, d3 = np.shape( data )
	n_dat = np.zeros( ( ( d1, d2, d3 ) ) )

	sc = new_seasonal_cycle_3( data )

	for i in range( 12 ):
		for j in range( d1 ):
			if j % 12 == i:
				n_dat[j, :, :] = data[j, :, :] - sc[i, :, :]
	return n_dat


###############################
# Main analysis loop

binned_dat = np.zeros( ( ( ( m, 9, 500, b) ) ) ) #The final binned data
pdf_wap = np.zeros( ( ( m, 500, b ) ) ) #The yearly distributions of \omega_500

for z in range( m ):

	for i in range( o ): #Cycle through the variables needed for the analysis
		fname = Mods[i] + "_PI_control_0_500_" + opts[i] + ".nc"
		print "Doing:", fname
		f1 = si.netcdf_file(fname, 'r')

		if i == 0:
			#Get latitude bounds
			l1, l2, j = get_lats_lons( f1 )
			data = np.zeros( ( ( ( 9, t * 12, l2 - l1, j ) ) ) )
			data[i] = f1.variables[ opts[i] ][:, lev, l1:l2, :]

		else:
			data[i] = f1.variables[ opts[i] ][:, l1:l2, :]

		f1.close()
	print "Detrend everything but omega_500"
	data[1:] = ss.detrend( data[1:] - np.mean(data[1:], axis = 1)[:, np.newaxis, :, :], axis = 1 )

	print "Deseasonalize"
	for i in range( 1, 2 ):
		data[i, :, :, :] = remove_sc_3(data[i, :, :, :] )

	print "Bin data"
	binned_dat[z], pdf_wap[z] = w500_bin.annual_binned_data( data, bins, 1 )

	

###############################
# Save data

sdat( binned_dat, "data/monthly_binned_CF_data_5hPa.dat" )

















