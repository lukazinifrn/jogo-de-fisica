import pygame as game
from sys import exit

class Player(game.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = game.image.load("./player.png").convert()
        self.rect = self.image.get_rect(midbottom = (wW/2, ground_ypos))
        self.speed = 5
    def move(self):
        keys = game.key.get_pressed()
        if keys[game.K_d] or keys[game.K_RIGHT]:
            self.rect.x += self.speed
        if keys[game.K_a] or keys[game.K_LEFT]:
            self.rect.x -= self.speed
    def update(self):
        self.move()

game.init()
wW = 800
wH = 400
window = game.display.set_mode((wW, wH))
game.display.set_caption("Simulador de física.")
clock = game.time.Clock()
fps = 60
font = game.font.Font(None, 50)

ground = game.image.load("./ground.png").convert()
ground_ypos = wH - 70
ground_rect = ground.get_rect(topleft = (0, ground_ypos))

player = game.sprite.GroupSingle()
player.add(Player())

while True:
    for event in game.event.get():
        if event.type == game.QUIT:
            game.quit()
            exit()
    window.fill("lightblue")
    window.blit(ground, ground_rect)
    player.draw(window)
    player.update()
    
    game.display.update()
    clock.tick(fps)
