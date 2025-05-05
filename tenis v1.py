import pygame
from random import randint as r
from settings import *

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
screen_color = WHITE
Speed_Players = 5
pu,pd,au,ad = False,False,False,False
ava_mx,ava_my = True, True
out1_font = pygame.font.Font(None,50)
Stop_Game = False

def ranl():
    if (r(0,1) == 0): ndx = False 
    else: ndx = True
    if (r(0,1) == 0): ndy = False 
    else: ndy = True
    return (ndx,ndy)

dx,dy = ranl()

class Player():
    def __init__(self,pos_x,pos_y,width,height,speed,Pcolor):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.speed = speed
        self.Pcolor = Pcolor
        self.score = 0
    def PublicPlayer(self):
        pygame.draw.rect(screen,self.Pcolor,(self.pos_x,self.pos_y,self.width,self.height))
    def MovementUp(self):
        self.pos_y -= self.speed
    def MovementDown(self):
        self.pos_y += self.speed
    def MoveOn(self,pos_x,pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

class Ball():
    def __init__(self,pos_x,pos_y,speed,radius,Bcolor):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed = speed
        self.radius = radius
        self.Bcolor = Bcolor
        self.normal_speed = speed
    def PublicBall(self):
        pygame.draw.circle(screen,self.Bcolor,(self.pos_x,self.pos_y),float(self.radius))
    def MovementUp(self):
        self.pos_y -= self.speed
    def MovementDown(self):
        self.pos_y += self.speed
    def MovementLeft(self):
        self.pos_x -= self.speed
    def MovementRight(self):
        self.pos_x += self.speed
    def BackPosCenter(self):
        self.pos_x = WIDTH_CENTER
        self.pos_y = HEIGHT_CENTER

Player1 = Player(WIDTH_CENTER,HEIGHT_CENTER,10,100,Speed_Players,(0,0,0))
Player2 = Player(WIDTH_CENTER,HEIGHT_CENTER,10,100,Speed_Players,(0,0,0))
Player1.MoveOn(0,(HEIGHT-Player1.height) // 2)
Player2.MoveOn(WIDTH-Player2.width,(HEIGHT-Player2.height) // 2)

Game_Ball = Ball(WIDTH_CENTER,HEIGHT_CENTER,3,10,(0,0,0))

END_GAME = False
while not END_GAME:
    #logic
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            END_GAME = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                pu = True
            if event.key == pygame.K_s:
                pd = True
            if event.key == pygame.K_UP:
                au = True
            if event.key == pygame.K_DOWN:
                ad = True
            if event.key == pygame.K_SPACE:
                Stop_Game = not Stop_Game
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                pu = False
            if event.key == pygame.K_s:
                pd = False
            if event.key == pygame.K_UP:
                au = False
            if event.key == pygame.K_DOWN:
                ad = False
    if not Stop_Game:
        if pu and (Player1.pos_y >= 0): Player1.MovementUp()
        if pd and (Player1.pos_y+Player1.height <= HEIGHT): Player1.MovementDown()
        if au and (Player2.pos_y >= 0): Player2.MovementUp()
        if ad and (Player2.pos_y+Player2.height <= HEIGHT): Player2.MovementDown()
        if (Game_Ball.pos_y-Game_Ball.radius <= 0) or (Game_Ball.pos_y+Game_Ball.radius >= HEIGHT):
            dy = not dy
        if (Game_Ball.pos_x-Game_Ball.radius <= Player1.width):
            if (Game_Ball.pos_y+Game_Ball.radius >= Player1.pos_y) and (Game_Ball.pos_y-Game_Ball.radius <= Player1.pos_y+Player1.height):
                dx = not dx
                Game_Ball.speed += 0.25
            else:
                Game_Ball.BackPosCenter()
                Player2.score += 1
                Game_Ball.speed = Game_Ball.normal_speed
                dx,dy = ranl()
        if (Game_Ball.pos_x+Game_Ball.radius >= WIDTH-Player2.width):
            if (Game_Ball.pos_y+Game_Ball.radius >= Player2.pos_y) and (Game_Ball.pos_y-Game_Ball.radius <= Player2.pos_y+Player2.height):
                dx = not dx
                Game_Ball.speed += 0.25
            else:
                Game_Ball.BackPosCenter()
                Player1.score += 1
                Game_Ball.speed = Game_Ball.normal_speed
                dx,dy = ranl()

        if dx and dy:
            Game_Ball.MovementDown()
            Game_Ball.MovementRight()
        if not dx and dy:
            Game_Ball.MovementLeft()
            Game_Ball.MovementDown()
        if not dx and not dy:
            Game_Ball.MovementLeft()
            Game_Ball.MovementUp()
        if dx and not dy:
            Game_Ball.MovementUp()
            Game_Ball.MovementRight()
        if (Player1.score > 6) or (Player2.score > 6):
            END_GAME = True
    
    out1_text = out1_font.render(f'{Player1.score}',True,(0,0,0))
    out2_text = out1_font.render(f'{Player2.score}',True,(0,0,0))
    
    #draw
    screen.fill(pygame.color.Color(screen_color))
    pygame.draw.rect(screen,(0,0,0),(WIDTH_CENTER-5,0,10,HEIGHT))
    pygame.draw.rect(screen,(0,0,0),(0,0,WIDTH,1))
    text1_rect = out1_text.get_rect(center=(WIDTH // 4,80))
    text2_rect = out2_text.get_rect(center=((WIDTH // 4)*3,80))
    screen.blit(out1_text,text1_rect)
    screen.blit(out2_text,text2_rect)
    Player1.PublicPlayer()
    Player2.PublicPlayer()
    Game_Ball.PublicBall()
    if Stop_Game:
        pause_out = out1_font.render('Pause',True,WHITE,BLACK)
        text_pause = pause_out.get_rect(center=(WIDTH_CENTER,HEIGHT_CENTER))
        screen.blit(pause_out,text_pause)
    pygame.display.update()
    clock.tick(60)

pygame.quit()