#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Maxime Raynal <maxime.raynal@protonmail.com>
# LICENSE: MIT

import sys
from takuzu_solver import (
    solution_from_dimacs_string, dimacs_string_from_constraints,
    constraints_from_grid, grid_from_file
)


def main(args):
    if len(args) < 2:
        print(f"Usage: {args[0]} size_grid sat_or_unsat(optionnel)\nExiting")
        return
    elif len(args)==2:
        s=input("sat or unsat ?(sat/unsat) ")
        while s!="sat" and s!="unsat":
            s=input("sat or unsat ?(sat/unsat) ")
        filename = f"fichier_test_grid_{args[1]}_{s}.txt"
    elif len(args)==3:
        filename = f"fichier_test_grid_{args[1]}_{args[2]}.txt"
    N = int(args[1])
    res, d2 =         dimacs_string_from_constraints(
            constraints_from_grid(
                grid_from_file(filename,N)
            )
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
