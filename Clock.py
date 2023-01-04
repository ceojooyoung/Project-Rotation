import pygame
import os
import numpy as np
import time

pygame.init()

# 게임 윈도우 크기
WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 800

# 색 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# assets 경로 설정
current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'assets')

# 이미지 로드
background=pygame.image.load(os.path.join(assets_path, "background.png"))

font = pygame.font.SysFont("arial", 40, True, False)

center = np.array([WINDOW_WIDTH//2, WINDOW_HEIGHT//2])

def Rmat(deg):
    radian = np.deg2rad(deg)
    c = np.cos(radian)
    s = np.sin(radian)
    R = np.array( [[ c, -s, 0], [s, c, 0], [0, 0, 1] ] )
    return R
def Tmat(a,b):
    H = np.eye(3)
    H[0,2] = a
    H[1,2] = b
    return H

# Pygame 초기화
pygame.init()

# 윈도우 제목
pygame.display.set_caption("Pygame")

# 윈도우 생성
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 게임 화면 업데이트 속도
clock = pygame.time.Clock()

done = False

now = time.localtime(time.time())
ds=(now.tm_sec-1)*6-90
dm=round(now.tm_min+1*6+0.1*ds)-90
dh=((now.tm_hour+1)%12)*30+0.5*(dm)-90

poly = np.array( [[0, 0, 1], [250, 7, 1], [0, 14, 1]])
poly = poly.T
S = Tmat(center[0]-10, center[1]-7) @  Tmat(10, 7) @ Rmat(ds) @ Tmat(-10, -7) 
pp = S @ poly
q = pp[0:2, :].T

poly1 = np.array( [[0, 0, 1], [250, 0, 1], [250, 10, 1], [0, 10, 1]])
poly1 = poly1.T
M = Tmat(center[0]-10, center[1]-5) @  Tmat(10, 5) @ Rmat(dm) @ Tmat(-10, -5)
pp1 = M @ poly1
q1 = pp1[0:2, :].T

poly2 = np.array( [[0, 0, 1], [150, 0, 1], [150, 14, 1], [0, 14, 1]])
poly2 = poly2.T
H = Tmat(center[0]-10, center[1]-7) @  Tmat(10, 7) @ Rmat(dh) @ Tmat(-10, -7)
pp2 = H @ poly2
q2 = pp2[0:2, :].T
print(dh, dm, ds)

# 게임 반복 구간
while not done:
    # 이벤트 반복 구간
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    now = time.localtime(time.time())
    ds=now.tm_sec
    dm=now.tm_min
    dh=now.tm_hour
    date = str(dh)+":"+str(dm)+" "+str(ds)

    # 윈도우 화면 채우기
    screen.fill(WHITE)
    screen.blit(background, [center[0]-300,center[1]-300])

    S = S @  Tmat(10, 7) @ Rmat(0.1) @ Tmat(-10, -7) 
    pp = S @ poly
    q = pp[0:2, :].T

    M = M @  Tmat(10, 5) @ Rmat(1/600) @ Tmat(-10, -5) 
    pp1 = M @ poly1
    q1 = pp1[0:2, :].T

    H = H @  Tmat(10, 7) @ Rmat(1/36000) @ Tmat(-10, -7) 
    pp2 = H @ poly2
    q2 = pp2[0:2, :].T

    pygame.draw.polygon(screen, BLACK, q2, 0)
    pygame.draw.polygon(screen, BLACK, q1, 0)
    pygame.draw.polygon(screen, RED, q, 0)
    pygame.draw.circle(screen, BLACK, [center[0], center[1]], 20, 0)

    screen.blit(font.render(date, True, BLACK), [WINDOW_WIDTH-200, 50])
    
    # 화면 업데이트
    pygame.display.flip()

    # 초당 60 프레임으로 업데이트
    clock.tick(60)

# 게임 종료
pygame.quit()