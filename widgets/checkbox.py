import pygame

from .tools import write_on_screen
class CheckBox:
    def __init__(self,pos,size,action,text):
        self.x = pos[0]
        self.y = pos[1]
        self.w = size
        self.h = size
        self.action = action
        self.text = text
        self.on = False
        self.pos_factor = .1
        self.size_factor = 1-(self.pos_factor*2)
        self.outer_rect = pygame.Rect(self.x,self.y,self.w,self.h)
        self.inner_rect = pygame.Rect(self.x + (self.w*self.pos_factor),self.y + (self.h*self.pos_factor), self.w*self.size_factor,self.h*self.size_factor)
        self.inner_rect_color = 36,130,140
        self.outer_rect_color = pygame.Color('white')
        self.text_position = self.outer_rect.topright[0] ,self.y
        self.text_color = 36,130,140
    def mouse_interaction(self, mouse_pos, events):
        if self.outer_rect.collidepoint(mouse_pos):
            for ev in events:
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if ev.button == 1 or ev.button == 3:
                        self.action()
                        self.on = True if (self.on == False) else False


    def show(self,window,events):
        mouse_pos = pygame.mouse.get_pos()
        self.mouse_interaction(mouse_pos,events)
        if self.on:

            pygame.draw.rect(window,self.inner_rect_color,self.inner_rect,0)
        pygame.draw.rect(window,self.outer_rect_color,self.outer_rect,1)
        write_on_screen(self.text,self.text_position,window,self.text_color,15)
