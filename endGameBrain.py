# -*- coding:utf-8 -*-

import othello

# 終盤読み切り用
# 探索:AlphaBeta, 盤面評価:石差, MoveOrdering:着手可能手数の少ない順

class EndGameBrain():
  def __init__(self, board, color):
    self.board = board  # boardへの参照
    self.color = color  # 自分の色
    self.__valid = True
    #self.cutCounter = 0
    #self.__transpositionTable = None

  # <概要> 現盤面で打てる位置に対してそれぞれ評価関数を呼び出し,
  #        その値が最大となる位置を返す.
  def evaluate(self, turnCounter):
    #self.cutCounter = 0
    #self.__transpositionTable = transPositionTable.TranspositionTable()
    placeableCells = self.__moveOrdering(self.board.placeableCells(self.color), not self.color)
    stateCpy = self.board.getState()  # 盤面コピー
    maxValue = -othello.Config.INF
    a = -othello.Config.INF
    for placeableCell in placeableCells:
      self.board.put[placeableCell](self.color)
      value = -self.__alphaBeta(not self.color, 59 - turnCounter, -othello.Config.INF, -a, False)
      self.board.restoreState(stateCpy)
      if value > maxValue:
        a = max(a, value)
        maxValue = value
        res = placeableCell
    #print "cut:",self.cutCounter
    #print "col:",self.__transpositionTable.collision
    return res

  def isValid(self):  # TODO
    return self.__valid

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
    if height >= 8:
      placeableCells = self.__moveOrdering(placeableCells, color)
    stateCpy = self.board.getState()  # 盤面コピー
    maxValue = -othello.Config.INF
    a = alpha
    """
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
        self.board.restore(stateCpy)
        if value >= beta:
          self.cutCounter += 1
          self.__transpositionTable.store(key, i, (value, othello.Config.INF))
          return value  # カット
        if value > maxValue:
          a = max(a, value)
          maxValue = value
      if maxValue > alpha:
        self.__transpositionTable.store(key, i, (maxValue, maxValue))
      else:
        self.__transpositionTable.store(key, i, (-othello.Config.INF, maxValue))
      return maxValue
    else:
      for placeableCell in placeableCells:
        self.board.put(placeableCell, color)
        value = -self.__alphaBeta(not color, height - 1, -beta, -a, False)
        self.board.restoreState(stateCpy)
        if value >= beta:
          self.cutCounter += 1
          return value  # カット
        if value > maxValue:
          a = max(a, value)
          maxValue = value
      return maxValue
      """
    for placeableCell in placeableCells:
      self.board.put[placeableCell](color)
      value = -self.__alphaBeta(not color, height - 1, -beta, -a, False)
      self.board.restoreState(stateCpy)
      if value >= beta:
        #self.cutCounter += 1
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