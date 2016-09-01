
def plotGlobeMesh(elevation_longitude,  # Longitude dimension for elevation
    elevation_latitude,             # Latitude dimension for elevation
    elevation,                      # Elevation on (elevation_longitude, elevation_latitude) mesh
    variable_longitude,             # Longitude dimension for plotted variable
    variable_latitude,              # Latitude dimension for plotted variable
    variable,                       # Variable on (variable_longitude, variable_latitude) mesh
    vert_aspect=30000.,             # Optional vertical / horizontal aspect ratio
    sea_land_ratio=2.,              # Optional sea / land vertical aspect ratios
    vmin=None,                      # Minimum value of colormap for variable
    vmax=None,                      # Maximum values of colormap for variable
    cmap='RdYlBu',                  # Colormap key
    cmap_r=True):                   # Colormap reversing boolean (True is reverse)

    # Import Modules
    import sys
    import numpy as np
    from mayavi import mlab

    # Convert degrees to radians for elevation_latitude and elevation_longitude
    phi = (((elevation_latitude*np.pi*2)/360.)+np.pi/2.)
    theta = (-elevation_longitude*np.pi*2)/360.

    # Append elevation mesh to have longitudinally-periodic boundary condition
    theta = np.append(theta,[theta[0]],axis=0)
    append_theta = elevation[0,:]
    elevation = np.append(elevation, append_theta[None,:], axis=0)

    # Convert phi and theta to two-dimensional meshes
    phi, theta = np.meshgrid(phi,theta)

    # Apply sea / land aspect ratio
    elevation[elevation>-30]=elevation[elevation>-30]/sea_land_ratio

    # Global elevation dimensions mapped onto cartesian coordinates,
    # scaled by vertical / horizontal aspect ratio
    x = np.sin(phi) * np.cos(theta) * (1 + elevation/vert_aspect)
    y = np.sin(phi) * np.sin(theta) * (1 + elevation/vert_aspect)
    z = np.cos(phi) * (1 + elevation/vert_aspect)

    # Create figure, specifying size, background color, and foreground color
    mlab.figure(size = (1024,768),bgcolor = (1,1,1), fgcolor = (0.5, 0.5, 0.5))
    mlab.clf()

    # Split up ocean and land to give different colormaps
    cocean = np.copy(elevation)
    cland = np.copy(elevation)
    cocean[cocean>=0] = np.nan
    cland[cland<0] = np.nan

    # Plot ocean elevation with 'Blues' colorbar
    m = mlab.mesh(x, y, z, scalars = -cocean, colormap = 'Blues', vmin = 0, vmax = 7000)
    m.module_manager.scalar_lut_manager.lut.nan_color = [0,0,0,0]

    # Plot land elevation with 'gist_earth' colorbar
    m = mlab.mesh(x, y, z, scalars = cland, colormap = 'gist_earth', vmin = -1800, vmax = 1800)
    m.module_manager.scalar_lut_manager.lut.nan_color = [0,0,0,0]

    # Convert degrees to radians for variable_longitude and variable_latitude
    phi = (((variable_latitude*np.pi*2)/360.)+np.pi/2.)
    theta = (-variable_longitude*np.pi*2)/360.

    # Append variable mesh to have longitudinally-periodic boundary condition
    theta = np.append(theta,[theta[0]],axis=0)
    append_theta = variable[0,:]
    variable = np.append(variable, append_theta[None,:], axis=0)

    # Turn phi and theta into meshes
    phi, theta = np.meshgrid(phi,theta)

    # Global variable dimensions mapped onto cartesian coordinates
    x = np.sin(phi) * np.cos(theta)
    y = np.sin(phi) * np.sin(theta)
    z = np.cos(phi)

    # Mask sea surface mesh where variable mesh is masked
    z[np.isnan(variable)] = np.nan

    # Plot variable mesh on globe
    m = mlab.mesh(x, y, z, scalars = variable, colormap = cmap,vmin=vmin,vmax=vmax)
    m.module_manager.scalar_lut_manager.lut.nan_color = [0,0,0,0]
    m.module_manager.scalar_lut_manager.reverse_lut = cmap_r
    mlab.show()

