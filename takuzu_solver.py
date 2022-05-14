import sys
from takuzu_solver import *
(
    solution_from_dimacs_string, dimacs_string_from_constraints,
    constraints_from_grid, grid_from_file
)


def main(args):
    if len(args) > 2:
        print(f"Too many arguments!")
        return
    if len(args) == 2:
        filename = args[1]
    else:
        N=int(input("size of the grid N = "))
        while N%2 != 0:
            N=int(input("N has to be even, try again "))
        s=input("sat or unsat? ")
        while s!="sat" and s!="unsat":
            s=input("sat or unsat ?(sat/unsat) ")
        filename = f"{s}_{str(N)}*{str(N)}"

    grid = grid_from_file(filename)
    if grid == None:
        return
    res, d2 =         dimacs_string_from_constraints(
            constraints_from_grid(grid)
        )
    
    solution = solution_from_dimacs_string(res,d2)

    if solution == "UNSAT":
        return
    else:
        with open(f"fichier_test_grid_{N}_sat_sol.txt", 'w') as f:
            f.write(f"{N}" + '\n' + ('\n'.join(
            ''.join(
                str(solution[i][j]) for j in range(N)
            ) for i in range(N)
        )))
        print('\n'.join(
            ' '.join(
                str(solution[i][j]) for j in range(N)
            ) for i in range(N)
        ))


if __name__ == '__main__':
    main(sys.argv)
