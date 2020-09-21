import pygame, os
os.environ["SDL_VIDEO_CENTERED"] = "1"

pygame.init()

class Window:
    """
    A window provider that uses PyGame.
    
    """

    def __init__(self, config, name):
        self.config = config
        self.window = pygame.display.set_mode(config.size, pygame.DOUBLEBUF | pygame.OPENGL)
        pygame.display.set_caption(name)
    
    def start(self, update_func):
        """
        Start the main loop of the window.

        Parameters
        ----------
        updateFunc : function
            The function that calls the OpenGL calls.
        
        """
        self.update_func = update_func
        done = False
        clock = pygame.time.Clock()
        pygame.display.flip()
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            
            pressed = pygame.key.get_pressed()
            alt_pressed = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
            if pressed[pygame.K_ESCAPE] or (alt_pressed and pressed[pygame.K_F4]):
                done = True
                break
            
            self.update_func()
            pygame.display.flip()
            clock.tick(self.config.fps)
    
        pygame.display.quit()