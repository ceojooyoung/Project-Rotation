import pygame
import os
import numpy as np
import time

pygame.init()

# 게임 윈도우 크기
WINDOW_WIDTH = 1000
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
background = pygame.image.load(os.path.join(assets_path, "background.jpg"))

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

poly = np.array( [[0, 0, 1], [250, 7, 1], [0, 14, 1]])
poly2 = np.array( [[0, 0, 1], [0, 7, 1], [250, 7, 1]])
poly = poly.T
poly2 = poly2.T
S = Tmat(center[0]-10, center[1]-7) @  Tmat(10, 7) @ Rmat(0) @ Tmat(-10, -7)
S1 = Tmat(center[0]-10, center[1]-7) @  Tmat(10, 7) @ Rmat(120) @ Tmat(-10, -7)
S2 = Tmat(center[0]-10, center[1]-7) @  Tmat(10, 7) @ Rmat(240) @ Tmat(-10, -7)
pp = S @ poly
pp1 = S1 @ poly
pp2 = S2 @ poly
pp3 = S @ poly2
pp4 = S1 @ poly2
pp5 = S2 @ poly2
q = pp[0:2, :].T
q1 = pp1[0:2, :].T
q2 = pp2[0:2, :].T
q3 = pp3[0:2, :].T
q4 = pp4[0:2, :].T
q5 = pp5[0:2, :].T


# 게임 반복 구간
while not done:
    # 이벤트 반복 구간
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # 윈도우 화면 채우기
    screen.fill(WHITE)
    screen.blit(background, [0, 0])

    S = S @ Tmat(10, 7) @ Rmat(1.5) @ Tmat(-10, -7)
    S1 = S1 @ Tmat(10, 7) @ Rmat(1.5) @ Tmat(-10, -7)
    S2 = S2 @ Tmat(10, 7) @ Rmat(1.5) @ Tmat(-10, -7)

    pp = S @ poly
    pp1 = S1 @ poly
    pp2 = S2 @ poly

    q = pp[0:2, :].T
    q1 = pp1[0:2, :].T
    q2 = pp2[0:2, :].T

    pp3 = S @ poly2
    pp4 = S1 @ poly2
    pp5 = S2 @ poly2

    q3 = pp3[0:2, :].T
    q4 = pp4[0:2, :].T
    q5 = pp5[0:2, :].T

    pygame.draw.polygon(screen, (102, 102, 102), [[475, 400], [525, 400], [525, 700], [475, 700]], 0)
    pygame.draw.polygon(screen, (153, 153, 153), [[478, 400], [522, 400], [522, 700], [478, 700]], 0)
    pygame.draw.polygon(screen, (204, 204, 204), [[484, 400], [515, 400], [515, 700], [484, 700]], 0)
    pygame.draw.polygon(screen, WHITE, [[490, 400], [510, 400], [510, 700], [490, 700]], 0)
    pygame.draw.line(screen, (102, 102, 102), [475, 700], [525, 700], 5)
    pygame.draw.line(screen, (102, 102, 102), [475, 400], [525, 400], 5)
    pygame.draw.polygon(screen, (102, 102, 102), q, 0)
    pygame.draw.polygon(screen, (102, 102, 102), q1, 0)
    pygame.draw.polygon(screen, (102, 102, 102), q2, 0)
    pygame.draw.polygon(screen, (204, 204, 204), q3, 0)
    pygame.draw.polygon(screen, (204, 204, 204), q4, 0)
    pygame.draw.polygon(screen, (204, 204, 204), q5, 0)
    pygame.draw.circle(screen, BLACK, [center[0], center[1]], 20)
    pygame.draw.circle(screen, WHITE, [center[0], center[1]], 12)


    # 화면 업데이트
    pygame.display.flip()

    # 초당 60 프레임으로 업데이트
    clock.tick(60)

# 게임 종료
pygame.quit()