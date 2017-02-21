
import cv2
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
#from matplotlib.Artist import artist
from matplotlib.mlab import dist_point_to_segment
#from matplotlib.line import Lines2D

class imageCanvas():
    def __init__(self,image):
        self.fname = image
        self.img = cv2.imread(self.fname)
        self.img_width = self.img.shape[1]
        self.img_height = self.img.shape[0]
        print self.img.shape
        self.point = ()
        self.polygon = []

    def initFigure(self):
        if self.img:
            self.fig = plt.figure(figsize=(1,1))
            self.ax = fig.add_subplot(111)
            plt.imshow(self.img)
            self.cid = self.fig.canvas.mpl_connect()


    def getCoord(self):
        fig = plt.figure()
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

    def convertPolygonPointsToWorld(self,bounds):
        bounds_width = bounds['maxX'] - bounds['minX']
        bounds_height = bounds['maxY'] - bounds['minY']

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
