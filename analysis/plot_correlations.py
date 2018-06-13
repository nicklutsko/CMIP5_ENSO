""""
Nicholas Lutsko -- EAPS department, MIT

Script to plot correlations between frequency-dependent regression co-efficients and sensitivity estimates

Last updated -- June 13th 2018
"""

import numpy as np
import matplotlib.pylab as plt

Mods = ["GFDL-CM3_", "GFDL-ESM2G_", "GFDL-ESM2M_", "CCSM4_", "IPSL-CM5A-LR_", "HadGEM2-ES_", "GISS-E2-R_", "MPI-ESM-LR_", "MIROC5_", "CSIRO-Mk3-6-0_", "inmcm4_", "FGOALS-s2_", "bcc-csm1-1_", "CNRM-CM5_", "BNU-ESM_", "MRI-CGCM3_", "NorESM1-M_", "CanESM2_"]
m = len( Mods )

coeffs = np.zeros( (5, m ) ) 

#The Forster et al estimates
coeffs1[0] = [0.7, 1.29, 1.38, 1.23, 0.75, 0.64, 1.79, 1.13, 1.52, 0.63, 1.43, 0.92, 1.14, 1.14, 0., 1.25, 1.11, 1.04] #\beta_F
coeffs1[2] = [3.97, 2.39, 2.44, 2.89, 4.13, 4.59, 2.11, 3.63, 2.72, 4.08, 2.08, 4.17, 2.82, 3.25, 0., 2.6, 2.8, 3.69] #ECS
coeffs1[4] =  [ -0.48, 0.26, 0.33, 0.16, -0.7, -0.37, 0.48, 0.04, 0.51, -0.23, 0.12, 0.48, 0.07, 0.2, 0., 0.09, 0.11, -0.13 ] #\beta_F, C
#The Geoffroy et al estimates
coeffs[1] = [ 0., 0., 1.38, 1.4, 0.79, 0.61, 2.03, 1.21, 1.58, 0.68, 1.56, 0.87, 1.28,  1.12, 0.92, 1.31, 1.15, 1.06 ] #\beta_F
coeffs[3] = [ 0., 0., 2.5, 3., 4.25, 5.5, 2.25, 3.9, 2.8, 5.1, 1.9, 4.5, 2.9, 3.2, 3.9, 2.7, 3.25, 3.9] #ECS

bins = np.arange( -95 , 100., 5. )
b = len( bins )

titles = ["$C(\omega)'$", "$L(\omega)'$", "$S(\omega)'$"]

vals = np.zeros( m )

pdf_data = np.load( "../Bony_decomp/data/AM_pdf_wap.dat" ) * 100. / 60. / 60. / 24.

w_med = np.zeros( ( m, b ) )
for z in range( m ):
	w_med[z] = np.mean( pdf_data[z], axis = 0)

def make_axis( a ):

	a.spines['top'].set_color('none')
   	a.spines['right'].set_color('none')
   	a.tick_params(axis = 'x', which = 'both', bottom="off", top = "off", labelbottom = "on")
   	a.tick_params(axis="y", which="both", bottom="off", top="off", labelbottom="off", left="off", right="off", labelleft="on") 

	ticks = np.arange( -100., 120, 20 )
	plt.xticks( ticks, fontsize = 12)
	plt.xlabel("$\omega$ [hPa day$^{-1}$]", fontsize = 12)
	plt.xlim([-100., 100. ])

	return 0

fig = plt.figure( figsize = (10, 12) )
plt.subplots_adjust(left = 0.08, right = 0.98, bottom = 0.06, top = 0.95, hspace = 0.3, wspace = 0.3)

#frequencies to average over:
f1 = 165 
f2 = 190

#bins to average over
b1 = 22
b2 = 25

for z in range( 3 ):

	freqs = np.load( "../frequency_regr/data/freqs.dat" )
	f = len( freqs )

	a = np.load( "../frequency_regr/data/" + opt + "_as.dat" )[z]
	av_a = np.mean( a[:, :, f1:f2], axis = 2 ) * w_med[:, :]


	corc = np.zeros( (5, b ) )
	for k in range( 5 ):
		for j in range( b ):
			if k == 0 or k == 2 or k == 4:
				nm = m - 1
				ncs = np.zeros( nm )
				nvals = np.zeros( nm )
				c = 0
				for y in range( m ):
					if coeffs[k, y] != 0.:
						ncs[c] = coeffs[k, y]
						nvals[c] = av_a[y, j]	
						c += 1

				corr = lin_regression( nvals[:], ncs )[2] ** 2
				corc[k, j] = corr

			elif k == 1 or k == 3:
				nm = m - 2
				ncs = np.zeros( nm )
				nvals = np.zeros( nm )
				c = 0
				for y in range( m ):
					if coeffs[k, y] != 0.:
						ncs[c] = coeffs[k, y]
						nvals[c] = av_a[y, j]	
						c += 1

				corr = lin_regression( nvals[:], ncs )[2] ** 2
				corc[k, j] = corr

	if z == 0:
		vals = np.mean( av_a[:, b1:b2], axis = 1 )

	labs = ['ko-', 'kv--', 'ks-.', 'kD:', 'k*-' ]

	ax1 = plt.subplot( 3, 1, z + 1 )
	plt.title( titles[z] )

	for i in range( 4 ):
		plt.plot( bins, corc[i, :39], labs[i], linewidth = 2. )

	if z == 1:
		plt.legend(["$\\beta_{F, 1}$", "$\\beta_{F, 2}$", "ECS 1", "ECS 2"], frameon = False, loc = "upper left", ncol = 2 )

	make_axis( ax1 )
	plt.ylabel("$r^2$")

	plt.ylim([0., 0.7])

plt.savefig( "AM_binned_data_corrs_2_5_3.png" )
plt.savefig( "AM_binned_data_corrs_2_5_3.pdf" )
plt.show()
