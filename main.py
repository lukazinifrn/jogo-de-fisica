import pygame as game
import buttons as b
import text as t
import input
from sys import exit

# Player Config 

class Player(game.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.framesRight = [
            game.transform.scale_by(game.image.load("./sprites/player/player_walk_right_0.png"),2).convert_alpha(),
            game.transform.scale_by(game.image.load("./sprites/player/player_walk_right_1.png"),2).convert_alpha(),
            game.transform.scale_by(game.image.load("./sprites/player/player_walk_right_2.png"),2).convert_alpha(),
            game.transform.scale_by(game.image.load("./sprites/player/player_walk_right_3.png"),2).convert_alpha()
        ]
        self.framesLeft = [
            game.transform.scale_by(game.image.load("./sprites/player/player_walk_left_0.png"),2).convert_alpha(),
            game.transform.scale_by(game.image.load("./sprites/player/player_walk_left_1.png"),2).convert_alpha(),
            game.transform.scale_by(game.image.load("./sprites/player/player_walk_left_2.png"),2).convert_alpha(),
            game.transform.scale_by(game.image.load("./sprites/player/player_walk_left_3.png"),2).convert_alpha()
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

# Operational functions
def draw_meter_markers(distance):
    f = game.font.Font(None, 24)
    for i in range(int(distance/meter)-5, int(distance/meter)+5):
        text = f.render(convertUnits(i, 3), False, "black").convert()
        text_rect = text.get_rect(midtop = (wW/2 + meter*i - distance, ground_ypos + 25))
        game.draw.rect(window, "black", (wW/2 + meter*i - distance, ground_ypos, 3, 20))
        window.blit(text, text_rect)

def groundMove(distance):
    for i in range(int(distance/wW)-1, 2+int(distance/wW)):
        ground = game.image.load("./sprites/ground.png").convert()
        ground_rect = ground.get_rect(topleft = (wW*i-distance, ground_ypos))
        window.blit(ground, ground_rect)

def convertUnits(num, d):
    if num >= 1000000000:
        return f"{(num/1000000000):.{d}f}*10⁶Km"
    elif num >= 1000000:
        return f"{(num/1000000):.{d}f}*10³Km"
    elif num >= 1000:
        return f"{(num/1000):.{d}f}Km"
    else:
        return f"{num:.{d}f}m"

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

# Input mark animation
MARKFLIP = game.USEREVENT + 1
game.time.set_timer(MARKFLIP, 500)
markflip = False

## Texts
# Home
home_title = t.makeText("Escolha o que simular", 64, (wW/2, 80), "black", window)

# MUV 
title = t.makeText("Simulador de MUV", 64, (wW/2, 40), "black", window)
time_text = t.makeText("0s", 40, (wW - 140, 180), "black", window)
equation_text = t.makeText("(0m) + (1m)t + (0m)t²", 20, (wW/2, 120), "blue", window)
perDist_text = t.makeText("Dist. pecorrida: 0m", 20, (wW/2, 150), "red", window)
perTime_text = t.makeText("Tempo pecorrido: 0s", 20, (wW/2, 180), "red", window)

## Buttons
# Home
muv_button = b.makeButtons("./sprites/buttons/muv.png", (wW/2 - 150, wH/2), window, 4)
muv_button_text = t.makeText("MUV", 36, (wW/2 - 150, wH/2 + 82), "black", window)
ql_button = b.makeButtons("./sprites/buttons/ql.png", (wW/2 + 150, wH/2), window, 4)
ql_button_text = t.makeText("Queda livre", 36, (wW/2 + 150, wH/2 + 82), "black", window)

# MUV
restart_button = b.makeButtons("./sprites/buttons/restart.png", (wW - 220, 100), window,2)
restart_button_text = t.makeText("Restaurar", 30, (wW - 220, 150), "black", window)
play_button = b.makeButtons("./sprites/buttons/play.png", (wW - 140, 100), window,2)
play_button_text = t.makeText("Play", 30, (wW - 140, 150), "black", window)
pause_button = b.makeButtons("./sprites/buttons/pause.png", (wW - 60, 100), window,2)
pause_button_text = t.makeText("Pause", 30, (wW - 60, 150), "black", window)

## Input
# MUV
pos_input = input.Input((180, 80), window, "0")
pos_input_text = t.makeText("Posição", 30, (60, 80), "black", window)
speed_input = input.Input((180, 120), window, "1")
speed_input_text = t.makeText("Vel.", 30, (60, 120), "black", window)
acceleration_input = input.Input((180, 160), window, "0")
acceleration_input_text = t.makeText("Ace.", 30, (60, 160), "black", window)

time = 0

# Gamestates
home = True
muv = False
ql = False


while True:
    # Deltatime logic
    deltaTime = clock.tick(fps) / 1000
    for event in game.event.get():
        if event.type == game.QUIT:
            game.quit()
            exit()
        if event.type == MARKFLIP:
            markflip = not markflip
        if muv:
            if play_button.isClicked(event) and not(running):
                pos_input.clicked = False
                speed_input.clicked = False
                acceleration_input.clicked = False
                player.sprite.distance = float(pos_input.text)*meter
                player.sprite.speed = float(speed_input.text)*meter
                player.sprite.acceleration = float(acceleration_input.text)*meter
                equation_text.updateText(f"({convertUnits(float(pos_input.text), 2)}) + ({convertUnits(float(speed_input.text), 2)})t + ({convertUnits(float(acceleration_input.text)/2, 2)})t²")
                running = True
            if pause_button.isClicked(event) and running:
                perTime_text.updateText(f"Tempo pecorrido: {time:.2f}s")
                perDist_text.updateText(f"Dist. pecorrida: {convertUnits(abs(float(pos_input.text) - float(player.sprite.distance/meter)), 2)}")
                pos_input.text = f"{player.sprite.distance/meter:.1f}"
                speed_input.text = f"{player.sprite.speed/meter:.1f}"
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
    
    if home:
        window.fill("yellow")

        home_title.showText()
        muv_button.showButton()
        muv_button_text.showText()
        ql_button.showButton()
        ql_button_text.showText()

    if muv:
        if running:
            time += deltaTime
        time_text.updateText(f"{time:.3f}s")
        window.fill("lightblue")
        game.draw.rect(window, (255, 255, 0), (0,0,800,200))
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
        pos_input.showMark(markflip)
        speed_input.showInput()
        speed_input_text.showText()
        speed_input.showMark(markflip)
        acceleration_input.showInput()
        acceleration_input_text.showText()
        acceleration_input.showMark(markflip)
        perTime_text.showText()
        equation_text.showText()
        perDist_text.showText()
        
        groundMove(player.sprite.distance)
        draw_meter_markers(player.sprite.distance)
        player.draw(window)
        player.update(deltaTime)
    game.display.update()
    
