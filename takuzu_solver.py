import itertools
import subprocess
import os

def grid_from_file(file_name):
    """Reads a grid stored in a file"""
    f=open(file_name)
    grid=[]
    grid=f.readlines()
    global N
    N=int(grid[0])
    # test if n = length of list - 1
    if int(N) != (len(grid)-1) :
        print("erreur d'entree!")
        return None
    grid.pop(0)
    # loop for each element of the list (index >= 1)
    for i in range(len(grid)):
    #create list l
        l = []
        ligne = grid[i]
    #if elem type is char add each char to l
        for j in range(len(ligne)):
            case = ligne[j]
            # if '0' add 0
            # if '1' add 1
            # else add None
            if case == '0':
                l.append(0)
            elif case == '1':
                l.append(1)
            elif case == '-':
                l.append(None)                
        #and then lignes[indice] = l
        grid[i] = l
    f.close()   
    return grid

def constraints_from_grid(grid):
    """
    Models the takuzu into boolean constraints.
    Variable 'x_i_j' is true iff the number 1 is in the cell (i,j),
    and false iff the number 0 is in the cell (i,j)
    Preceded by a '-' if the variable is negated.
    So we have N*N variables.
    All constraints will be expressed directly as FNCs.
    Stored as list(product) of lists(clauses).
    The principle of the pigeon hole (théorème des tiroirs) is used extensively
    to simplify the constraints expression.
    """
    
    constraints = []
    n = len(grid)
                
    #(1) There must be N/2 0’s and N/2 1’s in each line (respectively column).
    
    # S subset of size N/2 +1  and S C= {1,...N}
    S = list(itertools.combinations(range(1,n+1), int(n/2) + 1))

    # for all i in 1.. N, ET de (S C {1,...N} ) OU de (j C S) -Xij
    for i in range(1,n+1):
        for subset in S: # OU de (j C S) -Xij 
            OU = []
            OU2 = []
            for j in subset:
                OU += [f"-x_{i}_{j}"]
                OU2 += [f"x_{i}_{j}"]
            constraints += [OU]
            constraints += [OU2]
    # for all j in 1.. N, ET de (S C {1,...N} ) OU de (i C S) -Xij
    for j in range(1,n+1):
        for subset in S: # OU de (i C S) -Xij 
            OU = []
            OU2 = []
            for i in subset:
                OU += [f"-x_{i}_{j}"]
                OU2 += [f"x_{i}_{j}"]
            constraints += [OU]
            constraints += [OU2]

    #(2) No more than two adjacent cells can contain the same number.
    for i in range(1,n+1):
        for j in range(1,n-1):
            constraints+= [[f"x_{i}_{j}",f"x_{i}_{j+1}",f"x_{i}_{j+2}"]]
            constraints+= [[f"-x_{i}_{j}",f"-x_{i}_{j+1}",f"-x_{i}_{j+2}"]]

    
    for j in range(1,n+1):
        for i in range(1,n-1):
            constraints+= [[f"x_{i}_{j}",f"x_{i+1}_{j}",f"x_{i+2}_{j}"]]
            constraints+= [[f"-x_{i}_{j}",f"-x_{i+1}_{j}",f"-x_{i+2}_{j}"]]


    #(3) There can be no identical rows or columns.
    for i in range(1,n+1):
        OU=[]
        for j1 in range(1,n+1):
            for j2 in range(1,n+1):
                if j1 != j2:
                    OU+= [f"z_{i}_{j1}_{i}_{j2}"]
        constraints+= [OU]
                          
    for j in range(1,n+1):
        OU=[]
        for i1 in range(1,n+1):
            for i2 in range(1,n+1):
                if i1 != i2:
                    OU+= [f"z_{i1}_{j}_{i2}_{j}"]
        constraints+= [OU]

    #(4) Each puzzle begins with several squares in the grid already filled.
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 0:
                constraints += [[f"-x_{i+1}_{j+1}"]]
            elif grid[i][j] == 1:
                constraints += [[f"x_{i+1}_{j+1}"]]  
       
    return constraints


def dimacs_string_from_constraints(constraints):
    """Numbering rule: index in list L of var_name"""
    res = ""
    nb_var = N*N
    nb_clauses = len(constraints)
    res+= f"p cnf {nb_var} {nb_clauses}\n"

    L = []
    for constraint in constraints:
        for var_name in constraint:
            if var_name[0]=='-':
                 if var_name[1:] not in L:
                    L.append(var_name[1:])
            elif var_name not in L:
                L.append(var_name) 

    sorted_L = sorted(L)
    d = dict()      # keys of d = variable names and their values are indexes
    d2 = dict()     # keys of d2 = indexes and their values are variable names

    for i,v in enumerate(L):
        d[v] = i+1
        d2[i+1] = v

    for constraint in constraints:
        for var_name in constraint:
            if var_name[0]=='-':
                index = d[var_name[1:]]
                res+= '-' + str(index) + " "
            else:
                index = d[var_name]
                res+= str(index) + " " 
        res+= "0\n"

    return res, d2


def solution_from_dimacs_string(dimacs_str, d2):
    # write the dimacs into a file
    with open("constraints.dimacs.tmp", 'w') as f:
        f.write(dimacs_str)
    # run a solver (here minisat)
    subprocess.run(["minisat", "constraints.dimacs.tmp", "out.tmp"])
    with open("out.tmp", 'r') as output:
        solution_as_str = output.read().splitlines()
    os.remove("constraints.dimacs.tmp")
    os.remove("out.tmp")

    if solution_as_str[0] == 'UNSAT':
        return "UNSAT"
    # else
    solution_as_str = {int(i) for i in solution_as_str[1].split()}
    # solution_grid = [[0 for _ in range(N)] for __ in range(N)]
    # for nb in solution_as_str:
    #     if nb >0:
    #         var_name = d2[nb]
    #         if 'z' not in var_name:
    #             i = int(var_name.split('_')[-2])
    #             j = int(var_name.split('_')[-1])
    #         # if 'z' in var_name:
    #         #     i_prime = int(var_name.split('_')[-4])
    #         #     j_prime = int(var_name.split('_')[-3])
    #             solution_grid[i-1][j-1] = 1
    
    solution_grid = [[None for _ in range(N)] for __ in range(N)]
    for nb in solution_as_str:
        if nb >0:
            var_name = d2[nb]
            if 'z' not in var_name:
                i = int(var_name.split('_')[-2])
                j = int(var_name.split('_')[-1])
                solution_grid[i-1][j-1] = 1
        elif nb <0:
            var_name = d2[-nb]
            if 'z' not in var_name:
                i = int(var_name.split('_')[-2])
                j = int(var_name.split('_')[-1])
                solution_grid[i-1][j-1] = 0

    # for nb in solution_as_str:
    #     if nb >0:
    #         var_name = d2[nb]
    #         if 'z' in var_name:
    #             i = int(var_name.split('_')[-4])
    #             j = int(var_name.split('_')[-3])
    #             i_prime = int(var_name.split('_')[-2])
    #             j_prime = int(var_name.split('_')[-1])
    #             if solution_grid[i-1][j-1] != None:
    #                 solution_grid[i_prime-1][j_prime-1] = 1 - solution_grid[i-1][j-1]
    #             solution_grid[i-1][j-1] = 1
    #     elif nb <0:
    #         var_name = d2[-nb]
    #         if 'z' not in var_name:
    #             i = int(var_name.split('_')[-2])
    #             j = int(var_name.split('_')[-1])
    #             solution_grid[i-1][j-1] = 0

 
    
    return solution_grid
