# -*- coding:utf-8 -*-

import othello

# 終盤読み切り用
# 探索:AlphaBeta, 盤面評価:石差, MoveOrdering:着手可能手数の少ない順

class EndGameBrain():
  def __init__(self, board, color):
    self.board = board  # boardへの参照
    self.color = color  # 自分の色
    #self.cutCounter = 0
    #self.__transpositionTable = None

  # <概要> 現盤面で打てる位置に対してそれぞれ評価関数を呼び出し,
  #        その値が最大となる位置を返す.
  def evaluate(self, turnCounter):
    #self.__transpositionTable = transPositionTable.TranspositionTable()
    placeableCells = self.__moveOrdering(self.board.placeableCells(self.color), not self.color)
    stateCpy = self.board.getState()  # 盤面コピー
    maxValue = -othello.Config.INF
    a = -othello.Config.INF
    for placeableCell in placeableCells:
      self.board.put[placeableCell](self.color)
      value = -self.__negaScout(not self.color, 59 - turnCounter, -othello.Config.INF, -a, False)
      self.board.restoreState(stateCpy)
      if value > maxValue:
        a = max(a, value)
        maxValue = value
        res = placeableCell
    return res

  def isValid(self, turnCounter):
    return True

  def __negaScout(self, color, height, alpha, beta, passed):
    placeableCells = self.board.placeableCells(color)
    if not len(placeableCells):
      if passed:
        return self.__evaluateLeaf(color) # 連続パスでゲーム終了 TODO
      return -self.__negaScout(not color, height, -beta, -alpha, True)  # パス
    stateCpy = self.board.getState()
    if height >= 5:
      placeableCells = self.__moveOrdering(placeableCells, color)
      self.board.put[placeableCells[0]](color)
      maxValue = value = -self.__negaScout(not color, height - 1, -beta, -alpha, False)
      self.board.restoreState(stateCpy)
      if value >= beta:
        return value
      if value > alpha:
        alpha = value
      for placeableCell in placeableCells[1:]:
        self.board.put[placeableCell](color)
        value = -self.__negaScout(not color, height - 1, (-alpha) - 1, -alpha, False)
        self.board.restoreState(stateCpy)
        if value >= beta:
          return value
        if value > alpha:
          alpha = value
          self.board.put[placeableCell](color)
          value = -self.__negaScout(not color, height - 1, -beta, -alpha, False)
          self.board.restoreState(stateCpy)
          if value >= beta:
            return value
          if value > alpha:
            alpha = value
        maxValue = max(maxValue, value)
      return maxValue
    else:
      maxValue = -othello.Config.INF
      for placeableCell in placeableCells:
        self.board.put[placeableCell](color)
        value = -self.__alphaBeta(not color, height - 1, -beta, -alpha, False)
        self.board.restoreState(stateCpy)
        if value >= beta:
          return value  # カット
        if value > maxValue:
          alpha = max(alpha, value)
          maxValue = value
      return maxValue

  # <概要> http://uguisu.skr.jp/othello/alpha-beta.html
  # <引数> board:Board型, color:int(0~1), height:(1~MAX_SEARCH_HEIGHT), alpha:int, beta:int
  # <返値> int
  def __alphaBeta(self, color, height, alpha, beta, passed):
    if not height: # 設定した深さまでたどり着いたら再帰終了
      return self.__evaluateLeaf(color)
    placeableCells = self.board.placeableCells(color)
    if not len(placeableCells):
      if passed:
        return self.__evaluateLeaf(color) # 連続パスでゲーム終了
      return -self.__alphaBeta(not color, height, -beta, -alpha, True)  # パス
    #if height >= 8:
    # placeableCells = self.__moveOrdering(placeableCells, color)
    stateCpy = self.board.getState()  # 盤面コピー
    maxValue = -othello.Config.INF
    a = alpha
    for placeableCell in placeableCells:
      self.board.put[placeableCell](color)
      value = -self.__alphaBeta(not color, height - 1, -beta, -a, False)
      self.board.restoreState(stateCpy)
      if value >= beta:
        return value  # カット
      if value > maxValue:
        a = max(a, value)
        maxValue = value
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