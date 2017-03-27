#!/usr/bin/python
import sys,copy
class Game(object):
    def __init__(self, mode=0, size=0, myplayer=None, presentplayer=None, opponent=None, cutoffdepth=0, curboardstate=[],
                 valueboard=[]):
        self.n = size
        self.myplayer = myplayer
        self.cutoffdepth = cutoffdepth
        self.presentplayer = presentplayer
        self.opponent = opponent
        self.curboardstate = curboardstate
        self.valueboard = valueboard
        self.mode = mode
        self.movetype=''
        self.row=''
        self.column=''

    def checkNeighbour(self, i, j, player):
        up = 0
        down = 0
        left = 0
        right = 0
        if (i == 0 and j == 0):
            if (self.curboardstate[i + 1][j] == player):
                down = 1
            if (self.curboardstate[i][j + 1] == player):
                right = 1
        elif (i == self.n - 1 and j == self.n - 1):
            if (self.curboardstate[i - 1][j] == player):
                up = 1
            if (self.curboardstate[i][j - 1] == player):
                left = 1
        elif (i == 0 and j == self.n - 1):
            if (self.curboardstate[i + 1][j] == player):
                down = 1
            if (self.curboardstate[i][j - 1] == player):
                left = 1
        elif (i == self.n - 1 and j == 0):
            if (self.curboardstate[i - 1][j] == player):
                up = 1
            if (self.curboardstate[i][j + 1] == player):
                right = 1
        elif (i == 0):
            if (self.curboardstate[i + 1][j] == player):
                down = 1
            if (self.curboardstate[i][j + 1] == player):
                right = 1
            if (self.curboardstate[i][j - 1] == player):
                left = 1
        elif (j == 0):
            if (self.curboardstate[i + 1][j] == player):
                down = 1
            if (self.curboardstate[i][j + 1] == player):
                right = 1
            if (self.curboardstate[i - 1][j] == player):
                up = 1
        elif (i == self.n-1):
            if (self.curboardstate[i][j + 1] == player):
                right = 1
            if (self.curboardstate[i - 1][j] == player):
                up = 1
            if (self.curboardstate[i][j - 1] == player):
                left = 1
        elif (j == 4):
            if (self.curboardstate[i + 1][j] == player):
                down = 1
            if (self.curboardstate[i - 1][j] == player):
                up = 1
            if (self.curboardstate[i][j - 1] == player):
                left = 1
        elif (i > 0 and j > 0 and i < self.n - 1 and j < self.n - 1):
            if (self.curboardstate[i + 1][j] == player):
                down = 1
            if (self.curboardstate[i][j + 1] == player):
                right = 1
            if (self.curboardstate[i - 1][j] == player):
                up = 1
            if (self.curboardstate[i][j - 1] == player):
                left = 1
        return [up, down, left, right]

    def nextMove(self, i, j):
        self.movetype='Stake'
        if (1 in self.checkNeighbour(i, j, self.presentplayer)):
            val = self.checkNeighbour(i, j, self.opponent)
            if (val[0] == 1):
                self.curboardstate[i - 1][j] = self.presentplayer
                self.movetype='Raid'
            if (val[1] == 1):
                self.curboardstate[i + 1][j] = self.presentplayer
                self.movetype='Raid'
            if (val[2] == 1):
                self.curboardstate[i][j - 1] = self.presentplayer
                self.movetype='Raid'
            if (val[3] == 1):
                self.curboardstate[i][j + 1] = self.presentplayer
                self.movetype='Raid'
        self.curboardstate[i][j] = self.presentplayer

    def Eval(self, player):
        curval = 0
        nxtval = 0
        for i in xrange(0, self.n):
            for j in xrange(0, self.n):
                if (self.curboardstate[i][j] == player):
                    curval += self.valueboard[i][j]
                elif (self.curboardstate[i][j] != "."):
                    nxtval += self.valueboard[i][j]
        return curval - nxtval

    def emptycell(self):
        c = 0
        for i in xrange(0, self.n):
            for j in xrange(0, self.n):
                if ((self.curboardstate[i][j] == ".")):
                    c += 1
        return c

    def switchplayer(self):
        if (self.presentplayer == "X"):
            self.presentplayer = "O"
            self.opponent = "X"
        else:
            self.presentplayer = "X"
            self.opponent = "O"

    def Minimax(self):
        max, x, y = Max_Node(self, self.cutoffdepth, -1, -1, self.emptycell())
        self.nextMove(x, y)
        self.row=x
        self.column=y

    def AlphaBeta(self):
        max, x, y = AlphaBetaMax(self, self.cutoffdepth, -1, -1, self.emptycell(), -sys.maxint - 1, sys.maxint)
        self.nextMove(x, y)
        self.row=x
        self.column=y


def getMoveVal(i, j):
    return chr(j + ord('A')) + str(i + 1)



def Max_Node(self, depth, x, y, empty):
    if (depth == 0 or empty == 0):
        curval = self.Eval(self.myplayer)
        return curval, x, y
    maxval = -sys.maxint - 1
    x1 = -1
    y1 = -1
    for i in xrange(0, self.n):
        for j in xrange(0, self.n):
            if ((self.curboardstate[i][j] == ".")and 1 not in self.checkNeighbour(i, j, self.presentplayer)):
                newboard = copy.deepcopy(self)
                newboard.nextMove(i, j)
                newboard.switchplayer()
                curval, x2, y2 = Min_Node(newboard, depth - 1, i, j, empty - 1)
                if (curval > maxval):
                    maxval = curval
                    x1 = i
                    y1 = j
    for i in xrange(0, self.n):
        for j in xrange(0, self.n):
            if ((self.curboardstate[i][j] == ".")and 1 in self.checkNeighbour(i, j, self.presentplayer)):
                newboard = copy.deepcopy(self)
                newboard.nextMove(i, j)
                newboard.switchplayer()
                curval, x2, y2 = Min_Node(newboard, depth - 1, i, j, empty - 1)
                if (curval > maxval):
                    maxval = curval
                    x1 = i
                    y1 = j
    return maxval, x1, y1


def Min_Node(self, depth, x, y, empty):
    if (depth == 0 or empty == 0):
        curval = self.Eval(self.myplayer)
        return curval, x, y
    minval = sys.maxint
    x1 = -1
    y1 = -1
    for i in xrange(0, self.n):
        for j in xrange(0, self.n):
            if ((self.curboardstate[i][j] == ".")and 1 in self.checkNeighbour(i, j, self.presentplayer)):
                newboard = copy.deepcopy(self)
                newboard.nextMove(i, j)
                newboard.switchplayer()
                curval, x2, y2 = Max_Node(newboard, depth - 1, i, j, empty - 1)
                if (curval < minval):
                    minval = curval
                    x1 = i
                    y1 = j
    for i in xrange(0, self.n):
        for j in xrange(0, self.n):
            if ((self.curboardstate[i][j] == ".")and 1 in self.checkNeighbour(i, j, self.presentplayer)):
                newboard = copy.deepcopy(self)
                newboard.nextMove(i, j)
                newboard.switchplayer()
                curval, x2, y2 = Min_Node(newboard, depth - 1, i, j, empty - 1)
                if (curval > minval):
                    minval = curval
                    x1 = i
                    y1 = j
    return minval, x1, y1


def AlphaBetaMax(self, depth, x, y, empty, alpha, beta):
    if (depth == 0 or empty == 0):
        curval = self.Eval(self.myplayer)
        return curval, x, y
    maxval = -sys.maxint - 1
    x1 = -1
    y1 = -1
    for i in xrange(0, self.n):
        for j in xrange(0, self.n):
            if ((self.curboardstate[i][j] == ".") and 1 not in self.checkNeighbour(i, j, self.presentplayer)):
                newboard = copy.deepcopy(self)
                newboard.nextMove(i, j)
                newboard.switchplayer()
                curval, x2, y2 = AlphaBetaMin(newboard, depth - 1, i, j, empty - 1, alpha, beta)
                if (curval > maxval):
                    maxval = curval
                    x1 = i
                    y1 = j
                if (maxval >= beta):
                    return maxval, i, j;
                alpha = max(alpha, maxval)
    for i in xrange(0, self.n):
        for j in xrange(0, self.n):
            if ((self.curboardstate[i][j] == ".")and 1 in self.checkNeighbour(i, j, self.presentplayer)) :
                newboard = copy.deepcopy(self)
                newboard.nextMove(i, j)
                newboard.switchplayer()
                curval, x2, y2 = AlphaBetaMin(newboard, depth - 1, i, j, empty - 1, alpha, beta)
                if (curval > maxval):
                    maxval = curval
                    x1 = i
                    y1 = j
                if (maxval >= beta):
                    return maxval, i, j;
                alpha = max(alpha, maxval)
    return maxval, x1, y1


def AlphaBetaMin(self, depth, x, y, empty, alpha, beta):
    if (depth == 0 or empty == 0):
        curval = self.Eval(self.myplayer)
        return curval, x, y
    minval = sys.maxint
    x1 = -1
    y1 = -1
    for i in xrange(0, self.n):
        for j in xrange(0, self.n):
            if ((self.curboardstate[i][j] == ".") and 1 not in self.checkNeighbour(i, j, self.presentplayer)):
                newboard = copy.deepcopy(self)
                newboard.nextMove(i, j)
                newboard.switchplayer()
                curval, x2, y2 = AlphaBetaMax(newboard, depth - 1, i, j, empty - 1, alpha, beta)
                if (curval < minval):
                    minval = curval
                    x1 = i
                    y1 = j
                if (minval <= alpha):
                    return minval, i, j
                beta = min(minval, beta)
    for i in xrange(0, self.n):
        for j in xrange(0, self.n):
            if ((self.curboardstate[i][j] == ".") and 1 in self.checkNeighbour(i, j, self.presentplayer)):
                newboard = copy.deepcopy(self)
                newboard.nextMove(i, j)
                newboard.switchplayer()
                curval, x2, y2 = AlphaBetaMax(newboard, depth - 1, i, j, empty - 1, alpha, beta)
                if (curval < minval):
                    minval = curval
                    x1 = i
                    y1 = j
                if (minval <= alpha):
                    return minval, i, j
                beta = min(minval, beta)
    return minval, x1, y1


def readFile(gameboard, inputFile):
    i = 0
    with open(inputFile,'rU') as f:
        content = f.readlines()
    for val in content:
        val = val.replace('\n', '')
        if (i == 0):
            i += 1
            gameboard.n = int(val)
            continue
        if (i== 1 ):
            if( val == 'MINIMAX'):
                gameboard.mode=1
            else:
                gameboard.mode=2
            i+=1
            continue
        if (i == 2):
            gameboard.presentplayer=val
            gameboard.myplayer=val
            if (val == "X"):
                gameboard.opponent = "O"
            else:
                gameboard.opponent = "X"
            i += 1
            continue
        if (i == 3):
            gameboard.cutoffdepth = int(val)
            i += 1
            continue
        if (i >= 4 and i < 4 + gameboard.n):
            gameboard.valueboard.append(list(int(x) for x in val.split(' ')))
            i += 1
            continue
        if (i >= 4+gameboard.n and i < 4+gameboard.n+gameboard.n):
            gameboard.curboardstate.append(list(val))
            i += 1
            continue

def createoutput(gameobj):
    outfile=open('output.txt','w')
    mymove=getMoveVal(gameobj.row,gameobj.column)
    outfile.write(mymove+' ')
    outfile.write(gameobj.movetype+'\n')
    for i in xrange(0, gameobj.n):
            outfile.write(''.join(gameobj.curboardstate[i]))
            if (i < gameobj.n - 1):
                outfile.write('\n')
def main():
    game_board = Game()
    readFile(game_board, 'input.txt')
    if (game_board.mode == 1):
        game_board.Minimax()
        createoutput(game_board)
    elif (game_board.mode == 2):
        game_board.AlphaBeta()
        createoutput(game_board)

if __name__ == "__main__":
    main()

