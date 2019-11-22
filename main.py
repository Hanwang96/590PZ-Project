import copy
import random

class Board(object):
    def __init__(self, size):
        # size: The maximum number shown in the game
        self.size = size
        self.width = size + 2
        self.height = size + 1
        # generate an empty board
        self.board = [[0 for i in range(self.width)]
                      for i in range(self.height)]


    def generator(self):
        # generate a random puzzle
        # num: how many "n" the board has
        num = int(self.width * self.height / (self.size+1))
        container = []
        for i in range(self.size + 1):
            for j in range(num):
                container.append(i)
        # randomly pick a number to fill the board
        for i in range(self.height):
            for j in range(self.width):
                n = random.randint(0, len(container) - 1)
                self.board[i][j] = container[n]
                container.pop(n)
        # If there is a solution, then it is a valid board.
        # If there is no solution, generate again.
        sol = self.solve_all()
        if sol == []:
            self.generator()



    def scratch_board(self) -> [[int]]:
        # add extra (helper) row and column of '-1' to the board
        scratch_board = [[-1 for i in range(self.width+1)]
                         for i in range(self.height+1)]
        # copy the board to the scratch board
        for i in range(self.height):
            for j in range(self.width):
                scratch_board[i][j] = self.board[i][j]
        return scratch_board

    def solve_one(self) -> [[int]]:
        # return one solution
        # board_for_solve = self.generator()
        solution = self.solver(self.scratch_board(), 0, 0, [], set())
        return solution

    def solve_all(self) -> [[[int]]]:
        # return all solution(s)
        solutions = []
        self.solver_all(self.scratch_board(), 0, 0, [], set(), solutions)
        return solutions

    def full(self, board) -> bool:
        res = True
        for i in range(self.height):
            for j in range(self.width):
                if board[i][j] != -1:
                    res = False
        return res

    def solver(self, board, i, j, recorder, used_domino: {(int, int)}):
        # recursive, backtracking
        # i : current row index
        # j : current col index
        # example for recorder:
        # [[(2,3),0,1,0],
        #  [(1,1),1,2,1]]
        # (2,3): the numbers in the domino
        # 0,1: the row, column index of the top/left cell
        # 0: orientation, 0 for horizontal. 1 for vertical
        # each line(list) is a domino

        if self.full(board):
            return recorder

        while i != self.height:
            while j != self.width and board[i][j] == -1:
                # If the current one is unavailable, move to next one
                j += 1

            if j == self.width:
                # reach the end column, go to the next line
                i, j = i+1, 0
                continue
            break

        if i == self.height:
            # reach the end line, no solution found
            return []

        # try horizontally put the next domino
        d = (board[i][j], board[i][j + 1])
        # Sort the domino
        domino = (d[0], d[1]) if d[0] < d[1] else (d[1], d[0])
        if domino not in used_domino and board[i][j+1] != -1:
            recorder_new = copy.deepcopy(recorder)
            recorder_new.append([domino, i, j, 0])
            board_new = copy.deepcopy(board)
            # Copy a new board to save the move result
            board_new[i][j] = -1
            board_new[i][j + 1] = -1
            used_domino_new = copy.deepcopy(used_domino)
            used_domino_new.add(domino)
            res = self.solver(board_new, i, j + 1,
                              recorder_new, used_domino_new)
            if res != []:
                return res

        # try vertically put the next domino
        d = (board[i][j], board[i+1][j])
        domino = (d[0], d[1]) if d[0] < d[1] else (d[1], d[0])
        if domino not in used_domino and board[i + 1][j] != -1:
            record = [domino, i, j, 1]
            recorder_new = copy.deepcopy(recorder)
            recorder_new.append(record)
            board_new = copy.deepcopy(board)
            board_new[i][j] = -1
            board_new[i + 1][j] = -1
            used_domino_new = copy.deepcopy(used_domino)
            used_domino_new.add(domino)
            res = self.solver(board_new, i, j + 1,
                              recorder_new, used_domino_new)
            if res != []:
                return res

    def solver_all(self, board, i, j, recorder, used_domino: {(int, int)}, solutions:[]):
        # recursive, backtracking
        # print(recorder)
        if self.full(board):
            solutions.append(recorder)

        while i != self.height:
            while j != self.width and board[i][j] == -1:
                j += 1
            if j == self.width:
                i, j = i+1, 0
                continue
            break
        if i == self.height:
            return

        # try horizontally put the next domino
        d = (board[i][j], board[i][j + 1])
        domino = (d[0], d[1]) if d[0] < d[1] else (d[1], d[0])
        if domino not in used_domino and board[i][j+1] != -1:
            recorder_new = copy.deepcopy(recorder)
            recorder_new.append([domino, i, j, 0])
            board_new = copy.deepcopy(board)
            board_new[i][j] = -1
            board_new[i][j + 1] = -1
            used_domino_new = copy.deepcopy(used_domino)
            used_domino_new.add(domino)
            self.solver_all(board_new, i, j + 1,
                              recorder_new, used_domino_new, solutions)

        # try vertically put the next domino
        d = (board[i][j], board[i+1][j])
        domino = (d[0], d[1]) if d[0] < d[1] else (d[1], d[0])
        if domino not in used_domino and board[i + 1][j] != -1:
            record = [domino, i, j, 1]
            recorder_new = copy.deepcopy(recorder)
            recorder_new.append(record)
            board_new = copy.deepcopy(board)
            board_new[i][j] = -1
            board_new[i + 1][j] = -1
            used_domino_new = copy.deepcopy(used_domino)
            used_domino_new.add(domino)
            self.solver_all(copy.deepcopy(board_new), i, j + 1, recorder_new, used_domino_new, solutions)


if __name__ == "__main__":

    board = Board(3)
    board.generator()
    print("Game:")
    for each in board.board:
        print(each)

    print("====================")
    print("The number of solution(s) is:")
    solutions = board.solve_all()
    print(len(solutions))
    print("-------------")
    print("Solutions:")
    print("-------------")
    for s in solutions:
        for a in s:
            print(a)
        print("-------------")