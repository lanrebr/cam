import numpy as np
import cv2
import math
from linear import Line,find_lines, graphPoints
from PIL import Image, ImageDraw
import time
from bentley_ottmann.planar import segments_intersections

def get_canny(image,sigma=0.33):
    v = np.median(image)
    lower = int(max(0,1.0-sigma) * v)
    upper = int(min(255, (1.0+sigma) * v))
    edge = cv2.Canny(image, lower,upper)
    return edge

def logt(msg, prvt):
    curt = time.time()
    print(msg +": %s s" % (curt- prvt))
    return curt

def glines(img):

    gray = img[:,:,0]
    edges = cv2.Canny(gray,50,150,apertureSize = 3) 

    rho = 0.5  # distance resolution
    theta = np.pi / 180  # angular resolution
    thres = 50  # minimum number of votes
    min_length = 10  # minimum number of pixels
    max_gap = 40  # maximum gap between line segments

    hlines = cv2.HoughLinesP(edges, rho, theta, thres, np.array([]), min_length, max_gap)

    lines = []
    for hline in hlines:
        for x1,y1,x2,y2 in hline:
            l = Line()
            if x1 < x2:
                l.xmn = x1
                l.xmx = x2
                l.ymn = y1
                l.ymx = y2
            else:
                l.xmn = x2
                l.xmx = x1
                l.ymn = y2
                l.ymx = y1          
            l.init()
            found = False
            for line in lines:
                if l.aligned(line,22) and l.near(line,80):
                    line.merge(l)
                    found = True
                    break
            if not found:
                lines.append(l)
    
    
    return lines

curt = time.time()
tott = curt

img = cv2.imread("note.jpg")
curt = logt("read",curt)

lines = glines(img)
curt = logt("lines",curt)

print(len(lines))
im= img.copy()
curt = logt("copy-image",curt)

for line in lines:
    cv2.line(im,(int(line.xmn),int(line.ymn)),(int(line.xmx),int(line.ymx)),(155,0,0),2)

for line in lines:
    for i in range(-1,1):
        for j in range(-1,1):
            im[int(line.ymn) + i, int(line.xmn) + j] = [0, 255, 0]
            im[int(line.ymx) + i, int(line.xmx) + j] = [0, 255, 0]

curt = logt("graph",curt)

filename = "note-lines.jpg"
try:
    cv2.imwrite(filename, im)
except IOError:
    print("cannot save", filename)

curt = logt("save",curt)
tott = logt("total",tott)
