import pygame
import os
from os import path
import orb
import random

pygame.init()

#변수 설정 및 초기화
#색
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

#UI 크기
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1280
BUTTON_SIZE = 60

#폰트
title = pygame.font.SysFont("arial", 60, True, False)
mode = pygame.font.SysFont("arial", BUTTON_SIZE//4, True, False)
name = pygame.font.SysFont("arial", 15, True, False)

#파이게임 설정
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Solar System Simulator")
clock = pygame.time.Clock()
event = pygame.event.poll()
done=False

# assets 경로 설정
current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'assets')

# 사운드
pygame.mixer.music.load(path.join(assets_path, 'bgm.mp3'))
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(loops=-1)

#게임변수
# Solar System 1 / Inner Planet 2 / Jupiter 3
MODE = 1
for i in orb.Planet :
    i.R *= SCREEN_HEIGHT//20
    i.R += 100
    if i.satelite :
        for j in i.satelite :
            j.R *= 50
            if i.inner : j.R += 0.1*i.size
            else : j.R+=0.6*i.size
cx=SCREEN_WIDTH//2
cy=SCREEN_HEIGHT//2

#이미지
s={} #Solar System Mode
b={} #Inner Planet Mode
s['Mercury'] = pygame.image.load(path.join(assets_path, 'sMercury.png')) 
b['Mercury'] = pygame.image.load(path.join(assets_path, 'bMercury.png'))
s['Venus'] = pygame.image.load(path.join(assets_path, 'svenus.png'))
b['Venus'] = pygame.image.load(path.join(assets_path, 'bVenus.png'))
s['Earth'] = pygame.image.load(path.join(assets_path, 'sEarth.png'))
b['Earth'] = pygame.image.load(path.join(assets_path, 'bEarth.png'))
s['Mars']= pygame.image.load(path.join(assets_path, 'sMars.png'))
b['Mars'] = pygame.image.load(path.join(assets_path, 'bMars.png'))
s['Saturn']= pygame.image.load(path.join(assets_path, 'Saturn.png'))
s['Jupiter'] = pygame.image.load(path.join(assets_path, 'Jupiter.png'))
s['Moon'] = pygame.image.load(path.join(assets_path, 'sMoon.png'))
b['Moon'] = pygame.image.load(path.join(assets_path, 'bMoon.png'))
s['Io'] =  pygame.image.load(path.join(assets_path, 'sIo.jpg'))
b['Io'] = pygame.image.load(path.join(assets_path, 'bIo.jpg'))
s['Europa'] = pygame.image.load(path.join(assets_path, 'sEuropa.jpg'))
b['Europa'] = pygame.image.load(path.join(assets_path, 'bEuropa.jpg'))
s['Ganymede'] = pygame.image.load(path.join(assets_path, 'sGanymede.jpg'))
b['Ganymede']= pygame.image.load(path.join(assets_path, 'bGanymede.jpg'))
s['Callisto'] = pygame.image.load(path.join(assets_path, 'sCallisto.jpg'))
b['Callisto'] = pygame.image.load(path.join(assets_path, 'bCallisto.jpg'))
s['Titan'] = pygame.image.load(path.join(assets_path, 'Titan.png'))
Sun = pygame.image.load(path.join(assets_path, "Sun.png"))

# 배경 관련 변수, 함수
r=[random.randint(1,254) for i in range(200)]
g=[random.randint(1,254) for i in range(200)]
B=[random.randint(1,254) for i in range(200)]
X=[random.randint(0,SCREEN_WIDTH) for i in range(200)]
Y=[random.randint(0,SCREEN_HEIGHT) for i in range(200)]
L=[random.randint(0,1) for i in range(200)]

def twinkleinit(r, g, B, X, Y, L) :
    for i in range(200) :
        r[i] = random.randint(1,254)
        g[i] = random.randint(1,254)
        B[i] = random.randint(1,254)
        X[i] = random.randint(0,SCREEN_WIDTH)
        Y[i] = random.randint(0,SCREEN_HEIGHT)
        L[i] = random.randint(0,1)
        
def star(r, g, B, X, Y, L) :
    for i in range(200) :
        pygame.draw.circle(screen, (r[i], g[i], B[i]),[X[i], Y[i]],1,0)
        if L[i] :
            if r[i]==254 : L[i]=0
            else : r[i]+=1
            if g[i]==254 : L[i]=0
            else : g[i]+=1
            if B[i]==255 : L[i]=0
            else : B[i]+=1
        else : 
            if r[i]==1 : L[i]=1
            else : r[i]-=1
            if g[i]==1 : L[i]=1
            else : g[i]-=1
            if B[i]==1 :  L[i]=1
            else : B[i]-=1

# 게임 반복 구간
while not done:
    # 이벤트 반복 구간
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos[0], event.pos[1]
            if y < 1.5*BUTTON_SIZE and x > SCREEN_WIDTH - 6*BUTTON_SIZE :
                if x < SCREEN_WIDTH - 4*BUTTON_SIZE : 
                    if MODE == 2 :
                        # Inner to Solar
                        for i in orb.Planet:
                            if i.inner : i.R /= 3
                            if i.name == "Earth" : orb.Moon.R /= 3
                        twinkleinit(r, g, B, X, Y, L)
                        MODE = 1
                    elif MODE == 3:
                        # Jupiter to Solar
                        orb.speed -= 150
                        for i in orb.Jupiter.satelite : i.R /= 3
                        twinkleinit(r, g, B, X, Y, L)
                        MODE = 1
                elif x < SCREEN_WIDTH - 2*BUTTON_SIZE :
                    if MODE == 3 :
                        # Jupiter to Inner
                        orb.speed -= 150
                        for i in orb.Jupiter.satelite : i.R /= 3
                        for i in orb.Planet:
                            if i.inner : i.R *= 3
                            if i.name == "Earth" : orb.Moon.R *= 3
                        twinkleinit(r, g, B, X, Y, L)
                        MODE = 2
                    elif MODE == 1 :
                        # Solar to Inner
                        for i in orb.Planet:
                            if i.inner : i.R *= 3
                            if i.name == "Earth" : orb.Moon.R *= 3
                        twinkleinit(r, g, B, X, Y, L)
                        MODE = 2
                else : 
                    if MODE == 1 :
                        #Solar to Jupiter
                        orb.speed += 150
                        for i in orb.Jupiter.satelite : i.R *= 3
                        twinkleinit(r, g, B, X, Y, L)
                        MODE = 3
                    elif MODE == 2 :
                        #Inner to Jupiter
                        orb.speed += 150
                        for i in orb.Jupiter.satelite : i.R *= 3
                        for i in orb.Planet:
                            if i.inner : i.R /= 3
                            if i.name == "Earth" : orb.Moon.R /= 3
                        twinkleinit(r, g, B, X, Y, L)
                        MODE = 3
                                            
            #회전 속도 조절 파트
            if y > 1.5*BUTTON_SIZE and y < 3*BUTTON_SIZE and x > SCREEN_WIDTH - 6*BUTTON_SIZE:
                if x < SCREEN_WIDTH - 4*BUTTON_SIZE : orb.init()
                elif x < SCREEN_WIDTH - 2*BUTTON_SIZE : orb.faster()
                else : orb.slower()

    #UI
    #Button
    for i in range(1,4) : pygame.draw.line(screen, WHITE, [SCREEN_WIDTH-BUTTON_SIZE*i*2,0],[SCREEN_WIDTH-BUTTON_SIZE*i*2, BUTTON_SIZE*3],2)
    for i in range(1,3) : pygame.draw.line(screen, WHITE, [SCREEN_WIDTH-3*BUTTON_SIZE*2, BUTTON_SIZE*i*1.5], [SCREEN_WIDTH, BUTTON_SIZE*i*1.5], 2)
    screen.blit(mode.render("Jupiter", True, WHITE,),[SCREEN_WIDTH-BUTTON_SIZE*1.4, int(0.55*BUTTON_SIZE)])
    screen.blit(mode.render("Inner Planet", True, WHITE,),[SCREEN_WIDTH-BUTTON_SIZE*3.6, int(0.55*BUTTON_SIZE)])
    screen.blit(mode.render("Solar System", True, WHITE,),[SCREEN_WIDTH-BUTTON_SIZE*5.6, int(0.55*BUTTON_SIZE)])
    screen.blit(mode.render("Speed Slower", True, WHITE,),[SCREEN_WIDTH-BUTTON_SIZE*1.7, int(2.05*BUTTON_SIZE)])
    screen.blit(mode.render("Speed Faster", True, WHITE,),[SCREEN_WIDTH-BUTTON_SIZE*3.7, int(2.05*BUTTON_SIZE)])
    screen.blit(mode.render("Speed Initialize", True, WHITE,),[SCREEN_WIDTH-BUTTON_SIZE*5.75, int(2.05*BUTTON_SIZE)])
    
    #Speed Indicator
    screen.blit(mode.render("Speed : "+str(100 - orb.speed), True, WHITE,),[SCREEN_WIDTH-BUTTON_SIZE*7.5, int(2.05*BUTTON_SIZE)])

    #반짝이는 별 이미지
    star(r, g, B, X, Y, L)

    #태양, 행성, 위성 이미지 띄우기
    if MODE <3 :
        screen.blit(Sun, [cx-100, cy-100])
        screen.blit(name.render("Sun", True, WHITE), [cx, cy+100])
        if MODE == 1:
            for i in orb.Planet :
                i.location()
                pygame.draw.circle(screen, WHITE, [cx, cy], i.R, 1)
                if i.inner : screen.blit(name.render(i.name, True, WHITE), [cx+i.x, cy+i.y+0.2*i.size])
                else : screen.blit(name.render(i.name, True, WHITE), [cx+i.x, cy+i.y+0.5*i.size])
                if i.name == 'Saturn' or i.name== 'Jupiter': 
                    screen.blit(s[i.name], [cx+i.x-round(i.size/2), cy+i.y-round(i.size/2)])
                else : screen.blit(s[i.name], [cx+i.x-round(i.size/20), cy+i.y-round(i.size/20)])
                if i.satelite :
                    for j in i.satelite :
                        screen.blit(name.render(j.name, True, WHITE), [cx+i.x+j.x, cy+i.y+j.y])
                        pygame.draw.circle(screen, WHITE, [cx+i.x, cy+i.y], j.R, 1)
                        if i.name == 'Saturn' or i.name == 'Jupiter':
                            screen.blit(s[j.name], [cx+j.x+i.x-round(j.size/2), cy+j.y+i.y-round(j.size/2)])
                        else : screen.blit(s[j.name], [cx+i.x+j.x-round(j.size/20), cy+j.y+i.y-round(j.size/20)])
    
        elif MODE == 2:
            for i in orb.Planet :
                if i.inner :
                    i.location() 
                    screen.blit(b[i.name], [cx+i.x-round(i.size/2), cy+i.y-round(i.size/2)])
                    screen.blit(name.render(i.name, True, WHITE), [cx+i.x, cy+i.y+i.size/2])
                    pygame.draw.circle(screen, WHITE, [cx,cy], i.R, 1)
            screen.blit(b[orb.Moon.name], [cx+orb.Earth.x+orb.Moon.x-round(orb.Moon.size/2), cy+orb.Earth.y+orb.Moon.y-round(orb.Moon.size/2)])
            screen.blit(name.render(orb.Moon.name, True, WHITE), [cx+orb.Earth.x+orb.Moon.x, cy+orb.Earth.y+orb.Moon.y+orb.Moon.size/2])
            pygame.draw.circle(screen, WHITE, [cx+orb.Earth.x, cy+orb.Earth.y], orb.Earth.satelite[0].R, 1)
             

    elif MODE == 3:
        screen.blit(s['Jupiter'], [cx-orb.Jupiter.size//2, cy-orb.Jupiter.size//2])
        screen.blit(name.render("Jupiter", True, WHITE), [cx, cy+orb.Jupiter.size//2])
        for i in orb.Jupiter.satelite :
            i.location()
            screen.blit(b[i.name], [i.x+cx-i.size//2, i.y+cy-i.size//2])
            screen.blit(name.render(i.name, True, WHITE), [cx+i.x-0.1*i.size, cy+i.y+0.2*i.size])
            pygame.draw.circle(screen, WHITE, [cx, cy], i.R, 1)

    #제목
    if MODE == 3: screen.blit(title.render("Jupiter", True, WHITE), [SCREEN_WIDTH//2-20, 50])
    elif MODE == 2: screen.blit(title.render("Inner Planet", True, WHITE), [SCREEN_WIDTH//2-100, 50])
    else : screen.blit(title.render("Solar System", True, WHITE), [SCREEN_WIDTH//2-100, 50])
    
    pygame.display.update()
    screen.fill(BLACK)
    clock.tick(60)

    #Time Flow
    orb.time += 1/orb.speed
    
pygame.quit() 