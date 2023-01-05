import pygame
import numpy as np

# 게임 윈도우 크기
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700

# 색 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

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
pygame.display.set_caption("Drawing")

# 윈도우 생성
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 게임 화면 업데이트 속도
clock = pygame.time.Clock()

# 게임 종료 전까지 반복
done = False

# poly: 4 x 3 matrix
poly = np.array( [[0, 0, 1], [150, 0, 1], [150, 20, 1], [0, 20, 1]])
poly = poly.T # 3x4 matrix 

cor = np.array([10, 10, 1])

degree = [10, 0, 0]
ctrj = 2
clockwise = None

# 게임 반복 구간
while not done:
# 이벤트 반복 구간
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN :
            if event.key==pygame.K_LEFT : 
                clockwise = True
            elif event.key==pygame.K_RIGHT:
                clockwise = False
            elif event.key==pygame.K_UP:
                if ctrj <= 1: ctrj += 1
            elif event.key==pygame.K_DOWN:
                if ctrj >=1 : ctrj -= 1
        elif event.type == pygame.KEYUP :
            clockwise = None

    if clockwise : 
        degree[2-ctrj] -= 1
        print(degree)
    elif clockwise == False : 
        degree[2-ctrj] += 1
        print(degree)

    # 윈도우 화면 채우기
    screen.fill(WHITE)

    # 다각형 그리기
    # poly: 3xN 

    H = Tmat(100, 600) @ Tmat(10, 10) @ Rmat(degree[0]) @ Tmat(-10, -10) 
    pp = H @ poly
    corp = H @ cor

    H1 = H @ Tmat(150, 0)
    if ctrj == 1: H1 = H1 @ Rmat(degree[1])
    pp1 = H1 @ poly 
    corp1 = H1 @ cor

    H2 = H1 @ Tmat(150, 0)
    if ctrj == 0 : H2 = H2 @ Rmat(degree[2])
    pp2 = H2 @ poly
    corp2 = H2 @ cor

    # print(pp.shape, pp, pp.T )

    q = pp[0:2, :].T # N x 2 matrix
    q1 = pp1[0:2, :].T
    q2 = pp2[0:2, :].T
    pygame.draw.polygon(screen, RED, q, 4)
    pygame.draw.circle(screen, BLACK, corp[:2], 17, 0)
    pygame.draw.circle(screen, WHITE, corp[:2], 7, 0)
    pygame.draw.polygon(screen, RED, q1, 4)
    pygame.draw.circle(screen, BLACK, corp1[:2], 17, 0)
    pygame.draw.circle(screen, WHITE, corp1[:2], 7, 0)
    pygame.draw.polygon(screen, RED, q2, 4)
    pygame.draw.circle(screen, BLACK, corp2[:2], 17, 0)
    pygame.draw.circle(screen, WHITE, corp2[:2], 7, 0)

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(60)

# 게임 종료
pygame.quit()