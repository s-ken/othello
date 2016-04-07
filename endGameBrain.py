# -*- coding:utf-8 -*-

import othello
import time

# 終盤読み切り用
# 探索:AlphaBeta, 盤面評価:石差, MoveOrdering:着手可能手数の少ない順

class EndGameBrain():
  def __init__(self, board, color, visible):
    self.board = board  # boardへの参照
    self.color = color  # 自分の色
    self.nodeCounter = 0
    self.__visible = visible
    #self.__transpositionTable = None

  # <概要> 現盤面で打てる位置に対してそれぞれ評価関数を呼び出し,
  #        その値が最大となる位置を返す.
  def evaluate(self, turnCounter):
    if self.__visible:
      start = time.time()
    self.nodeCounter = 0
    #self.__transpositionTable = transPositionTable.TranspositionTable()
    placeableCells = self.__moveOrdering(self.board.placeableCells(self.color), not self.color)
    stateCpy = self.board.getState()  # 盤面コピー
    emptyCpy = list(self.board.emptyCells)
    maxValue = -othello.Config.INF
    a = -othello.Config.INF
    for pos in placeableCells:
      self.nodeCounter += 1
      self.board.put[pos](self.color)
      self.board.modifyEmptyCells(pos)
      value = -self.__negaScout(not self.color, 59 - turnCounter, -othello.Config.INF, -a, False)
      self.board.restoreState(stateCpy)
      self.board.emptyCells = list(emptyCpy)
      if value > maxValue:
        a = max(a, value)
        maxValue = value
        res = pos
    if self.__visible:
      t = time.time()-start
      print ("time: {0}".format(t)+"[sec]")
      print "node:", self.nodeCounter
      if t != 0:
       print "nps:", self.nodeCounter / t
      print "expectation:", maxValue
    return res

  def __negaScout(self, color, height, alpha, beta, passed):
    if height >= 7:
      placeableCells = self.board.placeableCells(color)
      if not len(placeableCells):
        if passed:
          return self.__evaluateLeaf(color) # 連続パスでゲーム終了 TODO
        return -self.__negaScout(not color, height, -beta, -alpha, True)  # パス
      stateCpy = self.board.getState()
      emptyCpy = list(self.board.emptyCells)
      placeableCells = self.__moveOrdering(placeableCells, color)
      self.board.put[placeableCells[0]](color)
      self.board.modifyEmptyCells(placeableCells[0])
      maxValue = value = -self.__negaScout(not color, height - 1, -beta, -alpha, False)
      self.board.restoreState(stateCpy)
      self.board.emptyCells = list(emptyCpy)
      if value >= beta:
        return value
      if value > alpha:
        alpha = value
      for pos in placeableCells[1:]:
        self.nodeCounter += 1
        self.board.put[pos](color)
        self.board.modifyEmptyCells(pos)
        value = -self.__negaScout(not color, height - 1, (-alpha) - 1, -alpha, False)
        if value >= beta:
          self.board.restoreState(stateCpy)
          self.board.emptyCells = list(emptyCpy)
          return value
        if value > alpha:
          alpha = value
          value = -self.__negaScout(not color, height - 1, -beta, -alpha, False)
          if value >= beta:
            self.board.restoreState(stateCpy)
            self.board.emptyCells = list(emptyCpy)
            return value
          if value > alpha:
            alpha = value
        maxValue = max(maxValue, value)
        self.board.restoreState(stateCpy)
        self.board.emptyCells = list(emptyCpy)
      return maxValue
    else:
      stateCpy = self.board.getState()  # 盤面コピー
      emptyCpy = list(self.board.emptyCells)
      maxValue = -othello.Config.INF
      a = alpha
      count = 0
      for pos in list(self.board.emptyCells):
        if self.board.placeable[pos](color):
          self.nodeCounter += 1
          count += 1
          self.board.put[pos](color)
          self.board.modifyEmptyCells(pos)
          value = -self.__alphaBeta(not color, height - 1, -beta, -a, False)
          self.board.restoreState(stateCpy)
          self.board.emptyCells = list(emptyCpy)
          if value >= beta:
            return value  # カット
          if value > maxValue:
            a = max(a, value)
            maxValue = value
      if not count:
        if passed:
          return self.__evaluateLeaf(color) # 連続パスでゲーム終了
        return -self.__alphaBeta(not color, height, -beta, -alpha, True)  # パス
      return maxValue

  # <概要> http://uguisu.skr.jp/othello/alpha-beta.html
  # <引数> board:Board型, color:int(0~1), height:(1~MAX_SEARCH_HEIGHT), alpha:int, beta:int
  # <返値> int
  def __alphaBeta(self, color, height, alpha, beta, passed):
    if height == 1: # 空きマスラスト1 --> ラスト1手最適化
      if self.board.placeable[self.board.emptyCells[0]](color):
        self.nodeCounter += 1
        return self.__evaluateLeafLast1(color, self.board.emptyCells[0])
      else:
        if passed:
          return self.__evaluateLeaf(color) # 連続パスでゲーム終了
        if self.board.placeable[self.board.emptyCells[0]](not color):
          self.nodeCounter += 1
          return -self.__evaluateLeafLast1(not color, self.board.emptyCells[0])
        else:
          return -self.__evaluateLeaf(not color) # 連続パスでゲーム終了
    else:
      stateCpy = self.board.getState()  # 盤面コピー
      emptyCpy = list(self.board.emptyCells)
      maxValue = -othello.Config.INF
      a = alpha
      count = 0
      for pos in list(self.board.emptyCells):
        if self.board.placeable[pos](color):
          self.nodeCounter += 1
          self.board.put[pos](color)
          self.board.modifyEmptyCells(pos)
          value = -self.__alphaBeta(not color, height - 1, -beta, -a, False)
          self.board.restoreState(stateCpy)
          self.board.emptyCells = list(emptyCpy)
          if value >= beta:
            return value  # カット
          if value > maxValue:
            a = max(a, value)
            maxValue = value
          count += 1
      if not count:
        if passed:
          return self.__evaluateLeaf(color) # 連続パスでゲーム終了
        return -self.__alphaBeta(not color, height, -beta, -alpha, True)  # パス
      return maxValue

  # <概要> 相手の置ける場所が少なくなる順にソート
  def __moveOrdering(self, cellPosList ,color):
    stateCpy = self.board.getState()  # 盤面コピー
    values = [0] * len(cellPosList)
    for i, pos in enumerate(cellPosList):
      self.board.put[pos](color)
      #values[i] = self.board.getMobility(not color)
      values[i] = self.board.placeableCellsNum(not color)
      self.board.restoreState(stateCpy)
    return [pos for value, pos in sorted(zip(values, cellPosList))]

  # <概要> 石差で評価
  def __evaluateLeaf(self, color):
    return self.board.getDifference(color)

  def __evaluateLeafLast1(self, color, pos):
    return self.board.getDifference(color) + (self.board.takes[pos](color) << 1) + 1