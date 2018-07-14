import sys, pygame, itertools
from enum import Enum, unique, auto
from collections import deque, namedtuple

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

Point = namedtuple("Point", "x y")

class Snake:
    def __init__(self, x = int(kWorldWidth/2), y = int(kWorldHeight/2), direction = Direction.DOWN):
        self.direction = direction
        self.speed = 1
        self.i = 0
        assert(x-1 >= 0)
        self.__body = deque([Point(x-1,y), Point(x,y)])

    def head(self):
        return self.__body[-1]

    def body(self):
        return itertools.islice(self.__body, len(self.__body)-1)

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
        head = self.head()
        if self.direction == Direction.UP:
            head = Point(head.x, head.y - 1)
            if head.y < 0:
                head = Point(head.x, kWorldHeight - 1)

        elif self.direction == Direction.RIGHT:
            head = Point(head.x + 1, head.y)
            if head.x >= kWorldWidth:
                head = Point(0, head.y)

        elif self.direction == Direction.DOWN:
            head = Point(head.x, head.y + 1)
            if head.y >= kWorldHeight:
                head = Point(head.x, 0)

        elif self.direction == Direction.LEFT:
            head = Point(head.x - 1, head.y)
            if head.x < 0:
                head = Point(kWorldWidth - 1, head.y)

        self.__body.append(head)
        self.__body.popleft()
        

class Game:
    def __init__(self):
        self.running = True
        self.snejk = Snake()

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
    def DrawSnakePart(surface, color, pos):
        pygame.draw.rect(surface, color, (pos.x*kTileSize, pos.y*kTileSize, kTileSize, kTileSize))

    for part in g.snejk.body():
        DrawSnakePart(surface, (0, 155, 0), part)
    DrawSnakePart(surface, (255, 0, 0), g.snejk.head())

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
