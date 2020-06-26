import numpy as np
import cv2
import math
from linear import find_lines, graphPoints
from PIL import Image, ImageDraw
import time

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

curt = time.time()

img = cv2.imread("note.jpg")
curt = logt("read",curt)

gray = img[:,:,0]
curt = logt("gray",curt)

edges = cv2.Canny(gray,50,150,apertureSize = 3) 
curt = logt("edges",curt)

lines = cv2.HoughLines(edges,1,np.pi/180, 250) 
curt = logt("lines",curt)

n,m = img.shape[:2]
print(n,m)

im= img.copy()
for line in lines:
    for r,theta in line: 
        a = np.cos(theta) 
        b = np.sin(theta) 
        x0 = a*r 
        y0 = b*r 
        x1 = int(x0 + n*(-b)) 
        y1 = int(y0 + n*(a)) 
        x2 = int(x0 - n*(-b)) 
        y2 = int(y0 - n*(a)) 
        cv2.line(im, (x1,y1), (x2,y2),(0,0,0),3) 

curt = logt("graph",curt)

filename = "note-lines.jpg"
try:
    cv2.imwrite(filename, im)
except IOError:
    print("cannot save", filename)

curt = logt("save",curt)
