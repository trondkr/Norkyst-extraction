# encoding: utf-8

import numpy as np
import iso


def zslice(var, z, mask, depth, mode='linear'):
   
    if mode=='linear':
        imode=0
    elif mode=='spline':
        imode=1

    depth = -abs(depth)
    depth = depth * np.ones(z.shape[1:])

    zslice = iso.zslice(z, var, depth, imode)

    # mask land
    zslice = np.ma.masked_where(mask == 0, zslice)
    # mask region with shalower depth than requisted depth
    zslice = np.ma.masked_where(zslice == 1e20, zslice)

    return zslice

