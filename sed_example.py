import numpy as np
import matplotlib.pyplot as plt
import json
from astropy.io import fits
from astropy.table import Table

def cigale_filters(v=25):

    path = 'CIGALE25_filters_parsed.json'
    with open(path, "r") as f:
        loaded = json.load(f)
    return loaded

def findPhoto(table):

    x = []
    y = []
    yerr = []
    xupper = []
    yupper = []
    labels = []

    for c in table.columns:

        try:
            if table[c + '_err'] < 0:

                xupper = np.append(xupper, [cigale[c]])
                yupper = np.append(yupper, [table[c]])

            else:
                x = np.append(x, [cigale[c]])
                y = np.append(y, [table[c]])
                yerr = np.append(yerr, [table[c + '_err']])

                labels.append(c)

        except:
            pass

    return x, y, yerr, xupper, yupper, labels

observations = Table.read('before_crossmatch80.fits')
cigale = cigale_filters()

for galaxy in observations:

    xobs, yobs, yerrobs, xupperobs, yupperobs, labels = findPhoto(galaxy)

    plt.scatter(xobs, yobs, marker = 'o')
    plt.scatter(xobs, yobs, marker = 'v')