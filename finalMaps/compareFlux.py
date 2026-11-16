from astropy.table import Table
from astropy.io import fits
import numpy as np
from uncertainties import unumpy
import matplotlib.pyplot as plt
from astropy.cosmology import LambdaCDM, FlatwCDM
import astropy.units as u
from astroquery.mast import Observations
from astropy.coordinates import SkyCoord
from PyRite.cosmologyRelated import *
from PyRite.plotting import *
from PyRite.otherUseful import change_image
import sep

# lsst = np.loadtxt('LSST_LSST.r.dat')
# hst = np.loadtxt('HST_ACS_WFC.F606W.dat')
# plt.plot(lsst[:,0], lsst[:,1], label ='lsst')
# plt.plot(hst[:,0], hst[:,1], label = 'hst')
# plt.legend()
# plt.show()
# print(aa)


def detect_sources(image, thresh = 1.3, deblend_nthresh = 32, deblend_cont = 0.0001):
    """
    This class runs sextractor with python and allows user to build necessary files for galfit.
    :param image: Array
    :param thresh: Sextractor parameter.
    :param deblend_nthresh: Sextractor parameter.
    :param deblend_cont: Sextractor parameter.
    """
    image = image
    image = image.byteswap().view(image.dtype.newbyteorder())
    image = image.astype(np.float32)

    bkg = sep.Background(image)
    bkg_image = bkg.back()
    data_sub = image - bkg_image

    objects = sep.extract(data_sub, thresh,
                               err=bkg.globalrms,
                               deblend_nthresh=deblend_nthresh,
                               deblend_cont=deblend_cont)
    return objects
def is_pixel_in_ellipse(image_size, center, a, b, theta, scale = 1, ap = 0):
    # Generate the grid of coordinates
    a = a*scale +ap
    b = b*scale +ap
    y, x = np.indices(image_size)
    theta = np.deg2rad(theta)

    # Shift the coordinates to the ellipse center
    x_shifted = x - center[0]
    y_shifted = y - center[1]

    # Apply the rotation matrix to the shifted coordinates
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    x_rot = x_shifted * cos_theta + y_shifted * sin_theta
    y_rot = -x_shifted * sin_theta + y_shifted * cos_theta

    # Ellipse equation (x_rot / a)^2 + (y_rot / b)^2 <= 1
    ellipse_mask = ((x_rot / a) ** 2 + (y_rot / b) ** 2) <= 1
    return ellipse_mask
def make_mask(image, objects, additionalSize = 2, centralSourceDistance = 10, scale = 3):
    result = np.zeros(image.shape)
    centralPositionX, centralPositionY = image.shape[0]/2, image.shape[1]/2

    no = 0
    for o in objects:
        no += 1
        if no%100 == 0:
            print(f'Done {no/len(objects)}')
        dist = np.sqrt((o['x'] - centralPositionX)**2 + (o['y'] - centralPositionY)**2)
        if dist>centralSourceDistance:
            mask = is_pixel_in_ellipse(image.shape,
                               (o['x'] - 1, o['y'] - 1),
                                      o['a'],
                                      o['b'],
                                      np.rad2deg(o['theta']),
                                      scale = scale,
                                      ap=additionalSize)
            result[mask] = 1
    return result
def showMask(ax, maskToShow, maskColor = 'dodgerblue'):
    xTick = np.arange(maskToShow.shape[0])
    yTick = np.arange(maskToShow.shape[1])

    YC, XC = np.meshgrid(xTick + (xTick[1] - xTick[0]) / 2+1,
                         yTick + (yTick[1] - yTick[0]) / 2+1)
    ax.contour(XC, YC, maskToShow.T, levels=[0.5], colors=[maskColor],
               linewidths = [2])

    maskToShow = np.log10(maskToShow)
    maskToShow[maskToShow>-np.inf] = 1
    Y, X = np.meshgrid(xTick+1, yTick+1)
    ax.pcolormesh(X, Y, maskToShow.T,
                  alpha=0.45, zorder=2,
                  cmap='Blues_r')
def aperture_flux(data, x, y, radius,mask, telescope, pixsize, bkg=True, n_sigma = 3, sb = False):
    """
    Measure aperture flux using SEP.

    Parameters
    ----------
    data : 2D ndarray
        HST science image. Your image should be in the units given
        by BUNIT = '10.0*nanoJansky'.

    x, y : list
        Aperture centre in pixel coordinates.

    radius : list
        Aperture radius in pixels.

    bkg : sep.Background, optional
        SEP background object. If None, a background is estimated
        from the image.

    Returns
    -------
    flux_mJy : float
        Background-subtracted aperture flux in mJy.

    flux_err_mJy : float
        SEP aperture flux uncertainty in mJy.
    """



    data = np.asarray(data, dtype=np.float64)
    data = data.byteswap().newbyteorder()

    if bkg:
        gals = detect_sources(data)
        newmask = make_mask(data, gals, centralSourceDistance=-1)

        bkg = sep.Background(data, mask = newmask)
        data_sub = data - bkg.back()
        rms = bkg.globalrms
        #print(np.mean(bkg.back()), np.median(bkg.back()), rms)
        # plt.close()
        # plt.imshow(bkg.back(), origin='lower')
        # plt.show()

        # res.write('bkg/%s_%i.fits'%(telescope, top[gal]['id']), overwrite = True, header = )
    else:
        data_sub = data# - bkg
        rms = np.std(data_sub[mask==0])



    vals = np.copy(data_sub)
    vals[newmask==1] = 0
    vals = vals.flatten()
    vals = vals[vals!=0]
    sigma = np.std(vals)

    data_sub[mask==1] = 0
    # Circular aperture photometry
    flux, __, flag = sep.sum_circle(
        data_sub,
        x,
        y,
        radius
    )
    aperture_area_pix, _, _ = sep.sum_circle(
        (~(mask == 1)).astype(float),
        x,
        y,
        radius
    )

    area_arcsec2 = aperture_area_pix * pixsize ** 2
    annuliSize = area_arcsec2[0]
    annuliSize = np.append(annuliSize, area_arcsec2[1::] - area_arcsec2[0:-1])


    fluxerr = rms * np.sqrt(annuliSize)
    #print(flux/fluxerr)


    if telescope == 'hst':
        # Image units = 10 nJy
        flux_nJy = flux * 10.0
        fluxerr_nJy = fluxerr * 10.0
        sigma *= 10
        sigma *= n_sigma
    elif telescope == 'lsst':
        # Image units = 1 nJy
        flux_nJy = flux
        fluxerr_nJy = fluxerr
        sigma *= n_sigma
    # nJy -> mJy

    flux_mJy = flux_nJy / 1e6
    fluxerr_mJy = fluxerr_nJy / 1e6
    sigma /= 1e6
    if not sb:
        return flux_mJy, fluxerr_mJy, 0
    limitSigma = sigma/pixsize**2

    res =flux_mJy[0]
    res = np.append(res, flux_mJy[1::] - flux_mJy[0:-1])

    return res/annuliSize, fluxerr_mJy, limitSigma
def find_intersections(x, y1, y2):
    """
    Find x positions where two curves intersect.

    Parameters
    ----------
    x : array-like
        Common x values, assumed sorted.
    y1, y2 : array-like
        Y values of the two curves.

    Returns
    -------
    x_intersections : ndarray
        Interpolated x positions of the intersections.
    """
    x = np.asarray(x)
    y1 = np.asarray(y1)
    y2 = np.asarray(y2)

    diff = y1 - y2

    # Exact intersections
    exact = x[diff == 0]

    # Sign changes between consecutive points
    idx = np.where(diff[:-1] * diff[1:] < 0)[0]

    # Linear interpolation of diff(x) = 0
    x_cross = x[idx] - diff[idx] * (
        x[idx + 1] - x[idx]
    ) / (diff[idx + 1] - diff[idx])

    return np.unique(np.concatenate([exact, x_cross]))
cmap = truncate_colormap('magma', 0.2)

pixjwst = 0.05
pixlsst = 0.2
apertures = np.arange(0.4, 16.2, 0.4)
set_style(axisRatio=1)

top = fits.open('before_crossmatch80.fits')[1].data
top = top[np.argsort(top['hst.acs.wfc.F606W'])[::-1]]
lsst4arcsec = []
hst4arcsec = []

for gal in range(30):
    print(top[gal]['id'])
    #if top[gal]['id'] != 244396: continue
    try:
        lsst = np.loadtxt('lsst_cutouts/%i.txt'%top[gal]['id'])
        jwst = fits.open('hst_cutouts/%i_F606W.fits'%top[gal]['id'])[0].data
    except Exception as err:
        print(err)
        continue

    fig = plt.figure()
    ax1, ax2 = makeSubplots(fig, 2, 1, [0.12, 0.5, 0.1, 0.1], xspace=0)
    ax1.tick_params(which = 'both',left = False, labelleft = False, bottom = False, labelbottom = False)
    ax2.tick_params(which = 'both',left = False, labelleft = False, bottom = False, labelbottom = False)

    toShowLSST = change_image(lsst)
    ax1.imshow(toShowLSST, origin='lower', cmap = cmap)
    ax1.set_title('LSST.r')
    for i in [2,4,8]:
        c1 = plt.Circle((75*4,75*4), i/pixlsst, fc = 'None', ec = 'w', lw = 1)
        ax1.add_patch(c1)

        c1 = plt.Circle((300*4,300*4), i/pixjwst, fc = 'None', ec = 'w', lw = 1)
        ax2.add_patch(c1)
    ax1.plot([],[], lw = 1, c = 'w', label = '2, 4, 8 arcsec')
    #gals = detect_sources(lsst)
    #masklsst = make_mask(lsst, gals, centralSourceDistance=4/pixlsst)
    #showMask(ax1, masklsst)
    ax1.legend()

    toShowJWST = change_image(jwst)
    ax2.imshow(toShowJWST, origin='lower', cmap = cmap)
    ax2.set_title('HST.F606W')

    #gals = detect_sources(jwst)
    # maskhst = make_mask(jwst, gals, additionalSize=2, centralSourceDistance=6/pixjwst)
    # showMask(ax2, maskhst)


    # lsstFlux, lsstFluxErr,lsstlim = aperture_flux(lsst,
    #                                       [75*4]*len(apertures),
    #                                       [75*4]*len(apertures),
    #                                       apertures/pixlsst,
    #                                       masklsst, 'lsst',
    #                                       pixlsst, bkg=True,)
    lsst = np.asarray(lsst, dtype=np.float64)
    lsstFlux, __, flag = sep.sum_circle(lsst,
                                        [75*4]*len(apertures),
                                        [75*4]*len(apertures),
                                        apertures/pixlsst)

    lsstFlux = lsstFlux / 1e6

    # hstFlux, hstFluxErr,hstlim = aperture_flux(jwst, [300*4]*len(apertures), [300*4]*len(apertures),
    #                                            apertures/pixjwst, maskhst, 'hst', pixjwst, bkg=True)
    jwst = np.asarray(jwst, dtype=np.float64)
    hstFlux, __, flag = sep.sum_circle(jwst,
                                        [300*4]*len(apertures),
                                        [300*4]*len(apertures),
                                        apertures/pixlsst)
    hstFlux = hstFlux * 10.0/ 1e6
    ax = makeSubplots(fig, 1 ,1, [0.12, 0.08, 0.1, 0.52])
    ax.plot(apertures, lsstFlux/hstFlux)
    lsst4arcsec.append(lsstFlux[9])
    hst4arcsec.append(hstFlux[9])
    # ax.errorbar(apertures, hstFlux, yerr = hstFluxErr,
    #             label = 'HST.F606W', marker = '.', capsize= 5, c = 'r')
    #
    # ax.errorbar(apertures, lsstFlux, yerr = lsstFluxErr,
    #             label = 'LSST.r', marker = '.', capsize= 5, c = 'b')
    # ax.axvline(x=2)
    # try:
    #     xinter = find_intersections(apertures, hstFlux, lsstFlux)[0]
    #     ax.axvline(x = xinter, ls = '--', c = 'r')
    # except:
    #     pass
    # ax.axhline(y = hstlim, c = 'r')
    # ax.axhline(y = lsstlim, c = 'b')

    ax.legend()
    ax.set_xlabel('Annulus aperture [arcsec]')
    ax.set_ylabel('LSST/HST')
    #ax.set_yscale('log')
    # ax.set_ylim(1e-6, 2e-1)
    # ax.set_xlim(0, 15)
    plt.savefig('results/%i.png'%top[gal]['id'])
    plt.close()

lsst4arcsec = np.array(lsst4arcsec)
hst4arcsec = np.array(hst4arcsec)

a, b = np.polyfit(lsst4arcsec, hst4arcsec, 1)
plt.scatter(lsst4arcsec, hst4arcsec)
plt.plot(lsst4arcsec, lsst4arcsec, c = 'r')
plt.plot(lsst4arcsec, lsst4arcsec*a + b, c = 'k')
print(a,b)
plt.show()