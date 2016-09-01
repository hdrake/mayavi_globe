import numpy as np
from plotGlobe import *

# Demo variables are temperature, salinity, oxygen, and silicate
varname = 'temperature'

# Load bathymetry data for demo
ocean_depth_data = np.load('sample_data/ETOPO1_60min.npz')
bath_depth = np.swapaxes(ocean_depth_data['z'][:,:],0,1)
bath_latitude = ocean_depth_data['y'][:]
bath_longitude = ocean_depth_data['x'][:]

# Load data for variable mesh
ocean_var_data = np.load('sample_data/Glodap_demo_surface_data.npz')
data_variable = np.swapaxes(ocean_var_data[varname][:,:],0,1)
data_latitude = ocean_var_data['latitude'][:]
data_longitude = ocean_var_data['longitude'][:]

# Mask variable mesh at land (land values are flagged with values of -999 in this case)
data_variable[data_variable==-999] = np.nan

# Vertical aspect ratio (float)
vert_aspect = 30000.
sea_land_ratio = 2.
vmin = None
vmax = None
cmap = 'RdYlBu'

# Plot a variable mesh on a globe interactively using plotGlobeMesh
plotGlobeMesh(bath_longitude,bath_latitude,bath_depth,
	data_longitude,data_latitude,data_variable,
	vert_aspect=30000., sea_land_ratio=2.,
	vmin=None,vmax=None,cmap='RdYlBu',cmap_r=True)