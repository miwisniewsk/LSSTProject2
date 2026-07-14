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

i_band10.fits - file with every tenth most massive galaxy in i and u band (vmax 99)

galaxies_images_ui.fits - file with every tenth most massive galaxy in i and u band (vmax 99)