from selenium import webdriver
from modules import WebSudokuPage, Board, SudokuSolver
import time

"""
Automatically solve Sudoku puzzles from https://websudoku.com
with Backtracking method https://en.wikipedia.org/wiki/Sudoku_solving_algorithms#Backtracking
using Selenium Webdriver https://www.selenium.dev/documentation/webdriver/getting_started/
"""

with webdriver.Firefox() as driver:
    page = WebSudokuPage(driver)
    page.load()  # open web page

    board = Board(*page.get_grid())  # dump webpage board data and create Board instance
    print(board)  # print initial board state

    solver = SudokuSolver(board)
    solver.solve()  # Solve board

    print(solver.status_repr)  # Report solution status

    if solver.status:  # Solved successfully
        print(board)  # Print solved board state
        page.set_grid(board.grid)  # Fill webpage with solved data
        page.submit()

    time.sleep(5)
