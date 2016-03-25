# -*- coding:utf-8 -*-

import othello
import transPositionTable

# 中盤
# 探索:AlphaBeta, 盤面評価:位置+着手可能手数+確定石数, MoveOrdering:1手先の盤面評価値

class MidGameBrain():
  def __init__(self, board, color):
    self.board = board  # boardへの参照
    self.color = color  # 自分の色
    self.__valid = True
    #self.cutCounter = 0
    self.__transpositionTable = None

  # <概要> 現盤面で打てる位置に対してそれぞれ評価関数を呼び出し,
  #        その値が最大となる位置を返す.
  def evaluate(self, turnCounter):
    #self.cutCounter = 0
    self.__transpositionTable = transPositionTable.TranspositionTable()
    placeableCells = self.board.placeableCells(self.color)
    self.__moveOrderingFirst(self.board.placeableCells(self.color), self.color)
    stateCpy = self.board.getState()  # 盤面コピー
    maxValue = -othello.Config.INF
    a = -othello.Config.INF
    for placeableCell in placeableCells:
      self.board.put[placeableCell](self.color)
      value = -self.__alphaBeta(not self.color, othello.Config.MID_HEIGHT-1, -othello.Config.INF, -a, False)
      self.board.restoreState(stateCpy)
      if value > maxValue:
        a = max(a, value)
        maxValue = value
        res = placeableCell
    #print "cut:",self.cutCounter
    #print "col:",self.__transpositionTable.collision
    if turnCounter+2 >= othello.Config.LAST_PHASE:
      self.__valid = False
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
        return self.__evaluateLeaf(color) # 連続パスでゲーム終了 TODO
      return -self.__alphaBeta(not color, height, -beta, -alpha, True)  # パス
    if height >= 3:
      placeableCells = self.__moveOrdering(placeableCells, color)
    stateCpy = self.board.getState()  # 盤面コピー
    maxValue = -othello.Config.INF
    a = alpha
    """
    if height >= 7:
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
        self.board.put[placeableCell](color)
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

  # <概要> 与えられた次手候補cellリストを評価値の見込みが高い順にソートする.
  #        これによってゲーム木探索中の枝刈り回数を増加させる.
  #        具体的には1手先の盤面を評価関数で評価した値を比較している.
  def __moveOrdering(self, cellPosList, color):
    stateCpy = self.board.getState()  # 盤面コピー
    values = [0] * len(cellPosList)
    for i, pos in enumerate(cellPosList):
      self.board.put[pos](color)
      values[i] = self.__evaluateLeaf(color)
      self.board.restoreState(stateCpy)
    return [pos for value, pos in sorted(zip(values, cellPosList),reverse=True)]

  # <概要> 探索木のrootでのMoveOrdering関数
  #        // 深さ3の探索の評価値をもとにソートする
  #        通常のやつと同じ
  def __moveOrderingFirst(self, cellPosList, color):
    stateCpy = self.board.getState()  # 盤面コピー
    values = [0] * len(cellPosList)
    for i, pos in enumerate(cellPosList):
      self.board.put[pos](color)
      #values[i] = -self.__alphaBeta(not color, 2, -othello.Config.INF, othello.Config.INF, False)
      values[i] = self.__evaluateLeaf(color)
      self.board.restoreState(stateCpy)
    return [pos for value, pos in sorted(zip(values, cellPosList),reverse=True)]

  # <概要> http://uguisu.skr.jp/othello/5-1.html の位置重み付け + 確定石数差*8 + 置ける場所の数の差*4
  def __evaluateLeaf(self, color):
    res =  self.board.getEval(color)
    res += self.board.getSettled(color) << 3
    res += self.board.getMobility(color) << 1 # 着手可能候補数
    return res