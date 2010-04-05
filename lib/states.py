from header import *
from random import randint
##import pickle
##import builder
##cerealizer.register(builder.Level)
from level import Level
##cerealizer.register(__main__.Level)
import os
import cerealizer
data_py = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.normpath(os.path.join(data_py, '..', 'data'))
level_dir = musicpath = os.path.normpath(os.path.join(data_dir, 'levels'))

##class Level(object):
##    """
##    Container object to be pickled and loaded.
##    tile = (name, pos, type, pointlist, angle)
##    """
##    def __init__(self):
##        self.size = (576, 576)
##        self.bg = None
##        self.tiles = []

##cerealizer.register(Level)

class BaseState(object):
    """
    BaseState includes the basic functionality of the application. 
    -   Events are passed to the state, blindly, and can be handled if desired
        by adding an entry in the function matrix and providing a handling method.
    """
    def __init__(self):
        pass
        
    def get_signal_matrix(self):
        """
        A hard-coded map of signal-type to listening handle method
        """
        return {
            'quit' : self.on_quit,
            'keydown' : self.on_key_down,
            'mousemotion' : self.on_mouse_motion,
            'mousebuttondown' : self.on_mouse_down,
            'mousebuttonup' : self.on_mouse_up
            }

    def enter(self, app):
        """
        Called after State registers with the stack.
        """
        self.app = app
    
    def leave(self):
        """
        Called before State unregisters with the stack.
        """
        pass
    
    #DEFAULT EVENT HANDLERS
    def on_quit(self):
        self.app.PopAll()
    
    def on_key_down(self, unicode, key, mod):
        if key == pygame.K_ESCAPE:
            self.app.Pop()
        if key == pygame.K_SPACE:
            pass
            
    def on_mouse_motion(self, pos, rel, buttons, only_last):
        pass
        
    def on_mouse_down(self, pos, button):
        pass
        
    def on_mouse_up(self, pos, button):
        pass

class SplashState(BaseState):
    def __init__(self):
        pass
    
    def enter(self, app):
        super(SplashState, self).enter(app)
        screen = self.app.screen
        #blackness overlay
        self.blackness = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA).convert(screen)
        self.blackness.set_alpha(255)
        #pygame segment
        self.pygamelogo = data.load_image("madewith.png")
        #team segment
        self.teambg = data.load_image("teambg.png")
        self.teamheader = data.load_image("teamheader.png")
        self.headerpos = [0, 0]
        self.teamframes = {}
        for n in range(1, 11):
            self.teamframes[n] = data.load_image("teambanner%d.png" % n)
        self.start_time = 0
        
    def get_signal_matrix(self):
        sm = super(SplashState, self).get_signal_matrix()
        sm.update({
            'render' : self.on_render
            })
        return sm
    def on_key_down(self, unicode, key, mod):
        if key == pygame.K_ESCAPE:
            self.app.Pop()
        else: self.start_levels()
        
    def start_levels(self):
        self.app.Pop()
##        self.app.Push(LevelBase('my_file.cer'))
##        self.app.Push(LevelBase('big.pkl'))
##        self.app.Push(LevelBase('menu.pkl'))
        self.app.Push(MyMenu())
            
    def on_render(self):
        screen = self.app.screen
        if self.start_time == 0:
            self.start_time = pygame.time.get_ticks()
        now = pygame.time.get_ticks()
        diff = now - self.start_time
        #Pygame Fade in on 7 seconds, hold for 2
        if diff < 4000:
            screen.fill((0, 0, 0))
        elif diff < 9000:
            screen.fill((255, 255, 255))
            screen.blit(self.pygamelogo[0], (50, 200))
            screen.blit(self.blackness, (0, 0))
            self.blackness.set_alpha( self.blackness.get_alpha() - 1.5 )
        #Pygame Fade out on 9 seconds hold for 2
        elif diff < 13000:
            screen.fill((255, 255, 255))
            screen.blit(self.pygamelogo[0], (50, 200))
            screen.blit(self.blackness, (0, 0))
            self.blackness.set_alpha( self.blackness.get_alpha() + 2.8 )
        elif diff < 16000:
            screen.fill((0, 0, 0))
            screen.blit(self.teambg[0], (0, 200))
            #print self.headerpos
            screen.blit(self.teamheader[0], self.headerpos)
            self.headerpos[0] += 0.5
            screen.blit(self.blackness, (0, 0))
            self.blackness.set_alpha( self.blackness.get_alpha() - 1.3)
        elif diff < 20000:
            screen.fill((0, 0, 0))
            screen.blit(self.teambg[0], (0, 200))
            screen.blit(self.teamheader[0], self.headerpos)
            self.headerpos[0] += 0.5
            if diff < 16400:
                screen.blit(self.teamframes[10][0], (0, 200))
            elif diff < 16800:
                screen.blit(self.teamframes[9][0], (0, 200))
            elif diff < 17200:
                screen.blit(self.teamframes[8][0], (0, 200))
            elif diff < 17600:
                screen.blit(self.teamframes[7][0], (0, 200))
            elif diff < 18000:
                screen.blit(self.teamframes[6][0], (0, 200))
            elif diff < 18400:
                screen.blit(self.teamframes[5][0], (0, 200))
            elif diff < 18800:
                screen.blit(self.teamframes[4][0], (0, 200))
            elif diff < 19200:
                screen.blit(self.teamframes[3][0], (0, 200))
            elif diff < 19600:
                screen.blit(self.teamframes[2][0], (0, 200))
            else:
                screen.blit(self.teamframes[1][0], (0, 200))
        elif diff < 25000:
            screen.fill((0, 0, 0))
            screen.blit(self.teambg[0], (0, 200))
            screen.blit(self.teamheader[0], self.headerpos)
            self.headerpos[0] += 0.5
            screen.blit(self.teamframes[1][0], (0, 200))
        else:
            screen.fill((0, 0, 0))
            screen.blit(self.teambg[0], (0, 200))
            screen.blit(self.teamheader[0], self.headerpos)
            self.headerpos[0] += 0.5
            screen.blit(self.teamframes[1][0], (0, 200))
            self.blackness.set_alpha( self.blackness.get_alpha() + 1.3)
            screen.blit(self.blackness, (0, 0))
            if self.blackness.get_alpha() >= 255:
                self.start_levels()
        
class LevelBase(BaseState):
    def __init__(self, levelname):
        self.debug = False
        self.dragging = False
        self.spinning = False
        self.angle = 0
        self.fixed_angle = 0
        self.delta_angle = 0
        self.ball = None
        self.levelname = levelname
        self.level = None
        self.clock = pygame.time.Clock()
        self.num_coins = 0
        self.num_collected_coins = 0
        self.retries = 0
        self.paused = False
        
    def get_signal_matrix(self):
        sm = super(LevelBase, self).get_signal_matrix()
        sm.update({
            'render' : self.on_render
            })
        return sm
        
        
    def load_level(self, levelname):
        
        filename = os.path.join(level_dir, levelname)
        f = open(filename, 'r')
##        self.level = pickle.load(f)
##        cerealizer.register(Level)
        #print "going to laod cerealized file"
        self.level = cerealizer.load(f)
        #print "level", self.level
        #print "size", self.level.size
        #print "name", self.levelname
        #print "tiles", self.level.tiles
        self.bg = self.level.bg
        self.size = self.level.size
        self.ball.rect.center = self.level.ball
##        self.world.set_size( self.level.size )
        for t in self.level.tiles:
            name, pos, type, pointlist, angle = t
            #print t
            if type > 1:
                #TODO : Hack! Detect any Goal Tiles
                self.world.tiles.append(tiles.PolygonTile(name, pointlist, pos, angle))
                if name == 'exit.PNG':
##                    self.world.tiles.append(tiles.Bar(name, pos, angle))
                    #print "Found an exit!"
                    self.world.tiles[-1].collision_response = self.my_coll_handler
##                elif name == 'bar.PNG':
##                    self.world.tiles.append(tiles.Bar(name, pos, angle))
##                else:
##                    self.world.tiles.append(tiles.PolygonTile(name, pointlist, pos, angle))
            else:
                if name == 'coin.PNG':
                    self.num_coins += 1
                    tile = tiles.Coin(name, pos)
                    self.world.tiles.append(tile)
                    tile.collision_response = self.collect_coin
                elif name == 'circle.PNG':
                    tile = tiles.Circle(name, pos)
                    self.world.tiles.append(tile)
                else:
                    #TODO: tiles shoud be instances of their class
                    self.world.tiles.append(tiles.Tile(name, pos))
            
    def build_level(self):
        pass
      
    def enter(self, app):
        super(LevelBase, self).enter(app)
        self.ball = ball.Ball('test_ball.PNG', (0,0))
        # init values, needed for restart
        self.num_coins = 0
        self.dragging = False
        self.spinning = False
        self.angle = 0
        self.fixed_angle = 0
        self.delta_angle = 0
        # handle broken ball
        self.ball.exit = self.ball_broken
        self.world = tilemap.TileMap()
        try:
            if self.levelname:
                self.load_level(self.levelname)
        except:
            print "Erroneous level", self.levelname
        self.build_level()
        #View setup
        self.view = viewport.RotatableView(self.app.screen, pygame.Rect(0, 0, 800, 600), self.world, pygame.Rect(0, 0, 800, 600), bg = self.bg)
        for tile in self.world.tiles:
            coll_tile = tile.get_collision_tile()
            if coll_tile: # filter None
                self.world.collision_tiles.append(coll_tile)
        self.ball.world = self.world
##        self.world.tiles.append(self.ball)
        self.ball.get_collision_tile()
        if self.ball.debug:
            self.debug = True
            self.ball.screen = self.view.surface
        
    def ball_broken(self):
        self.restart()
        
    def on_render(self):
        if self.paused:
            return
        
        dt = min(self.clock.tick(), 20)
        #print "tick", dt
        
        angle = self.angle + self.delta_angle
        self.ball.update(angle, dt)
        
        if not self.debug:
            self.view.world_rect.center = self.ball.rect.center
        
        self.view.draw_rot(angle)
        
        if self.debug:
            cx, cy = self.ball.rect.center
            wx, wy = self.view.world_rect.center
            dx, dy = ((-wx+self.view.half_view_x), (-wy+self.view.half_view_y))
            for norm in self.ball.debug_normals:
                pygame.draw.line(self.view.surface, (255,255,255), (cx+dx, cy+dy), (cx+dx+30*norm[0], cy+dy+30*norm[1]))
            self.view.surface.blit(self.ball.image, (cx+dx-self.ball.rect.width/2, cy+dy-self.ball.rect.height/2))
            for tile in self.world.tiles:
                if len(tile.collider.vertices):
                    px, py = tile.rect.center
                    pointlist = [(cx+px+dx, cy+py+dy)for cx, cy in tile.collider.vertices ]
                    pygame.draw.polygon(self.view.surface, (0,255,0), pointlist)
            
        else:
            
            self.view.surface.blit(self.ball.image, (self.view.half_view_x-self.ball.rect.width/2, self.view.half_view_y-self.ball.rect.height/2))
            
        
        
    def on_mouse_down(self, pos, button):
        if self.debug:
            self.dragging = True
            px, py = pos
            wx, wy = self.view.world_rect.center
            self.ball.rect.center = (px-(-wx+self.view.half_view_x), py+(wy-self.view.half_view_y))
        else:
            mx, my = pos
            self.fixed_angle = math.atan2(my-self.view.half_view_y, mx-self.view.half_view_x)
            self.spinning = True
        
    def on_mouse_motion(self, pos, rel, buttons, only_last):
        if self.debug:
            if self.dragging:
                px, py = pos
                wx, wy = self.view.world_rect.center
                self.ball.rect.center = (px-(-wx+self.view.half_view_x), py+(wy-self.view.half_view_y))
        else:
            if self.spinning:
                mx, my = pos
                current_angle = math.atan2(my-self.view.half_view_y, mx-self.view.half_view_x)
                self.delta_angle = current_angle - self.fixed_angle
    
    def on_mouse_up(self, pos, button):
        if self.debug:
            self.dragging = False
        else:
            self.angle += self.delta_angle
            self.angle %= (2*math.pi)
            self.delta_angle = 0
            self.spinning = False
            
    def on_key_down(self, unicode, key, mod):
        if self.debug:
            step = 50
            if key==pygame.K_a:
                self.view.world_rect.move_ip(-step, 0)
            if key==pygame.K_d:
                self.view.world_rect.move_ip(step, 0)
            if key==pygame.K_s:
                self.view.world_rect.move_ip(0, -step)
            if key==pygame.K_w:
                self.view.world_rect.move_ip(0, step)
        else:
            if key==pygame.K_r:
                self.restart()
            elif key==pygame.K_p:
                self.paused ^= 1
        if key==pygame.K_F10:
            self.debug ^= 1
            self.ball.debug = self.debug
        if key == pygame.K_ESCAPE:
            self.app.Pop()
            self.app.Pop()
                
    def restart(self):
        self.retries += 1
        #TODO
        print "restarting level"
        self.enter(self.app)
                
    def my_coll_handler(self, tile, ctile, norm, other):
        # called when exit tile is hit
        # only exit when all coins are eaten
        if self.num_coins == 0:
            self.app.Pop()
        
    def collect_coin(self, tile, ctile, norm, other):
##        print "going to collect coin"
        try:
            self.world.tiles.remove(tile)
            self.world.collision_tiles.remove(ctile)
##            print "collected a coin", tile, other
            self.num_coins -= 1
            self.num_collected_coins += 1
        except:
            pass
            
            
    def leave(self):
        #TODO pass all info to upper level
        #TODO: HACK to pass some information
        try:
            parent = self.app.statestack[-2]
            parent.setinfo(self.retries, self.num_collected_coins)
        except:
            pass
        
class TestLevel(LevelBase):
      
    def build_level(self):
        # here add the tiles of that level
        # self.world is an instance of TileMap
        #self.ball = Ball(radius, pos, image_name)
        self.bg = "bgmosaic.PNG"
        self.ball = ball.Ball('test_ball.PNG', (100,100))
##        self.ball.debug = True # if setting this you can debug the level
        self.world.set_size((3000, 3200))
        #self.world.tiles.append(tilemap.Tile('test_tile1.PNG', (160, 320-64), (10, 128)))
        #self.world.tiles.append(tilemap.Tile('test_tile1.PNG', (160, 64), (30, 128)))
##        self.world.tiles.append(tilemap.PolygonTile('test_tile2.PNG', [(0,0),(64,0),(64,-64), (0, -64)], (200,320-32), angle_deg=0))
##        self.world.tiles.append(tilemap.LeftHillLow( 'lefthill_low.PNG', (60,320 - 166), angle_deg=-45))
##        self.world.tiles.append(tilemap.LeftHillLow( 'lefthill_low.PNG', (200,320 - 166), angle_deg=90+45))
        d=0
        for angle in range(0,360, 30):
            self.world.tiles.append(tilemap.LeftHillHeigh('lefthill_high.PNG', (200, 50+d), angle))
            self.world.tiles.append(tilemap.RightHillHeigh('righthill_high.PNG', (300, 50+d), angle))
            self.world.tiles.append(tilemap.LargeHill('largehill.PNG', (400, 50+d), angle))
            self.world.tiles.append(tilemap.LeftHillLow('lefthill_low.PNG', (500, 50+d), angle))
            self.world.tiles.append(tilemap.RightHillLow('righthill_low.PNG', (600, 50+d), angle))
            self.world.tiles.append(tilemap.PolygonTile('diamond.png',[(0,0), (32, -16), (32, -48), (0,-64), (-32, -48), (-32,-16)] , (700, 50+d), angle))
            d += 100
        self.world.tiles.append(tilemap.Bar('exit.PNG', (50, 550)))
        # Trigger demo
        self.world.tiles[-1].collision_response = self.my_coll_handler
        
        
    def my_coll_handler(self, tile, ctile, norm, other):
        #print "******************", self, norm, other
        self.app.Pop()

        
class HugeRandomLevel(LevelBase):
    
    def build_level(self):
        self.bg = data.load_image("bgmosaic.PNG")[0]
        self.ball = ball.Ball('test_ball.PNG', (100,100))
        w = h = 3200
        self.ball.debug = True
        self.world.set_size((w,h))
        for i in range(50):
                self.world.tiles.append(tiles.Tile('test_tile2.PNG', (randint(200,w), randint(200,h))))
        for i in range(50):
                self.world.tiles.append(tiles.Circle('thum_test_ball.png', (randint(200,w), randint(200,h))))
##LeftHillHeigh
##RightHillHeigh
##LargeHill
##LeftHillLow
##RightHillLow

        for i in range(50):
                self.world.tiles.append(tilemap.LeftHillHeigh('lefthill_high.PNG', (randint(200,w), randint(200,h)), randint(0,360)))
        for i in range(50):
                self.world.tiles.append(tilemap.RightHillHeigh('righthill_high.PNG', (randint(200,w), randint(200,h)), randint(0,360)))
        for i in range(50):
                self.world.tiles.append(tilemap.LargeHill('largehill.PNG', (randint(200,w), randint(200,h)), randint(0,360)))
        for i in range(50):
                self.world.tiles.append(tilemap.LeftHillLow('lefthill_low.PNG', (randint(200,w), randint(200,h)), randint(0,360)))
        for i in range(50):
                self.world.tiles.append(tilemap.RightHillLow('righthill_low.PNG', (randint(200,w), randint(200,h)), randint(0,360)))


class LevelRotator(BaseState):
    
    def __init__(self):
        super(LevelRotator, self).__init__()
        self.total_coins = 0
        self.levellist = ['tech1.pkl','hard1.pkl', 'medium2.pkl', 'medium1.pkl', 'easy2.pkl', 'easy1.pkl'] #TODO: names
        self.current_level = 0

    def get_signal_matrix(self):
        sm = super(LevelRotator, self).get_signal_matrix()
        sm.update({
            'render' : self.on_render
            })
        return sm

    def on_render(self):
        print "levelrotator", self.current_level, len(self.levellist)
##        while len(self.levellist):
        print self.levellist
        if len(self.levellist):
            name = self.levellist.pop()
            print "running level:", name
            self.app.Push(LevelBase(name))
            self.current_level += 1
        else:
            print "pop level of levelrotator"
            self.app.Pop()
        

    def setinfo(self, retries, num_collected_coins):
        self.total_coins += 1
        
        
        
class Menu(LevelBase):
    
    def __init__(self):
        super(Menu, self).__init__(None)

    def build_level(self):
        #TODO: level
        self.bg = "bgmosaic.PNG"
        self.ball = ball.Ball('test_ball.PNG', ((11*64)/2,64+32))
        self.ball.hit_threshold = 1.1 # never break
        
        self.world.tiles.append(tiles.Tile('default.PNG', (0*64, 3*64)))
        self.world.tiles.append(tiles.Tile('default.PNG', (0*64, 6*64)))
        
        self.world.tiles.append(tiles.Tile('default.PNG', (1*64, 2*64)))
        self.world.tiles.append(tiles.Tile('default.PNG', (1*64, 4*64)))
        self.world.tiles.append(tiles.Tile('default.PNG', (1*64, 5*64)))
        self.world.tiles.append(tiles.Tile('default.PNG', (1*64, 7*64)))
        
        self.world.tiles.append(tiles.Tile('default.PNG', (2*64, 1*64)))
        self.world.tiles.append(tiles.Tile('default.PNG', (2*64, 8*64)))
        
        self.world.tiles.append(tiles.Tile('default.PNG', (3*64, 0*64)))
        self.world.tiles.append(tiles.Tile('default.PNG', (3*64, 2*64)))
        self.world.tiles.append(tiles.Tile('default.PNG', (3*64, 4*64)))
        self.world.tiles.append(tiles.Tile('default.PNG', (3*64, 5*64)))
        self.world.tiles.append(tiles.Tile('default.PNG', (3*64, 7*64)))
        
        self.world.tiles.append(tiles.Tile('default.PNG', (4*64, 0*64)))
        self.world.tiles.append(tiles.Tile('default.PNG', (4*64, 5*64)))
        self.world.tiles.append(tiles.Tile('default.PNG', (4*64, 7*64)))
        
        self.world.tiles.append(tiles.Tile('default.PNG', (5*64, 0*64)))
        self.world.tiles.append(tiles.Tile('default.PNG', (5*64, 2*64)))
        self.world.tiles.append(tiles.Tile('default.PNG', (5*64, 4*64)))
        self.world.tiles.append(tiles.Tile('default.PNG', (5*64, 5*64)))
        self.world.tiles.append(tiles.Tile('default.PNG', (5*64, 7*64)))
        
        self.world.tiles.append(tiles.Tile('default.PNG', (11*64, 3*64)))
        self.world.tiles.append(tiles.Tile('default.PNG', (11*64, 6*64)))
        
        self.world.tiles.append(tiles.Tile('default.PNG', (10*64, 2*64)))
        self.world.tiles.append(tiles.Tile('default.PNG', (10*64, 4*64)))
        self.world.tiles.append(tiles.Tile('default.PNG', (10*64, 5*64)))
        self.world.tiles.append(tiles.Tile('default.PNG', (10*64, 7*64)))
        
        self.world.tiles.append(tiles.Tile('default.PNG', (9*64, 1*64)))
        self.world.tiles.append(tiles.Tile('default.PNG', (9*64, 8*64)))
        
        self.world.tiles.append(tiles.Tile('default.PNG', (8*64, 0*64)))
        self.world.tiles.append(tiles.Tile('default.PNG', (8*64, 2*64)))
        self.world.tiles.append(tiles.Tile('default.PNG', (8*64, 4*64)))
        self.world.tiles.append(tiles.Tile('default.PNG', (8*64, 5*64)))
        self.world.tiles.append(tiles.Tile('default.PNG', (8*64, 7*64)))
        
        self.world.tiles.append(tiles.Tile('default.PNG', (7*64, 0*64)))
        self.world.tiles.append(tiles.Tile('default.PNG', (7*64, 5*64)))
        self.world.tiles.append(tiles.Tile('default.PNG', (7*64, 7*64)))
        
        self.world.tiles.append(tiles.Tile('default.PNG', (6*64, 0*64)))
        self.world.tiles.append(tiles.Tile('default.PNG', (6*64, 2*64)))
        self.world.tiles.append(tiles.Tile('default.PNG', (6*64, 4*64)))
        self.world.tiles.append(tiles.Tile('default.PNG', (6*64, 5*64)))
        self.world.tiles.append(tiles.Tile('default.PNG', (6*64, 7*64)))
        
        self.world.tiles.append(tiles.Bar('exit.PNG', (2*64, 2*64), 0))
        self.world.tiles[-1].collision_response = self.handle_game_exit
        self.world.tiles.append(tiles.Bar('info.PNG', (1*64, 6*64), 90))
        self.world.tiles[-1].collision_response = self.handle_game_info
        self.world.tiles.append(tiles.Bar('start.PNG', (5*64+32, 3*64), 90))
        self.world.tiles[-1].collision_response = self.handle_game_start
        self.world.tiles.append(tiles.Bar('restart.PNG', (5*64+32, 6*64), 90))
        self.world.tiles[-1].collision_response = self.handle_game_restart
        self.world.tiles.append(tiles.Bar('credits.PNG', (9*64, 2*64), 0))
        self.world.tiles[-1].collision_response = self.handle_game_credits
        self.world.tiles.append(tiles.Bar('exit.PNG', (10*64, 6*64), -90))
        self.world.tiles[-1].collision_response = self.handle_game_exit
        
    def handle_game_start(self, tile, ctile, norm, other):
        #TODO: level
        print "start game"
        self.app.Push(LevelRotator())
        self.restart()
        
    def handle_game_exit(self, tile, ctile, norm, other):
        #TODO: level
        print "game exit"
        self.app.PopAll()
        
    def handle_game_info(self, tile, ctile, norm, other):
        #TODO: level
        print "game info"
        self.app.Push(Info(None))

    def handle_game_editor(self, tile, ctile, norm, other):
        #TODO: level
        print "editor"
##        self.app.Push(Editor())

    def handle_game_credits(self, tile, ctile, norm, other):
        #TODO: level
        print "credits"
        self.app.Push(Credits(None))

    def handle_game_restart(self, tile, ctile, norm, other):
        self.restart()


class Info(LevelBase):
      
    def build_level(self):
        self.bg = "bgmosaic.PNG"
        self.ball = ball.Ball('test_ball.PNG', (100,100))
        self.world.set_size((768, 768))
        self.world.tiles.append(tiles.Bar('exit.PNG', (64, 64), 90))
        self.world.tiles[-1].collision_response = self.my_coll_handler

class Credits(LevelBase):
      
    def build_level(self):
        self.bg = "bgmosaic.PNG"
        self.ball = ball.Ball('test_ball.PNG', (100,100))
        self.world.set_size((768, 768))
        self.world.tiles.append(tiles.Bar('exit.PNG', (64, 64), 90))
        self.world.tiles[-1].collision_response = self.my_coll_handler

class MyMenu(LevelBase):
    
    def __init__(self):
        super(MyMenu, self).__init__('menu.pkl')
        
    def enter(self, app):
        super(MyMenu, self).enter(app)
        screen = self.app.screen
        self.blackness = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA).convert(screen)
        self.blackness.set_alpha(255)
        self.fade_in = True
        self.fade_out = False
        
    def build_level(self):
        #TODO: level
        self.bg = "menusplash.PNG"
        self.ball.hit_threshold = 1.1 # never break
        self.world.tiles.append(tiles.NonCollidingTile('plunge.png', (400, 128)))
        
        #self.world.tiles.append(tiles.Bar('exit.PNG', (2*64, 2*64), 0))
        #self.world.tiles[-1].collision_response = self.handle_game_exit
        
    def on_render(self):
        if self.fade_in:
            self.blackness.set_alpha( self.blackness.get_alpha() - 1.5 )
            if self.blackness.get_alpha == 0:
                self.fade_in = False
        if self.fade_out:
            self.blackness.set_alpha( self.blackness.get_alpha() + 1.5 )
            if self.blackness.get_alpha() >= 255:
                self.app.Push(LevelRotator())
                self.restart()
        dt = min(self.clock.tick(), 20)
        #print "tick", dt
        
        angle = self.angle + self.delta_angle
        self.ball.update(angle, dt)
        
        if not self.debug:
            self.view.world_rect.center = self.ball.rect.center
        
        self.view.draw_rot(angle)
        
        if self.debug:
            cx, cy = self.ball.rect.center
            wx, wy = self.view.world_rect.center
            dx, dy = ((-wx+self.view.half_view_x), (-wy+self.view.half_view_y))
            for norm in self.ball.debug_normals:
                pygame.draw.line(self.view.surface, (255,255,255), (cx+dx, cy+dy), (cx+dx+30*norm[0], cy+dy+30*norm[1]))
            self.view.surface.blit(self.ball.image, (cx+dx-self.ball.rect.width/2, cy+dy-self.ball.rect.height/2))
            for tile in self.world.tiles:
                if len(tile.collider.vertices):
                    px, py = tile.rect.center
                    pointlist = [(cx+px+dx, cy+py+dy)for cx, cy in tile.collider.vertices ]
                    pygame.draw.polygon(self.view.surface, (0,255,0), pointlist)
            
        else:
            
            self.view.surface.blit(self.ball.image, (self.view.half_view_x-self.ball.rect.width/2, self.view.half_view_y-self.ball.rect.height/2))
        self.app.screen.blit(self.blackness, (0, 0))

    def handle_game_start(self, tile, ctile, norm, other):
        #TODO: level
        print "start game"
        self.app.Push(LevelRotator())
        self.restart()
        
    def handle_game_exit(self, tile, ctile, norm, other):
        #TODO: level
        print "game exit"
        self.app.PopAll()
        
    def collect_coin(self, tile, ctile, norm, other):
##        print "going to collect coin"
        try:
            self.world.tiles.remove(tile)
            self.world.collision_tiles.remove(ctile)
##            print "collected a coin", tile, other
            self.fade_out = True
            self.fade_in = False
        except:
            pass
        
    def my_coll_handler(self, tile, ctile, norm, other):
            # called when exit tile is hit
            # only exit when all coins are eaten
            self.app.Pop()
        
