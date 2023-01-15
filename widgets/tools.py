import pygame


def write_on_screen(  message, position, window, color, fontsize, font = 'Consolas'):
    #### _this function  writes  a message to the user
    pygame.font.init()
    try:
        mess_obj = pygame.font.SysFont(font, fontsize)
    except:
        print('no such font as %s'%font, '...')
        mess_obj = pygame.font.SysFont('consolas', fontsize)
    mess_render = mess_obj.render(message, 20, color)
    window.blit(mess_render, position)
 
