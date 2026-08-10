from astropy.io import fits
from astropy.table import Table
from astropy.table import join
import numpy as np
from uncertainties import ufloat
from uncertainties import unumpy as unp

# Loading data
hdul = fits.open('hlsp_jades_jwst_nircam_goods-s-deep_photometry_v2.0_catalog.fits')

table3 = Table(hdul[3].data)
table6 = Table(hdul[4].data)
table9 = Table(hdul[9].data)

# I intialize the data structure with following data
table = Table(table3[["ID", "RA", "DEC", "R_KRON", "A", "B"]])

# Here I get all the filters and name them properly
jwst_filters = "F090W F115W F150W F182M F200W F210M F277W F335M F356W F410M F430M F444W F460M F480M " 
hst_acs_wfc_filters = "F435W F606W F775W F814W "
hst_wfc_ir_filters = "F105W F125W F140W F160W"

filter_prefixes = ["jwst.nircam.", "hst.acs.wfc.", "hst.wfc3.ir."]
filter_types = [jwst_filters, hst_acs_wfc_filters, hst_wfc_ir_filters]

fluxes = Table(table6[["ID"]])

for i in range(3):
    filters = filter_types[i]
    for filter in filters.split():
        flux = table6[["ID", filter + "_CIRC6", filter + "_CIRC6_e"]]
        # nJy to mJy
        flux[filter + "_CIRC6"] = 1e-6 * flux[filter + "_CIRC6"]
        flux[filter + "_CIRC6_e"] = 1e-6 * flux[filter + "_CIRC6_e"]

        flux.rename_column(filter + "_CIRC6", filter_prefixes[i] + filter)
        flux.rename_column(filter + "_CIRC6_e", filter_prefixes[i] + filter + "_err")

        fluxes = join(fluxes, flux, keys="ID")

table = join(table, fluxes, keys="ID")

# Adding redshift and chi2
new_columns = table9[["ID", "EAZY_z_a", "EAZY_chisq_min"]]
new_columns.rename_column("EAZY_z_a", "redshift")
table = join(table, new_columns, keys="ID")

# Filterring data
table = table[(0.01 < table["redshift"]) & (table["redshift"] < 0.3)]
table = table[table["EAZY_chisq_min"] < 20]

# Adding empty LSST filters: (u g r i z y)
LSST_filters = "u g r i z y"

for LSST_filter in LSST_filters.split():
    filter_name = "rubin.lsst." + LSST_filter
    table[filter_name] = -99.9
    err_name = filter_name + "_err" 
    table[err_name] = -99.9

# Adding brightness, here we need F435W_KRON, which is correctly called hst.acs.wfc.F435W in magAB, but CIGALE 
# needs it in mJy and in the column are values in mJy
def mJy_tomagAB(x):
    mask = (unp.nominal_values(x) > 0) & (np.isfinite(unp.nominal_values(x)))
    y = np.full(len(x), np.nan, dtype=object)
    y[mask] = 23.9 - 2.5 * unp.log10(x[mask] * 1e3)
    return y
table6 = Table(hdul[4].data)

values = table["hst.acs.wfc.F435W"]
errors = table["hst.acs.wfc.F435W_err"]

F435W = unp.uarray(values, errors)

F435W = mJy_tomagAB(F435W)

# values of F435_KRON in magAB
table["F435mag"] = unp.nominal_values(F435W)
table["F435mag_err"] = unp.std_devs(F435W)
# values of miu_x
miu = F435W + 2.5 * np.log10(2 * np.pi * table["R_KRON"] ** 2) 
# adding corrections
miu_corr = miu + 2.5 * np.log10(table["B"]/table["A"]) - 10 * np.log10(1 + table["redshift"]) 

table["miu_x_corr"] = unp.nominal_values(miu_corr)
table["miu_x_corr_err"] = unp.std_devs(miu_corr)

table.rename_column("ID", "id")

table.write("before_crossmatch80.fits", format="fits", overwrite=True)

print(table)