import pygame, sys
import constrants as cs

def getColor(element):
    if element == 0:
        return cs.WHITE
    elif isinstance(element, str):
        return cs.GREEN
    else:
        return cs.COLOR[element]

def draw_map(surface, map):
    row = len(map)
    col = len(map[0])

    for i in range(row):
        for j in range(col):
            rect = pygame.Rect(j*cs.LENGTH, (row - i - 1)*cs.LENGTH, cs.LENGTH, cs.LENGTH)
            pygame.draw.rect(surface, getColor(map[i][j]), rect)

def draw_grid(surface, map):
    row = len(map)
    col = len(map[0])

    for i in range(col+1):
        new_height = i*cs.LENGTH
        pygame.draw.line(surface, cs.BLACK, (new_height, 0), (new_height, cs.LENGTH*row), 1)

    for i in range(row+1):
        new_width = i*cs.LENGTH
        pygame.draw.line(surface, cs.BLACK, (0, new_width), (cs.LENGTH*col, new_width), 1)

def draw_path(surface, path, map):
    row = len(map)
    col = len(map[0])

    for pos in path[1]:
        rect = pygame.Rect(pos[1]*cs.LENGTH, (row - pos[0] - 1)*cs.LENGTH, cs.LENGTH, cs.LENGTH)
        pygame.draw.rect(surface, cs.GREEN, rect)

def init(map):
    cs.SCREEN_WIDTH += cs.LENGTH*len(map[0])
    cs.SCREEN_HEIGHT += cs.LENGTH*len(map)

    pygame.init()
    surface = pygame.display.set_mode((cs.SCREEN_WIDTH, cs.SCREEN_HEIGHT))
    pygame.display.set_caption("finding road")
    surface.fill(cs.WHITE)
    return surface

def loop(surface, map, path):    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        draw_map(surface, map)
        draw_grid(surface, map)
        draw_path(surface, path, map)
        draw_grid(surface, map)
        pygame.display.update()
