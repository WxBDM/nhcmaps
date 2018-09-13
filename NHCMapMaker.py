'''
Author: Brandon Molyneaux
Date: 9/13/18

The purpose of this is to re-use code when generating maps.

'''

class NHCMapMaker:
    
    modules = [] # checks for what modules were imported.
    
    def __init__(self, rightlon = None, botlat = None, leftlon = None, 
        toplat = None):
        
        if rightlon is None or botlat is None or leftlon is None or toplat is None:
            raise ValueError("One field is empty. Check.")
        
        #checks to make sure input values are right.
        if botlat > toplat: raise ValueError("Switch bottom and top lats")
        if rightlon < leftlon: raise ValueError("Switch left and right lons")
        
        #values to access later.
        self.rightlon = rightlon
        self.botlat = botlat
        self.leftlon = leftlon
        self.toplat = toplat
        self.bounds = [rightlon, botlat, leftlon, toplat]  
    
    def makeMap(self,  proj = 'merc', mapBackground = 'ShadedRelief', 
        drawCoastlines = True, drawStates = True, drawCountries = True, 
        drawParellels = True, drawMeridians = True):
        '''
        Generates the map.
        
        ----- Summary -----
        | Required Inputs: rightlon, botlat, leftlon, toplat
        |
        | Optional Inputs: proj, shade, drawCoastlines, drawStates, drawCountries,
        |    drawParellels, drawMeridians
        | 
        | Returns: Basemap object
        --------------------
        
        Details below:
        
        ----------------------------------------------------
        Required Inputs  | leftlon => Western Longitude
        Description      | rightlon => Eastern Longitude
                         | toplat => Northern Latitude
                         | botlat => Southern Latitude
        ----------------------------------------------------
        Optional Inputs  | proj => Projection of map. 
        Description      |     Default: merc
                         |     Options: any basemap projection. See docs.
                         | shade => Map background.
                         |     Default: 'ShadedRelief'
                         |     Options: 'BlueMarble', 'ETopo', 'None'
                         | drawCoastlines => Draws coastlines. If true, draw them.
                         |     Default: True
                         | drawStates => Draws states. If true, draw them.
                         |     Default: True
                         | drawCountries => Draws countries. If true, draw them.
                         |     Default: True
                         | drawParellels => Draws parellels. If true, draw them.
                         |     Default: True
                         | drawMeridians => Draws countries. If true, draw them.
                         |     Default: True
        ----------------------------------------------------                  
        Returns          | Basemap object (AKA m)
        ----------------------------------------------------
        '''
        
        from mpl_toolkits.basemap import Basemap
        import numpy as np
        
        m = Basemap(projection = proj, llcrnrlat= self.botlat, urcrnrlat= self.toplat, 
                    llcrnrlon= self.leftlon, urcrnrlon= self.rightlon,
                    resolution = 'l')
                    
        if mapBackground == "ShadedRelief":
            m.shadedrelief()
        if mapBackground == "BlueMarble":
            m.bluemarble()
        if mapBackground == "ETopo":
            m.etopo()
        
        if drawCountries == True:
            m.drawcountries(linewidth=0.5)
        if drawStates == True:
            m.drawstates(linewidth=0.3) 
        if drawCoastlines == True:
            m.drawcoastlines(linewidth=0.5)
        
        if drawParellels == True:
            m.drawparallels(np.arange(-90, 90, 10), linewidth = 0.2, 
                        labels = [True, False, True, False], fontsize = 'x-small')
        if drawMeridians == True:
            m.drawmeridians(np.arange(-180, 180, 10), linewidth = 0.2, 
                        labels = [False, False, False, True], fontsize = 'x-small')
        
        return m
    
    def getZipFiles(savePath, url,  deleteTree = False):  
        '''
        Grabs zip files and unzips in specified path
        ----------------------------------------------------
        Required Inputs | dirPath => path to directory to save zip files
        Description     | zipFileURL => the url to the zip file.
        ----------------------------------------------------
        Returns         | None
        ----------------------------------------------------
        '''  
        
        import requests, zipfile, io
        import shutil, os
    
        if deleteTree == True:
            shutil.rmtree(savePath)
            os.mkdir(savePath)
        
        url = url + ".zip"
        
        r = requests.get(url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(savePath)
     
    def write_text(x, y, text, halign, valign, fontsize = 'x-small', color = 'k',
                bbox = False, outline = False):
        ''' 
        Writes text to the graph.
        ----------------------------------------------------
        Required Inputs  | x => position on the x axis
                         | y => position on the y axis
                         | text => the text you want to display
                         | halign => horizontal alignment
                         | valign => veritcal alignment
        ----------------------------------------------------
        Optional Inputs  | fontsize => the size of the font
                         |      Default: x-small
                         | color => the color of the text                         
                         |      Default: black
                         | bbox => When True, put a white bounding box around the text.
                         |      Default: False
                         | outline => If true, outline the text with black.
                         |      Default: False
        ----------------------------------------------------
        Returns          | None
        ----------------------------------------------------
        '''
        import matplotlib.patheffects as path_effects
        ax = plt.gca()
        
        if bbox is True:
            bbox_props = dict(boxstyle="square,pad=0.3", fc="white", 
                ec="black", lw=1)
            ax.text(x, y, text, horizontalalignment = halign, 
                verticalalignment = valign, transform=ax.transAxes, 
                fontsize = fontsize, color = color, bbox = bbox_props,
                fontname = fontfamily)
        elif outline is True:
            if color == 'k' or color == 'black':
                color = 'white'
            
            text = ax.text(x, y, text, horizontalalignment = halign, 
                verticalalignment = valign, transform=ax.transAxes, 
                fontsize = fontsize, color = color, fontname = fontfamily)
            text.set_path_effects([path_effects.Stroke(linewidth=0.5, 
                foreground='black'), path_effects.Normal()])
        else:
            ax.text(x, y, text, horizontalalignment = halign, 
                verticalalignment = valign, transform=ax.transAxes, 
                fontsize = fontsize, color = color, fontname = fontfamily)

        
        