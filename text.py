import pygame

class makeText(pygame.sprite.Sprite):
    def __init__(self, text:str, size:int, pos:tuple, color:str, surface:pygame.surface) -> None:
        super().__init__()
        self.font = pygame.font.Font(None, size)
        self.text = self.font.render(text, True, color)
        self.rect = self.text.get_rect(center = pos)
        self.surface = surface
        self.color = color
        self.pos = pos
        
    def showText(self) -> None:
        self.surface.blit(self.text, self.rect)
    
    def updateText(self, new: str) -> None:
        self.text = self.font.render(new, True, self.color)
        self.rect = self.text.get_rect(center = self.pos)

# EXAMPLE
if __name__ == "__main__":
    from sys import exit
    pygame.init()
    screen = pygame.display.set_mode((800, 400))
    teste = makeText("Hello World!", 100, (400, 200), "#e6da35", screen)
    
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.fill("black")
        teste.showText()
        
        pygame.display.update()
        # WORKS!
        