import pygame
import sys
class Screen:
    def __init__(self, size = (1000,700), fps = 40):
        pygame.init()
        self.running = True
        self.name = ""
        self.size = size
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.events = pygame.event.get()
        self.window = pygame.display.set_mode(self.size  ,pygame.NOFRAME)
        pygame.display.set_caption(self.name)

    def screen_backend(self):
        self.clock.tick(self.fps)
        pygame.display.set_caption(self.name)

    def quit_event(self  ):
            # anticipate a quit event

        for ev in self.events:
            if ev.type == pygame.QUIT:
                sys.exit()

    def dipslay_widgets(self):
        pass
    def show(self):
        while self.running:
            self.display_widgets()
            self.events = pygame.event.get()
            self.screen_backend()

            self.quit_event()
            pygame.display.update()
            continue
