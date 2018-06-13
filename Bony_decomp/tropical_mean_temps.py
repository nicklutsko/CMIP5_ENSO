""""
Nicholas Lutsko -- EAPS department, MIT

Script to calculate the tropical-mean temperatures in data from the CMIP5 archive. Assumes the netcdf files are labeled according to their model names. 

Last updated -- June 13th 2018
"""
import numpy as np
import scipy.io as si #Easier than xarray because of weird dates

Mods = ["GFDL-CM3", "GFDL-ESM2G", "GFDL-ESM2M", "CCSM4", "IPSL-CM5A-LR", "HadGEM2-ES", "GISS-E2-R", "MPI-ESM-LR", "MIROC5", "CSIRO-Mk3-6-0", "inmcm4", "FGOALS-s2", "bcc-csm1-1", "CNRM-CM5", "BNU-ESM", "MRI-CGCM3", "NorESM1-M", "CanESM2"]
m = len( Mods )

opt ="tas"

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

def yrmn(w):
	#Take yearly mean

	l = len(w) / 12
	d1, d2 = np.shape(w[0])
	fm = np.zeros( ( ( l, d1, d2 ) ) )
	for i in range(l):
		print "Doing:", i
		fm[i, :, :] = np.mean(w[i * 12:(i * 12)+12, :, :], axis = 0)
	return fm


def tropical_mean( data, lats, lons ):

	cos_lat = np.cos( np.pi / 180. * lats[:] )
	sin_lat = np.sin( np.pi / 180. * lats[:] )
	fact = 1. / 2. / np.pi / ( max(sin_lat) - min(sin_lat) )

	inte = np.trapz( np.trapz(data * cos_lat[np.newaxis, np.newaxis, :, np.newaxis], lons * np.pi / 180. , axis = 3), lats * np.pi / 180., axis = 2)
	ndat = fact * inte

	return ndat

def sdat(c, F):
	#For saving data
        data = open(F, "w")
        print "Saving in:", F
        np.save(data, c)
        data.close()
        return 0


###############################
# Main analysis loop

trop_temp = np.zeros( ( m 500 ) ) 

for z in range( m ):

	fname = Mods[i] + "_PI_control_0_500_" + opt + ".nc"
	print "Doing:", fname
	f1 = si.netcdf_file(fname, 'r')

	#Get latitude bounds
	l1, l2, j = get_lats_lons( f1 )
	data = f1.variables[ opts[i] ][:, l1:l2, :]

	print "Detrend"
	data = ss.detrend( data - np.mean(data, axis = 0) )

	print "Take annual mean"
	data = yrmn( data )

	print "Take tropical mean"
	trop_temp[z] = tropical_mean( data, f1.variables['lat'][:], f1.variables['lon'][:] )

	f1.close()

###############################
# Save data

sdat( trop_temp, "data/AM_trop_temp.dat" )





















