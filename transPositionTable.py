# -*- coding:utf-8 -*-

import othello

class TranspositionTable: # TODO

  class Element:
    def __init__(self):
      self.indexes = [None] * 8
      self.alphaBeta = None   # タプル

  def __init__(self):
    self.TABLE_SIZE = othello.Config.TABLE_SIZE
    self.__table = [TranspositionTable.Element() for i in range(self.TABLE_SIZE)]

  @classmethod
  def __hash(cls, indexes):
    #for i in range(8):
    #  res += indexes[i] * (17 ** i)
    return (((((((indexes[7]*17+indexes[6])*17+indexes[5])*17+indexes[4])*17+indexes[3])*17+indexes[2])*17+indexes[1])*17+indexes[0]) % self.TABLE_SIZE

  def refer(self, board, alphaBeta):
    indexes = board.board[:8]
    key = (((((((indexes[7]*17+indexes[6])*17+indexes[5])*17+indexes[4])*17+indexes[3])*17+indexes[2])*17+indexes[1])*17+indexes[0]) % self.TABLE_SIZE
    if self.__table[key].alphaBeta is None or self.__table[key].indexes != indexes:
      self.__table[key].alphaBeta = alphaBeta
      self.__table[key].indexes   = indexes
      return (False, key, alphaBeta)
    else:
      return (True, key, self.__table[key].alphaBeta)

  def store(self, key, alphaBeta):
    self.__table[key].alphaBeta = alphaBeta

  def stored(self, board):
    indexes = board.board[:8]
    key = (((((((indexes[7]*17+indexes[6])*17+indexes[5])*17+indexes[4])*17+indexes[3])*17+indexes[2])*17+indexes[1])*17+indexes[0]) % self.TABLE_SIZE
    return self.__table[key].alphaBeta is not None and self.__table[key].indexes == indexes
