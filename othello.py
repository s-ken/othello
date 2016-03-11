# -*- coding:utf-8 -*-

"""
  references:
    http://d.hatena.ne.jp/Megumi221/20081031/1225450482
"""

import pygame
from pygame.locals import *
import sys
import board
import book

    
class Config:
  BLACK         = 0
  WHITE         = 1
  EMPTY         = 2
  CELL_WIDTH    = 100
  CELL_NUM      = 8
  WINDOW_WIDTH  = CELL_WIDTH * CELL_NUM
  WPOS          = CELL_WIDTH * (CELL_NUM - 1)
  AI_COLOR      = WHITE
  MAX_SEARCH_HEIGHT = 6 # ゲーム木の高さ
  INF = 1 << 15
  WEIGHTS = (  30, -12,  0, -1, -1,  0, -12,  30,
              -12, -15, -3, -3, -3, -3, -15, -12,
                0,  -3,  0, -1, -1,  0,  -3,   0,
               -1,  -3, -1, -1, -1, -1,  -3,  -1,
               -1,  -3, -1, -1, -1, -1,  -3,  -1,
                0,  -3,  0, -1, -1,  0,  -3,   0,
              -12, -15, -3, -3, -3, -3, -15, -12,
               30, -12,  0, -1, -1,  0, -12,  30
            )
  MIDDLE_PHASE = 20
  LAST_PHASE   = 40
  TABLE_SIZE   = 65537
  CHAIN_LENGTH = 2

class Player(object):
  def __init__(self, board, color, openingBook):
    self.board = board  # boardへの参照
    self.color = color  # 自分の色
    self.openingBook = openingBook
  def takeTurn(self):
    raise NotImplementedError
  def canPut(self):
    return len(self.board.placeableCells(self.color)) > 0


class AI(Player):
  def __init__(self, board, color, openingBook):
    super(AI, self).__init__(board, color, openingBook)
    self.__brain = BookBrain(board, color, openingBook)
    self.__middleBrain  = AlphaBetaBrain(board, color)
    self.__endBrain     = AlphaBetaBrain(board, color)

  def __str__(self):
    return "AI"

  def takeTurn(self):
    if not self.__brain.isValid():
      self.__changeBrain()
    pos = self.__brain.evaluate()
    self.board.put(pos, self.color)  # 位置(x,y)に駒を置く
    self.board.modifyEmptyCells(pos) # 空マスリストの更新

  def __changeBrain(self):
    if self.__brain is self.__middleBrain:
      self.__brain = self.__endBrain
    else:
      self.__brain = self.__middleBrain


class Brain(object):
  def __init__(self, board, color):
    self.board = board  # boardへの参照
    self.color = color  # 自分の色
  def evaluate(self): 0
  def isValid(self):  0
     

class BookBrain(Brain):
  def __init__(self, board, color, openingBook):
    super(BookBrain, self).__init__(board, color)
    self.__openingBook = openingBook

  # <概要> OpeningBookを参照して次の手を返す
  def evaluate(self):
    x, y = self.__openingBook.readBook()
    return x + y * 8

  def isValid(self):
    return self.__openingBook.isValid()


class AlphaBetaBrain(Brain):
  def __init__(self, board, color):
    super(AlphaBetaBrain, self).__init__(board, color)
    self.__valid = True
    self.cutCounter = 0
    self.__transpositionTable = None

  # <概要> 現盤面で打てる位置に対してそれぞれ評価関数を呼び出し,
  #        その値が最大となる位置を返す.
  def evaluate(self):
    self.cutCounter = 0
    self.__transpositionTable = TranspositionTable()
    placeableCells = self.board.placeableCells(self.color)
    maxValue = -Config.INF
    for placeableCell in placeableCells:
      value = self.__evalateCell(placeableCell) # cellを評価
      if value > maxValue:
        maxValue = value
        res = placeableCell
    print "cut:",self.cutCounter
    print "col:",self.__transpositionTable.collision
    return res

  def isValid(self):  # TODO
    return self.__valid

  # <概要> 与えられたcellに駒を置いた場合の評価値を返す
  #        序盤中盤終盤ごとに評価関数を割当てている
  def __evalateCell(self, cellPos):
    statesCpy = list(self.board.board)  # 盤面コピー
    self.board.put(cellPos, self.color)
    res = -self.__alphaBeta(not self.color, Config.MAX_SEARCH_HEIGHT, -Config.INF, Config.INF, False)
    self.board.board = list(statesCpy)
    return res

  # <概要> http://uguisu.skr.jp/othello/alpha-beta.html
  # <引数> board:Board型, color:int(0~1), height:(1~MAX_SEARCH_HEIGHT), alpha:int, beta:int
  # <返値> int
  def __alphaBeta(self, color, height, alpha, beta, passed):
    if not height: # 設定した深さまでたどり着いたら再帰終了
      return self.__evaluateLeaf(color)
    placeableCells = self.board.placeableCells(color)
    if not len(placeableCells):
      if passed:
        self.__valid = False
        return self.__evaluateLeaf(color) # ゲーム終了
      return -self.__alphaBeta(not color, height, -beta, -alpha, True)  # パス
    #placeableCells = self.__moveOrdering(placeableCells, color)
    statesCpy = list(self.board.board)  # 盤面コピー
    maxValue = -Config.INF
    a = alpha
    if height > 3:
      found, key, i, alphaBeta = self.__transpositionTable.refer(self.board.board, (alpha, beta))
      if found:
        if alphaBeta[1] <= alpha:
          self.cutCounter += 1
          return alphaBeta[1]
        if alphaBeta[0] >= beta:
          self.cutCounter += 1
          return alphaBeta[0]
        if alphaBeta[0] == alphaBeta[1]:
          self.cutCounter += 1
          return alphaBeta[1]
        alpha = max(alpha, alphaBeta[0])
        beta  = min(beta,  alphaBeta[1])
      for placeableCell in placeableCells:
        self.board.put(placeableCell, color)
        value = -self.__alphaBeta(not color, height - 1, -beta, -a, False)
        self.board.board = list(statesCpy)
        if value >= beta:
          self.cutCounter += 1
          self.__transpositionTable.store(key, i, (value, Config.INF))
          return value  # カット
        if value > maxValue:
          a = max(a, value)
          maxValue = value
      if maxValue > alpha:
        self.__transpositionTable.store(key, i, (maxValue, maxValue))
      else:
        self.__transpositionTable.store(key, i, (-Config.INF, maxValue))
      return maxValue
    else:
      for placeableCell in placeableCells:
        self.board.put(placeableCell, color)
        value = -self.__alphaBeta(not color, height - 1, -beta, -a, False)
        self.board.board = list(statesCpy)
        if value >= beta:
          self.cutCounter += 1
          return value  # カット
        if value > maxValue:
          a = max(a, value)
          maxValue = value
      return maxValue

  # <概要> てきとーに http://uguisu.skr.jp/othello/5-1.html の重み付け
  def __evaluateLeaf(self, color):
    res = 0
    for y in range(8):
      code = self.board.board[y]
      for x in range(8)[::-1]:
        state = code / 3 ** x
        if state == color:
          res += Config.WEIGHTS[x + (y << 3)]
        elif state == (not color):
          res -= Config.WEIGHTS[x + (y << 3)]
    return res

  # <概要> 与えられた次手候補cellリストを評価値の見込みが高い順にソートする
  #        これによってゲーム木探索中の枝刈り回数を増加させる
  def __moveOrdering(self, cellPosList, color):
    statesCpy = list(self.board.board)  # 盤面コピー
    values = [0] * len(cellPosList)
    for i, pos in enumerate(cellPosList):
      self.board.put(pos, color)
      values[i] = - self.__evaluateLeaf(not color)
      self.board.board = list(statesCpy)
    res = []
    for value, pos in sorted(zip(values, cellPosList)):
      res += [pos]
    return res
  

class You(Player):
  def __init__(self, board, color, openingBook):
    super(You, self).__init__(board, color, openingBook)
  def __str__(self):
    return "You"
  def takeTurn(self):
    while 1:
      for event in pygame.event.get():
        if (event.type == KEYDOWN and event.key == K_ESCAPE):
          sys.exit()  # ESCAPEキーが押されたら終了
        if (event.type == KEYDOWN and event.key == K_BACKSPACE):
          raise UndoRequest() # BACKSPACEキーが押されたらUndo
        if (event.type == MOUSEBUTTONDOWN):
          xpos = int(pygame.mouse.get_pos()[0]/Config.CELL_WIDTH)
          ypos = int(pygame.mouse.get_pos()[1]/Config.CELL_WIDTH)
          if self.board.placeable(xpos + ypos * Config.CELL_NUM, self.color):
            self.board.storeStates()   # boardの要素のstateを書き換える前に,各stateを保存する
            self.board.put(xpos + ypos * Config.CELL_NUM, self.color)  # 位置(xpos,ypos)に駒を置く
            self.board.modifyEmptyCells(xpos + ypos * Config.CELL_NUM)
            if self.openingBook.isValid():
              self.openingBook.proceed(xpos, ypos)  # 定石通りかどうかチェック
            return
          else:
            print "ERROR: You cannot put here."   # クリック地点が置けない場所ならループ継続


class UndoRequest(Exception):
  def __init__(self): 0


# ============================== TranspositionTable ==============================
class TranspositionTable: # TODO

  class Element:
    def __init__(self):
      self.indexes = [None] * Config.CELL_NUM
      self.alphaBeta = None   # タプル

  def __init__(self):
    self.__table = [[TranspositionTable.Element() for j in range(Config.CHAIN_LENGTH)] for i in range(Config.TABLE_SIZE)]
    self.collision = 0

  @classmethod
  def __hash(cls, board):
    res = 0
    for i in range(8):
      res += board[i] * (17 ** i)
    return res % Config.TABLE_SIZE

  def refer(self, board, alphaBeta):
    key = TranspositionTable.__hash(board)
    for i in range(Config.CHAIN_LENGTH):
      if self.__table[key][i].alphaBeta is None:
        self.__table[key][i].alphaBeta = alphaBeta
        self.__table[key][i].indexes   = board[:8]
        return (False, key, i, alphaBeta)
      else:
        if self.__table[key][i].indexes == board[:8]:  # 発見
          return (True, key, i, self.__table[key][i].alphaBeta)
    self.collision += 1
    self.__table[key][Config.CHAIN_LENGTH-1].indexes   = board[:8]
    self.__table[key][Config.CHAIN_LENGTH-1].alphaBeta = alphaBeta
    return (False, key, Config.CHAIN_LENGTH-1, alphaBeta)

  def store(self, key, i, alphaBeta):
    self.__table[key][i].alphaBeta = alphaBeta
# ================================================================================

class Game:
  def __init__(self):
    self.__board      = board.Board()
    self.__turn       = Config.BLACK
    self.__passedFlag = False
    self.__player     = [None] * 2
    self.__openingBook = book.OpeningBook()
    self.__player[Config.AI_COLOR]      = AI(self.__board, Config.AI_COLOR, self.__openingBook)
    self.__player[not Config.AI_COLOR]  = You(self.__board, not Config.AI_COLOR, self.__openingBook)
  def run(self):
    while 1:
      self.__board.printBoard()
      if self.__player[self.__turn%2].canPut():  # 置ける場所があればTrue
        try:
          self.__player[self.__turn%2].takeTurn() # 俺のターン
          self.__passedFlag = False
        except UndoRequest:
          self.__undo()
          continue
      else:     
        print self.__player[self.__turn%2], " passed."
        if self.__passedFlag:  # 二人ともパス->終了
          return
        self.__passedFlag = True
      self.__turn += 1
  def output(self):
    self.__board.printResult()    
  def __undo(self):
    self.__board.loadStates()


def main():
  game = Game()
  game.run()
  game.output()

if __name__ == "__main__":
  main()