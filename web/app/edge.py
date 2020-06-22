import numpy as np
import cv2
import math

def get_canny(image,sigma=0.33):
    v = np.median(image)
    lower = int(max(0,1.0-sigma) * v)
    upper = int(min(255, (1.0+sigma) * v))
    edge = cv2.Canny(image, lower,upper)
    return edge


image = cv2.imread("note.jpg")
#gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#blurred = cv2.GaussianBlur(gray, (3, 3), 0)
b,g,r = cv2.split(image)
be = cv2.Canny(b, 50, 200,8)
ge = cv2.Canny(b, 50, 200,8)
re = cv2.Canny(b, 50, 200,8)
rc = np.maximum(be,ge,re)
cv2.imwrite("note-b.jpg",b)
cv2.imwrite("note-g.jpg",g)
cv2.imwrite("note-r.jpg",r)
cv2.imwrite("note-combined.jpg",rc)

