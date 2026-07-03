import pygame as game
import buttons as b
import text as t
import input
from sys import exit

class Player(game.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.framesRight = [
            game.transform.scale_by(game.image.load("jogo-de-fisica/sprites/player/player_walk_right_0.png"),2).convert_alpha(),
            game.transform.scale_by(game.image.load("jogo-de-fisica/sprites/player/player_walk_right_1.png"),2).convert_alpha(),
            game.transform.scale_by(game.image.load("jogo-de-fisica/sprites/player/player_walk_right_2.png"),2).convert_alpha(),
            game.transform.scale_by(game.image.load("jogo-de-fisica/sprites/player/player_walk_right_3.png"),2).convert_alpha()
        ]
        self.framesLeft = [
            game.transform.scale_by(game.image.load("jogo-de-fisica/sprites/player/player_walk_left_0.png"),2).convert_alpha(),
            game.transform.scale_by(game.image.load("jogo-de-fisica/sprites/player/player_walk_left_1.png"),2).convert_alpha(),
            game.transform.scale_by(game.image.load("jogo-de-fisica/sprites/player/player_walk_left_2.png"),2).convert_alpha(),
            game.transform.scale_by(game.image.load("jogo-de-fisica/sprites/player/player_walk_left_3.png"),2).convert_alpha()
        ]
        self.image = self.framesRight[0]
        self.frameRight = 0
        self.frameLeft = 0
        self.toRight = False
        self.toLeft = False
        self.rect = self.image.get_rect(midbottom = (wW/2, ground_ypos))
        self.distance = 0
        self.speed = meter*1
        self.acceleration = 0
        self.i = True
        
    def move(self, dt):
        if self.speed > 0 and running:
            self.distance += self.speed * dt
            self.toRight = True
        else:
            self.toRight = False
        if self.speed < 0 and running:
            self.distance += self.speed * dt
            self.toLeft = True
        else:
            self.toLeft = False
        self.speed += self.acceleration * dt
            
    def animation(self, dt):
        if (self.toLeft and self.toRight) or (not(self.toLeft) and not(self.toRight)):
            self.image = self.framesRight[0]
        elif self.toRight:
            self.frameRight += 12 * dt
            self.image = self.framesRight[(int(self.frameRight))%4]
        else:
            self.frameLeft += 12 * dt
            self.image = self.framesLeft[(int(self.frameLeft))%4]
            
    def update(self, dt):
        self.move(dt)
        self.animation(dt)

def draw_meter_markers(distance):
    f = game.font.Font(None, 24)
    for i in range(int(distance/meter)-5, int(distance/meter)+5):
        text = f.render(convertUnits(i), False, "black").convert()
        text_rect = text.get_rect(midtop = (wW/2 + meter*i - distance, ground_ypos + 25))
        game.draw.rect(window, "black", (wW/2 + meter*i - distance, ground_ypos, 3, 20))
        window.blit(text, text_rect)

def groundMove(distance):
    for i in range(int(distance/wW)-1, 2+int(distance/wW)):
        ground = game.image.load("jogo-de-fisica/sprites/ground.png").convert()
        ground_rect = ground.get_rect(topleft = (wW*i-distance, ground_ypos))
        window.blit(ground, ground_rect)

def convertUnits(num):
    if num >= 1000000000:
        return f"{(num/1000000000):.2f}*10⁶Km"
    elif num >= 1000000:
        return f"{(num/1000000):.2f}*10³Km"
    elif num >= 1000:
        return f"{(num/1000):.2f}Km"
    else:
        return f"{num:.2f}m"
    
game.init()
wW = 800
wH = 600
window = game.display.set_mode((wW, wH))
game.display.set_caption("Simulador de física.")
clock = game.time.Clock()
fps = 120
meter = 100
running = False
ground_ypos = wH - 70

player = game.sprite.GroupSingle()
player.add(Player())

title = t.makeText("Simulador de MUV", 64, (wW/2, 40), "black", window)
restart_button = b.makeButtons("jogo-de-fisica/sprites/buttons/restart.png", (wW - 220, 100), window,2)
restart_button_text = t.makeText("Restaurar", 30, (wW - 220, 150), "black", window)
play_button = b.makeButtons("jogo-de-fisica/sprites/buttons/play.png", (wW - 140, 100), window,2)
play_button_text = t.makeText("Play", 30, (wW - 140, 150), "black", window)
pause_button = b.makeButtons("jogo-de-fisica/sprites/buttons/pause.png", (wW - 60, 100), window,2)
pause_button_text = t.makeText("Pause", 30, (wW - 60, 150), "black", window)
time_text = t.makeText("0s", 40, (wW - 140, 180), "black", window)
equation_text = t.makeText("(0m) + (1m)t + (0m)t²", 20, (wW/2, 120), "blue", window)
perDist_text = t.makeText("Dist. pecorrida: 0m", 20, (wW/2, 150), "red", window)
perTime_text = t.makeText("Tempo pecorrido: 0s", 20, (wW/2, 180), "red", window)

pos_input = input.Input((180, 80), window, "0")
pos_input_text = t.makeText("Posição", 30, (60, 80), "black", window)
speed_input = input.Input((180, 120), window, "1")
speed_input_text = t.makeText("Vel.", 30, (60, 120), "black", window)
acceleration_input = input.Input((180, 160), window, "0")
acceleration_input_text = t.makeText("Ace.", 30, (60, 160), "black", window)
time = 0


while True:
    deltaTime = clock.tick(fps) / 1000
    for event in game.event.get():
        if event.type == game.QUIT:
            game.quit()
            exit()
        if play_button.isClicked(event) and not(running):
            player.sprite.distance = float(pos_input.text)*meter
            player.sprite.speed = float(speed_input.text)*meter
            player.sprite.acceleration = float(acceleration_input.text)*meter
            equation_text.updateText(f"({convertUnits(float(pos_input.text))}) + ({convertUnits(float(speed_input.text))})t + ({convertUnits(float(acceleration_input.text)/2)})t²")
            running = True
        if pause_button.isClicked(event) and running:
            perTime_text.updateText(f"Tempo pecorrido: {time:.2f}s")
            perDist_text.updateText(f"Dist. pecorrida: {convertUnits(abs(float(pos_input.text) - float(player.sprite.distance/meter)))}")
            pos_input.text = str(int(player.sprite.distance/meter))
            speed_input.text = str(int(player.sprite.speed/meter))
            time = 0
            running = False
        if restart_button.isClicked(event) and not(running):
            perTime_text.updateText("Tempo pecorrido: 0s")
            perDist_text.updateText("Dist. pecorrida: 0m")
            pos_input.text = "0"
            speed_input.text = "1"
            acceleration_input.text = "0"
            player.sprite.distance = 0
            time = 0
        if not(running):
            pos_input.updateText(event)
            speed_input.updateText(event)
            acceleration_input.updateText(event)
            
    window.fill("lightblue")
    game.draw.rect(window, (255, 255, 0), (0,0,800,200))
    if running:
        time += deltaTime
    time_text.updateText(f"{time:.3f}s")
    
    title.showText()
    restart_button.showButton()
    restart_button_text.showText()
    pause_button.showButton()
    pause_button_text.showText()
    play_button.showButton()
    play_button_text.showText()
    time_text.showText()
    pos_input.showInput()
    pos_input_text.showText()
    speed_input.showInput()
    speed_input_text.showText()
    acceleration_input.showInput()
    acceleration_input_text.showText()
    perTime_text.showText()
    equation_text.showText()
    perDist_text.showText()
    
    groundMove(player.sprite.distance)
    draw_meter_markers(player.sprite.distance)
    player.draw(window)
    player.update(deltaTime)
    game.display.update()
    
