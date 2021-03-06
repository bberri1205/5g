from display import *
from matrix import *


def add_circle( points, cx, cy, cz, r, step ):
    t = step
    x_p = cx+r*math.cos(0)
    y_p = cy+r*math.sin(0)
    while t <= 1+step:
        theta = (t)*2*math.pi
        x = cx+r*math.cos(theta)
        y = cy+r*math.sin(theta)
        z = 0
        add_edge(points, x_p, y_p, z, x, y, z)
        x_p = x
        y_p = y
        t += step
def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):
    if curve_type == 'hermite':
        add_hermite_curve(points,x0,y0,x1,y1,x2,y2,x3,y3,step)
    if curve_type == 'bezier':
        add_bezier_curve(points,x0,y0,x1,y1,x2,y2,x3,y3,step)

'''
hermite: adds a hermite curve to the edge matrix - takes 8 parameters (x0, y0, x1, y1, rx0, ry0, rx1, ry1)
The curve is between points (x0, y0) and (x1, y1).
(rx0, ry0) and (rx1, ry1) are the rates of change at each endpoint
'''
def add_hermite_curve( points, x0, y0, x1, y1, rx0, ry0, rx1, ry1, step ):
    x_p = x0
    y_p = y0
    x_co = generate_curve_coefs( x0, x1, rx0, rx1, 'hermite' )
    y_co = generate_curve_coefs( y0, y1, ry0, ry1, 'hermite' )
    t = step
    while t <= 1+step:
        x = x_co[0]*(t**3)+x_co[1]*(t**2)+x_co[2]*(t)+x_co[3]
        y = y_co[0]*(t**3)+y_co[1]*(t**2)+y_co[2]*(t)+y_co[3]
        z = 0
        add_edge(points, x_p, y_p, z, x, y, z)
        x_p = x
        y_p = y
        t += step
'''
bezier: adds a bezier curve to the edge matrix - takes 8 parameters (x0, y0, x1, y1, x2, y2, x3, y3)
This curve is drawn between (x0, y0) and (x3, y3)
(x1, y1) and (x2, y2) are the control points for the curve.
'''
def add_bezier_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step ):
    x_co = generate_curve_coefs( x0, x1, x2, x3, 'bezier' )
    y_co = generate_curve_coefs( y0, y1, y2, y3, 'bezier' )
    x_p = x0
    y_p = y0
    t = step
    while t <= 1+step:
        x = x_co[0]*(t**3)+x_co[1]*(t**2)+x_co[2]*(t)+x_co[3]
        y = y_co[0]*(t**3)+y_co[1]*(t**2)+y_co[2]*(t)+y_co[3]
        z = 0
        add_edge(points, x_p, y_p, z, x, y, z)
        x_p = x
        y_p = y
        t += step



def draw_lines( matrix, screen, color ):
    if len(matrix) < 2:
        print 'Need at least 2 points to draw'
        return
    
    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   screen, color)    
        point+= 2
        
def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)
    
def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )
    



def draw_line( x0, y0, x1, y1, screen, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        x0 = x1
        y0 = y1
        x1 = xt
        y1 = yt

    x = x0
    y = y0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)

    #octants 1 and 8
    if ( abs(x1-x0) >= abs(y1 - y0) ):

        #octant 1
        if A > 0:            
            d = A + B/2

            while x < x1:
                plot(screen, color, x, y)
                if d > 0:
                    y+= 1
                    d+= B
                x+= 1
                d+= A
            #end octant 1 while
            plot(screen, color, x1, y1)
        #end octant 1

        #octant 8
        else:
            d = A - B/2

            while x < x1:
                plot(screen, color, x, y)
                if d < 0:
                    y-= 1
                    d-= B
                x+= 1
                d+= A
            #end octant 8 while
            plot(screen, color, x1, y1)
        #end octant 8
    #end octants 1 and 8

    #octants 2 and 7
    else:
        #octant 2
        if A > 0:
            d = A/2 + B

            while y < y1:
                plot(screen, color, x, y)
                if d < 0:
                    x+= 1
                    d+= A
                y+= 1
                d+= B
            #end octant 2 while
            plot(screen, color, x1, y1)
        #end octant 2

        #octant 7
        else:
            d = A/2 - B;

            while y > y1:
                plot(screen, color, x, y)
                if d > 0:
                    x+= 1
                    d+= A
                y-= 1
                d-= B
            #end octant 7 while
            plot(screen, color, x1, y1)
        #end octant 7
    #end octants 2 and 7
#end draw_line
