from header import *
from level import Level
import cerealizer

class LevelBuilder(BaseState):
    """
    Engine state to allow for building levels.
    
    Move View : wasd
    Select Piece : 1 - 7
    Place Piece : Mouse-Click
    Save : o
    Save and Test : p
    
    """
    def __init__(self, levelname = None, size = (576, 576)):
        self.debug = False
        self.piece_angle = 0
        self.bg = None
        self.ball = None
        self.level = Level()    #Level Container Object
        self.size = size
        self.levelname = levelname #Level Filename
        #Palette Defines what TileTypes can be placed
        self.palette = [tiles.Tile,tiles.LeftHillLow, tiles.LeftHillHeigh, tiles.RightHillLow, tiles.RightHillHeigh, tiles.LargeHill, tiles.Bar, tiles.Circle, tiles.Coin]
        self.holding = None #Currently holding a piece?
        self.piece = None   #Temporary Piece to be Placed
        self.old_tile = False
        self.ball = None
        self.grid_step = 64
        self.grid_stepx = 64
    
    def load_level(self, levelname):
        """
        Load a level from file.
        
        levelname = level filename
        level_dir = global level directory defined in headers.py
        """
        filename = os.path.join(level_dir, levelname)
        f = open(filename, 'rb')
##        self.level = pickle.load(f)
        self.level = cerealizer.load(f)
        self.ball = ball.Ball('test_ball.PNG', self.level.ball)
        self.world = tilemap.TileMap()
        self.world.tiles.append(self.ball)
##        self.world.set_size( self.level.size )
        for t in self.level.tiles:
            name, pos, type, pointlist, angle = t
##            print t
            if type > 1:
                self.world.tiles.append(tiles.PolygonTile(name, pointlist, pos, 0))
                self.world.tiles[-1].angle_deg = angle
            else:
                self.world.tiles.append(tiles.Tile(name, pos))
        
    def save_level(self, levelname):
        """
        Save a level to file.
        """
        self.level.tiles = []
        print "saving level:", self.levelname
        print "size:", self.size
        print "num tiles:", len(self.world.tiles)
        for tile in self.world.tiles:
            name = tile.image_name
            pos = tile.rect.center
            type = tile.collision_type
            if type > 1:
                pointlist = tile.pointlist
                angle = tile.angle_deg
            else:
                pointlist = None
                angle = None
            if tile != self.ball:
                self.level.tiles.append((name, pos, type, pointlist, angle))
        self.level.ball = self.ball.rect.center
##        self.level.size = self.world.size
        self.level.bg = self.bg
        self.level.size = self.size
        print "level saving:", self.level.size
        filename = os.path.join(level_dir, levelname)
        f = open(filename, 'wb')
##        pickle.dump(self.level, f)
        cerealizer.dump(self.level, f)
        
    def get_signal_matrix(self):
        sm = super(LevelBuilder, self).get_signal_matrix()
        sm.update({
            'render' : self.on_render, 'wheeldown' : self.on_wheel_down, 'wheelup' : self.on_wheel_up
            })
        return sm
    
    #def build_level(self):
    #    for tile in self.world.tiles:
    #        coll_tile = tile.get_collision_tile()
    #        if coll_tile: # filter None
    #            self.world.collision_tiles.append(coll_tile)
      
    def enter(self, app):
        super(LevelBuilder, self).enter(app)
        #Load level or setup blank
        print self.levelname
        try: 
            self.load_level(self.levelname)
            print self.levelname, 'loaded!'
        except:
            self.world = tilemap.TileMap()
            self.world.set_size(self.size)
            self.world.set_size(self.size, (64, 64), image_name='editordefault.PNG')
            self.ball = ball.Ball('test_ball.PNG', (self.size[0]/2, self.size[1]/2))
            self.world.tiles.append(self.ball)
        #View setup
        self.view = viewport.ViewPort(self.app.screen, pygame.Rect(0, 0, 800, 600), self.world, pygame.Rect(0, 0, 800, 600), bg = self.bg)
        
        
    def on_render(self):
        self.view.draw()
        #Draw held piece
        if self.holding:
            cx, cy = self.piece.rect.center
            wx, wy = self.view.world_rect.center
            dx, dy = ((-wx+self.view.half_view_x), (-wy+self.view.half_view_y))
            if self.piece.angle_deg:
                self.view.surface.blit(self.piece.images[int(self.piece.angle_deg)][0], (cx+dx-self.piece.rect.width/2, cy+dy-self.piece.rect.height/2))
            else:
                self.view.surface.blit(self.piece.images[0][0], (cx+dx-self.piece.rect.width/2, cy+dy-self.piece.rect.height/2))
            
        
        
    def on_mouse_down(self, pos, button):
        #Place tile
        if self.holding:
            if self.piece == self.ball:
                screen_rect = pygame.Rect(self.ball.rect)
                screen_rect.inflate_ip(5,5)
                screen_rect.center = pos
                if len(self.view.get_at(screen_rect))>1:
                    return
            if pygame.key.get_mods() & pygame.KMOD_CAPS:
                print "snap to grid"
                px, py = self.piece.rect.center
                self.piece.rect.center = ((px/self.grid_stepx)*self.grid_stepx+self.grid_stepx/2, (py/self.grid_step)*self.grid_step+self.grid_step/2)
            if self.old_tile:
                self.old_tile = False
            else:
                self.world.tiles.append(self.piece)
                
            self.holding = None
            self.piece = None
        else:
            self.piece = self.view.get_at(pygame.Rect(pos, (0,0)))
            if len(self.piece)>0:
                self.piece = self.piece[0]
                self.holding = True
                self.old_tile = True
            else:
                self.piece = None
            print "selected:", self.piece
                  
        
    def on_mouse_motion(self, pos, rel, buttons, only_last):
        if self.holding:
            px, py = pos
            wx, wy = self.view.world_rect.center
            if self.piece != self.ball:
                self.piece.rect = pygame.Rect(self.piece.images[self.piece.angle_deg][1])
            self.piece.rect.center = (px-(-wx+self.view.half_view_x), py+(wy-self.view.half_view_y))
    
    def on_wheel_down(self, pos):
        self.grid_step /= 2
        if self.grid_step == 1:
            self.grid_step = 128
        pygame.display.set_caption("grid_stepx:"+str(self.grid_stepx)+" grid_stepy:"+str(self.grid_step))
        
        
    def on_wheel_up(self, pos):
        self.grid_stepx /= 2
        if self.grid_stepx == 1:
            self.grid_stepx = 128
        pygame.display.set_caption("grid_stepx:"+str(self.grid_stepx)+" grid_stepy:"+str(self.grid_step))
    
    
            
    def on_key_down(self, unicode, key, mod):
        super(LevelBuilder, self).on_key_down(unicode, key, mod)
        if key==pygame.K_a:
            self.view.world_rect.move_ip(-64, 0)
        if key==pygame.K_d:
            self.view.world_rect.move_ip(64, 0)
        if key==pygame.K_s:
            self.view.world_rect.move_ip(0, -64)
        if key==pygame.K_w:
            self.view.world_rect.move_ip(0, 64)
        
        if key==pygame.K_q and not isinstance(self.holding,  tiles.Tile) and self.holding:
            self.piece.angle_deg += 5
            self.piece.angle_deg %= 360
        if key==pygame.K_e and not isinstance(self.holding, tiles.Tile) and self.holding:
            self.piece.angle_deg -= 5
            self.piece.angle_deg %= 360
        if key==pygame.K_1:
            self.holding = self.palette[0]
            self.piece = self.holding("default.PNG", (0, 0))
        if key==pygame.K_2:
            self.holding = self.palette[1]
            self.piece = self.holding("lefthill_low.PNG", (0, 0), 0)
        if key==pygame.K_3:
            self.holding = self.palette[2]
            self.piece = self.holding("lefthill_high.PNG", (0, 0), 0)
        if key==pygame.K_4:
            self.holding = self.palette[3]
            self.piece = self.holding("righthill_low.PNG", (0, 0), 0)
        if key==pygame.K_5:
            self.holding = self.palette[4]
            self.piece = self.holding("righthill_high.PNG", (0, 0), 0)
        if key==pygame.K_6:
            self.holding = self.palette[5]
            self.piece = self.holding("largehill.PNG", (0, 0), 0)
        if key==pygame.K_7:
            self.holding = self.palette[6]
            self.piece = self.holding("exit.PNG", (0, 0), 0)
        if key==pygame.K_8:
            self.holding = self.palette[6]
            self.piece = self.holding("bar.PNG", (0, 0), 0)
        if key==pygame.K_9:
            self.holding = self.palette[8]
            self.piece = self.holding("coin.PNG", (0, 0))
        if key==pygame.K_0:
            self.holding = self.palette[7]
            self.piece = self.holding("circle.PNG", (0, 0))
        if key==pygame.K_p:
            self.save_level(self.levelname)
            testlevel = LevelBase(self.levelname)
            self.app.Push(testlevel)
        if key == pygame.K_b:
            self.piece = self.ball
            self.holding = True
            self.old_tile = True
        if key==pygame.K_o:
            self.save_level(self.levelname)
        if key==pygame.K_DELETE:
            if self.holding:
                if self.piece in self.world.tiles and self.piece != self.ball:
                    self.world.tiles.remove(self.piece)
                self.piece = None
                self.holding = None
        
        if self.holding:
            px, py = pygame.mouse.get_pos()#self.piece.rect.center
            wx, wy = self.view.world_rect.center
            self.piece.rect = pygame.Rect(self.piece.images[self.piece.angle_deg][1])
            self.piece.rect.center = (px-(-wx+self.view.half_view_x), py+(wy-self.view.half_view_y))
            
            
            
if '__main__' == __name__:
    name, width, height = 'default.pkl', 576, 576
    if sys.argv[1]:
        name = sys.argv[1]
    if len(sys.argv)>3 and sys.argv[2] and sys.argv[3]:
        width, height = int(sys.argv[2]), int(sys.argv[3])
    app = engine.Engine(LevelBuilder(name, (width, height)))
    app.run()