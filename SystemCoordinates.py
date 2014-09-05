import math

class Point2d():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def length(self):
        return math.sqrt(self.x*self.x+self.y*self.y)

    def angle(self):
        return math.atan2(self.y,self.x)

    def add(self, point):
        return Point2d(self.x+point.x,self.y+point.y)

    def sub(self, point):
        return Point2d(self.x-point.x,self.y-point.y)

    def multiply(self, point):
        return self.x*point.x + self.y*point.y

    def constantMultiply(self, constant):
        return Point2d(self.x*constant,self.y*constant)

    def printPoint(self):
        print('x=',self.x,'y=',self.y)


class TransformCoord2d():
    def __init__(self, old1, old2, old3, new1, new2, new3):
        det = old1.x*old2.y - old1.y*old2.x - old1.x*old3.y + old1.y*old3.x + old2.x*old3.y - old2.y*old3.x
        l1x = (old2.y-old3.y)*new1.x + (old3.y - old1.y)*new2.x + (old1.y-old2.y)*new3.x
        l1y = (old2.y-old3.y)*new1.y + (old3.y - old1.y)*new2.y + (old1.y-old2.y)*new3.y
        l2x = (old3.x-old2.x)*new1.x + (old1.x - old3.x)*new2.x + (old2.x-old1.x)*new3.x
        l2y = (old3.x-old2.x)*new1.y + (old1.x - old3.x)*new2.y + (old2.x-old1.x)*new3.y
        l3x = (old2.x*old3.y - old2.y*old3.x)*new1.x + (old1.y*old3.x - old1.x*old3.y)*new2.x + (old1.x*old2.y - old1.y*old2.x)*new3.x
        l3y = (old2.x*old3.y - old2.y*old3.x)*new1.y + (old1.y*old3.x - old1.x*old3.y)*new2.y + (old1.x*old2.y - old1.y*old2.x)*new3.y
        self.alpha = 1.*l1x/det
        self.beta = 1.*l2x/det
        self.dx = 1.*l3x/det
        self.gamma = 1.*l1y/det
        self.delta = 1.*l2y/det
        self.dy = 1.*l3y/det
        
    def transform(self, point):
        x = point.x*self.alpha+point.y*self.beta+self.dx
        y = point.x*self.gamma+point.y*self.delta+self.dy
        return Point2d(x,y)
