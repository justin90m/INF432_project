#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Maxime Raynal <maxime.raynal@protonmail.com>
# LICENSE: MIT

import sys
from takuzu_solver import (
    solution_from_dimacs_string, dimacs_string_from_constraints,
    constraints_from_grid, grid_from_file, N
)


def main(args):
    if len(args) < 2:
        print(f"Usage: {args[0]} path_to_grid\nExiting")
        return
    filename = args[1]
    res, d2 =         dimacs_string_from_constraints(
            constraints_from_grid(
                grid_from_file(filename)
            )
        )
   
    solution = solution_from_dimacs_string(res, d2)

    if solution == "UNSAT":
        return
    else:
        print('\n'.join(
            ' '.join(
                str(solution[i][j]) for j in range(N)
            ) for i in range(N)
        ))


if __name__ == '__main__':
    main(sys.argv)