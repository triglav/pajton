import sys, pygame, itertools, random
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

random.seed()

pygame.init()
screen = pygame.display.set_mode([kWidth, kHeight], pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption("Tajga ~ Pajton")

font = pygame.font.SysFont('Arial', 15)

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
        self.speed = 2
        self.i = 0
        self.parts = deque([Point(x,y)])
        self.Grow()

    def head(self):
        return self.parts[-1]

    def body(self):
        return itertools.islice(self.parts, len(self.parts)-1)

    def Grow(self):
        self.__do_grow = True

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

        self.parts.append(head)
        if self.__do_grow:
            self.__do_grow = False
        else:
            self.parts.popleft()
        

class Game:
    @unique
    class State(Enum):
        RUNNING = auto()
        PAUSE = auto()
        END_GAME = auto()
        QUIT = auto()

    def __init__(self):
        self.state = Game.State.RUNNING
        self.snejk = Snake()
        self.SpawnApple()
        self.score = 0

    def SpawnApple(self):
        while 1:
            self.apple = Point(
                random.randint(0, kWorldWidth - 1),
                random.randint(0, kWorldHeight - 1))
            if self.apple not in self.snejk.parts:
                break

    def Update(self):
        if self.state == Game.State.RUNNING:
            self.snejk.Update()
            if self.snejk.head() in self.snejk.body():
                print("BANG - END OF THE GAME")
                self.state = Game.State.END_GAME
            if self.snejk.head() == self.apple:
                print("HAM HAM HAM")
                self.score += 1
                self.snejk.Grow()
                self.SpawnApple()
        
    def PumpEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = Game.State.QUIT
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = Game.State.QUIT
                elif event.key == pygame.K_RIGHT:
                    self.snejk.TurnRight()
                elif event.key == pygame.K_LEFT:
                    self.snejk.TurnLeft()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_PAUSE or event.key == pygame.K_p:
                    if self.state == Game.State.RUNNING:
                        print("PAUSED")
                        self.state = Game.State.PAUSE
                    elif self.state == Game.State.PAUSE:
                        print("RESUMED")
                        self.state = Game.State.RUNNING

gejm = Game()

label_paused = font.render("PAUSED", False, (255, 255, 255), (0, 0, 0))
label_game_over = font.render("GAME OVER", False, (255, 255, 255), (0, 0, 0))

def center_label_position(screen, label):
    lw, lh = label.get_size()
    w, h = screen.get_size()
    return (w - lw) / 2, (h - lh) / 2

def Draw(surface, g):
    def DrawTile(surface, color, pos):
        pygame.draw.rect(surface, color, (pos.x*kTileSize, pos.y*kTileSize, kTileSize, kTileSize))

    def DrawSnake(surface, snake):
        d = 50.0 / len(snake.parts)
        c = 130.0
        for part in snake.body():
            DrawTile(surface, (0, int(c), 0), part)
            c += d
        DrawTile(surface, (220, 0, 0), snake.head())

    DrawTile(surface, (155, 155, 0), g.apple)
    DrawSnake(surface, g.snejk)
    # Score
    score_text = font.render("Score: " + str(g.score), False, (255, 255, 255), (0, 0, 0))
    screen.blit(score_text, (0, 0))
    # Labels
    if g.state == Game.State.PAUSE:
        screen.blit(label_paused, center_label_position(screen, label_paused))
    elif g.state == Game.State.END_GAME:
        screen.blit(label_game_over, center_label_position(screen, label_game_over))

next_tick = pygame.time.get_ticks()
while gejm.state != Game.State.QUIT:
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
