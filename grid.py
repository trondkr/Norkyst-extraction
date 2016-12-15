 
from vgrid import *

def setupVertical(cdf):

   
    theta_s=np.float(cdf.variables['theta_s'][:])
    theta_b=np.float(cdf.variables['theta_b'][:])
    Tcline=np.float(cdf.variables['Tcline'][:])
    Vtrans=np.float(cdf.variables['Vstretching'][:])
    h=cdf.variables['h'][:]

    N = len(cdf.dimensions['s_rho'])
    zeta=None
    hraw=None

    if Vtrans == 1:
        vgrid = s_coordinate(h, theta_b, theta_s, Tcline, N, hraw=hraw, zeta=zeta)
    elif Vtrans == 2:
        vgrid = s_coordinate_2(h, theta_b, theta_s, Tcline, N, hraw=hraw, zeta=zeta)
    elif Vtrans == 4:
        vgrid = s_coordinate_4(h, theta_b, theta_s, Tcline, N, hraw=hraw, zeta=zeta)

    return vgrid.z_r[:]