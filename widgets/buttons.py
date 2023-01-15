
import pygame, os,  time
from .tools import write_on_screen


COLORS = {
'b_ntc':(250,250,250),
'b_htc':(250,250,0),
'b_ctc':(0,100,0),
}
HIGHLIGHT_BLUE = 36,130,140

class SimpleButton:
    def __init__(self,pos, action,text, dimensions, normal_rectcolor = (200,200,200), highlighted_rectcolor = HIGHLIGHT_BLUE, textcolor =(0,0,0), font= 15  ):
        self.action = action
        self.clicked = False
        self.dimensions = dimensions
        self.pos = pos
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.width = self.dimensions[0]
        self.height = self.dimensions[1]
        self.text = text
        self.font = font
        self.clicked = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.highlighted_rectcolor = highlighted_rectcolor
        self.normal_rectcolor = normal_rectcolor
        self.textcolor = textcolor
        self.highlighted = False
        self.rect_color = self.normal_rectcolor

    def show(self, window, mouse_pos, events):
        if self.highlighted:
            self.rect_color = self.highlighted_rectcolor
        else:
            self.rect_color = self.normal_rectcolor
        self.pos = self.x,self.y
        self.dimensions = self.width,self.height
        text_pos = self.x + self.width*.2  , self.y + self.height*.25
        self.rect = pygame.Rect(self.pos,self.dimensions)
        pygame.draw.rect(window,self.rect_color,self.rect,0)
        write_on_screen(self.text, text_pos, window, self.textcolor,self.font)
        self.mouse_interaction(mouse_pos, events)




    def mouse_interaction(self, mouse_pos, events):
        if self.rect.collidepoint(mouse_pos):
            self.highlighted = True
            for ev in events:
                if ev.type == pygame.MOUSEBUTTONDOWN and self.clicked == False:
                    if ev.button == 1 or ev.button == 3:
                        self.clicked = True
                        self.action()
                        time.sleep(.1)
                else:
                    self.clicked = False
        else:
            self.highlighted = False

class TaskBarButton(SimpleButton):
    def __init__(self,pos, action,text, dimensions = (100,20) ):
        SimpleButton.__init__(self,pos, action,text, dimensions)
    def update_pos(self,vector_x):
        new_x = self.pos[0] + vector_x
        self.pos = (new_x, self.pos[1])
    def mouse_interaction(self, mouse_pos, events):
        if self.rect.collidepoint(mouse_pos):
            self.highlighted = True
            for ev in events:
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if ev.button == 1 or ev.button == 3:
                        self.action[0]((self.action[1]))
        else:
            self.highlighted = False

#--------------------------------------------------------------------------------------------------------------------------
class TransparentNoRectButton:
    '''
    A transparent button with no rect
    '''
    def __init__(self,pos, action,text, dimensions, normal_textcolor, highlighted_textcolor, clicked_textcolor ,  font= 30,border = 5, border_radius = 10,showrect = False):
        self.action = action
        self.clicked = False
        self.dimensions = dimensions
        self.pos = pos
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.width = self.dimensions[0]
        self.height = self.dimensions[1]

        self.text = text
        self.font = font
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.highlighted_textcolor = highlighted_textcolor
        self.clicked_textcolor = clicked_textcolor
        self.normal_textcolor = normal_textcolor
        self.current_textcolor = self.normal_textcolor




        self.border = border
        self.border_radius = border_radius
        self.highlighted = False
        self.showrect = showrect
    def show(self, window, mouse_pos, events):
        text_pos = self.x  , self.y + self.height*.25
        self.rect = pygame.Rect(self.pos,self.dimensions)
        write_on_screen(self.text, text_pos, window, self.current_textcolor,self.font)
        self.mouse_interaction(mouse_pos, events)

    def transform(self, textcolor ):
        # change color depending on state
        self.current_textcolor = textcolor


    def mouse_interaction(self, mouse_pos, events):
        imaginary_rect =  pygame.Rect(mouse_pos[0], mouse_pos[1], 10,10 )
        # mouse hover
        if imaginary_rect.colliderect(self.rect):
            self.highlighted = True
            self.transform(self.highlighted_textcolor)
            for ev in events:
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if ev.button == 1 or ev.button == 3:
                        self.transform(self.clicked_textcolor )
                        self.clicked = True
                        self.action()
                else:
                    self.clicked = False
        # no mouse interaction, normal
        else:
            self.transform(self.normal_textcolor )
            self.highlighted = False

class UIbutton(TransparentNoRectButton):
    def __init__(self,pos, action,text ,size = (300,70) ):
        TransparentNoRectButton.__init__(self, pos,action, text, size,COLORS['b_ntc'], COLORS['b_htc'], COLORS['b_ctc'], font = 40)
