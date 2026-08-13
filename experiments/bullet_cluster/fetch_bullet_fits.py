import numpy as np
import matplotlib.pyplot as plt
from astroquery.skyview import SkyView
from astropy.wcs import WCS
from astropy.io import fits
from astropy.coordinates import SkyCoord
import astropy.units as u
import os

def fetch_real_data():
    print("Fetching real observational FITS data for 1E 0657-56 (Bullet Cluster)...")
    
    # Coordinates of the Bullet Cluster
    position = SkyCoord('06h58m20s', '-55d56m00s', frame='icrs')
    
    # We query DSS (Optical) and RASS (X-ray)
    try:
        paths = SkyView.get_images(position=position, survey=['DSS', 'RASS-Cnt Broad'], radius=15*u.arcmin)
        
        opt_fits = paths[0][0]
        xray_fits = paths[1][0]
        
        opt_fits.writeto('bullet_optical.fits', overwrite=True)
        xray_fits.writeto('bullet_xray.fits', overwrite=True)
        
        print("Successfully downloaded FITS files:")
        print("Optical: bullet_optical.fits")
        print("X-ray: bullet_xray.fits")
        
        # Test loading
        w = WCS(opt_fits.header)
        print("WCS Origin:", w.wcs.crval)
        print("Pixel scales:", w.wcs.cdelt)
        print("Data shape:", opt_fits.data.shape)
        
    except Exception as e:
        print("Error fetching data:", e)

if __name__ == '__main__':
    fetch_real_data()
