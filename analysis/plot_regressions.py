""""
Nicholas Lutsko -- EAPS department, MIT

Script to plot results of frequency-dependent regressions.

Last updated -- June 13th 2018
"""

import numpy as np
import matplotlib.pylab as plt

Mods = ["GFDL-CM3_", "GFDL-ESM2G_", "GFDL-ESM2M_", "CCSM4_", "IPSL-CM5A-LR_", "HadGEM2-ES_", "GISS-E2-R_", "MPI-ESM-LR_", "MIROC5_", "CSIRO-Mk3-6-0_", "inmcm4_", "FGOALS-s2_", "bcc-csm1-1_", "CNRM-CM5_", "BNU-ESM_", "MRI-CGCM3_", "NorESM1-M_", "CanESM2_"]
m = len( Mods )

bins = np.arange( -95 , 100., 5. )
b = len( bins )

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

pdf_data = np.load( "../Bony_decomp/data/AM_pdf_wap.dat" ) * 100. / 60. / 60. / 24.

w_med = np.zeros( ( m, b ) )
for z in range( m ):
	w_med[z] = np.mean( pdf_data[z], axis = 0)


lf = 1. / 5.
hf = 1. / 2.5

opt = "thermodynamic" #"dynamic"

#Colors for plotting SW and LW
cs = [(31 / 255., 119 / 255., 180 / 255.), (44. / 255., 160 / 255., 44 / 255.), (214 / 255., 39 / 255., 40 / 255.), (255 / 255., 127 / 255., 14 / 255.) ]

fig = plt.figure( figsize = (10, 12) )
plt.subplots_adjust(left = 0.08, right = 0.98, bottom = 0.06, top = 0.95, hspace = 0.3, wspace = 0.3)

for z in range( 3 ):

	freqs = np.load( "../frequency_regr/data/freqs.dat" )

	cohs = np.load( "../frequency_regr/data/" + opt + "_cohs.dat" )[z]
	phs = np.load( "../frequency_regr/data/" + opt + "_phs.dat" )[z]
	a = np.load( "../frequency_regr/data/" + opt + "_as.dat" )[z]

	f = len( freqs )

	av_a = np.zeros( ( m, b ) )
	av_c = np.zeros( ( m, b ) )
	av_p = np.zeros( ( m, b ) )

	for i in range( m ):
		for j in range( f ):
			if freqs[j] > lf:
				f1 = j
				break
		for j in range( 250 ):
			if freqs[i, 10, j] > hf:
				f2 = j
				break
		av_a[i, :] = np.mean( a[i, :, f1:f2], axis = 1 ) * w_med[i, :]
		av_c[i, :] = np.mean( cohs[i, :, f1:f2], axis = 1 )
		av_p[i, :] = np.mean( -phs[i, :, f1:f2], axis = 1 ) #Sign convention


	ax1 = plt.subplot(3, 1, 1)
	if z == 0:
		for i in range( 18 ):
			plt.plot( bins,  av_c[i, :39], 'k', alpha = 0.2 )
		plt.plot( bins,  np.median( av_c[:, :39], axis = 0 ), 'ko-', linewidth = 2. )
	if z == 1:
		plt.plot( bins,  np.median( av_c[:, :39], axis = 0 ), 'v-', color = cs[0], linewidth = 2., markeredgecolor = cs[0] )
	if z == 2:
		plt.plot( bins,  np.median( av_c[:, :39], axis = 0 ), 'rs-', linewidth = 2., markeredgecolor = 'r' )

	plt.ylabel("Coherence$^2$", fontsize = 12)
	plt.ylim([0., 1.])
	plt.yticks([0., .2, .4, .6, .8, 1.], fontsize = 12 )

	make_axis( ax1 )

	ax1 = plt.subplot(3, 1, 2)
	if z == 0:
		for i in range( 18 ):
			plt.plot( bins,  av_p[i, :39], 'k', alpha = 0.2 )
		plt.plot( bins,  np.median( av_p[:, :39], axis = 0 ), 'ko-', linewidth = 2. )
	if z == 1:
		plt.plot( bins,  np.median( av_p[:, :39], axis = 0 ), 'v-', color = cs[0], linewidth = 2., markeredgecolor = cs[0] )
	if z == 2:
		plt.plot( bins,  np.median( av_p[:, :39], axis = 0 ), 'rs-', linewidth = 2., markeredgecolor = 'r' )

	make_axis( ax1 )
	plt.ylabel("Phase [$^\circ$]", fontsize = 12)
	plt.ylim([-180., 180.])
	plt.yticks([-180., -90., 0., 90., 180.], fontsize = 12)
	plt.axhline( y = 0., color = 'k', linestyle = '-', linewidth = 2. )
	ax1.spines['bottom'].set_color('none')
	ax1.spines['bottom'].set_position(('data',0))
	ticks = np.arange( -100., 120, 20 )
	plt.xticks( ticks, fontsize = 12)

	ax1 = plt.subplot(3, 1, 3)
	if z == 0:
		for i in range( 18 ):
			plt.plot( bins,  av_a[i, :39], 'k', alpha = 0.2 )
		plt.plot( bins,  np.median( av_a[:, :39], axis = 0 ), 'ko-', linewidth = 2., label = "$C(\omega)'$" )
	if z == 1:
		plt.plot( bins,  np.median( av_a[:, :39], axis = 0 ), 'v-', color = cs[0], linewidth = 2., markeredgecolor = cs[0], label = "$L(\omega)'$" )
	if z == 2:
		plt.plot( bins,  np.median( av_a[:, :39], axis = 0 ), 'rs-', linewidth = 2., markeredgecolor = 'r', label = "$S(\omega)'$" )

	make_axis( ax1 )
	plt.ylabel("a [Wm$^{-2}$ / K / 5hPa]", fontsize = 12)
	plt.ylim([0., 0.2]))

	plt.legend(frameon = False)

plt.savefig( "AM_2_5_5_binned_data_regressions.png" )
plt.savefig( "AM_2_5_5_binned_data_regressions.pdf" )
plt.show()




def make_axis2( a ):

	a.spines['top'].set_color('none')
   	a.spines['right'].set_color('none')
   	a.tick_params(axis = 'x', which = 'both', bottom="off", top = "off", labelbottom = "on")
   	a.tick_params(axis="y", which="both", bottom="off", top="off", labelbottom="off", left="off", right="off", labelleft="on") 

	plt.xlabel("$a$ [Wm$^{-2}$ / K / 5hPa]", fontsize = 12)
	plt.xlim([0., .12 ])

	return 0

fig = plt.figure( figsize = (12, 7) )
plt.subplots_adjust(left = 0.08, right = 0.98, bottom = 0.1, top = 0.95, hspace = 0.3, wspace = 0.3)

for i in range( 4 ):

	ax = plt.subplot(2, 2, i + 1 )
	plt.plot( np.ma.masked_where( coeffs[i] == 0., vals), np.ma.masked_where( coeffs[i] == 0., coeffs[i]), 'ko' )

	make_axis2( ax )

	if i > 1:
		plt.ylim([0., 6.])
	else:
		plt.ylim([0., 2.2])


	if i == 0:
		plt.ylabel( "$\\beta_{F, 1}$" )
	elif i == 1:
		plt.ylabel( "$\\beta_{F, 2}$" )
	elif i == 2:
		plt.ylabel( "$ECS_1$" )
	elif i == 3:
		plt.ylabel( "$ECS_2$" )

plt.savefig("ind_models_0_20hPa.png")
plt.savefig("ind_models_0_20hPa.pdf")
plt.show()
