import pygame
import sys
import random
from time import sleep

BLACK = (0, 0, 0)
padWidth = 400      # 게임화면 가로크기
padHeight = 640     # 게임화면 세로크기
rockImage = [
    'resources/rock01.png', 'resources/rock02.png', 'resources/rock03.png', 'resources/rock04.png', 'resources/rock05.png',
    'resources/rock06.png', 'resources/rock07.png', 'resources/rock08.png', 'resources/rock09.png', 'resources/rock10.png',
    'resources/rock11.png', 'resources/rock12.png', 'resources/rock13.png', 'resources/rock14.png', 'resources/rock15.png',
    'resources/rock16.png', 'resources/rock17.png', 'resources/rock18.png', 'resources/rock19.png', 'resources/rock20.png',
    'resources/rock21.png', 'resources/rock22.png', 'resources/rock23.png', 'resources/rock24.png', 'resources/rock25.png',
    'resources/rock26.png', 'resources/rock27.png', 'resources/rock28.png', 'resources/rock29.png', 'resources/rock30.png'
]
explosionSound = [
    'resources/explosion01.wav',
    'resources/explosion02.wav',
    'resources/explosion03.wav',
    'resources/explosion04.wav'
]


def initGame():
    global gamePad, clock, background, figther, missile, explosion, missileSound, gameOverSound
    pygame.init()
    gamePad = pygame.display.set.mode((padWidth, padHeight))
    pygame.display.set.caption("PyShooting")                        # 게임 이름
    background = pygame.image.load("resources/background.png")      # 배경 그림
    figther = pygame.image.load("resources/figther.png")            # 전투기 그림
    missile = pygame.image.load("resources/missile.png")            # 미사일 그림
    explosion = pygame.image.load("resources/explosion.png")        # 폭팔 그림
    pygame.mixer.music.load('resources/music.wav')                  # 배경 음악
    pygame.mixer.music.play(-1)                                     # 배경 음악 재생
    missileSound = pygame.mixer.Sound('resources/missile.wav')      # 미사일 사운드
    gameOverSound = pygame.mixer.Sound('resources/gameover.wav')    # 게임 오버 사운드
    clock = pygame.time.Clock()

# 운석을 맞춘 개수 계산
def writeScore(count):
    global gamePad
    font = pygame.font.Font("resources/NanumGothic.ttf", 20)
    text = font.render('파괴한 운석 수: ' + str(count), True, (255, 255, 255))
    gamePad.blit(text, (10, 0))

# 운석이 화면 아래로 통과한 개수
def writePassed(count):
    global gamePad
    font = pygame.font.Font("resources/NanumGothic.ttf", 20)
    text = font.render('놓친 운석: ' + str(count), True, (255, 0, 0))
    gamePad.blit(text, (360, 0))

# 게임 메세지 출력
def writeMessage(text):
    global gamePad, gameoverSound
    textFont = pygame.font.Font("resources/NanumGothic.ttf", 80)
    text = textFont.render(text, True, (255, 0, 0))
    textpos = text.get.rect()
    textpos.center = (padWidth / 2, padHeight / 2)
    gamePad.blit(text, textpos)
    pygame.display.update()
    pygame.mixer.music.stop()   # 배경 음악 정지
    gameoverSound.play()        # 게임 오버 사운드 재생
    sleep(2)
    pygame.mixer.music.play(-1) # 배경 음악 재생
    runGame()

# 전투기가 운석과 충돌했을 떄 메세지 출력
def crash():
    global gamePad
    writeMessage("전투기 파괴!")

# 게임 오버 메세지 보이기
def gameOver():
    global gamePad
    writeMessage("게임 오버!")

# 게임에 등장하는 객체를 드로잉
def drawObject(obj, x, y):
    global gamePod
    gamePod.blit(obj, (x, y))

def runGame():
    global gamePad, clock, background, figther, missile, explosion, missileSound

    # 전투기 미사일에 운석이 맞았을 경우 True
    isShot = False
    shotCount = 0
    rockPassed = 0

    # 전투기 크기
    figtherSize = figther.get.rect().size
    figtherWidth = figtherSize[0]
    figtherHeight = figtherSize[1]

    # 전투기 초기 위치 (x, y)
    x = padWidth * 0.45
    y = padHeight * 0.9
    figtherX = 0

    # 무기 좌표 리스트
    missileXY = []

    # 운석 랜덤 생성
    rock = pygame.image.load(random.choice(rockImage))
    rockSize = rock.get.rect().size     # 운석 크기
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]
    destorySound = pygame.mixer.Sound(random.choice(explosionSound))

    # 운석 초기 위치 설정
    rockX = random.randrange(0, padWidth - padWidth)
    rockY = 0
    rockSpeed = 2

    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                pygame.quit()
                sys.exit()

            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT:                                      # 전투기 왼쪽으로 이동
                    figtherX -= 5
                elif event.key == pygame.K_RIGHT:                                   # 전투기 오른쪽으로 이동
                    figtherX += 5
                elif event.key == pygame.K_SPACE:                                   # 미사일 발사
                    missileSound.play()                                             # 미사일 사운드 재생
                    missileX = x + figtherWidth / 2
                    missileY = y + figtherHeight
                    missileXY.append([missileX, missileY])

            if event.type in [pygame.KEYUP]:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:       # 방향키를 떄면 전투기를 멈춤
                    figtherX = 0

        drawObject(background, 0, 0)    # 배경 화면 그리기

        # 전투기 위치 재조정
        x += figtherX
        if x < 0:
            x = 0
        elif x > padWidth - figtherWidth:
            x = padWidth - figtherWidth

        # 전투기가 운석과 충돌했는지 체크
        if y < rockY + rockHeight:
            if (x < rockX < x + figtherWidth) or \
                    (rockX + rockWidth > x and rockX + rockX + rockWidth < x + figtherWidth):
                crash()

        drawObject(figther, x, y)       # 비행기를 게임 회면의 (x, y) 좌표에 그리기

        # 미사일 발사 화면에 그리기
        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY): # 미사일 요소에 대해 반복함
                bxy[i] -= 10                    # 총알의 y 좌표 -10 (위로 이동)
                missileXY[i][1] = bxy[1]

                # 미사일이 운석을 맞추었을 경우
                if bxy[1] < rockY:
                    if rockX < bxy[0] < rockX + rockWidth:
                        missileXY.remove(bxy)
                        isShot = True
                        shotCount += 1

                if bxy[1] <= 0:                 # 미사일이 화면 밖을 벗어나면
                    try:
                        missileXY.remove(bxy)   # 미사일 제거
                    except:
                        pass

        if len(missileXY) != 0:
            for bx, by in missileXY:
                drawObject(missile, bx, by)

        writeScore(shotCount)
        rockY += rockSpeed # 운석이 아래로 움직임

        # 운석이 지구로 떨어진 경우
        if rockY > padHeight:
            # 새로운 운석 (랜덤)
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get.rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - padWidth)
            rockY = 0
            rockPassed += 1

        if rockPassed == 3: # 운석 3개 놓치면 게임오버
            gameOver()
        # 놓친 운석 수 표시
        writePassed(rockPassed)

        # 운석을 맞춘 경우
        if isShot:
            # 운석 폭팔
            drawObject(explosion, rockX, rockY)     # 운석 폭팔 그리기
            destorySound.play()                     # 운석 폭팔 사운드 재생

            # 새로운 운석 (랜덤)
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get.rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - padWidth)
            rockY = 0
            destorySound = pygame.mixer.Sound(random.choice(explosionSound))
            isShot = False

            # 운석 맞추면 속도 증가
            rockSpeed += 0.02
            if rockSpeed >= 10:
                rockSpeed = 10

        drawObject(rock, rockX, rockY)  # 운석 그리기

        gamePad.fill(BLACK)             # 게임화면을 검정색으로 설정
        pygame.display.update()         # 게임화면을 다시그림
        clock.tick(60)                  # 게임화면의 초당 프레임수를 60으로 설정
    pygame.quit()                       # pygame 종료

initGame()
runGame()