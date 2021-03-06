# -*- coding:utf-8 -*-

"""
  references:
    http://d.hatena.ne.jp/Megumi221/20081031/1225450482
"""

import pygame
from pygame.locals import *
import sys
import bitBoard
import indexBoard
import book
import AI


class Config:
  BLACK         = 0
  WHITE         = 1
  EMPTY         = 2
  CELL_WIDTH    = 100
  CELL_NUM      = 8
  WINDOW_WIDTH  = CELL_WIDTH * CELL_NUM
  WPOS          = CELL_WIDTH * (CELL_NUM - 1)
  INF           = sys.maxint
  POW3          = [3 ** i for i in range(8)]

  AI_COLOR      = BLACK
  MID_HEIGHT    = 7       # 中盤ゲーム木の高さ
  LAST_PHASE    = 44      # 終盤読み切りを開始するタイミング
  TABLE_SIZE    = 65537   # 置換表のハッシュテーブルサイズ
  WEIGHTS       = [ [ 30, -12,  0, -1, -1,  0, -12,  30],
                    [-12, -15, -3, -3, -3, -3, -15, -12],
                    [  0,  -3,  0, -1, -1,  0,  -3,   0],
                    [ -1,  -3, -1, -1, -1, -1,  -3,  -1],
                    [ -1,  -3, -1, -1, -1, -1,  -3,  -1],
                    [  0,  -3,  0, -1, -1,  0,  -3,   0],
                    [-12, -15, -3, -3, -3, -3, -15, -12],
                    [ 30, -12,  0, -1, -1,  0, -12,  30] ]
  BITBOARD      = False    # 終盤探索でBitBoardを使用するか否か

class You():
  def __init__(self, board, color, openingBook):
    self.board = board  # boardへの参照
    self.color = color  # 自分の色
    self.openingBook = openingBook
  def canPut(self):
    return len(self.board.placeableCells(self.color)) > 0
  def __str__(self):
    return "You"
  def takeTurn(self, turnCounter): # turnCounterは使わない
    while 1:
      for event in pygame.event.get():
        if (event.type == KEYDOWN and event.key == K_ESCAPE):
          sys.exit()  # ESCAPEキーが押されたら終了
        if (event.type == KEYDOWN and event.key == K_BACKSPACE):
          raise UndoRequest() # BACKSPACEキーが押されたらUndo
        if (event.type == MOUSEBUTTONDOWN):
          xpos = int(pygame.mouse.get_pos()[0]/Config.CELL_WIDTH)
          ypos = int(pygame.mouse.get_pos()[1]/Config.CELL_WIDTH)
          pos  = xpos + ypos * Config.CELL_NUM
          if self.board.placeable(pos,self.color):
            self.board.storeState()   # boardの要素のstateを書き換える前に,各stateを保存する
            self.board.put(pos,self.color)
            self.board.modifyEmptyCells(pos)
            if self.openingBook.isValid():
              self.openingBook.proceed(xpos, ypos)  # 定石通りかどうかチェック
            return pos
          else:
            print "ERROR: You cannot put here."   # クリック地点が置けない場所ならループ継続
  def setBoard(self, board):  # BitBoard切り替え用
    self.board = board

class UndoRequest(Exception):
  def __init__(self): 0


class Game:
  def __init__(self):
    self.__board  = indexBoard.IndexBoard(True)
    self.__player = [None] * 2
    self.__openingBook = book.OpeningBook()
    self.__player[Config.AI_COLOR]     = AI.AI(self.__board, Config.AI_COLOR, self.__openingBook, None, Config.MID_HEIGHT, Config.LAST_PHASE, True)
    self.__player[not Config.AI_COLOR] = You(self.__board, not Config.AI_COLOR, self.__openingBook)
  def init(self):
    self.__board.init()
    self.__turn         = Config.BLACK # = 0
    self.__turnCounter  = 0
    self.__passedFlag   = False
    self.__puttedPos    = -1

  def run(self):
    while 1:
      self.__board.printBoard(self.__puttedPos, self.__turn%2)
      if self.__turnCounter == 60:
        break
      if self.__turnCounter == Config.LAST_PHASE and Config.BITBOARD and isinstance(self.__board, indexBoard.IndexBoard):
        cells = self.__board.getCells()
        empcells = list(self.__board.emptyCells)
        self.__board = bitBoard.BitBoard(True)  # boardをindexからbitに変更
        self.__board.setState(cells, empcells)
        self.__player[0].setBoard(self.__board)
        self.__player[1].setBoard(self.__board)
        self.__board.printBoard(self.__puttedPos, self.__turn%2)
      if self.__player[self.__turn%2].canPut():  # 置ける場所があればTrue
        try:
          print "Turn:", self.__turnCounter
          self.__puttedPos  = self.__player[self.__turn%2].takeTurn(self.__turnCounter) # 俺のターン
          self.__passedFlag = False
        except UndoRequest:
          self.__undo()
          self.__turnCounter -= 2
          continue
        self.__turnCounter += 1
      else:
        print self.__player[self.__turn%2], " passed."
        if self.__passedFlag:  # 二人ともパス->終了
          return
        self.__passedFlag = True
      self.__turn += 1

  def output(self):
    self.__board.printResult()

  def __undo(self):
    self.__board.loadState()  

def main():
  game = Game()
  game.init()
  game.run()
  game.output()

if __name__ == "__main__":
  main()
