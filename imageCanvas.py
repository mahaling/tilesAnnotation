
import cv2
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
#from matplotlib.Artist import artist
from matplotlib.mlab import dist_point_to_segment
#from matplotlib.line import Lines2D

class Polygon():
    self.coords = []
    self.start_point = ()
    self.end_point = ()
    self.roicolor = 'r'

class imageCanvas():
    def __init__(self,image,bounds):
        self.fname = image
        self.img = cv2.imread(self.fname)
        self.img_width = self.img.shape[1]
        self.img_height = self.img.shape[0]
        self.bounds = bounds
        print self.img.shape
        self.point = ()
        self.polygon = []
        self.newPoly = Polygon()


        # all variables that are required for polygon
        self.previous_point = []
        self.line = None


    def getCoord(self):
        self.fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_title(self.fname)
        plt.imshow(self.img)
        cid = fig.canvas.mpl_connect('button_press_event', self.__onclick__)
        plt.show()
        return self.point

    def __onclick__(self,click):
        self.point = (click.xdata,click.ydata)
        print self.point
        return self.point

    def __button_press_callback(self,event):
        if event.inaxes:
            x,y = evet.xdata,event.ydata
            ax = event.inaxes
            if event.button == 1 and event.dblclick == False: # pressed the left button and it is a single click
                if self.line == None: # if there is no line, create a line
                    self.line = plt.Line2D([x,x], [y,y], marker='o', color=self.roicolor)
                    self.previous_point = [x,y]
                    self.newPoly.coords.append([x,y])
                    self.newPoly.start_point = (x,y)
                    ax.add_line(self.line)
                    self.fig.canvas.draw()
                else: # if there is a line, then create a line segment (the polygon is already initialized)
                    self.line = plt.Line2D([self.previous_point[0], x],
                                           [self.previous_point[1], y],
                                           marker='o', color=newPoly.roicolor)
                    self.previous_point = [x,y]
                    self.newPoly.coords.append([x,y])
                    event.inaxes.add_line(self.line)
                    self.fig.canvas.draw()
            elif ((event.button == 1 and even.dblclick == True) or
                  (event.button == 3 and event.dblclick == False)) and self.line != None:
                  # add the polgon to the list of polygons
                  # complete the line connecting the start and the end point
                  # display the image
                  self.line.set_data([])

    def convertPolygonPointsToWorld(self):
        bounds_width = self.bounds['maxX'] - self.bounds['minX']
        bounds_height = self.bounds['maxY'] - self.bounds['minY']

        # compute the scale between downscaled and original section
        scale = self.img_width*1.0/bounds_width

        # check if polygon points have been chosen
        coords = [[]]
        if self.polygon:
            for x,y in self.polygon:
                # convert the points to world coordinates
                x = (x/scale) + bounds['minX']
                y = (y/scale) + bounds['minY']
                coords[0].append([x,y])
        return coords
