'''
This program generates the solutions for the famous non-intersecting
queens problem
https://en.wikipedia.org/wiki/Eight_queens_puzzle

The solution is not restricted to the specific case of 8 queens, but
takes a positive integer as input and generates all the solutions for
a board of the specified size. We can print just the solution count
for a given board size, or print the entire list of solutions. E.g.
$ python3 queens.py 8
8-Queens has 92 solutions
$ python3 queens.py -v 4
(2, 4, 1, 3)
(3, 1, 4, 2)
4-Queens has 2 solutions
'''
import sys


def usage():
    """
    Print the usage message
    return: None
    """
    print("Usage: Queens [-v] number")
    print("Option: -v verbose output, print all solutions")


def print_board(board):
    """
    Print the board. Used in the verbose option.
    board: Board detailing the position of all the queens
    return: None
    """
    sys.stdout.write("(")

    for i in range(1, n):
        print(board[i][0], end=', ')
    print(board[n][0], end='')

    print(")")


def place_queen(board, row, col):
    """
    Identify an available spot and place the queen there.
    Update the squares that are covered by the new queen.
    param board: Board to be updated.
    param row: Row being updated
    param col: Column being updated
    return: None
    """
    board[row][col] = 1
    board[row][0] = col

    for i in range(row + 1, n + 1):
        for j in range(1, n + 1):
            if j in (col - (i - row), col, col + (i - row)):
                board[i][j] -= 1


def remove_queen(board, row, col):
    """
    Remove the queen. If a queen can't be placed, we need to remove a
    preceding queen and try another arrangement. The board positions
    covered by the now removed queen should be updated.
    param board: Board to be updated.
    param row: Row being updated
    param col: Column being updated
    return: None
    """
    board[row][col] = 0
    board[row][0] = 0

    for i in range(row + 1, n + 1):
        for j in range(1, n + 1):
            if j in (col - (i - row), col, col + (i - row)):
                board[i][j] += 1


def find_solutions(board, i, mode):
    """
    The top level recursive function, that places and removes
    queens as required to find the solution(s).
    param board: Board to be updated.
    param i: Start with the first row till the board size
    param mode: Verbose or normal
    return: None
    """
    num_solutions = 0

    if i > n:
        if mode == "VERBOSE":
            print_board(board)
        return 1

    for j in range(1, n+1):
        if B[i][j] == 0:
            place_queen(board, i, j)
            num_solutions += find_solutions(B, i+1, mode)
            remove_queen(board, i, j)

    return num_solutions


if __name__ == '__main__':
    MODE = "COUNT"

    if len(sys.argv) < 2 or len(sys.argv) > 3:
        usage()
        sys.exit(1)

    if len(sys.argv) == 3:
        if sys.argv[1] != "-v":
            usage()
            sys.exit(1)
        else:
            MODE = "VERBOSE"

    try:
        n = int(sys.argv[-1])
        B = [[0 for i in range(n + 1)] for j in range(n + 1)]
        solutionsCount = find_solutions(B, 1, MODE)
        print("{}-Queens has {} solutions".format(n, solutionsCount))
    except ValueError:
        usage()
        sys.exit(1)
