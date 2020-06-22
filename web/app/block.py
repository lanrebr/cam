from PIL import Image, ImageDraw

class Point:
    x = 0.0
    y = 0.0
    z = 0.0

    def __init__(self,x=0,y=0,z=0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self)->str:
        return "{x:"+str(self.x)+", y:"+str(self.y)+", z:"+str(self.z)+"}"

    def dot(self, p:'Point')->float:
        return self.x*p.x+self.y*p.y+self.z*p.z

    def scale(self, coef)->'Point':
        return Point(coef*self.x, coef*self.y, coef*self.z)
    
    def plus(self,p:'Point')->'Point':
        return Point(self.x+p.x,self.y+p.y,self.z+p.z)

    def minus(self,p:'Point')->'Point':
        return Point(self.x-p.x,self.y-p.y,self.z-p.z)

    def dim2(self)->float:
        return self.dot(self)
    
class Block:
    beg = Point(0,0,0)
    end = Point(0,0,0)

    def __init__(self, beg, end):
        self.beg = beg
        self.end = end

    def __str__(self)->str:
        return "{beg:"+str(self.beg)+", end:"+str(self.end)+"}"

    def paths(self)->list:
        paths = []

        points = []
        points.append(Point(self.beg.x, self.beg.y, self.beg.z))
        points.append(Point(self.end.x, self.beg.y, self.beg.z))
        points.append(Point(self.end.x, self.end.y, self.beg.z))
        points.append(Point(self.beg.x, self.end.y, self.beg.z))
        points.append(Point(self.beg.x, self.beg.y, self.beg.z))
        paths.append(points)

        points = []
        points.append(Point(self.beg.x, self.beg.y, self.end.z))
        points.append(Point(self.end.x, self.beg.y, self.end.z))
        points.append(Point(self.end.x, self.end.y, self.end.z))
        points.append(Point(self.beg.x, self.end.y, self.end.z))
        points.append(Point(self.beg.x, self.beg.y, self.end.z))
        paths.append(points)

        points = []
        points.append(Point(self.beg.x, self.beg.y, self.beg.z))
        points.append(Point(self.beg.x, self.beg.y, self.end.z))
        paths.append(points)

        points = []
        points.append(Point(self.beg.x, self.end.y, self.beg.z))
        points.append(Point(self.beg.x, self.end.y, self.end.z))
        paths.append(points)

        points = []
        points.append(Point(self.end.x, self.beg.y, self.beg.z))
        points.append(Point(self.end.x, self.beg.y, self.end.z))
        paths.append(points)

        points = []
        points.append(Point(self.end.x, self.end.y, self.beg.z))
        points.append(Point(self.end.x, self.end.y, self.end.z))
        paths.append(points)

        return paths

    def proj(self, cam:Point)->list:
        c2 = cam.dim2()
        paths = []
        for path in self.paths():
            points = []
            for point in path:
                coef = c2/cam.dot(point)
                p = point.scale(coef).minus(cam)
                points.append((p.x, p.y))
            paths.append(points)
        return paths

    def draw(self, cam, draw):
        for points in self.proj(cam):
            draw.line(points, fill=0)

cam = Point(110,130,330)

beg =Point(220,240,250)
end = Point(340,310,320)
blk = Block(beg,end)

im= Image.new("RGB", (648, 648), "#FFFFFF")
draw = ImageDraw.Draw(im)

blk.draw(cam,draw)

filename = "test.jpg"
try:
    im.save(filename, "PNG")
except IOError:
    print("cannot save", filename)