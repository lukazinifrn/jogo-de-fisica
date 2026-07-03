import pygame

class Input:
    def __init__(self, pos: tuple, surface: pygame.surface.Surface, defaultValue: str):
        self.font = pygame.font.Font(None, 24)
        self.rect = pygame.Rect(0, 0, 120, 30)
        self.rect.center = pos
        self.surface = surface
        self.text = defaultValue
        self.image = self.font.render(self.text, False, "black")
        self.clicked = False
        
    def showInput(self):
        pygame.draw.rect(self.surface, "white", self.rect)
        self.surface.blit(self.image, (self.rect.x + 7, self.rect.y + 7))
        
    def verifyInput(self) -> bool:
        valid = "1234567890"
        if self.text[0] in "-+":
            if len(self.text) > 1 and self.text[1] == ".":
                return False
        else:
            if self.text[0] not in valid:
                return False
        valid += "."
        canPoint = True
        for i in self.text[1:]:
            if i == ".":
                if canPoint:
                    canPoint = False
                else:
                    return False
            elif i not in valid:
                return False
        return True
                
    def updateText(self, event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
            else:
                self.clicked = False
        if event.type == pygame.KEYDOWN and self.clicked:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if self.text == "0":
                    if event.unicode == ".":
                        self.text = "0."
                    else:
                        self.text = event.unicode
                else:
                    self.text += event.unicode

        if not(len(self.text)): self.text = "0"
        if not(self.verifyInput()): self.text = "0"
        if len(self.text) > 1 and (float(self.text) >= 10000000 or float(self.text) <= -10000000): self.text = self.text[:-1]
        self.image = self.font.render(self.text, False, "black")
    
    def getValue(self):
        return float(self.text)
    
if __name__ == "__main__":
    from sys import exit
    pygame.init()
    window = pygame.display.set_mode((400,400))
    test = Input((100,100), window, "0")
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            test.updateText(event)
        test.showInput()
                
        pygame.display.update()
    # WORKS!