import sys, pygame
from enum import Enum, unique, auto

kWidth = 800
kHeight = 600

kTileSize = 20
kWorldWidth = 40
kWorldHeight = 30

kTicksPerSecond = 25
assert 1000 % kTicksPerSecond == 0, "(1000 / kTicksPerSecond) should result in zero"

kSkipTicks = 1000 / kTicksPerSecond
kMaxFrameSkip = kTicksPerSecond / 5

pygame.init()
screen = pygame.display.set_mode([kWidth, kHeight], pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption("Tajga ~ Pajton")

@unique
class Direction(Enum):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()

class Snake:
    def __init__(self, x, y, direction = Direction.DOWN):
        self.pos_x = x
        self.pos_y = y
        self.direction = direction
        self.speed = 1
        self.i = 0

    def Update(self):
        self.i += 1
        if self.i < self.speed:
            return
        self.i = 0
        self.__move()

    def TurnRight(self):
        if self.direction == Direction.UP:
            self.direction = Direction.RIGHT
        elif self.direction == Direction.RIGHT:
            self.direction = Direction.DOWN
        elif self.direction == Direction.DOWN:
            self.direction = Direction.LEFT
        elif self.direction == Direction.LEFT:
            self.direction = Direction.UP
    
    def TurnLeft(self):
        if self.direction == Direction.UP:
            self.direction = Direction.LEFT
        elif self.direction == Direction.LEFT:
            self.direction = Direction.DOWN
        elif self.direction == Direction.DOWN:
            self.direction = Direction.RIGHT
        elif self.direction == Direction.RIGHT:
            self.direction = Direction.UP

    def __move(self):
        if self.direction == Direction.UP:
            self.pos_y -= 1
            if self.pos_y < 0:
                self.pos_y = kWorldHeight - 1

        elif self.direction == Direction.RIGHT:
            self.pos_x += 1
            if self.pos_x >= kWorldWidth:
                self.pos_x = 0

        elif self.direction == Direction.DOWN:
            self.pos_y += 1
            if self.pos_y >= kWorldHeight:
                self.pos_y = 0

        elif self.direction == Direction.LEFT:
            self.pos_x -= 1
            if self.pos_x < 0:
                self.pos_x = kWorldWidth - 1
        

class Game:
    def __init__(self):
        self.running = True
        self.snejk = Snake(0, 0)

    def Update(self):
        self.snejk.Update()
        
    def PumpEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.snejk.TurnRight()
                elif event.key == pygame.K_LEFT:
                    self.snejk.TurnLeft()

gejm = Game()

def Draw(surface, g):
    pygame.draw.rect(surface, (255, 0, 0), (g.snejk.pos_x*kTileSize, g.snejk.pos_y*kTileSize, kTileSize, kTileSize))

next_tick = pygame.time.get_ticks()
while gejm.running:
    loops = 0
    while pygame.time.get_ticks() > next_tick and loops < kMaxFrameSkip:
        gejm.PumpEvents()
        gejm.Update()

        next_tick += kSkipTicks
        loops += 1

    screen.fill((0, 0, 0))

    Draw(screen, gejm)

    pygame.display.flip()

pygame.quit()
