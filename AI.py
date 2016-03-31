# -*- coding:utf-8 -*-

import othello
import midGameBrain
import endGameBrain
import time

class AI():
  def __init__(self, board, color, openingBook, weight):
    self.board = board  # boardへの参照
    self.color = color  # 自分の色
    self.__endBrain = endGameBrain.EndGameBrain(board, color)
    self.__middleBrain = midGameBrain.MidGameBrain(board, color, weight)
    if openingBook is None:
      self.__brain = self.__middleBrain
    else:
      self.__brain = BookBrain(board, color, openingBook)

  def setWeight(self, weight):
    self.__middleBrain.setWeight(weight)
    self.__brain = self.__middleBrain

  def canPut(self):
    return len(self.board.placeableCells(self.color)) > 0

  def __str__(self):
    return "AI"

  def takeTurn(self, turnCounter):
    if not self.__brain.isValid(turnCounter):
      self.__changeBrain()
    #  print "change"
    #start = time.time()
    pos = self.__brain.evaluate(turnCounter)
    self.board.put[pos](self.color)  # 位置(x,y)に駒を置く
    self.board.modifyEmptyCells(pos) # 空マスリストの更新
    #print ("time:{0}".format(time.time()-start))+"[sec]"
    return pos

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

  def isValid(self, turnCounter):
    return self.__openingBook.isValid()
