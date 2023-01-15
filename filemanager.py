import os

from kivy.uix.filechooser import FileChooser,FileChooserIconLayout,FileChooserListLayout
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from config import Config

class MainManager(ScreenManager):
    def get_last_path(self):
        last_path = Config.read('filemanager','last_path',data_if_none = 'C:/')
        if os.path.isdir(last_path):
            return last_path
        else:
            return os.getcwd()

    def exit_app(self,app):
        app.stop()
    def open_map(self,selection,app):
        # check if it is of .pmp format
        if selection == []:
            return
        path = selection[0]
        print(path)
        if path[-4:] == '.pmp':
             Config.write('file_cache','open_this',path)

    def save_last_path(self,path):
         Config.write('filemanager','last_path',path)

    def select_directory(self,path):
        Config.write('file_cache','directory_to_create_map',path)

class FileManager(FileChooser):
    pass
class MainScreen(Screen):
    pass

class OpenFileApp(App):
    def build(self):
        kv_file = Builder.load_file('kvs/filemanager.kv')
        return kv_file
class DirectoryChooser(App):
    def build(self):
        kv_file = Builder.load_file('kvs/dirchooser.kv')
        return kv_file
if __name__ == '__main__':
    DirectoryChooser().run()
    pass
