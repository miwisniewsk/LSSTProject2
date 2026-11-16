# LSSTproject
This is a repository, where I upload my progress with LSST project.

WORK before: 

Reading papers on dust attenuation
Downloading and learning basics of Topcat
Downloading anaconda and CIGALE
Data preparation (python) using astropy and uncertainties library
Reading Małek 2024
Test runs of CIGALE (Małek 2024 parameters)

25.02.2026r.

Making this repository.

26.02.2026r.

From JBST catalog I chose points where chi2>20, 0.01>z>0.3. I added new columns representing LSST filters and their uncertainties so that CIGALE could predict those values (6282 rows).

Using topcat I made an intersection of selected sources from JWST and ECDFS - radius 20 arsec saved as Intersection20 (974 rows) file. But we are interested in JWST\ECDFS (we want to substract AGNs) so I made that with topcat as well - selected_cleaned (5387 rows, 6282 - 974 = 5308) file (I picked radius 20).

Update: I changed radius to 2 arcsec and ended up removing only 6 objects

03.03.2026, 05.03.2026

Preparing cigale file and running cigale.

20.03.2026

Previous work: learning more about cigale, making different intersections in top cat

Today: running Cigale with changed parameters and corrected input file; the cleaning of AGNs for radius of 2 arcsec (output folder too big for github)

27.03.2026

Making log-log mass to SFR plot with colored attenuation based on cigale results.

29.03, 01.04

Trying linear fit with cosmological time from Speagle

10.04

Adding attenuation bins, trying linear fit for bins, adding code for calculating number of points at a distance d from the line.

21.04
Previous work: adding Krzysiek code for calculating SFR from different models, learing how to use LSST data, creating ORCID account
and registering on Rubin Science Platorm, attending Observational techniques in astronomy class and installing required packets.

Today's: ploting SFR difference between cigale calculated and modeled SFR. 

11.05

Previous and current: Learning about RSP and using it to extract LSST images, using SEP for backgroung substracttion and photometry.

15.05

Calculating circular photometry for different radiuses, picking the radius that have 80% of the flux and changing this flux into mag.
File galaxy_photometry2.ipynb has shortened version of the analysis (no images etc) for different filters.

29.05

Previous and current work: In Lsst_img I changed catalog from selected_cleaned to a merge of selected_cleaned (contains RA, DEC)
and results (contians mass according to CIGALE), so that I could sort this catalog on mass and search images of the most massive galaxies.
I also debuged this code a little. In galaxy_photometry I changed ADU to mJy (Is it correct?)

galaxy_photometry: In this file there is a sep tutorial for a single galaxy in ugrizy filters. There is background subtraction, object decetction, circular photometry (with images) plus flux to radius plot.

galaxy_photometry2: Everything from first file (without images and object detection) plus flux to radius plots for all filters.

galaxy_photometry3: There is a program for a number of galaxies where I subtract the background, find a relevant radius for a circular photometry
and then I plot all images with this circle. I calculate the magnitudes in different filters, but without flux to radius plots.

Next steps: check if ADU to mJy is correct (probably not), it is clear looking at the images that circular photometry is not good enough
in some cases, because it is getting the light from other sources (eg. object 36), I am not sure about the CIGALE simualtion because some of these "most massive" galaxies look dim.

25.06

galaxy_images_probe.fits - File with 7 galaxies with different luminosities

masking.py - Krzysiek's code for masking (with 2 edits)

masking.ipynb - my usage of Krzysiek's code

galaxy_photomery4.ipynb - Adding masking to my photometry pipeline

3.07

Adding gri masking

9.07

galaxy_photometry5.ipynb - masking in i band in every tenth massive galaxy

i_band10.fits - file with every tenth most massive galaxy in i and u band (vmax 90)

galaxies_images_ui.fits - file with every tenth most massive galaxy in i and u band (vmax 99)

14.07

Adding making a SFR plot in i band to galaxy_photometry4.ipynb
Other mini tasks: making a cutout (file 5), checking mass and position of random galaxies

17.07

galaxies_images245.fits - generated file with a larger numer of galaxies 
Performing photometry and calculating SNR plot for these objects.

20.07

Making a mass histogram (in galaxy photometry 4), setting a red line around 180 galaxy, because after that a lot
of galaxies have SNR above 3.

23.07

lsst_lum_cat.ipynb - with methods used in galaxy_photometry files I extract lsst luminosities only for most massive galaxies that have calculated luminosity in all filters and add this to selected_cleaned.fits
lsst_lum_cat.ipynb - resulting file

*Documenting undocumented so far files*

convert.py - file that creates catalog from james webb
before_crossmatch.fits - file created by convert.py
galaxies.images.fits - top 100 most massive galaxies
Lsst_img.ipynb - pipeline for getting images from RSP
main_seq.ipynb - file with mass to SFR plots etc

27.07

I am changing input catalog (changes in convert.py) so that we have 80% flux not 100%
before_crossmatch80.fits - new output catalog
In lsst_lum_cat I have changed zero points - previous cigale run showed incorrections
cigale80 - folder with cigale files where we have changed data
lsst_match.fits - file with 80% flux in lsst and jwst with old zp
lsst_lum_files - file with 80% flux in lsst and jwst with new zp

29.07

Changing methods (previously assuming wrong units ADU, it is nJy) and running cigale to check how consistnent it is now.

TODO:
* taking care of the repository
* checking the percentage of maskings in images
* checking in catalog documentation (JWST, Hubble) how 80% flux is defined
* making one big pipeline - with all of the content from galaxy_photometry files, maybe removing some of them, making sure the method is corrected
* removing objects with SNR < 3 
* making sure the unit in LSST is actually nJy - printing header of an image
* adding interpolation
* flux to radius ratio but per pixel, and making sure it is done for masked images
* comparing fluxes in LSST and JWST (SED)
* comparing fluxes in LSST and JWST when photometry is performed on an image and not taken from the catalog
* test with a constant aperture - to check where the inconsistencies come from 

30.07

photometry_flux_plots.ipynb - file with different ways of showing flux plots (made from galaxy_photometry2), writing code for a single galaxy
photometry_pipeline.ipynb - fixed methods (masking percentage, correct units) from galaxy_photometry files + SNR in i band + mass histogram
old_photometry - folder with galaxy_photometry files - contain mistakes, no need for fix, no longer in use

Done:
* checking the percentage of maskings in images
* making one big pipeline - with all of the content from galaxy_photometry files, maybe removing some of them, making sure the method is corrected
* flux to radius ratio but per pixel, and making sure it is done for masked images
* removing objects with SNR < 3 (in i band)

Left todo:
* taking care of the repository
* checking in catalog documentation (JWST, Hubble) how 80% flux is defined
* making sure the unit in LSST is actually nJy - printing header of an image
* adding interpolation
* comparing fluxes in LSST and JWST (SED)
* comparing fluxes in LSST and JWST when photometry is performed on an image and not taken from the catalog
* test with a constant aperture - to check where the inconsistencies come from 

10.08

Done:

* making sure the unit in LSST is actually nJy - it is
* adding interpolation - kinda
* test with a constant aperture - 0.5 arcsec = 2.5 pixels in lsst - in const_aperture_test folder
const_aperture_test - results.fits, HST catalog, galaxies_images245.fits the same, the rest is modified

sed_example.psy, CIGALE25_filters_parsed.json - Krzysiek's code for SED analysis without a whole cigale run

Left todo:
* taking care of the repository
* checking in catalog documentation (JWST, Hubble) how 80% flux is defined
* interpolation - checking if it is done correctly
* comparing fluxes in LSST and JWST when photometry is performed on an image and not taken from the catalog

8.10

I have commited uncommited changes so far, that inculdes analysis of vizier data, new cigale run and their comparison. Other work: making a report and an abstract.

table1-3.fits - tables from vizier

join.py - file that takes these columns and selects a sample

vizierSample - file generated by join.py

analysis.ipynb - makes a comparison of estimated mass of cigale results (files not commited) and vizier data

12.11

Little break in coding for making a presentationn and attending a LSST conference.

Fixing everything I commited last time - using same data from the different source - COSMOSWeb mastercatalog, and making code for checking mag - mJy conversion

joinCatalog.py - Krzysiek code for checking mag - mJy conversion

check.ipynb - my code for mag - mJy conversion

joinCosmos.ipynb - the updates version of join.ipynb code for different database - making a Cigale ready file

cosmosSample.fits - Cigale ready file generated by joinCosmos.ipynb

16.11

Generating SEDs and comparing SFRs for previous cigale analysis.

Adding fake LSST bands to cigale

