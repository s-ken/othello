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
  MAX_SEARCH_HEIGHT = 4 # ゲーム木の高さ
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
  LAST_PHASE = 40

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
    self.__endBrain     = EndBrain(board, color)

  def __str__(self):
    return "AI"

  def takeTurn(self):
    if not self.__brain.isValid():
      self.__changeBrain()
      print "change"
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

  # <概要> 現盤面で打てる位置に対してそれぞれ評価関数を呼び出し,
  #        その値が最大となる位置を返す.
  def evaluate(self):
    placeableCells = self.board.placeableCells(self.color)
    maxValue = -Config.INF
    for placeableCell in placeableCells:
      value = self.__evalateCell(placeableCell) # cellを評価
      if value > maxValue:
        maxValue = value
        res = placeableCell
    return res

  def isValid(self):  # TODO
    return self.__valid

  # <概要> 与えられたcellに駒を置いた場合の評価値を返す
  #        序盤中盤終盤ごとに評価関数を割当てている
  def __evalateCell(self, cellPos):
    statesCpy = list(self.board.board)  # 盤面コピー
    self.board.put(cellPos, self.color)
    res = -self.__alphaBeta(not self.color, Config.MAX_SEARCH_HEIGHT, -Config.INF, Config.INF)
    self.board.board = list(statesCpy)
    return res

  # <概要> http://uguisu.skr.jp/othello/alpha-beta.html
  # <引数> board:Board型, color:int(0~1), height:(1~MAX_SEARCH_HEIGHT), alpha:int, beta:int
  # <返値> int
  def __alphaBeta(self, color, height, alpha, beta):
    if not height: # 設定した深さまでたどり着いたら再帰終了
      return self.__evaluateLeaf(color)
    placeableCells = self.board.placeableCells(color)
    if not len(placeableCells):  # パス発生or試合終了でも再帰終了
      self.__valid = False
      return self.__evaluateLeaf(color)
    #placeableCells = self.__moveOrdering(placeableCells, color)
    statesCpy = list(self.board.board)  # 盤面コピー
    for placeableCell in placeableCells:
      self.board.put(placeableCell, color)
      alpha = max(alpha, -self.__alphaBeta(not color, height - 1, -beta, -alpha))
      if alpha >= beta:
        return alpha  # カット
      self.board.board = list(statesCpy)
    return alpha

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

  """ TODO
  # <概要> 与えられた次手候補cellリストを評価値の見込みが高い順にソートする
  #        これによってゲーム木探索中の枝刈り回数を増加させる
  def __moveOrdering(self, cells, color):  # TODO
    statesCpy = self.board.getStates()
    values = [None] * len(cells)
    for i, cell in enumerate(cells):
      self.board.put(cell.x, cell.y, color)
      values[i] = - self.__evaluateLeaf(not color)
      self.board.restoreStates(statesCpy)
    res = []
    for value, cell in sorted(zip(values, cells), reverse = True):
      res += [cell]
    return res
  """

class EndBrain(Brain):
  def __init__(self, board, color):
    super(EndBrain, self).__init__(board, color)

  # <概要> 現盤面で打てる位置に対してそれぞれ評価関数を呼び出し,
  #        その値が最大となる位置を返す.
  def evaluate(self):
    placeableCells = self.board.placeableCells(self.color)
    maxValue = -Config.INF
    for placeableCell in placeableCells:
      value = self.__evalateCell(placeableCell) # cellを評価
      if value > maxValue:
        maxValue = value
        res = placeableCell
    return res

  def isValid(self):  # TODO
    return True

  # <概要> 与えられたcellに駒を置いた場合の評価値を返す
  #        序盤中盤終盤ごとに評価関数を割当てている
  def __evalateCell(self, cellPos):
    statesCpy = list(self.board.board)  # 盤面コピー
    self.board.put(cellPos, self.color)
    res = -self.__alphaBeta(not self.color, Config.MAX_SEARCH_HEIGHT, -Config.INF, Config.INF)
    self.board.board = list(statesCpy)
    return res

  # <概要> http://uguisu.skr.jp/othello/alpha-beta.html
  # <引数> board:Board型, color:int(0~1), height:(1~MAX_SEARCH_HEIGHT), alpha:int, beta:int
  # <返値> int
  def __alphaBeta(self, color, height, alpha, beta):
    if not height: # 設定した深さまでたどり着いたら再帰終了
      return self.__evaluateLeaf(color)
    placeableCells = self.board.placeableCells(color)
    if not len(placeableCells):  # パス発生or試合終了でも再帰終了
      return self.__evaluateLeaf(color)
    #placeableCells = self.__moveOrdering(placeableCells, color)
    statesCpy = list(self.board.board)  # 盤面コピー
    for placeableCell in placeableCells:
      self.board.put(placeableCell, color)
      alpha = max(alpha, -self.__alphaBeta(not color, height - 1, -beta, -alpha))
      if alpha >= beta:
        return alpha  # カット
      self.board.board = list(statesCpy)
    return alpha

  # <概要> てきとーに http://uguisu.skr.jp/othello/5-1.html の重み付け
  def __evaluateLeaf(self, color):
    res = 0
    for y in range(8):
      code = self.board.board[y]
      for x in range(8)[::-1]:
        state = code / 3 ** x
        if state == color:
          res += 1
        elif state == (not color):
          res -= 1
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

"""
class TranspositionTable: # TODO

  class Element:
    def __init__(self):
      self.indexes = [None] * Config.CELL_NUM
      self.alpha = None
      self.beta = None

  def __init__(self):
    self.__table = [Element() for i in range(Config.TABLE_SIZE)]  # 窓幅を格納(min, max)

  @classmethod
  def __hash(self, board):
    res = 0
    for i, cell in enumerate(board.board):
      res += (cell.state * 3 ** (i % Config.CELL_NUM)) * 17 ** (i / Config.CELL_NUM)
      res %= Config.TABLE_SIZE
    return res
"""

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
