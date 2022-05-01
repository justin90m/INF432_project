import pygame
import copy
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
original_elt_colour = (125, 125, 125)#original values are in gray
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 600
GRID_HEIGHT = 400
GRID_WIDTH = 400
    
def full_grid(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
                       if grid[i][j]!=0 and grid[i][j]!=1:
                           return False
    return True


def set_px_py(grid_size):
    if grid_size==10:
        return (-4,-5)
    if grid_size==8:
        return (0,0)
    if grid_size==6:
        return (10,5)
    if grid_size==4:
        return (25,20)

def game_interface(original_grid):
    global win, CLOCK, grid, font_numbers, nb_of_squares,size_squares, d, grid_size, px_grid, py_grid
    grid=copy.deepcopy(original_grid)
    grid_size=len(grid)
    (px_grid,py_grid)=set_px_py(grid_size)
    pygame.init()
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("TAKUZU")
    nb_of_squares = len(grid)
    d = (WINDOW_WIDTH-GRID_WIDTH) // 2
    size_squares = GRID_HEIGHT // nb_of_squares
    CLOCK = pygame.time.Clock()
    win.fill(WHITE)
    font_numbers = pygame.font.SysFont('Comic Sans Ms', 45)
    drawGrid(grid)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                i,j = ((pos[1]-d)//size_squares), (pos[0]-d)//size_squares
                if 0<=i<=grid_size-1 and 0<=j<=grid_size-1 and original_grid[i][j]==2:
                    #if grid[i][j]!=2 we need to erase the value to replace it:
                    if grid[i][j]!=2:
                        size = (size_squares-2,size_squares-2)
                        empty_surface = pygame.Surface(size)
                        pygame.Surface.fill(empty_surface,WHITE)
                        win.blit(empty_surface, (j*size_squares+d+2, i*size_squares+d+2))
                    #now if the original value was 2(None) or 0 we need to replace it by 0 or 1
                    if grid[i][j]==0 or grid[i][j]==2:
                        value = font_numbers.render(str((grid[i][j]+1)%3), True, BLACK)
                        win.blit(value, (j*size_squares+d+15+px_grid, i*size_squares+d+py_grid))
                    grid[i][j]=(grid[i][j]+1)%3
        if full_grid(grid):
                #check the grid
                pass
                    
        pygame.display.update()


def drawGrid(grid):
    d = (WINDOW_WIDTH-GRID_WIDTH) // 2
    for i in range(nb_of_squares+1):
        pygame.draw.line(win, (0,0,0), (d+size_squares*i, d), (d+size_squares*i,d+size_squares*nb_of_squares), 2)
        pygame.draw.line(win, (0,0,0), (d, d+size_squares*i), (d+size_squares*nb_of_squares, d+size_squares*i), 2)
    #i=ordonnée, j=abcisse
    for i in range(0, len(grid)):
        for j in range(0,len(grid[0])):
            if grid[i][j]==0 or grid[i][j]==1:
                value = font_numbers.render(str(grid[i][j]), True, original_elt_colour)
                win.blit(value, (j*size_squares+d+15+px_grid, i*size_squares+d+py_grid))

#blit : j*size_squares+d+11, i*size_squares+d-5
original_grid10 = [[0,2,2,0,2,1,2,2,1,2],
        [2,2,2,0,2,1,2,2,0,1],
        [2,2,2,1,2,2,2,2,2,2],
        [2,2,2,2,2,2,2,2,1,0],
        [2,2,2,1,2,1,2,2,0,1],
        [1,2,2,2,2,2,1,1,2,2],
        [2,2,2,0,2,1,2,2,2,2],
        [2,2,0,2,2,2,2,2,0,0],
        [2,2,2,0,2,1,2,2,2,2],
        [2,2,2,1,2,0,2,2,2,2]]
#blit : original : j*size_squares+d+15, i*size_squares+d
original_grid8 = [[0,2,2,0,2,1,2,2],
        [2,2,2,0,2,1,2,2],
        [2,2,2,1,2,2,2,2],
        [2,2,2,2,2,2,2,2],
        [2,2,2,1,2,1,2,2],
        [1,2,2,2,2,2,1,1],
        [2,2,2,0,2,1,2,2],
        [2,2,0,2,2,2,2,2]]
#blit : j*size_squares+d+25, i*size_squares+d+5
original_grid6 = [[0,2,2,0,2,1],
        [2,2,2,0,2,1],
        [2,2,2,1,2,2],
        [2,2,2,2,2,2],
        [2,2,2,1,2,1],
        [1,2,2,2,2,2]]
#blit : j*size_squares+d+40, i*size_squares+d+20
original_grid4 = [[0,2,2,0],
        [2,2,2,0],
        [2,2,2,1],
        [2,2,2,2]]
game_interface(original_grid4)
