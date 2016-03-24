# -*- coding:utf-8 -*-

import othello
import midGameBrain
import endGameBrain
#import transPositionTable # 使うとむしろ遅くなる
import time

class AI():
  def __init__(self, board, color, openingBook):
    self.board = board  # boardへの参照
    self.color = color  # 自分の色
    self.openingBook = openingBook
    self.__brain = BookBrain(board, color, openingBook)
    self.__middleBrain  = midGameBrain.MidGameBrain(board, color)
    self.__endBrain     = endGameBrain.EndGameBrain(board, color)
    self.__turnCounter  = color

  def canPut(self):
    return len(self.board.placeableCells(self.color)) > 0

  def __str__(self):
    return "AI"

  def takeTurn(self, turnCounter):
    if not self.__brain.isValid():
      self.__changeBrain()
      print "change"
    start = time.time()
    pos = self.__brain.evaluate(turnCounter)
    self.board.put[pos](self.color)  # 位置(x,y)に駒を置く
    self.board.modifyEmptyCells(pos) # 空マスリストの更新
    print ("time:{0}".format(time.time()-start))+"[sec]"

  def __changeBrain(self):
    if self.__brain is self.__middleBrain:
      self.__brain = self.__endBrain
    else:
      self.__brain = self.__middleBrain


class BookBrain():
  def __init__(self, board, color, openingBook):
    self.board = board  # boardへの参照
    self.color = color  # 自分の色
    self.__openingBook = openingBook

  # <概要> OpeningBookを参照して次の手を返す
  def evaluate(self, turnCounter): # turnCounterはここでは使わない
    x, y = self.__openingBook.readBook()
    return x + y * 8

  def isValid(self):
    return self.__openingBook.isValid()
