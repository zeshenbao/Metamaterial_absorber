from math import *
from turtle import *


tile_height = 3
tile_len = 1
tile_wid = tile_len
angle = (pi/6)/2



h = tile_height/2
w = h*tan(angle)

k = 1/tan(2*angle)
a = tile_len - 2*w
s = a*cos(2*angle)

dx = s*cos(2*angle)
dy = s*sin(2*angle)


xa_1 = (s+dy)/(2*k)
xa_2 = (s+dy)/(2*k)+dx
ya_1 = (s+dy)/2
ya_2 = (s-dy)/2

xa = (xa_1+xa_2)/2
ya = (ya_1+ya_2)/2

c1 = xa
c2 = a - c1

scale = 500

def y1(x1):
    return k*x1

def y2(x2):
    return k*(x2-a)

def line(p1, p2):
    pu()
    goto(p1[0]*scale, p1[1]*scale)
    pd()
    goto(p2[0]*scale, p2[1]*scale)

def dot(p, d=2):
    r = d/2
    pu()
    goto(p[0]*scale,p[1]*scale-r)
    pd()
    begin_fill()
    circle(r)
    end_fill()

def fill(pts):
    pu()
    goto(pts[0][0]*scale, pts[0][1]*scale)
    pd()
    begin_fill()
    for p in pts:
        goto(p[0]*scale, p[1]*scale)
    end_fill()
    
        
        
        



speed(0)
ht()
#left line
color("blue")
line((0,0), (a,y1(a)))

#ground line
color("black")
line((0,0), (a,y2(a)))

#right line
color("red")
line((a,y2(a)), (2*a, y2(2*a)))


#circle
color("gray")
dot((xa, ya), s*scale)

"""
#area to add
color("green")
pts1 = [(0,0),
        (xa,0),
        (xa,ya),
        (xa_1, ya_1)]
fill(pts1)

color("blue")
pts2 = [(xa,0),
        (a,0),
        (xa_2,ya_2),
        (xa,ya)]
fill(pts2)
"""


#s line
color("orange")
line((xa_1,ya_1), (xa_2,ya_2))

#s dots
color("purple")
dot((xa_1, ya_1))
dot((xa_2, ya_2))
color("green")
dot((xa, ya))

#c dots
color("yellow")
dot((xa,0))






