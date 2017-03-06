
import cv2
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
#from matplotlib.Artist import artist
from matplotlib.mlab import dist_point_to_segment
#from matplotlib.line import Lines2D

class Polygon():
    def __init__(self):
        self.coords = []
        self.worldCoords = []
        self.start_point = ()
        self.end_point = ()
        self.roicolor = 'r'

class imageCanvas():
    def __init__(self,image):
        self.fname = image
        self.img = cv2.imread(self.fname)
        self.img_width = self.img.shape[1]
        self.img_height = self.img.shape[0]
        #self.bounds = bounds
        print self.img.shape
        self.point = ()
        self.polygon = []
        self.newPoly = Polygon()

        # all variables that are required for polygon
        self.previous_point = []
        self.line = None

    def showImage(self):
        self.fig = plt.figure()
        ax = self.fig.add_subplot(111)
        ax.set_title(self.fname)
        plt.imshow(self.img)
        self.__ID1 = self.fig.canvas.mpl_connect('motion_notify_event',self.__motion_notify_callback)
        self.__ID2 = self.fig.canvas.mpl_connect('button_press_event',self.__button_press_callback)
        self.__ID3 = self.fig.canvas.mpl_connect('close_event',self.__handle_close)
        plt.show()

    def getCoord(self):
        self.fig = plt.figure()
        ax = self.fig.add_subplot(111)
        ax.set_title(self.fname)
        plt.imshow(self.img)
        cid = self.fig.canvas.mpl_connect('button_press_event', self.__onclick__)
        plt.show()
        return self.point

    def __onclick__(self,click):
        self.point = (click.xdata,click.ydata)
        print self.point
        return self.point

    def __motion_notify_callback(self,event):
        if event.inaxes:
            ax = event.inaxes
            x,y = event.xdata, event.ydata
            if (event.button == None or event.button == 1) and self.line != None:
                self.line.set_data([self.previous_point[0],x],
                                    [self.previous_point[1],y])
                self.fig.canvas.draw()

    def __button_press_callback(self,event):
        if event.inaxes:
            x,y = event.xdata,event.ydata
            ax = event.inaxes
            if event.button == 1 and event.dblclick == False: # pressed the left button and it is a single click
                if self.line == None: # if there is no line, create a line
                    self.newPoly = Polygon()
                    self.line = plt.Line2D([x,x], [y,y], marker='o', color=self.newPoly.roicolor)
                    self.previous_point = [x,y]
                    self.newPoly.coords.append([x,y])
                    self.newPoly.start_point = (x,y)
                    ax.add_line(self.line)
                    self.fig.canvas.draw()
                else: # if there is a line, then create a line segment (the polygon is already initialized)
                    self.line = plt.Line2D([self.previous_point[0], x],
                                           [self.previous_point[1], y],
                                           marker='o', color=self.newPoly.roicolor)
                    self.previous_point = [x,y]
                    self.newPoly.coords.append([x,y])
                    event.inaxes.add_line(self.line)
                    self.fig.canvas.draw()
            elif ((event.button == 1 and even.dblclick == True) or
                  (event.button == 3 and event.dblclick == False)) and self.line != None:
                  # add the polgon to the list of polygons
                  # complete the line connecting the start and the end point
                  # display the image
                  self.line.set_data([self.previous_point[0],
                                      self.newPoly.start_point[0]],
                                     [self.previous_point[1],
                                      self.newPoly.start_point[1]])
                  ax.add_line(self.line)
                  self.fig.canvas.draw()
                  self.line = None
                  self.newPoly.end_point = self.previous_point
                  # you can either opt to append the first point again at the end of newPoly.coords or just leave it
                  self.polygon.append(self.newPoly)

    def __handle_close(self,event):
        print('Closed figure!')
        print self.polygon

    def convertPolygonPointsToWorld(self,stackBounds):
        bounds_width = stackBounds['maxX'] - stackBounds['minX']
        bounds_height = stackBounds['maxY'] - stackBounds['minY']

        # compute the scale between downscaled and original section
        scale = self.img_width*1.0/bounds_width

        # check if polygon points have been chosen
        coords = [[]]
        if len(self.polygon) > 0:
            #for i in xrange(0,len(self.polygon)-1):
            #    for j in xrange(0,len(self.polygon[i].coords)-1):
            for i,poly in enumerate(self.polygon):
                for x,y in poly:
                    # convert the points to world coordinates
                    x = (x/scale) + bounds['minX']
                    y = (y/scale) + bounds['minY']
                    self.polygon[i].worldCoords.append([x,y])
        
