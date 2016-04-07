# -*- coding:utf-8 -*-

import othello
import midGameBrain
import endGameBrain
import time

class AI():
  def __init__(self, board, color, openingBook, weight, midGameTreeHeight, endPhaseBeginAt, visible):
    self.board = board  # boardへの参照
    self.color = color  # 自分の色
    self.__endPhaseBeginAt = endPhaseBeginAt
    self.__endBrain        = endGameBrain.EndGameBrain(board, color, visible)
    self.__middleBrain     = midGameBrain.MidGameBrain(board, color, weight, midGameTreeHeight, visible)
    if openingBook is None:
      self.__brain = self.__middleBrain
    else:
      self.__brain = BookBrain(board, color, openingBook)

  def setBoard(self, board):  # BitBoard切り替え用
    self.board = board
    self.__endBrain.setBoard(board)
    self.__middleBrain.setBoard(board)

  def changeEndPhaseBeginAt(self, endPhaseBeginAt):
    self.__endPhaseBeginAt = endPhaseBeginAt

  def setWeight(self, weight):
    self.__middleBrain.setWeight(weight)
    self.__brain = self.__middleBrain

  def canPut(self):
    return len(self.board.placeableCells(self.color)) > 0

  def __str__(self):
    return "AI"

  def takeTurn(self, turnCounter):
    if isinstance(self.__brain, BookBrain):
      if not self.__brain.isValid(turnCounter):
        self.__brain = self.__middleBrain
    elif isinstance(self.__brain, midGameBrain.MidGameBrain):
      if turnCounter >= self.__endPhaseBeginAt:
        self.__brain = self.__endBrain
    pos = self.__brain.evaluate(turnCounter)
    self.board.put(pos,self.color)
    self.board.modifyEmptyCells(pos)
    return pos

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
