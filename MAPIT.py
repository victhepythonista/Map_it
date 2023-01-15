import pygame
import pyautogui
import sys
import os


from screen import Screen
from  widgets import buttons,dropdown,checkbox,tools
import filemanager
from gameframe import GameFrame
from config import Config
from colors import *
EDITOR_BG = (250,250,250)
TASKBAR_WIDGET_Y = 10
BASE_MAP_INFO = "{'name': '%s' ,'gameframe': %s ,'rects':[]}"
RECT_COLOR =  50,50,50

global SPEED,UP,DOWN,LEFT,RIGHT
SPEED = 2
UP = 0,-SPEED
DOWN = 0,SPEED
LEFT = -SPEED,0
RIGHT = SPEED,0


def save_map(name,path, gameframe_size):
    with open(path, 'w') as f:
        f.write(BASE_MAP_INFO % (name,gameframe_size))
def get_map_to_open_path():
    return Config.read('file_cache','open_this')

class Map:
    def __init__(self,file_path):
        self.gameframe = None
        self.name = None
        self.rects = None
        self.file_path = file_path
        self.is_valid = False
        self.load()
    def load(self):
        if not os.path.isfile(self.file_path):return
        with open(self.file_path, 'r') as mapfile:

            data = eval(mapfile.read())
            if type(data) == dict:
                pass

        gameframe_size = data['gameframe']
        rects =data['rects']
        self.gameframe = GameFrame(0,0,gameframe_size)
        self.gameframe.load_tiles(rects)
        self.name = data['name']
        self.is_valid = True
class Task:
    def __init__(self,map,button ):
        self.map =map
        self.button = button
        self.name = map.name
class TaskManager:
    '''
    handles the maps and switching of maps to edit
    '''
    def __init__(self):
        self.x = 0
        self.y = 50
        self.tasks = []

        self.current_task = None
        self.button_width = 100
        self.button_height = 30
        self.taskbar_width = 1000
        self.taskbar_rect = pygame.Rect(self.x,self.y,self.taskbar_width,20)
        self.load_recents()
    def close_all(self):
        for t in self.tasks:
            self.save_task(t)
            self.tasks.pop(self.tasks.index(t))
        self.current_task = None
    def load_recents(self):
        recents_list = Config.read('file_cache','recents')
        try:
            recents = eval(recents_list)
            if type(recents) == list:
                pass
        except:
            return
        for path in recents :
            self.load_map(path)

        self.remove_duplicates()
    def remove_duplicates(self):
        names  = []
        for t in self.tasks:
            if t.name not in names:
                names.append(t.name)
            else:
                self.tasks.pop(self.tasks.index(t))


    def save_task(self,task):
        with open(task.map.file_path,'w') as f:
            gf = task.map.gameframe.position

            rects= [(r.x - gf[0],r.y - gf[1],r.w,r.h) for r in task.map.gameframe.tiles]
            data = {
                'name':task.map.name,
                'gameframe':task.map.gameframe.size,
                'rects':rects,
            }
            print('saving    %s'%task.map.file_path)
            f.write(str(data))
    def save_all(self, add_to_recents =True):
        recents =[]
        for t in self.tasks:
            self.save_task(t)
            recents.append(t.map.file_path)
        recents = str(recents)
        if add_to_recents:
            Config.write('file_cache','recents',recents)

    def get_task(self,name):
        for t in self.tasks:
            if t.name == name:
                return t
    def get_new_button_pos(self):
        pos_x = self.tasks[-1].button.rect.topright[0]
        return (pos_x,self.y)


    def switch_map(self,name):
        print('[ switching map  %s]'%name)
        task  =  self.get_task(name)
        if task != None:
            self.current_task = task
    def load_map(self,path):
        map = Map(path)
        if map.is_valid:
            new_pos = (self.x,self.y) if self.tasks == [] else self.get_new_button_pos()
            button =  buttons.TaskBarButton(new_pos,[self.switch_map,map.name],map.name)
            new_task = Task(map,button)
            self.tasks.append(new_task)
            self.current_task = new_task
            print('loaded map ',map.name)
        else:
            print('could not load map',path)
        self.remove_duplicates()
    def scroll_right(self):
        pass
    def scroll_left(self):
        pass
    def show(self,window,events):
        mouse_pos = pygame.mouse.get_pos()
        if self.current_task != None:
            # display the rects
            self.current_task.map.gameframe.show(window)
            # display the current_task indicator
            button_rect = self.current_task.button.rect
            pos = button_rect.bottomleft
            pygame.draw.rect(window,(20,70,200),pygame.Rect(pos[0],pos[1],100,5),0)
        # display the taskbar background
        self.taskbar_rect = pygame.Rect(self.x,self.y,self.taskbar_width,20)
        pygame.draw.rect( window, TASKBAR_COLOR, self.taskbar_rect, 0)
        # display the taskbar buttons
        for t in self.tasks:
            t.button.show(window,mouse_pos,events)

    def move_map (self,direction):
        if self.current_task != None:

            if direction == 'up':
                self.current_task.map.gameframe.move(UP)
            elif direction == 'down':
                self.current_task.map.gameframe.move(DOWN)

            elif direction == 'left':
                self.current_task.map.gameframe.move(LEFT)
            elif direction == 'right':
                self.current_task.map.gameframe.move(RIGHT)



    @property
    def has_task(self):
        if self.tasks != []:
            return True
        return False
class App(Screen):
    def __init__(self):
        Screen.__init__(self)
        self.name = 'MAPIT  %s' %self.fps
        self.editor_on = True
        self.settings_on = False
        self.drawing = False
        self.auto_rect = False
        self.move_rect = False
        self.gameframe = None
        self.start_pos = None
        self.end_pos = None
        self.current_rect = None
        self.taskmanager = TaskManager()
        self.toolbar_buttons = [
            buttons.SimpleButton((550,TASKBAR_WIDGET_Y), self.goto, 'GoTo',(100,30)),
     
        ]

        self.dropdown = dropdown.DropDownButton((30,TASKBAR_WIDGET_Y),[
            ['scroll speed',self.change_scroll_speed],
            ['new map',self.create_new_map],
            ['open map',self.open_map],
            ['save all',self.save_all],
            ['close all tabs',self.close_all_tabs],
            ['exit',self.exit_app],

            ]
            )

        self.toolbar_rect =  pygame.Rect(0,0,self.size[0],50)
    def change_scroll_speed(self):
        self.close_dropdown()
        speed = pyautogui.prompt('New  scroll speed :')
        try:
            speed = int(speed)
            global SPEED,DOWN,RIGHT,LEFT,UP
            SPEED = speed
            UP = 0,-SPEED
            DOWN = 0,SPEED
            LEFT = -SPEED,0
            RIGHT = SPEED,0
        except:
            pyautogui.alert('wrong speed value !')


    def create_new_map(self):
        print('creating new map...........')
        self.close_dropdown()
        filemanager.DirectoryChooser().run()
        directory_selected = Config.read('file_cache','directory_to_create_map')
        if os.path.isdir(directory_selected):
            name = pyautogui.prompt('MAP NAME :')
            if name == None or name == '':
                pyautogui.alert("error creating map")
                return
            gameframe_size = pyautogui.prompt('GAMEFRAME SIZE : ','','500 500')
            gameframe_size = gameframe_size.split()
            try:
                size = int(gameframe_size[0]),int(gameframe_size[1])
            except:
                pyautogui.alert('invalid size format !')
                return


            full_path = os.path.join(directory_selected,name + '.pmp')
            save_map(name,full_path,size)
            self.taskmanager.load_map(full_path)

    def open_map(self):
        print('opening a pre-existing map..........')
        self.close_dropdown()
        filemanager.OpenFileApp().run()
        self.load_selected_map()

    def load_selected_map(self):
        path = Config.read('file_cache','open_this')
        self.taskmanager.load_map(path)
    def show_recents(self):
        print('displaying recent maps..........')
    def close_all_tabs(self):
        print('closing all tabs..................')
        self.taskmanager.close_all()
        self.close_dropdown()
    def switch_auto_rect(self):
        print('auto rect ')
    def switch_move_rect(self):
        print('switch_move_rect')
    def close_dropdown(self):
        self.dropdown.clicked = False
    def goto(self):
        # move to a certain point to the center of the screen
        if self.taskmanager.has_task:
            to = pyautogui.prompt('where to ??')
            to.replace(',','')
            to = to.split()
            try:
                x,y = int(to[0]),int(to[1])
            except:
                pyautogui.alert("Invalid format \n please use")
                return
            sx,sy =  self.size[0]/2,self.size[1]/2

            n_x,n_y = sx - x,sy -y
            self.taskmanager.current_task.map.gameframe.move_to(n_x,n_y)


 
    def show_editor_widgets(self):
        mouse_pos = pygame.mouse.get_pos()
        self.dropdown.show(self.window,self.events)

        for btn in self.toolbar_buttons:
            btn.show(self.window,mouse_pos,self.events)
    def open_settings(self):
        print('opening settings...........')

    def draw_taskbar(self):
        self.taskmanager.show(self.window,self.events)
    def draw_toolbar(self):
        pygame.draw.rect(self.window, TOOLBAR_COLOR, self.toolbar_rect, 0)
    def save_all(self):
        self.taskmanager.save_all()
    def exit_app(self):
        self.taskmanager.save_all()
        pygame.quit()
        sys.exit()

    def add_the_rect(self):
        if type(self.current_rect) == pygame.Rect and self.taskmanager.has_task:
            try:
                self.taskmanager.current_task.map.gameframe.new_tile(self.current_rect)
            except:
                pass
    def draw_current_rect_specs(self):
        if type(self.current_rect) == pygame.Rect and self.taskmanager.has_task:
            w,h = self.current_rect.w,self.current_rect.h
            tools.write_on_screen(str((w,h)), pygame.mouse.get_pos(), self.window,pygame.Color('steelblue'), 15 )

    def Drawing_Events(self):

        keys  = pygame.key.get_pressed()
        for ev in self.events:
            rect = ''
            if ev.type == pygame.MOUSEBUTTONDOWN:
                self.drawing = True
                self.start_pos = pygame.mouse.get_pos()
            if ev.type == pygame.MOUSEBUTTONUP:
                self.drawing = False
                self.end_pos = pygame.mouse.get_pos()
                self.add_the_rect()

        if keys[pygame.K_w]:
            self.taskmanager.move_map('up')
        elif keys[pygame.K_s]:
            self.taskmanager.move_map('down')
        if keys[pygame.K_d]:
            self.taskmanager.move_map('right')
        elif keys[pygame.K_a]:
            self.taskmanager.move_map('left')
    def Drawing(self):
        self.Drawing_Events()
        if self.drawing:

            curr_pos = pygame.mouse.get_pos()
            self.end_pos = curr_pos
            w,h  = self.end_pos[0] - self.start_pos[0], self.end_pos[1] - self.start_pos[1]
            self.current_rect = pygame.Rect(self.start_pos[0],self.start_pos[1],w,h)
            pygame.draw.rect(self.window,RECT_COLOR,self.current_rect,0)
            self.draw_current_rect_specs()
    def EditorDisplay(self):
        self.window.fill(EDITOR_BG)
        self.Drawing()
        self.draw_taskbar()
        self.draw_toolbar()
        self.show_editor_widgets()

    def SettingsDisplay(self):
        pass

    def display_widgets(self):
        if self.editor_on:
            self.EditorDisplay()
if __name__ == '__main__':
    App().show()
