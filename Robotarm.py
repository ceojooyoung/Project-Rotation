import pygame
import numpy as np

# 게임 윈도우 크기
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700

# 색 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255) 
GRAY = ((204, 204, 204), (153, 153, 153), (102, 102, 102), (51, 51, 51))
RED = (255, 0, 0)
PINK = ((255, 51, 51), (255, 102, 102), (255, 153, 153), (255, 204, 204))
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

poly1 = np.array( [[0, 0, 1], [80, 0, 1], [80, 14, 1], [0, 14, 1]])
poly1 = poly1.T # 3x4 matrix

cor = np.array([10, 10, 1])
cor1 = np.array([7, 7, 1])

def drawgradation(p) :
    for i in range(4) : pygame.draw.polygon(screen, GRAY[3-i], p, 10-2*i)

def drawgradation1(p) :
    for i in range(4) : pygame.draw.polygon(screen, GRAY[3-i], p, 8-2*i)

def drawcircle(pos):
    for i in range(4) : pygame.draw.circle(screen, GRAY[3-i], pos, 20-2*i)
    for i in range(4) : pygame.draw.circle(screen, GRAY[i], pos, 12-2*i)

def drawcircle1(pos):
    for i in range(4) : pygame.draw.circle(screen, GRAY[3-i], pos, 16-2*i)
    for i in range(4) : pygame.draw.circle(screen, GRAY[i], pos, 12-2*i)

def drawlight(pos) :
    pygame.draw.circle(screen, RED, pos, 9)
    for i in range(4) : pygame.draw.circle(screen, PINK[i], pos, 8-2*i)

font = pygame.font.SysFont('arial', 20, True, False)

degree = [-80, 0, 0, 60]
ctrj = 2
clockwise = None
moving = False
movingtime = 0

def catch():
    pass
    global moving
    moving = True
    global movingtime 
    movingtime = 60


# 게임 반복 구간
while not done:
# 이벤트 반복 구간
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN :
            if event.key==pygame.K_LEFT and not moving: 
                clockwise = True
            elif event.key==pygame.K_RIGHT and not moving:
                clockwise = False
            elif event.key==pygame.K_UP and not moving:
                if ctrj <= 1:
                    ctrj += 1
            elif event.key==pygame.K_DOWN and not moving:
                if ctrj >= 0 :
                    ctrj -= 1
            elif event.key==pygame.K_SPACE and ctrj==-1 and not moving:
                movingtime = 60
                catch()
        elif event.type == pygame.KEYUP :
            clockwise = None
    if ctrj >= 0 :
        if clockwise : 
            degree[2-ctrj] -= 1
        elif clockwise == False : 
            degree[2-ctrj] += 1

    movingtime -=1
    if movingtime > 30 :
        degree[3]-=1
    elif 0 < movingtime<= 30 :
        degree[3]+=1
    if movingtime <=0 :
        moving = False

    # 윈도우 화면 채우기
    screen.fill(WHITE)

    # UI
    screen.blit(font.render("press Left, Right to operate motor", True, BLACK), (40, 40))
    screen.blit(font.render("press Up Down to change motor", True, BLACK), (40, 60))
    screen.blit(font.render("press Space to catch when you are controling hand", True, BLACK), (20, 80))
    
    # 회전 반영
    H = Tmat(100, 600) @ Tmat(10, 10) @ Rmat(degree[0]) @ Tmat(-10, -10) 
    pp = H @ poly
    corp = H @ cor

    H1 = H @ Tmat(150, 0)
    H1 = H1 @ Tmat(10, 10) @ Rmat(degree[1]) @ Tmat(-10, -10)
    pp1 = H1 @ poly 
    corp1 = H1 @ cor

    H2 = H1 @ Tmat(150, 0)
    H2 = H2 @ Tmat(10, 10) @ Rmat(degree[2]) @ Tmat(-10, -10)
    pp2 = H2 @ poly
    corp2 = H2 @ cor

    H3 = H2 @ Tmat(150, 0)
    H3 = H3 @ Tmat(7, 7) @ Rmat(degree[3]) @ Tmat(-7, -7)
    corp3 = H3 @ cor1
    pp3 = H3 @poly1

    H4 = H2 @ Tmat(150, 0)
    H4 = H4 @ Tmat(7, 7) @ Rmat(-degree[3]) @ Tmat(-7, -7)
    corp4 = H4 @ cor1
    pp4 = H4 @ poly1

    H5 = H3 @ Tmat(75, 0)
    H5 = H5 @ Tmat(7, 7) @ Rmat(-1.5*degree[3]) @ Tmat(-7, -7)
    corp5 = H5 @ cor1
    pp5 = H5 @poly1

    H6 = H4 @ Tmat(75, 0)
    H6 = H6 @ Tmat(7, 7) @ Rmat(1.5*degree[3]) @ Tmat(-7, -7)
    corp6 = H6 @ cor1
    pp6 = H6 @poly1

    # print(pp.shape, pp, pp.T )
    q = pp[0:2, :].T # N x 2 matrix
    q1 = pp1[0:2, :].T
    q2 = pp2[0:2, :].T
    q3 = pp3[0:2, :].T
    q4 = pp4[0:2, :].T
    q5 = pp5[0:2, :].T
    q6 = pp6[0:2, :].T

    drawgradation(q)
    drawgradation(q1)
    drawgradation(q2)
    drawgradation1(q3)
    drawgradation1(q4)
    drawgradation1(q5)
    drawgradation1(q6)

    
    drawcircle(corp[:2])
    drawcircle1(corp[:2])
    if ctrj == 2: drawlight(corp[:2])
    else : pygame.draw.circle(screen, WHITE, corp[:2], 7, 0)
    drawcircle(corp1[:2])
    drawcircle1(corp1[:2])
    if ctrj == 1 : drawlight(corp1[:2])
    else : pygame.draw.circle(screen, WHITE, corp1[:2], 7, 0)
    drawcircle(corp2[:2])
    drawcircle1(corp2[:2])
    if ctrj ==0 : drawlight(corp2[:2])
    else : pygame.draw.circle(screen, WHITE, corp2[:2], 7, 0)
    drawcircle(corp3[:2])
    drawcircle1(corp3[:2])
    drawcircle1(corp6[:2])
    drawcircle1(corp5[:2])
    if ctrj == -1 : 
        drawlight(corp3[:2])
        drawlight(corp5[:2])
        drawlight(corp6[:2])
    else : 
        pygame.draw.circle(screen, WHITE, corp3[:2], 7, 0)
        pygame.draw.circle(screen, WHITE, corp5[:2], 7, 0)
        pygame.draw.circle(screen, WHITE, corp6[:2], 7, 0)
    
    # 화면 업데이트
    pygame.display.flip()
    clock.tick(60)

# 게임 종료
pygame.quit()
