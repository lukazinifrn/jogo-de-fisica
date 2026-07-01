import pygame

class makeButtons(pygame.sprite.Sprite):
    def __init__(self, image:str, pos:tuple, surface:pygame.surface, scale:float = 1) -> None:
        super().__init__()
        self.image = pygame.transform.scale_by(pygame.image.load(image), scale)
        self.rect = self.image.get_rect(center = pos)
        self.click = True
        self.surface = surface
    
    def isClicked(self, event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
            return True
    
    def showButton(self) -> None:
        self.surface.blit(self.image, self.rect)

# EXAMPLE
if __name__ == "__main__":
    from sys import exit
    pygame.init()
    screen = pygame.display.set_mode((800, 400))
    test = makeButtons("sprites/play.png", (200, 200), screen, 2)
    a = makeButtons("sprites/howtoplay.png", (600, 200), screen, 2)
    
    state1 = True
    state2 = False
    
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()
                
        screen.fill("black")
        
        if state1:
            test.showButton()
            if test.isClicked():
                print("Hello World!")
                state1 = False
                state2 = True
        
        if state2:
            a.showButton()
            if a.isClicked():
                print("Olá mundo!")
                state2 = False
                state1 = True
        
        pygame.display.update()
        # WORKS!