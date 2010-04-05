import pygame
import sys
########################################################################
import operator
import math
 
########################################################################
 
class vec2d(object):
 
    def __init__(self, x_or_pair, y = None):
        if y == None:
            try:
                self.vec = [x_or_pair[0],x_or_pair[1]]
            except TypeError:
                raise TypeError("vec2d constructor requires a tuple or"
                    " two arguments")
        else:
            self.vec = [x_or_pair,y]
 
    def get_x(self):
        return self.vec[0]
    def set_x(self, value):
        self.vec[0] = value
    x = property(get_x, set_x)
    
    def get_y(self):
        return self.vec[1]
    def set_y(self, value):
        self.vec[1] = value
    y = property(get_y, set_y)
    
    def set(self, x, y):
        self.vec[0] = x
        self.vec[1] = y
        
    # String representaion (for debugging)
    def __repr__(self):
        return 'vec2d(%s, %s)' % (self.x, self.y)
    
    # Array-style access
    def __len__(self): return 2
 
    def __getitem__(self, key):
        return self.vec[key]
 
    def __setitem__(self, key, value):
        self.vec[key] = value
 
    # Comparison
    def __eq__(self, other):
        return self.vec[0] == other[0] and self.vec[1] == other[1]
    
    def __ne__(self, other):
        return self.vec[0] != other[0] or self.vec[1] != other[1]
 
    def __nonzero__(self):
        return self.vec[0] or self.vec[1]
 
    # Generic operator handlers
    def _o2(self, other, f):
        "Any two-operator operation where the left operand is a vec2d"
        try:
            return vec2d(f(self.vec[0], other[0]),
                         f(self.vec[1], other[1]))
        except TypeError:
            return vec2d(f(self.vec[0], other),
                         f(self.vec[1], other))
 
    def _r_o2(self, other, f):
        "Any two-operator operation where the right operand is a vec2d"
        try:
            return vec2d(f(other[0], self.vec[0]),
                         f(other[1], self.vec[1]))
        except TypeError:
            return vec2d(f(other, self.vec[0]),
                         f(other, self.vec[1]))
 
    def _o1(self, f):
        "Any unary operation on a vec2d"
        return vec2d(f(self.vec[0]), f(self.vec[1]))
 
    # Addition
    def __add__(self, other):
        return self._o2(other, operator.add)
    __radd__ = __add__
 
    # Subtraction
    def __sub__(self, other):
        return self._o2(other, operator.sub)
    def __rsub__(self, other):
        return self._r_o2(other, operator.sub)
 
    # Multiplication
    def __mul__(self, other):
        return self._o2(other, operator.mul)
    __rmul__ = __mul__
 
    # Division
    def __div__(self, other):
        return self._o2(other, operator.div)
    def __rdiv__(self, other):
        return self._r_o2(other, operator.div)
 
    def __floordiv__(self, other):
        return self._o2(other, operator.floordiv)
    def __rfloordiv__(self, other):
        return self._r_o2(other, operator.floordiv)
 
    def __truediv__(self, other):
        return self._o2(other, operator.truediv)
    def __rtruediv__(self, other):
        return self._r_o2(other, operator.truediv)
 
    # Modulo
    def __mod__(self, other):
        return self._o2(other, operator.mod)
    def __rmod__(self, other):
        return self._r_o2(other, operator.mod)
 
    def __divmod__(self, other):
        return self._o2(other, operator.divmod)
    def __rdivmod__(self, other):
        return self._r_o2(other, operator.divmod)
 
    # Exponentation
    def __pow__(self, other):
        return self._o2(other, operator.pow)
    def __rpow__(self, other):
        return self._r_o2(other, operator.pow)
 
    # Bitwise operators
    def __lshift__(self, other):
        return self._o2(other, operator.lshift)
    def __rlshift__(self, other):
        return self._r_o2(other, operator.lshift)
 
    def __rshift__(self, other):
        return self._o2(other, operator.rshift)
    def __rrshift__(self, other):
        return self._r_o2(other, operator.rshift)
 
    def __and__(self, other):
        return self._o2(other, operator.and_)
    __rand__ = __and__
 
    def __or__(self, other):
        return self._o2(other, operator.or_)
    __ror__ = __or__
 
    def __xor__(self, other):
        return self._o2(other, operator.xor)
    __rxor__ = __xor__
 
    # Unary operations
    def __neg__(self):
        return self._o1(operator.neg)
 
    def __pos__(self):
        return self._o1(operator.pos)
 
    def __abs__(self):
        return self._o1(operator.abs)
 
    def __invert__(self):
        return self._o1(operator.invert)
 
    # vectory functions
    def get_length_sqrd(self): 
        return self.vec[0]**2 + self.vec[1]**2
 
    def get_length(self):
        return math.sqrt(self.vec[0]**2 + self.vec[1]**2)    
    def __setlength(self, value):
        self.normalize_return_length()
        self.vec[0] *= value
        self.vec[1] *= value
    length = property(get_length, __setlength, None,
        "gets or sets the magnitude of the vector")
       
    def rotate(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.vec[0]*cos - self.vec[1]*sin
        y = self.vec[0]*sin + self.vec[1]*cos
        self.vec[0] = x
        self.vec[1] = y
    
    def get_angle(self):
        if (self.get_length_sqrd() == 0):
            return 0
        return math.degrees(math.atan2(self.vec[1], self.vec[0]))
 
    def get_angle_between(self, other):
        cross = self.vec[0]*other[1] - self.vec[1]*other[0]
        dot = self.vec[0]*other[0] + self.vec[1]*other[1]
        return math.degrees(math.atan2(cross, dot))
    
    def __setangle(self, angle_degrees):
        self.vec[0] = self.length
        self.vec[1] = 0
        self.rotate(angle_degrees)
    angle = property(get_angle, __setangle, None,
        "gets or sets the angle of a vector")
        
    def normalized(self):
        length = self.length
        if length != 0:
            return self/length
        return vec2d(self)
 
    def perpendicular(self):
        return vec2d(self.vec[1], -self.vec[0])
    
    def perpendicular_normal(self):
        length = self.length
        if length != 0:
            return vec2d(self.vec[1]/length, -self.vec[0]/length)
        return vec2d(self)
        
    def normalize_return_length(self):
        length = self.length
        if length != 0:
            self.vec[0] /= length
            self.vec[1] /= length
        return length
 
    def dot(self, other):
        return self.vec[0]*other[0] + self.vec[1]*other[1]
        
    def get_distance(self, other):
        return math.sqrt((self.vec[0] - other[0])**2 +
            (self.vec[1] - other[1])**2)
        
    def projection(self, other):
        normal = other.normalized()
        projected_length = self.dot(normal)
        return normal*projected_length
    
    def cross(self, other):
        return self.vec[0]*other[1] - self.vec[1]*other[0]
    
    def interpolate_to(self, other, range):
        return vec2d(self.vec[0] + (other.vec[0] - self.vec[0])*range,
            self.vec[1] + (other.vec[1] - self.vec[1])*range)
    
    def convert_to_basis(self, x_vector, y_vector):
        return vec2d(self.dot(x_vector)/x_vector.get_length_sqrd(),
            self.dot(y_vector)/y_vector.get_length_sqrd())
pygame.init()

screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
background = pygame.Surface((640, 480))

terrain = pygame.sprite.Group()

gravity = vec2d(0, -0.2)
bounciness = 0.2
friction = 0

def origin(coord):
    return coord[0], 480 - coord[1]

def squareCollideTriangle(square, triangle):
    assert isinstance(square, Square)
    assert isinstance(triangle, RightTriangle)
    
    squareVertices = vec2d(origin(square.rect.topright)), vec2d(origin(square.rect.topleft)), vec2d(origin(square.rect.bottomleft)), vec2d(origin(square.rect.bottomright))
    triangleVertices = None
    
    triangleNormal = None
    squareNormal = [vec2d(-1, 0), vec2d(1, 0), vec2d(0, -1), vec2d(0, 1)]
    if triangle.orientation == "bottomright":
        triangleNormal = [vec2d(1, 0), vec2d(0, -1), triangle.hypotenuseNormal]
        triangleVertices = vec2d(origin(triangle.rect.bottomleft)),vec2d( origin(triangle.rect.bottomright)), vec2d(origin(triangle.rect.topright))
    elif triangle.orientation == "bottomleft":
        triangleNormal = [vec2d(-1, 0), vec2d(0, -1), triangle.hypotenuseNormal]
        triangleVertices = vec2d(origin(triangle.rect.bottomleft)), vec2d(origin(triangle.rect.topleft)), vec2d(origin(triangle.rect.bottomright))
    elif triangle.orientation == "topleft":
        triangleNormal = [vec2d(-1, 0), vec2d(0, 1), triangle.hypotenuseNormal]
        triangleVertices = vec2d(origin(triangle.rect.topleft)), vec2d(origin(triangle.rect.bottomleft)), vec2d(origin(triangle.rect.topright))
    elif triangle.orientation == "topright":
        triangleNormal = [vec2d(1, 0), vec2d(0, 1), triangle.hypotenuseNormal]
        triangleVertices = vec2d(origin(triangle.rect.topright)), vec2d(origin(triangle.rect.topleft)), vec2d(origin(triangle.rect.bottomright))
    
    pushVectors = []
    
    for n in triangleNormal:
        separate, push = axisSeparatePolygons(n, squareVertices, triangleVertices)
        if separate:
            return False, None
        pushVectors.append(push)
        
    #for n in squareNormal:
        #separate, push = axisSeparatePolygons(n, squareVertices, triangleVertices)
        #if separate:
            #return False, None
        #pushVectors.append(push)
    
    mtd = findMTD(pushVectors)
    
    d = vec2d(square.rect.centerx - triangle.rect.centerx, (480 - square.rect.centery) - (480 - triangle.rect.centery))
    if (d.dot(mtd) < 0):
        mtd = -mtd
    
    return True, (mtd.x, -mtd.y)
    
    
    

def findMTD(pushVectors):
    mtd = pushVectors[0]
    mind2 = pushVectors[0].dot(pushVectors[0])
    
    for v in pushVectors:
        d2 = v.dot(v)

        if (d2 < mind2):
            mind2 = d2
            mtd = v
    
    return mtd
def calculateInterval(normal, points):
    dot = normal.dot(points[0])
    min, max = dot, dot
    for p in points:
        dot = p.dot(normal)
        if dot < min:
            min = dot
        else:
            if dot > max:
                max = dot
    
    return min, max

def axisSeparatePolygons(normal, pointsA, pointsB):
    minA, maxA = calculateInterval(normal, pointsA)
    minB, maxB = calculateInterval(normal, pointsB)
    
    if minA > maxB or minB > maxA:
        return True, None
    
    depth1 = maxA - minB
    depth2 = maxB - minA
    
    depth = 0
    if depth1 < depth2:
        depth = depth1
    else:
        depth = depth2
        
    return False, normal * depth
        

    
        
class Square(pygame.sprite.Sprite):
    def __init__(self, rect, fillColour):
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect
        self.image = pygame.Surface(rect.size)
        self.image.fill(fillColour)
        
        self.touchingGround = False
        
    def collideSquare(self, otherSquare):
        otherRect = otherSquare.rect
        rect = self.rect
        
        overlapX = 0
        overlapY = 0
        
        if rect.centerx < otherRect.centerx:
            overlapX = rect.right - otherRect.left
            if overlapX <= 0:
                return False, None
        else:
            overlapX = rect.left - otherRect.right
            if overlapX >= 0:
                return False, None
        
        if rect.centery > otherRect.centery:
            overlapY = rect.top - otherRect.bottom
            if overlapY >= 0:
                return False, None
        else:
            overlapY = rect.bottom - otherRect.top
            if overlapY <= 0:
                return False, None
            
        
        if abs(overlapX) < abs(overlapY):
            return True, (-overlapX, 0)
        else:
            return True, (0, -overlapY)
            

    

        
class SquareTerrain(Square):
    def __init__(self, center):
        dimensions = (40, 90)
        Square.__init__(self, center, dimensions, (0, 255, 0))

class RightTriangle(pygame.sprite.Sprite):
    def __init__(self, rect, fillColour=(255, 255, 255), orientation="bottomleft"):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(rect.size)
        self.image.set_colorkey((0, 0, 0))
        self.rect = rect
        self.orientation = orientation
        dimensions = rect.size
        if orientation == "bottomleft":
            pointlist = [(0, dimensions[1]), (0, 0), (dimensions[0], dimensions[1]), (0, dimensions[1])]
            self.hypotenuseVector = vec2d(-self.rect.width, self.rect.height)
            self.hypotenuseNormal = self.hypotenuseVector.perpendicular_normal()
        elif orientation == "bottomright":
            pointlist = [(dimensions[0], dimensions[1]), (0, dimensions[1]), (dimensions[0], 0), (dimensions[0], dimensions[1])]
            self.hypotenuseVector = vec2d(-self.rect.width, -self.rect.height)
            self.hypotenuseNormal = self.hypotenuseVector.perpendicular_normal()
        elif orientation == "topleft":
            pointlist = [(0, 0), (0, dimensions[1]), (dimensions[0], 0), (0, 0)]
        elif orientation == "topright":
            pointlist = [(dimensions[0], 0), (0, 0), (0, dimensions[1]), (dimensions[0], 0)]
    
        pygame.draw.polygon(self.image, fillColour, pointlist)

class Player(Square):
    def __init__(self, center):
        dimensions = (25, 25)
        rect = pygame.Rect((0, 0), dimensions)
        rect.center = center
        Square.__init__(self, rect, (255, 0, 0))
    
        self.velocity = vec2d(0, 0)
        self.acceleration = vec2d(0, 0)
        
    def update(self):
        self.rect.move_ip(self.velocity.x, -self.velocity.y)
        self.velocity += gravity
        self.velocity += self.acceleration
        
        self.acceleration.x = 0; self.acceleration.y = 0
        

                    
        keysPressed = pygame.key.get_pressed()
    
        if keysPressed[pygame.K_DOWN]:
            self.moveDown()
        elif keysPressed[pygame.K_UP]:
            if self.touchingGround:
                self.moveUp()
            
        if keysPressed[pygame.K_LEFT]:
            self.moveLeft()
        elif keysPressed[pygame.K_RIGHT]:
            self.moveRight()
            
        for t in terrain:
            if isinstance(t, RightTriangle):
                collision, overlap = squareCollideTriangle(self, t)
                if collision:
                    self.rect.move_ip(overlap)
                    self.collisionResponse(vec2d(overlap[0], -overlap[1]))
                    self.touchingGround = True
                    
            elif isinstance(t, Square):
                collision, overlap = self.collideSquare(t)
                if collision:
                    self.rect.move_ip(overlap)
                    self.collisionResponse(vec2d(overlap[0], -overlap[1]))
                    self.touchingGround = True


        

    
    def collisionResponse(self, normal):
        normal = normal.normalized()
        #vn = self.velocity.dot(normal) * normal
        #vt = self.velocity - vn
        #self.velocity = vt * (1 - friction) + vn * -(bounciness)
        
        self.velocity = self.velocity - (((1 + bounciness) * self.velocity.dot(normal)) * normal)
    
            
    def moveLeft(self):
        self.acceleration += vec2d(-0.5, 0)
        #self.rect.move_ip(-10, 0)
    def moveRight(self):
        self.acceleration += vec2d(0.5, 0)
        #self.rect.move_ip(10, 0)
    
    def moveUp(self):
        self.acceleration += vec2d(0, 5)
        self.touchingGround = False
        #self.rect.move_ip(0, -10)
    def moveDown(self):
        #self.rect.move_ip((0, 10))
        pass
    
sprites = pygame.sprite.RenderUpdates()

playerSquare = Player((320, 240))

#setup terrain
tRect1 = pygame.Rect((0, 0), (100, 300))
terrain.add(RightTriangle(tRect1, (0, 255, 0), "bottomleft"))
tRect2 = pygame.Rect(tRect1.bottomright, (100, 100))
terrain.add(RightTriangle(tRect2, (0, 255, 0), "bottomleft"))
tRect3 = pygame.Rect(tRect2.bottomright, (400, 100))
terrain.add(Square(tRect3, (0, 255, 0)))
tRect4 = pygame.Rect((0, 0), (25, 25))
tRect4.bottomleft = tRect3.topright
terrain.add(RightTriangle(tRect4, (0, 255, 0), "bottomright"))
tRect5 = pygame.Rect((0, 0), (25, tRect4.top))
tRect5.bottomleft = tRect4.topright
terrain.add(Square(tRect5, (0, 255, 0)))
tRect6 = pygame.Rect((0, 0), (640, 25))
terrain.add(Square(tRect6,(0, 255, 0)))

#filler
tRect7 = pygame.Rect(tRect1.bottomleft, (100, 180))
terrain.add(Square(tRect7, (0, 255, 0)))
tRect8 = pygame.Rect(tRect2.bottomleft, (100, 400))
terrain.add(Square(tRect8, (0, 255, 0)))
tRect9 = pygame.Rect(tRect4.topright, (200, 400))
terrain.add(Square(tRect9, (0, 255, 0)))
tRect10 = pygame.Rect(tRect4.bottomleft, (100, 200))
terrain.add(Square(tRect10, (0, 255, 0)))
sprites.add(playerSquare)
sprites.add(terrain)

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        screen.fill((0, 0, 0))
        sprites.update()
        dirtyRects = sprites.draw(screen)
        pygame.display.flip()
        
        clock.tick(40)
        
if __name__ == "__main__":
    main()
