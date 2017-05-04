import os
import urllib2

import pylab as pl
from matplotlib import image






image_locations = dict(star=dict(RA=180.63040108,
                                 DEC=64.96767375),
                       galaxy=dict(RA=197.51943983,
                                   DEC=0.94881436),
                       quasar=dict(RA=226.18451462,
                                   DEC=4.07456639))


# Plot the images
fig = pl.figure(figsize=(9, 3))

# Check that PIL is installed for jpg support
if 'jpg' not in fig.canvas.get_supported_filetypes():
    raise ValueError("PIL required to load SDSS jpeg images")

object_types = ['star', 'galaxy', 'quasar']

for i, object_type in enumerate(object_types):
    ax = pl.subplot(131 + i, xticks=[], yticks=[])
    I = fetch_image(object_type)
    ax.imshow(I)
    if object_type != 'galaxy':
        pl.arrow(0.65, 0.65, -0.1, -0.1, width=0.005, head_width=0.03,
                 length_includes_head=True,
                 color='w', transform=ax.transAxes)
    pl.text(0.99, 0.01, object_type, fontsize='large', color='w', ha='right',
            transform=ax.transAxes)

pl.subplots_adjust(bottom=0.04, top=0.94, left=0.02, right=0.98, wspace=0.04)

pl.show()



# import astropy
# import astropy.units        as u
# import matplotlib.pyplot    as plt
# from pytz                   import timezone 
# from astroplan              import Observer, FixedTarget
# from astroplan.plots        import plot_parallactic
# 
# 
# long, lat,  = '28d45m38.3s', '+17d52m53.9s'
# elev, time  = 2332 * u.m, astropy.time.Time('2016-04-29 12:00:00')
# 
# location    = astropy.coordinates.EarthLocation.from_geodetic(long, lat, elev)
# 
# 
# WHT         = Observer(name='WHT', location=location, timezone=timezone('Atlantic/Canary'), description="WHT Telescope on Roque de los muchachos, La palma")
# 
# 
# coordinates = astropy.coordinates.SkyCoord(143.509956086, 55.2397619058, frame='icrs', unit="deg")
# vega        = FixedTarget(name='Vega', coord=coordinates)
# 
# angle = WHT.parallactic_angle(time, vega)
# print angle
# 
# plot_parallactic(vega, WHT, time)
#  
# plt.legend(loc=2)
# plt.show()
