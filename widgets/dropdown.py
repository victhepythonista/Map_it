

import pygame
from .buttons import SimpleButton
from .tools import write_on_screen
BUTTON_NORMAL_COLOR = 150,150,150
BUTTON_CLICKED_COLOR = 36,130,140
TEXT_COLOR = 10,10,10
DROPDOWN_RECT_COLOR = 100,200,100
def load_image(path):
    return pygame.image.load(path)



class DropDownButton:
    def __init__(self,pos,pre_button_list, clicked_image = None,normal_image = None,dropdown_width = 200,dropdown_height = 400,text= 'Options'):
        self.button_in_dropdown_height = 20
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.button_width = 100
        self.button_height = 30
        self.dropdown_width = dropdown_width
        self.dropdown_height = (self.button_in_dropdown_height * len(pre_button_list)) if (len(pre_button_list) != 0) else 50
        self.text = text
        self.text_pos = self.x+ (self.button_width*.1),self.y +(self.button_height*.1)
        self.pre_button_list = pre_button_list
        self.buttons_list = [ ]
        self.clicked = False
        self.clicked_image = None if clicked_image == None else load_image(clicked_image)
        self.normal_image = None if normal_image == None else load_image(normal_image)
        self.button_rect = pygame.Rect(self.pos[0],self.pos[1], self.button_width,self.button_height)
        self.dropdown_rect = pygame.Rect(self.pos[0],self.pos[1] + self.button_height,self.dropdown_width,self.dropdown_height)
        self.create_buttons()
    def create_buttons(self):
        number = len(self.pre_button_list )
        if number == 0:
            number = 1
        button_height = self.button_in_dropdown_height
        button_width = self.dropdown_width
        base_x = self.dropdown_rect.x
        base_y = self.dropdown_rect.y
        for info in self.pre_button_list :
            text = info[0]
            action = info[1]
            index = self.pre_button_list.index(info)
            x = base_x
            y = base_y + (index * button_height)
            width = button_width
            height = button_height

            button = SimpleButton((x,y), action,text,(width,height))
            self.buttons_list.append(button)



    def get_clicked(self, mouse_pos, events):

        if self.button_rect.collidepoint(mouse_pos):
            for ev in events:
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if ev.button == 1 or ev.button == 3:
                        self.clicked = True if self.clicked == False else False
    def update_rects(self):
        self.button_rect = pygame.Rect(self.pos[0],self.pos[1], self.button_width,self.button_height)
    def show(self,window,events):
        self.update_rects()
        mouse_pos = pygame.mouse.get_pos()
        self.get_clicked(mouse_pos,events)
        if self.clicked:
            for btn in self.buttons_list:
                btn.show(window, mouse_pos,events)
            if self.clicked_image :
                window.blit(self.clicked_image, self.pos)
            else:
                pygame.draw.rect(window,BUTTON_CLICKED_COLOR,self.button_rect,0)
            pygame.draw.rect(window,DROPDOWN_RECT_COLOR,self.dropdown_rect,2)
            for b in self.buttons_list:
                b.show(window, mouse_pos, events)
        else:
            if self.normal_image :
                window.blit(self.normal_image, self.pos)
            else:
                pygame.draw.rect(window,BUTTON_NORMAL_COLOR,self.button_rect,0)
        write_on_screen(self.text, self.text_pos,window,TEXT_COLOR,15)
