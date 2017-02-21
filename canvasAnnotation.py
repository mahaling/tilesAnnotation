
import cv2
import matplotlib.pyplot as plt

class Canvas():
    def __init__(self,image):
        self.fname = image
        self.img = cv2.imread(self.fname)
        self.img_width = self.img.shape[1]
        self.img_height = self.img_shape[0]
        self.point = ()
        self.polygon = []

    def getCoord(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.imshow(self.img)
        cid = fig.canvas.mpl_connect('button_press_event', self.__onclick__)
        plt.show()
        return self.point

    def __onclick__(self,click):
        self.point = (click.xdata,click.ydata)
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
                x = (x/scale) + bounds['minX']
                y = (y/scale) + bounds['minY']
                coords[0].append([x,y])
