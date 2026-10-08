from astropy.io import fits
from astropy.table import Table
from astropy.table import join
import numpy as np

hdul1 = fits.open('table1.fit')
hdul2 = fits.open('table2.fit')
hdul3 = fits.open('table3.fit')

t1 = Table(hdul1[1].data)
t2 = Table(hdul2[1].data)
t3 = Table(hdul3[1].data)

t1["id"] = np.arange(len(t1))
t2["id"] = np.arange(len(t2))
t3["id"] = np.arange(len(t3))

table = join(t1, t2, keys="id")
table = join(table, t3, keys="id")

def micro_to_mili(column):
    column = column * 10 ** (-3)
    return column

table.rename_column("zfinal", "redshift")

# Flux-aper-HST-F814W-4 -> hst.acs.wfc.F814W
# Flux-aper-CFHT-u-4 -> cfht.megacam.u

filters_before = ["Flux-aper-HST-F814W-4", "Flux-aper-CFHT-u-4", "Flux-aper-F770W-4", "Flux-aper-HSC-y-4"]
filters_after = ["hst.acs.wfc.F814W", "cfht.megacam.u", "jwst.miri.F770W", "subaru.suprime.Y"]

for i in range(len(filters_before)):
    table.rename_column(filters_before[i], filters_after[i])
    table[filters_after[i]] = micro_to_mili(table[filters_after[i]])
    table.rename_column("e_" + filters_before[i], filters_after[i] + "_err")
    table[filters_after[i] + "_err"] = micro_to_mili(table[filters_after[i] + "_err"])

# Flux-aper-F115W-4 -> jwst.nircam.F115W
jwst_filters = "F115W F150W F277W F444W"    
jwst_prefix = "jwst.nircam."

for jwst_filter in jwst_filters.split():
    new_name = jwst_prefix + jwst_filter
    table.rename_column("Flux-aper-" + jwst_filter + "-4", new_name)
    table[new_name] = micro_to_mili(table[new_name])
    table.rename_column("e_Flux-aper-" + jwst_filter + "-4", new_name + "_err")
    table[new_name + "_err"] = micro_to_mili(table[new_name + "_err"])

# Flux-aper-HSC-g-4 -> subaru.hsc.g (subaru.hsc.Y)
hsc_filters = "g r i z"
hsc_prefix = "subaru.suprime."

for hsc_filter in hsc_filters.split():
    new_name = hsc_prefix + hsc_filter
    table.rename_column("Flux-aper-HSC-" + hsc_filter + "-4", new_name)
    table[new_name] = micro_to_mili(table[new_name])
    table.rename_column("e_Flux-aper-HSC-" + hsc_filter + "-4", new_name + "_err")
    table[new_name + "_err"] = micro_to_mili(table[new_name + "_err"])

table = table[(table["zchi2"] <= 4.9)]
table = table[(table["chi2-AGN"] >= table["zchi2"])]
table = table[table["redshift"] < 0.3]
table = table[table["logMass-med"] > 8.5]
table = table[table["Type"] == 0]

table.write("vizierSample.fits", format="fits", overwrite=True)