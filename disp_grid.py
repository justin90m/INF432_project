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
"""checks if the given grid is correct and modify it to replace '1' and '0' by 1 and 0"""
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
            if grid[i][j]==0 or grid[i][j]==1 or grid[i][j]==2 or grid[i][j]==None:
                mod_grid[i][j] = grid[i][j]
            elif grid[i][j]=='1' or grid[i][j]=='0':
                mod_grid[i][j]=int(grid[i][j])
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



def set_px_py(grid_size):
    if grid_size==16:
        return (-8,-5)
    if grid_size==14:
        return (-7,-7)
    if grid_size==12:
        return (-5,-5)
    if grid_size==10:
        return (-4,-2)
    if grid_size==8:
        return (0,0)
    if grid_size==6:
        return (5,0)
    if grid_size==4:
        return (16,5)
    return (-15,-10)

def set_size(grid_size):
    if grid_size==16:
        return 25
    if grid_size==14:
        return 30
    if grid_size==12:
        return 30
    if grid_size==10:
        return 30
    if grid_size==8:
        return 35
    if grid_size==6:
        return 45
    if grid_size==4:
        return 65
    return 20
    
def disp_original_grid(grid):
    #Window parameters
    pygame.init()
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("TAKUZU")
    CLOCK = pygame.time.Clock()
    win.fill(WHITE)
    #grid parameters
    grid = check_grid(grid)
    grid_size=len(grid)
    size_squares = GRID_HEIGHT // grid_size
    num_size=set_size(grid_size)
    font_numbers = pygame.font.SysFont('Comic Sans Ms', num_size)
    d = (WINDOW_WIDTH-GRID_WIDTH) // 2
    (px_grid,py_grid)=set_px_py(grid_size)
    for i in range(grid_size+1):
        pygame.draw.line(win, (0,0,0), (d+size_squares*i, d), (d+size_squares*i,d+size_squares*grid_size), 2)
        pygame.draw.line(win, (0,0,0), (d, d+size_squares*i), (d+size_squares*grid_size, d+size_squares*i), 2)
    #i=ordonnée, j=abcisse
    for i in range(0, grid_size):
        for j in range(0,grid_size):
            if grid[i][j]==0 or grid[i][j]==1:
                value = font_numbers.render(str(grid[i][j]), True, original_elt_colour)
                win.blit(value, (j*size_squares+d+15+px_grid, i*size_squares+d+py_grid))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
    

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
grid_file = grid_from_file("fichier_test_grid12.txt")
disp_original_grid(grid_file)
