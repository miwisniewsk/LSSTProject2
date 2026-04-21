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
and registering on Rubin Science Platorm, attending Observational techniques in astronomy class and intalling required packets.

Today's: ploting SFR difference between cigale calculated and modeled SFR. 