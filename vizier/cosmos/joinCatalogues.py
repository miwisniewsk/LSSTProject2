import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table
from uncertainties import unumpy as unp

def mag_to_jy(mag, mag_err=None):
    if mag_err== None:
        flux = 10**((23.9-mag)/2.5)*1e-6
        flux_err = -99.9
    else:
        x = unp.uarray(mag, mag_err)
        flux = 10**((23.9-x)/2.5)*1e-6
        flux, flux_err = unp.nominal_values(flux), unp.std_devs(flux)
    return flux, flux_err
    
photoPSF = Table.read('COSMOSWeb_mastercatalog_v1.1_photom_primary.fits')
photoNoHomo = Table.read('COSMOSWeb_mastercatalog_v1.1_photom_secondary.fits')

f115_mag, __ = mag_to_jy(photoNoHomo['mag_aper_f115w'][:,-1], photoNoHomo['mag_err_aper_f115w'][:,-1])*1e3
f115_flux = photoNoHomo['flux_aper_f115w'][:,-1]*1e3
