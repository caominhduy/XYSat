"""
Given a rectangular grid with some of the squares blocked off, can the remaining
squares be filled with Xs and Ys so that every row and every column has at least
one X and at least one Y?

This program converts this problem into a SAT problem and pass it to the SAT
solver for the solution (if any).

You can choose:
    1. Copy the output as DIMACS cnf format and paste them into online SAT solver
    manually
    2. Or, let it automatically do that for you

beautifulsoup4 and numpy are required
"""

import numpy as np
import bs4 # beautifulsoup4 for web scraping

def read_user_input(input=input("Enter test data ")):
    dimension = input.split(',(')[0].split(',')
    dimension = [int(i) for i in dimension]
    new_input = input.split(',(')[1:]
    blocked_squares_as_strings = []
    for i in new_input:
        blocked_squares_as_strings.append(i[:len(i)-1])
    blocked_squares = []
    for i in blocked_squares_as_strings:
        blocked_squares.append(i.split(','))
    for i in range(len(blocked_squares)):
        for x in range(len(blocked_squares[i])):
            blocked_squares[i][x] = int(blocked_squares[i][x])
    return dimension, blocked_squares

def init_grid(d):
    grid = [['' for i in range(d[1])] for x in range(d[0])]
    return grid

def add_blocked_squares(grid, bs):
    for x in bs:
        grid[x[0]-1][x[1]-1] = 0
    return grid

def enum_(grid):
    counter = 1
    new_grid = grid
    for i in range(len(grid)):
        for x in range(len(grid[i])):
            if not grid[i][x] == 0:
                new_grid[i][x] = counter
                counter += 1
    np_grid = np.array(new_grid)
    return np_grid, counter

def cnf_converter(grid, number_of_variables):
    #output = 'p cnf '
    #output = output + str(number_of_variables) + ' '
    rot_grid = np.rot90(grid)
    output = ''
    clause = 0
    for row in grid:
        for item in row:
            if item > 0:
                output = output + str(item) + ' '
        output = output + '0println'
        clause += 1
        for item in row:
            if item > 0:
                output = output + '-' + str(item) + ' '
        output = output + '0println'
        clause += 1
    for row in rot_grid:
        for item in row:
            if item > 0:
                output = output + str(item) + ' '
        output = output + '0println'
        clause += 1
        for item in row:
            if item > 0:
                output = output + '-' + str(item) + ' '
        output = output + '0println'
        clause += 1
    output = 'p cnf ' + str(number_of_variables) + ' ' + str(clause) + 'println' + output
    cnf = output.split('println')
    return cnf

if __name__ == '__main__':
    dimension, blocked_squares = read_user_input()
    grid = add_blocked_squares(init_grid(dimension), blocked_squares)
    np_grid, max = enum_(grid)
    cnf = cnf_converter(np_grid, max)
    for i in cnf:
        print(i)
