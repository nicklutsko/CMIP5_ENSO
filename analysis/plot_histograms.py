""""
Nicholas Lutsko -- EAPS department, MIT

Script to plot histograms of P_\omega, as well as regress them P_\omega onto ENSO indices for the models.

Last updated -- June 13th 2018
"""

import numpy as np
import matplotlib.pylab as plt

Mods = ["GFDL-CM3", "GFDL-ESM2G", "GFDL-ESM2M", "CCSM4", "IPSL-CM5A-LR", "HadGEM2-ES", "GISS-E2-R", "MPI-ESM-LR", "MIROC5", "CSIRO-Mk3-6-0", "inmcm4", "FGOALS-s2", "bcc-csm1-1", "CNRM-CM5", "BNU-ESM", "MRI-CGCM3", "NorESM1-M", "CanESM2"]
m = len( Mods )
bins = np.arange( -97.5 , 102.5, 5. )
b = len( bins )

t = 500

data = np.load( "../Bony_decomp/data/monthly_pdf_wap.dat" ) * 100. / 60. / 60. / 24.

def yrmn(w):
	#Take yearly mean of P_\omega data
	l = len(w[0]) / 12
	d1, d2 = np.shape(w[:, 0])
	fm = np.zeros( ( ( d1, l, d2 ) ) )
	for i in range(l):
		#print "Doing:", i
		fm[ :, i, :] = np.mean(w[:, i * 12:(i * 12)+12, :], axis = 1)
	return fm

data = yrmn( data )


w_med = np.zeros( ( m, b ) )
for z in range( m ):
	w_med[z] = np.mean( data[z], axis = 0)


std_wap = np.std( w_med, axis = 0 ) 

fig = plt.figure( figsize = (12, 6) )
plt.subplots_adjust(left = 0.1, right = 0.98, bottom = 0.1, top = 0.95, hspace = 0.3, wspace = 0.3)

ax = plt.subplot(1, 2, 1)

plt.plot( bins, np.median( w_med, axis = 0 ), 'ko' )
plt.errorbar( bins, np.median( w_med, axis = 0 ), color = 'k', linewidth = 1., yerr = std_wap, ecolor = 'k', elinewidth = 1.)

ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
ax.tick_params(axis = 'x', which = 'both', bottom="off", top = "off", labelbottom = "on")
ax.tick_params(axis="y", which="both", bottom="off", top="off", labelbottom="off", left="off", right="off", labelleft="on") 

ticks = np.arange( -100., 120, 20 )
plt.xticks( ticks, fontsize = 12)
plt.xlabel("$\omega$ [hPa day$^{-1}$]", fontsize = 12)
plt.xlim([-100., 100. ])
plt.ylim([0., 0.02])

plt.ylabel( "Normalized Density", fontsize = 12 )


ENSO = np.load( "Bony_decomp/data/NINO3.4_index.dat" )

def yrmn_2(w):
	#Take yearly mean of ENSO indices
	l = len(w[0]) / 12
	d1 = len(w[:, 0])
	fm = np.zeros( (d1, l ) )
	for i in range(l):
		#print "Doing:", i
		fm[ :, i] = np.mean(w[:, i * 12:(i * 12)+12], axis = 1)
	return fm

import scipy.signal as ss

nENSO = yrmn_2( ENSO )
for i in range( 18 ):
	nENSO[i] = ss.detrend( nENSO[i] - np.mean( nENSO[i] ) )
	nENSO[i] /= np.std( nENSO[i])

regr = np.zeros( ( m, b ) )

for i in range( m ):
	regress = data[i, :, :] * nENSO[i, :, np.newaxis]
	regress = ss.detrend( regress )
	regr[i] = np.sum( regress, axis = 0 ) / float( t )

ax = plt.subplot(1, 2, 2)

for i in range( 18 ):
	plt.plot( bins, regr[i], 'k-', alpha = 0.4 )
plt.plot( bins, np.median( regr, axis = 0 ), 'ko-' )

ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
ax.tick_params(axis = 'x', which = 'both', bottom="off", top = "off", labelbottom = "on")
ax.tick_params(axis="y", which="both", bottom="off", top="off", labelbottom="off", left="off", right="off", labelleft="on") 

ticks = np.arange( -100., 120, 20 )
plt.xticks( ticks, fontsize = 12)
plt.xlabel("$\omega$ [hPa day$^{-1}$]", fontsize = 12)
plt.xlim([-100., 100. ])
plt.ylim([-0.0005, 0.0005])

plt.title( "Regression of $P(\omega)'$ on Nino3.4 index", fontsize = 12 )

plt.savefig("CMIP5_omega_dists.png" )
plt.savefig("CMIP5_omega_dists.pdf" )
plt.show()

