import pygame

class Tile:
    def __init__(self,rect):
        self.x = rect.x
        self.y = rect.y
        self.w = rect.w
        self.h = rect.h
        self.rect = pygame.Rect(self.x,self.y,self.w,self.h)

    def move(self,speed):
        self.x += speed[0]
        self.y += speed[1]
    def show(self,window):
        self.rect = pygame.Rect(self.x,self.y,self.w,self.h)
        pygame.draw.rect(window,(50,50,50),self.rect,0)

class GameFrame:

    def __init__(self,x,y,dimensions):
        self.x = x
        self.y = y
        self.w = dimensions[0]
        self.h = dimensions[1]
        self.rect = pygame.Rect(self.x, self.y,self.w,self.h)
        self.size = (self.w,self.h)
        self.tiles = []
        self.redo_list = []
    def new_tile(self,tile):
        self.tiles.append(Tile(pygame.Rect(tile[0],tile[1],tile[2],tile[3])))
    def load_tiles(self,rects):
        for r in rects:
            self.new_tile(r )
    @property
    def position(self):
        return self.x,self.y
    def undo(self):
        if self.tiles != []:
            last =self.tiles[-1]
            self.tiles.pop(-1)
            self.redo_list.append(last)
    def redo(self):
        if self.redo_list != []:
            self.tiles.append(self.redo_list[-1])
    def move_to(self,x,y):
        self.x = x
        self.y = y
    def move(self,speed):
        # speed is a tuple containing x,y  changes
        self.x += speed[0]
        self.y += speed[1]

        for tile in self.tiles :
            tile.move(speed)


    def show_tiles(self,window):
        for tile in self.tiles:
            tile.show(window)

    def update(self):
        self.rect = pygame.Rect(self.x, self.y,self.w,self.h)

    def show(self,window):
        self.update()
        pygame.draw.rect(window, pygame.Color('blue'), self.rect, 3 )
        self.show_tiles(window)
