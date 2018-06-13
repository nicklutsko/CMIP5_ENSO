""""
Nicholas Lutsko -- EAPS department, MIT

Script to perform lag-regressions between Nino3.4 index, low cloud cloud cover, tropical-mean surface temperature and low cloud CRE.

Last updated -- June 13th 2018
"""
import numpy as np
import matplotlib.pylab as plt
import scipy.signal as ss



###############################
# Some functions we need

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

def norm_corr( a, b ):

	a1 = (a - np.mean(a)) / (np.std(a))
	b1 = (b - np.mean(b)) / (np.std(b))

	return np.correlate( a1, b1, mode = "full" )  / len( a )


###############################
# Load data

trop_temp = np.load( "../Bony_decomp/data/AM_trop_temp.dat" )
nino = np.load( "../Bony_decomp/data/NINO3.4_index.dat" )

m, t = np.shape( nino )

#Bins to average over
b1 = 18
b2 = 23
o = 6 #total CRE

data = np.load( "../Bony_decomp/data/monthly_binned_data_5hPa.dat" ) #Note that the decompositions were done for just the monthly data

low_c = np.zeros( ( m, t ) )
data = np.mean( data[:, 6, :, b1:b2], axis = 2 )
for i in range( m ):
	low_c[i] = f.remove_sc( data[i, :] )
low_c = ss.detrend( low_c[:, :] - np.mean( low_c[:, :], axis = 1)[:, np.newaxis], axis = 1 )

data2 = np.load( "../Bony_decomp/data/monthly_binned_CF_data_5hPa.dat" ) #The binned cloud fraction
low_cf = np.zeros( ( m, t ) )
data2 = np.mean( data2[:, 1, :, b1:b2], axis = 2 )
for i in range( m ):
	low_cf[i] = f.remove_sc2( data[i, :] )
low_cf = ss.detrend( low_cf[:, :] - np.mean( low_cf[:, :], axis = 1)[:, np.newaxis], axis = 1 )


###############################
# Do correlations
corr = np.zeros( ( (4, m, 2 * t - 1 ) ) )

for j in range( m ):
	corr[0, k, :] = norm_corr( trop_temp[j, :], low_c[j, :] )
	corr[1, k, :] = norm_corr( nino[j, :], low_c[j, :] )
	corr[2, k, :] = norm_corr( nino[j, :], trop_temp[j, :] )
	corr[3, k, :] = norm_corr( low_c[j, :], low_cf[j, :] )


###############################
# Plot

def make_axis( a ):
    	a.spines['top'].set_color('none')
   	a.spines['right'].set_color('none')
   	a.tick_params(axis = 'x', which = 'both', bottom="off", top = "off", labelbottom = "on")
   	a.tick_params(axis="y", which="both", bottom="off", top="off", labelbottom="off", left="off", right="off", labelleft="on") 

	plt.axvline( x = 0, color = 'k' )

	plt.ylabel("Correlation", fontsize = 12)
	plt.ylim([-0.65, 1.])
	plt.yticks([-0.6, -0.4, -0.2, 0., 0.2, 0.4, 0.6, 0.8, 1.], fontsize = 12)
	plt.axhline( y = 0., color = 'k', linestyle = '-', linewidth = 2. )
	plt.xlim([-3., 3.])
	plt.xlabel("Lag [years]", fontsize = 12 )

	return 0

ti = np.arange( -float(t / 12) + 1. / 12, float(t / 12) - 1. / 12., 1. / 12. )

fig = plt.figure( figsize = (10, 10) )
ax = plt.subplots_adjust(left = 0.1, right = 0.98, bottom = 0.06, top = 0.95, hspace = 0.35, wspace = 0.3)

titles = ["Tropical mean - Low clouds", "Nino3.4 region - Low clouds", "Nino3.4 region - Tropical mean", "Low clouds - Tropical cloud cover"]

for i in range( 4 ):
	ax = plt.subplot(2, 2, i + 1 )
	plt.title( titles[i] )
	for j in range( m ):
		plt.plot( t, corr[j, i], 'k', alpha = 0.2 )
	plt.plot( t, np.median( corr[:, i], axis = 0 ), 'k', linewidth = 2. )

	make_axis( ax )

plt.savefig( "cross_correlations.png" )
plt.savefig( "cross_correlations.pdf" )
plt.show()


















