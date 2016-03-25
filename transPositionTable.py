# -*- coding:utf-8 -*-

import othello

class TranspositionTable: # TODO

  class Element:
    def __init__(self):
      self.indexes = [None] * 8
      self.alphaBeta = None   # タプル

  def __init__(self):
    self.__table = [[TranspositionTable.Element() for j in range(othello.Config.CHAIN_LENGTH)] for i in range(othello.Config.TABLE_SIZE)]
    self.collision = 0

  @classmethod
  def __hash(cls, board):
    res = 0
    for i in range(8):
      res += board[i] * (17 ** i)
    return res % othello.Config.TABLE_SIZE

  def refer(self, board, alphaBeta):
    key = TranspositionTable.__hash(board)
    for i in range(othello.Config.CHAIN_LENGTH):
      if self.__table[key][i].alphaBeta is None:
        self.__table[key][i].alphaBeta = alphaBeta
        self.__table[key][i].indexes   = board[:8]
        return (False, key, i, alphaBeta)
      else:
        if self.__table[key][i].indexes == board[:8]:  # 発見
          return (True, key, i, self.__table[key][i].alphaBeta)
    self.collision += 1
    self.__table[key][othello.Config.CHAIN_LENGTH-1].indexes   = board[:8]
    self.__table[key][othello.Config.CHAIN_LENGTH-1].alphaBeta = alphaBeta
    return (False, key, othello.Config.CHAIN_LENGTH-1, alphaBeta)

  def store(self, key, i, alphaBeta):
    self.__table[key][i].alphaBeta = alphaBeta