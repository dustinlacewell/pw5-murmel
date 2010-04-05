#!/usr/bin/env python
#
#
#
#
#

"""
#TODO: documentation!
"""

__author__ = "$Author: dlacewell $"
__version__ = "$Revision: 100 $"
__date__ = "$Date: 2007-09-07 00:40:20 -0500 (Fri, 07 Sep 2007) $"
__license__ = "see readme.txt"
__copyright__ = "DR0ID (c) 2006-2007"
__url__ = "http://dr0id.ch.vu"
__email__ = "dr0id@bluewin.ch"


import pygame
from math import hypot
from math import cos
from math import sin
from math import atan2
from math import radians
from math import sqrt

collision_function_map = {} # {(type1, type2): function(spr1, spr2)}


def register(type1, type2, func):
    """
    adds an collision handling function to the fucntion_map
    """
    global collision_function_map
    collision_function_map[(type1, type2)] = func
    collision_function_map[(type2, type1)] = func
    
    



CIRCLE_TYPE = 0
QUAD_TYPE = 1
POLY_TYPE = 2


def collision_sqare_circle(circle, square):
    if circle.type != CIRCLE_TYPE: # switch them
        circle, square = sqare, circle
    cx, cy = circle.rect.center
    srect = square.rect
    
    #    cases:
    #     7 | 6 | 5
    #    ---+---+---
    #     8 | 9 | 4
    #    ---+---+---
    #     1 | 2 | 3

    if cx < srect.left:
        if cy < srect.top:
            # case 7
            sx, sy = srect.topleft
            dx = cx - sx
            dy = cy - sy
            d = dx*dx+dy*dy
            if d < circle.radius*circle.radius:
                factor = circle.radius/sqrt(d) - 1
                return True, (dx*factor, dy*factor)
        elif cy > srect.bottom:
            # case 1
            sx, sy = srect.bottomleft
            dx = cx - sx
            dy = cy - sy
            d = dx*dx+dy*dy
            if d < circle.radius*circle.radius:
                factor = circle.radius/sqrt(d) - 1
                return True, (dx*factor, dy*factor)
        else:
            # case 8
            if srect.left-cx < circle.radius:
                return True, (srect.left-circle.radius - cx , 0)
    elif cx > srect.right:
        if cy < srect.top:
            # case 5
            sx, sy = srect.topright
            dx = cx - sx
            dy = cy - sy
            d = dx*dx+dy*dy
            if d < circle.radius*circle.radius:
                factor = circle.radius/sqrt(d) - 1
                return True, (dx*factor, dy*factor)
        elif cy > srect.bottom:
            # case 3
            sx, sy = srect.bottomright
            dx = cx - sx
            dy = cy - sy
            d = dx*dx+dy*dy
            if d < circle.radius*circle.radius:
                factor = circle.radius/sqrt(d) - 1
                return True, (dx*factor, dy*factor)
        else:
            # case 4
            if cx-srect.right < circle.radius:
                return True, (circle.radius - cx + srect.right, 0)
    else:
        if cy < srect.top:
            # case 6
            if srect.top-cy < circle.radius:
                return True, (0, srect.top-circle.radius - cy)
        elif cy > srect.bottom:
            # case 2
            if cy-srect.bottom < circle.radius:
                return True, (0, circle.radius - cy + srect.bottom)
        else:
            # case 9
            sx, sy = srect.center
            if cx > sx: # right
                if cy > sy: # bottom right
                    if srect.right - cx < srect.bottom - cy:
                        return True, (srect.right - cx + circle.radius, 0)
                    else:
                        return True, (0, srect.bottom - cy + circle.radius)
                else: # top right
                    if srect.right - cx < cy - srect.top:
                        return True, (srect.right - cx + circle.radius, 0)
                    else:
                        return True, (0, srect.top - cy - circle.radius)
            else: # left
                if cy > sy: # bottom left
                    if cx - srect.left < srect.bottom - cy:
                        return True, (srect.left - cx - circle.radius, 0)
                    else:
                        return True, (0, srect.bottom - cy + circle.radius)
                else: # top left
                    if cx - srect.left < cy - srect.top:
                        return True, (srect.left - cx - circle.radius, 0)
                    else:
                        return True, (0, srect.top - cy - circle.radius)
                
                
    return False, None
    
# first implementation, not accurate for left, right
##def collision_sqare_circle(circle, square):
##    if circle.type != CIRCLE_TYPE: # switch them
##        circle, square = sqare, circle
##        
##    cx, cy = circle.rect.center
##    radius = circle.radius
##    Cmaxx = cx + radius
##    Cminx = cx - radius
##    Cmaxy = cy + radius
##    Cminy = cy - radius
##    srect = square.rect
##    if Cmaxy < srect.top or Cminy > srect.bottom:
##        return False, None # no collision
##    if Cminx > srect.right or Cmaxx < srect.left:
##        return False, None
##    sx, sy = srect.center
##    
##    # find out if circle is in one of the diagonal squares
##    brx = None
##    if cx > srect.right: # right side
##        if cy > srect.bottom: # bottom right
##            brx, bry = square.rect.bottomright
##        elif cy < srect.top: # top right
##            brx, bry = square.rect.topright
##    elif cx < srect.left: # bottom left
##        if cy < srect.top:
##            brx, bry = square.rect.topleft
##        elif cy > srect.bottom:
##            brx, bry = square.rect.bottomleft
##    if brx:
##        normalx = cx-brx
##        normaly = cy-bry
##        len_normal = hypot(normalx, normaly)
##        if len_normal == 0:
##            return True, (normalx*radius, normaly*radius)
##        normalx = normalx/len_normal
##        normaly = normaly/len_normal
##        pointB = (cx-radius*normalx, cy-radius*normaly)
##        rect_factor = normalx*brx+normaly*bry
##        circle_factor = normalx*pointB[0]+normaly*pointB[1]
##        if rect_factor < circle_factor:
##            return False, None # no collision
##        
##        depth = rect_factor-circle_factor
##        return True, (normalx*depth, normaly*depth)
##    else:
###        print srect.top, srect.bottom, srect.left, srect.right, cx, cy, Cminx, Cmaxx, Cminy, Cmaxy
##        if (Cmaxy > srect.top or Cminy < srect.bottom) and \
##           (Cmaxx > srect.left or Cminx < srect.right):
##            if cx < srect.right and cx > srect.left:
##                if cy > srect.centery:
##                    return True, (0, srect.bottom - Cminy)
##                if cy < srect.centery:
##                    return True, (0, srect.top - Cmaxy)
##            if cx < srect.centerx:
##                return True, (srect.left - Cmaxx, 0)
##            if cx > srect.centerx: 
##                return True, (srect.right - Cminx, 0)
##            
##    return None, (0,0)
            
        

register(CIRCLE_TYPE, QUAD_TYPE, collision_sqare_circle)
    
def collision_circle_poly(circle, poly):
    # switch if needed
    if poly.type == CIRCLE_TYPE:
        circle, poly = poly, circle
    # find the nearest point to the circle and calucalte the axis
    # and the poinst of the circle on that axis
    cx, cy = circle.rect.center
    polyx, polyy = poly.rect.center
    mind = 999999999
    normal = None
    for px, py in poly.vertices:
        nx = px + polyx - cx
        ny = py + polyy - cy
        d = nx*nx+ny*ny
        if d < mind:
            mind = d
            normalx = nx
            normaly = ny
    len_n = sqrt(mind)
    if len_n:
        normalx /= len_n
        normaly /= len_n
    else:
        print 'WARNING: 0 length'
    # save normals
    axes = [(normalx, normaly)]
    axes += poly.normals
    push_vectors = []
    for normalx, normaly in axes:
        # project circle on axis
        cicle_center_on_axis = normalx*cx+normaly*cy
        radius = circle.radius
        minC = cicle_center_on_axis - radius
        maxC = cicle_center_on_axis + radius
        #project poly on axis
        minP = 999999999
        maxP = -99999999
        for px, py in poly.vertices:
            axis_point = (px+polyx) * normalx + (py+polyy) * normaly
            if axis_point < minP:
                minP = axis_point
##                if minP < maxC: 
##                    break
            if axis_point > maxP:
                maxP = axis_point
##                if maxP > minC: 
##                    break
        # test for collision
        if maxC < minP or minC > maxP:
            return False, None # no collision
        elif maxC > minP or minC < maxP: # if colliding get penetration depth
            depth = min(maxC-minP, maxP-minC)
            push_vectors.append((normalx*depth, normaly*depth))
    minlen = 9999999999
    minvecx = 0
    minvecy = 0
    for vx, vy in push_vectors:
        dot = vx*vx+vy*vy
##        print vx, vy, dot
        if dot<minlen:
            minlen = dot
            minvecx = vx * 1.1
            minvecy = vy * 1.1
##    print minvecx, minvecy, cx-polyx, cy-polyy
    if (cx-polyx)*minvecx + (cy-polyy)*minvecy < 0:
##        print 'a'
        return True, (-minvecx, -minvecy)
    return True, (minvecx, minvecy)


register(CIRCLE_TYPE, POLY_TYPE, collision_circle_poly)

def collision_circle_circle(circle1, circle2):
    cx, cy = circle1.rect.center
    rx, ry = circle2.rect.center
    dx = cx - rx
    dy = cy - ry
    r1 = circle1.radius
    r2 = circle2.radius
    if dx*dx+dy*dy < (r1+r2)**2:
        len_d = hypot(dx, dy)
        depth = r1+r2-len_d
        return True, (depth*dx/len_d, depth*dy/len_d)
    return False, None


register(CIRCLE_TYPE, CIRCLE_TYPE, collision_circle_circle)
        


        
        
class CObject(object):
    
    def __init__(self, size, pos, normals=[], vertices=[]):
        super(CObject, self).__init__()
        self.normals = normals
        self.vertices = vertices
        self.rect = pygame.Rect((0,0), size)# actual size
        self.rect.center = pos
        self.crect = self.rect.inflate(4,4)# bounding rect for fast collision detection
        self.crect.center = self.rect.center
        
    def rotate(self, angle, position=(0,0)):
        """
        returns rotate vertices and normals
        """
        if self.type != POLY_TYPE:
            raise "only polygons can be rotated!"
        vertices = []
        posx, posy = position
        for vertx, verty in self.vertices:
            radius = hypot(vertx, verty)
            dangle = atan2(verty, vertx)
            vertices.append((radius*cos(angle+dangle)+posx, radius*sin(angle+dangle)+posy))
        normals = []
        for nx, ny in self.normals:
            dangle = atan2(ny, nx)
            normals.append((cos(angle+dangle), sin(angle+dangle)))
        xmin = ymin = 9999999999
        xmax = ymax = -999999999
        for x,y in self.vertices:
            if x < xmin:
                xmin = x
            if x > xmax:
                xmax = x
            if y < ymin:
                ymin = y
            if y > ymax:
                ymax = y
        rect = pygame.Rect(0,0,xmax-xmin, ymax-ymin)
        rect.center = self.rect.center
        self.rect = rect
        self.crect = self.rect.inflate(4,4)
        self.crect.center = self.rect.center
        return vertices, normals
    
    def collision_response(self, norm, other = None):
        self.tile.collision_response(self.tile, self, norm, other)
    
class CCircle(CObject):
    
    def __init__(self, radius, pos_center):
        super(CCircle, self).__init__((2*radius, 2*radius), pos_center)
        self.radius = radius
        self.type = CIRCLE_TYPE
##        self.rect = pygame.Rect(0,0, 2*radius, 2*radius)
##        self.rect.center = pos_center
##        self.crect = self.rect.inflate(4,4)

class CSquare(CObject):
    
    def __init__(self, size, pos_center):
        super(CSquare, self).__init__(size, pos_center)
        self.type = QUAD_TYPE
        self.normals = [(1,0), (0,1), (-1,0), (0, -1)]
        self.half_height = self.rect.height/2
        self.half_width = self.rect.width/2


class CPoly(CObject):
    
    def __init__(self, pointlist, pos_center, size = None):
        """ 
        pointlist must have points in counter clockwise order
        point coord relative to center of polygone
        only CONVEX polygons possible (unexpected behavior using concave polygons)
        """
        self.type = POLY_TYPE
        
        # transforming such that (0,0) is in center of rect
        xmin = ymin = 9999999999
        xmax = ymax = -999999999
        for x,y in pointlist:
            if x < xmin:
                xmin = x
            if x > xmax:
                xmax = x
            if y < ymin:
                ymin = y
            if y > ymax:
                ymax = y
        dx = (xmin+xmax)/2
        dy = (ymin+ymax)/2
        self.vertices = [(vx-dx, vy-dy) for vx, vy in pointlist]
##        # resizing
##        if size:
##            ratiox = float((xmax-xmin))/size[0]
##            ratioy = float((ymax-ymin))/size[1]
##            self.vertices = [ (ratiox*px, ratioy*py) for px, py in self.vertices]
            
        # generating normals
        normals = []
        prevx, prevy = self.vertices[0]
        for x,y in self.vertices[1:]+[self.vertices[0]]:
            assert(x!=prevx or y!=prevy)
            nx = prevy-y
            ny = x-prevx
            len_n = hypot(nx, ny)
            normals.append((nx/len_n, ny/len_n))
            prevx = x
            prevy = y
        # init super class
        super(CPoly, self).__init__((xmax-xmin, ymax-ymin), pos_center, normals, self.vertices)


def get_instance_of_type(tile):
    if tile.collision_type == CIRCLE_TYPE:
        return CCircle(tile.rect.width/2, tile.rect.center)
    elif tile.collision_type == QUAD_TYPE:
        return CSquare(tile.rect.size, tile.rect.center)
    elif tile.collision_type == POLY_TYPE:
        return CPoly(tile.pointlist, tile.rect.center, tile.size)
    else:
        raise "unknown collision type!"+str(coll_type)
        

#------- helper functions -------------------


def proj_onto_unit(vec, unit):
    vx, vy = vec
    ox, oy = unit
    factor = vx*ox+vy*oy
    return ox * factor, oy * factor

def project(vec1, onto):
    vx, vy = vec1
    ox, oy = onto
    factor = (vx*ox+vy*oy)/float(hypot(ox, oy))
    return ox*factor, oy*factor

def rotate_rect_by_center(rect, angle): # -> new bounding rect
    diag = hypot(rect.width, rect.height)
    angle = angle + radians(45)
    nrect = pygame.Rect(0,0, diag*cos(angle), diag*sin(angle))
    nrect.center = rect.center
    return rect

if __name__=='__main__':
    vec = (1,1)
    print "vec:", vec
    onto = (1,0)
    print "onto:", onto
    print "projected:", project(vec, onto)
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    p = CPoly([(100,100), (100,-30), (-10,-200), (-100,50)], (400, 300))
    px, py = p.rect.center

    pygame.draw.polygon(screen, (255,0,0), [(px+vertx, py+verty) for vertx, verty in p.vertices])
    for nx, ny in p.normals:
        pygame.draw.line(screen, (255,255,255), (400, 300), (400+100*nx, 300+100*ny))
        
    vertices, normals = p.rotate(radians(45))
    vertix = []
    for vx, vy in vertices:
        vertix.append((vx+200, vy+200))
    pygame.draw.polygon(screen, (255,0,0), vertix)
    for nx, ny in normals:
        pygame.draw.line(screen, (255,0,255), (400, 300), (400+100*nx, 300+100*ny))
    pygame.display.flip()
    pygame.event.clear()
    pygame.event.wait()