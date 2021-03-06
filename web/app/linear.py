import numpy as np
import math
from PIL import Image, ImageDraw
import random

class Line:
    a=0.0
    b=0.0
    c=0.0
    d=0.0
    n=0.0
    xmn=999
    xmx=-xmn
    ymn =999
    ymx = -ymn

    def y(self,x):
        y= self.a*x+self.b
        return y
    
    def distance(self,x,y):
        xl = (self.a*(y-self.b) + x)/(1+self.a*self.a)
        yl = self.y(xl)
        dx = x - xl
        dy = y - yl
        d = math.sqrt(dx*dx+dy*dy)
        return d
    
    def init(self):
        dx = self.xmx-self.xmn
        dy = self.ymx-self.ymn
        a = 0.0
        if dx!=0.0:
            a = dy/dx
        b = self.ymn-a*self.xmn
        self.a = a
        self.b = b
        self.n = 2

    def intersect(self,l,th):
        result = False
        sp = 0
        lp = 0
        x = 99999.9
        y = 99999.9
        da = self.a - l.a
        if da!=0:
            db = self.b - l.b
            x=-db/da
            y=self.y(x)

            dx = self.xmn - x
            dy = self.ymn - y
            ds = math.sqrt(dx*dx+dy*dy)
            if ds < th:
               sp = 1
            else:
                dx = self.xmx - x
                dy = self.ymx - y
                ds = math.sqrt(dx*dx+dy*dy)
                if ds < th:
                    sp =2

            dx = l.xmn - x
            dy = l.ymn - y
            ds = math.sqrt(dx*dx+dy*dy)
            if ds < th:
               lp = 1
            else:
                dx = l.xmx - x
                dy = l.ymx - y
                ds = math.sqrt(dx*dx+dy*dy)
                if ds < th:
                    lp =2  

            if sp > 0 and lp >0:
                result = True
        
        return result,sp,lp,x,y

    def near(self, l, th):
        xmn = (self.a*(l.ymn-self.b) + l.xmn)/(1+self.a*self.a)
        xmx = (self.a*(l.ymx-self.b) + l.xmx)/(1+self.a*self.a)
        ds = 0.0
        if xmn > self.xmx:
            dx = self.xmx - l.xmn
            dy = self.ymx - l.ymn
            ds = math.sqrt(dx*dx + dy*dy)
        elif  xmx < self.xmn:
            dx = self.xmn - l.xmx
            dy = self.ymn - l.ymx
            ds = math.sqrt(dx*dx + dy*dy)
        if ds < th:
            return True
        return False

    def aligned(self, l, th):
        dn = self.distance(l.xmn, l.ymn)
        dx = self.distance(l.xmx, l.ymx)
        if dn<th and dx<th:
            return True
        return False

    def merge(self, l):
        self.a = (self.n * self.a + l.n * l.a)/(self.n + l.n)
        self.b = (self.n * self.b + l.n * l.b)/(self.n + l.n)
        self.n = self.n + l.n

        if self.xmn > l.xmn:
            self.xmn = l.xmn
        if self.xmx < l.xmx:
            self.xmx = l.xmx
        
        self.ymn = self.xmn * self.a + self.b
        self.ymx = self.xmx * self.a + self.b

    def __str__(self):
       return  'a={:f} b={:f} c={:f} d={:f} n={} x=({:f},{:f}) y=({:f},{:f})'.format(self.a, self.b,self.c,self.d,self.n, self.xmn,self.xmx,self.ymn,self.ymx)

    def graph(self, draw, frame, dx, dy):
        points =[]
        sx = dx/(frame.xmx - frame.xmn)
        sy= dy/(frame.ymx - frame.ymn)

        x = (self.xmn-frame.xmn)*sx
        y = (self.y(self.xmn) - frame.ymn)*sy
        points.append((x,y))

        x = (self.xmx-frame.xmn)*sx
        y = (self.y(self.xmx) - frame.ymn)*sy
        points.append((x,y))        

        draw.line(points, fill="blue", width=3)

def segments(x,y,r,n,frame):
    dx = (frame.xmx-frame.xmn)/n
    dy = (frame.ymx-frame.ymn)/n

    s=[]
    t=np.zeros(n*n,dtype=int)
    for i in range(0,len(x)):
        if dx>0 and r[i]==-1:
            px = int((x[i]-frame.xmn)/dx)
            py = int((y[i]-frame.ymn)/dy)
            k = px*(n-1)+py
            #print(px,py,n,k)
            t[k] = t[k]+1
            s.append(k)
        else:
            s.append(-1)
    return s,t

def setall(x,y,r,k):
    cnt = 0
    for i in range(0,len(x)):
        if r[i]==-1:
           r[i] = k
           cnt = cnt + 1
    return cnt

def remove(x,y,r,k,line,d):
    cnt = 0
    for i in range(0,len(x)):
        if r[i]==k and line.distance(x[i],y[i])>d:
           r[i] = -1
           cnt = cnt + 1
    return cnt

def add(x,y,r,k,line,d):
    cnt = 0
    for i in range(0,len(x)):
        if r[i]==-1 and line.distance(x[i],y[i])<=d:
           r[i] = k
           cnt = cnt + 1
    return cnt

def regression(x,y,r,k):
    sxy = 0.0
    sx2 = 0.0
    sy2 = 0.0
    sx = 0.0
    sy = 0.0
    m = len(x)
    n = 0
    line = Line()
    for i in range(0,m):
        if r[i]==k:
            sx = sx + x[i]
            sy = sy + y[i]
            sx2 = sx2 + x[i]*x[i]
            sy2 = sy2 + y[i]*y[i]
            sxy = sxy + x[i]*y[i] 
            n= n + 1

    ex2 = n * sx2 - sx * sx
    ey2 = n * sy2 - sy * sy
    et2 = n * sxy - sx * sy

    if n==0 or ex2 ==0 or ey2 == 0:
        return line

    line.a = et2 / ex2
    line.b = (sy - line.a * sx)/n
    line.c = et2 / ey2
    line.d = line.a * line.c + n/m
    line.n = n

    return line

def find_lines(x,y,max,nseg,band,dbg=False):
    frame = Line()
    r = []
    for i in range(0,len(x)):
        r.append(-1)
        if frame.xmn>=x[i]:
            frame.xmn=x[i]
        if frame.xmx<=x[i]:
            frame.xmx=x[i]
        if frame.ymn>=y[i]:
            frame.ymn=y[i]
        if frame.ymx<=y[i]:
            frame.ymx=y[i]

    n = 2
    l = 0
    lines=[]
    while len(lines)<max and n >=2:
        s,t = segments(x,y,r,nseg,frame)
        if dbg:
            print(s,t)
        line = Line()
        line.d=-999
        for i in range(0,len(t)):
            if t[i]>2:
                rline= regression(x,y,s,i)
                if dbg:
                    print("S",str(rline))
                if rline.n > 0 and line.d <= rline.d:
                    line = rline

        dx = band
        n = line.n
        if n>2:
            if dbg:
                print("F",str(line))
            while dx > 0.2*band:
                chg = 0.0
                if add(x,y,r,l,line,dx) > 0:
                    aline = regression(x,y,r,l)
                    if dbg:
                        print(aline)
                    remove(x,y,r,l,aline,0.5*dx)
                    cline = regression(x,y,r,l)
                    if dbg:
                        print(cline)
                    add(x,y,r,l,cline,0.3*dx)
                    nline= regression(x,y,r,l)
                    if dbg:
                        print(nline)
                    chg = abs(nline.d-aline.d)
                if chg<0.01:
                    dx = 0.0
                else:
                    dx = dx * 0.5
                line=nline

            if line.n == 0:
                break
            
            for i in range(0,len(x)):
                if r[i]==l:
                    s[i]=-1
                    if line.xmn>=x[i]:
                        line.xmn=x[i]
                    if line.xmx<=x[i]:
                        line.xmx=x[i]
                    if line.ymn>=y[i]:
                        line.ymn=y[i]
                    if line.ymx<=y[i]:
                        line.ymx=y[i]
            print(str(line))
            lines.append(line)
            l = l + 1
    return frame, lines, r

def graphPoints(x, y, r, draw, frame, dx, dy, dr):
    sx = dx/(frame.xmx - frame.xmn)
    sy= dy/(frame.ymx - frame.ymn)

    for i in range(0,len(x)):
        xp = (x[i] - frame.xmn)*sx
        yp = (y[i] - frame.ymn)*sy 
        #print(xp,yp)    
        draw.point((xp,yp), fill=300)
        draw.ellipse(((xp-dr,yp-dr),(xp+dr,yp+dr)),fill =300, outline="red")

def test():
    x=[]
    y=[]
    r=[]
    q = 0.3
    for i in range(0,10):
        xp = 1+i*0.2-q*(0.5-random.random())
        yp = 1.5*xp-3.2-q*(0.5-random.random())
        x.append(xp)
        y.append(yp)

    for i in range(0,10):
        xp = 0.5+i*0.3-q*(0.5-random.random())
        yp = -0.5*xp+2.1-q*(0.5-random.random())
        x.append(xp)
        y.append(yp)

    frame, lines, r =find_lines(x,y,5,2,3)    
    for line in lines:
        print(line) 
    print(r)

    im= Image.new("RGB", (648, 648), "#FFFFFF")
    draw = ImageDraw.Draw(im)
    for line in lines:
        line.graph(draw, frame, 648, 648)

    graphPoints(x,y,r,draw,frame,648,648,3)

    filename = "linear.jpg"
    try:
        im.save(filename, "PNG")
    except IOError:
        print("cannot save", filename)

test()