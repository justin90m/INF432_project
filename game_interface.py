import pygame
import copy
from takuzu_solver import grid_from_file
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
original_elt_colour = (125, 125, 125)#original values are in gray
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 600
GRID_HEIGHT = 400
GRID_WIDTH = 400
"""checks if the given grid is correct and modify it to replace '-' or None with 2, and '1' and '0' by 1 and 0"""
def check_grid(grid):
    for i in range(len(grid)):
        if len(grid)!=len(grid[i]):
            print("Grid not valid : number of line must be equal to number of columns.")
            print("ligne ", i, "has ", len(grid[i]), "elements while the grid has ", len(grid), "lines")
            return
    #Now we know that the nb_lines=nb_col
    if len(grid)%2!=0:
        print("The size of the grid must be even")
        return
    #now the grid should be correct, so we just need to modify it
    mod_grid = [[0 for x in range(len(grid[y]))] for y in range(len(grid))]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j]==0 or grid[i][j]==1 or grid[i][j]==2:
                mod_grid[i][j] = grid[i][j]
            elif grid[i][j]=='1' or grid[i][j]=='0':
                mod_grid[i][j]=int(grid[i][j])
            elif grid[i][j]=='-' or grid[i][j]==None:
                mod_grid[i][j]=2
            else:
                print("incorrect element in the grid at line ", i, "column ", j, " : ", grid[i][j])
    #We check if the new grid is correct too
    for i in range(len(mod_grid)):
        if len(mod_grid)!=len(mod_grid[i]):
            print("Couldn't generate a correct grid from the given grid")
            print("ligne ", i, "has ", len(mod_grid[i]), "elements while the grid has ", len(mod_grid), "lines")
            return
    if len(mod_grid)%2!=0:
        print("Couldn't generate a correct grid from the given grid")
        return
    return mod_grid


    
def full_grid(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
                       if grid[i][j]!=0 and grid[i][j]!=1:
                           return False
    return True


def set_px_py(grid_size):
    if grid_size==8:
        return (0,0)
    if grid_size==6:
        return (5,0)
    if grid_size==4:
        return (16,5)
    return (-4,-2)

def set_size(grid_size):
    if grid_size==8:
        return 35
    if grid_size==6:
        return 45
    if grid_size==4:
        return 65
    return 30

def game_interface(original_grid):
    global win, CLOCK, grid, font_numbers, nb_of_squares,size_squares, d, grid_size, px_grid, py_grid, num_size
    original_grid = check_grid(original_grid)
    if original_grid==None:
        return
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
    num_size=set_size(grid_size)
    font_numbers = pygame.font.SysFont('Comic Sans Ms', num_size)
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
original_grid8 = [[0,2,2,0,2,1,2,2],
        [2,2,2,0,2,1,2,2],
        [2,2,2,1,2,2,2,2],
        [2,2,2,2,2,2,2,2],
        [2,2,2,1,2,1,2,2],
        [1,2,2,2,2,2,1,1],
        [2,2,2,0,2,1,2,2],
        [2,2,0,2,2,2,2,2]]
original_grid6 = [[0,2,2,0,2,1],
        [2,2,2,0,2,1],
        [2,2,2,1,2,2],
        [2,2,2,2,2,2],
        [2,2,2,1,2,1],
        [1,2,2,2,2,2]]
original_grid4 = [['0','-','-','0'],
        ['-','-','-','0'],
        ['-','-','-','1'],
        ['-','-','-','-']]
grid_file = grid_from_file("fichier_test.txt")
game_interface(grid_file)
