""""
Nicholas Lutsko -- EAPS department, MIT

Script to calculate ENSO indices for data from the CMIP5 archive. Assumes the netcdf files are labeled according to their model names. 

Last updated -- June 13th 2018
"""
import numpy as np
import xarray as xr
import scipy.signal as ss


Mods = ["GFDL-CM3", "GFDL-ESM2G", "GFDL-ESM2M", "CCSM4", "IPSL-CM5A-LR", "HadGEM2-ES", "GISS-E2-R", "MPI-ESM-LR", "MIROC5", "CSIRO-Mk3-6-0", "inmcm4", "FGOALS-s2", "bcc-csm1-1", "CNRM-CM5", "BNU-ESM", "MRI-CGCM3", "NorESM1-M", "CanESM2"]
m = len( Mods )

opt ="tos"

t = 500

def seasonal_cycle( data ):
	d1 = len(data)
	sc = np.zeros( 12 )

	for i in range( 12 ):
		for j in range( d1 ):
			if j % 12 == i:
				sc[i] += data[j] / float( d1 ) * 12.
	return sc 

def remove_sc( data ):
	d1 = len(data)
	n_dat = np.zeros( d1 ) 

	sc = seasonal_cycle( data )

	for i in range( 12 ):
		for j in range( d1 ):
			if j % 12 == i:
				n_dat[j] = data[j] - sc[i]
	return n_dat



###############################
# Main analysis loop

sst = np.zeros( ( m, 500 * 12 ) )

slats = [ -5., 5.]
slons_1 = [-170., -120.] #Depends on how models do longitude
slons_2 = [ 190., 240.]

for z in range( m ):

	fname = Mods[i] + "_PI_control_0_500_" + opt + ".nc"
	print "Doing:", fname
	ds = xr.open_dataset( fname1 )

	if np.min( ds.lon[:] ) < -170.:
		nta = ds.tos.sel( lon = slice( slons_1[0], slons_1[1] ), lat = slice( slats[0], slats[1]) )
	elif np.min( ds.lon[:] ) > 0. and (z == 6 or z == 17):
		nta = ds.tos.sel( lon = slice( slons_2[0], slons_2[1] ), lat = slice( slats[0], slats[1]) )

	sst[z] = np.mean( np.mean( nta, axis = 1), axis = 1 )

	sst[z] = remove_sc( sst] )
	sst[z] = ss.detrend( sst[z] - np.mean( sst[z] ) )
	sst[z] /= np.std( sst[z] )


###############################
# Save data

sdat( sst, "data/NINO3.4_index.dat" )
