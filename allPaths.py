from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.patches import Polygon

#Created by: Brandon D. Molyneaux
#Last modification: 6/22/17
#This script is designed to download the NHC's shapefiles for tropical systems.
#The only thing that should be changed is the path (located below).
#This is where the shapefiles will be stored.

def identify_shapefile_name(shape_type):
    '''This function identifies what shapefile to use and stores it in the \n
    variables lin, pgn, pts, wwlin. These are PATH variables used to read in \n
    the path to the shapefile.'''
    
    shap_dict = {'lin': 0, 'pgn':5, 'pts': 10, 'wwlin':15} #dictionary for line below
    type1 = os.listdir(path)[shap_dict[shape_type]]
    full_name = os.path.splitext(type1)[0]
    return path + full_name

path = 'zipped_nhc_trop_outlook/'
plt.close('all') #closes plot if open

from NHCMapMaker import NHCMapMaker

hurrmap = NHCMapMaker(rightlon = -15, botlat = 10, leftlon = -90, toplat = 45)
m = hurrmap.makeMap()

xVal = []
yVal = []
for j in range(1, 56):
    url = "http://www.nhc.noaa.gov/gis/forecast/archive/al062018_5day_" + \
        '%0.3d' % j   
             
    hurrmap.getZipFiles("Desktop/" + path, url)
    
    print '   Advisory ' + str(j)

    pgn = identify_shapefile_name('pgn') #'bubble'
    pts = identify_shapefile_name('pts') #Points along the track
    
    points_info = m.readshapefile(pts, 'points')
    for info, shape in zip(m.points_info, m.points):
        x, y = zip(shape)
        if info['TAU'] == '0':
            xVal.append(x[0])
            yVal.append(y[0])
        else: pass      

bubble_info = m.readshapefile("/Users/Brandon/Desktop/testingShp", 
        'bubble', linewidth = 0.03) #bubble
for info, shape in zip(m.bubble_info, m.bubble):
    storm_name = info['STORMNAME']
    poly = Polygon(np.array(shape), facecolor= '#F5F5F5', alpha=0.5)
    plt.gca().add_patch(poly)
 
m.plot(xVal, yVal, linewidth = 1, color = 'k')  
m.plot(xVal, yVal, linewidth = 0.8, color = 'w')     

hurrmap.write_text(0.5, 1, "Hurricane Florence\nNHC Cones and Tracks", 'center', 
        'center', fontsize = 'medium', bbox = True)
hurrmap.write_text(1, 1, "Brandon Molyneaux\nwww.bdmweather.com", 'right', 'bottom', 
        fontsize = 'small')
hurrmap.write_text(0, -0.07, "This map shows advisories 1 - 57 with the track and all 5 day cones." + 
    "\nSee latest from NHC at www.nhc.noaa.gov.",
    'left', 'top', fontsize = 'xx-small')
hurrmap.write_text(0, 1, "Source: NHC\nwww.hurricanes.gov", 
    'left', 'bottom', fontsize = 'small')

plt.show()

#plt.savefig('florenceNHC', bbox_inches = 'tight', dpi = 500, facecolor = "#F5F5F5") #saves figure
