""""
Nicholas Lutsko -- EAPS department, MIT

Scrip for performing frequency-dependent regressions of binned data.

Last updated -- June 13th 2018
"""

import numpy as np
import multi_taper_analysis


###############################
# Load data


trop_mean = np.load( "../Bony_decomp/data/AM_trop_temp.dat" )

binned_dat = np.load( "../Bony_decomp/data/AM_binned_data_5hpa.dat" )
m, o, t, b = np.shape( binned_data )

pdf_wap = np.load( "../Bony_decomp/data/AM_pdf_wap_5hpa.dat" )


###############################
# Main analysis loops

#Thermodynamic regressions
c = np.zeros( ( ( ( 3, m, b, t / 2 ) ) ) ) #Focus on cloud fluxes
ph = np.zeros( ( ( ( 3, m, b, t / 2 ) ) ) ) 
a = np.zeros( ( ( ( 3, m, b, t / 2 ) ) ) )

for i in range( 3 ):
	for j in range( m ):
		for k in range( b ):
			freqs, c[i, j, k], ph[i, j, k], a[i, j, k], ci, phi = mta.multi_taper_coh( trop_mean[j], binned_data[i, 6 + i, k] )

#Dynamic regressions
cd = np.zeros( ( ( m, b, t / 2 ) ) ) 
phd = np.zeros( ( ( m, b, t / 2 ) ) ) 
ad = np.zeros( ( ( m, b, t / 2 ) ) )

for i in range( m ):
	for j in range( b ):
		freqs, c[i, j], ph[i, j], a[i, j], ci, phi = mta.multi_taper_coh( trop_mean[i], pdf_wap[i, :, j] )


###############################
# Save data

def sdat(c, F):
	#For saving data
        data = open(F, "w")
        print "Saving in:", F
        np.save(data, c)
        data.close()
        return 0


sdat( c, "data/thermodynamic_cohs.dat" )
sdat( ph, "data/thermodynamic_phs.dat" )
sdat( a, "data/thermodynamic_as.dat" )

sdat( cd, "data/dynamic_cohs.dat" )
sdat( phd, "data/dynamic_phs.dat" )
sdat( ad, "data/dynamic_as.dat" )



