# -*- coding:utf-8 -*-

import othello
import transPositionTable
import time

# 中盤
# 探索:AlphaBeta, 盤面評価:位置+着手可能手数+確定石数, MoveOrdering:1手先の盤面評価値

class MidGameBrain():
  STAGES   = 60/4
  FEATURES = 11
  PATTARNS = [3**8]*3 + [3**4, 3**5, 3**6, 3**7, 3**8] + [3**10]*2 + [3**9]  

  def __init__(self, board, color, weight, treeHeight, visible):
    self.board = board  # boardへの参照
    self.color = color  # 自分の色
    self.__treeHeight = treeHeight
    self.__visible = visible
    #self.__transpositionTable = None
    if weight is None:
      self.__weight = self.__loadWeights()
    else:
      self.__weight = weight  # Logistello重み

  # <概要> 現盤面で打てる位置に対してそれぞれ評価関数を呼び出し,
  #        その値が最大となる位置を返す.
  def evaluate(self, turnCounter):
    if self.__visible:
      start = time.time()
    #self.__transpositionTable = transPositionTable.TranspositionTable()
    placeableCells = self.board.placeableCells(self.color)
    self.__moveOrderingFirst(self.board.placeableCells(self.color), self.color, turnCounter)
    stateCpy = self.board.getState()  # 盤面コピー
    emptyCpy = list(self.board.emptyCells)
    maxValue = -othello.Config.INF
    a = -othello.Config.INF
    """
    self.board.put[placeableCells[0]](self.color)
    maxValue = value = -self.__negaScout(not self.color, self.__treeHeight-1, -othello.Config.INF, othello.Config.INF, False, turnCounter+1)
    res = placeableCells[0]
    self.board.restoreState(stateCpy)
    alpha = value
    beta  = othello.Config.INF
    for pos in placeableCells[1:]:
      self.board.put[pos](self.color)
      value = -self.__negaScout(not self.color, self.__treeHeight-1, (-alpha) - 1, -alpha, False, turnCounter+1)
      if value > alpha:
        alpha = value
        value = -self.__negaScout(not self.color, self.__treeHeight-1, -beta, -alpha, False, turnCounter+1)
        if value > alpha:
          alpha = value
      if value > maxValue:
        maxValue = value
        res = pos
      self.board.restoreState(stateCpy)
    if self.__visible:
      t = time.time()-start
      print ("time: {0}".format(t)+"[sec]")
    return res
    """
    for pos in placeableCells:
      self.board.put[pos](self.color)
      self.board.modifyEmptyCells(pos)
      value = -self.__alphaBeta(not self.color, self.__treeHeight-1, -othello.Config.INF, -a, False, turnCounter+1)
      self.board.restoreState(stateCpy)
      self.board.emptyCells = list(emptyCpy)
      if value > maxValue:
        a = max(a, value)
        maxValue = value
        res = pos
    if self.__visible:
      t = time.time()-start
      print ("time: {0}".format(t)+"[sec]")
    return res

  def setWeight(self, weight):
    self.__weight = weight

  """
  # 中盤ではnegaScoutよりalphaBetaの方が速い
  def __negaScout(self, color, height, alpha, beta, passed, turnCounter):
    if height >= 5:
      placeableCells = self.board.placeableCells(color)
      if not len(placeableCells):
        if passed:
          return self.__evaluateLeaf(color, turnCounter) # 連続パスでゲーム終了 TODO
        return -self.__negaScout(not color, height, -beta, -alpha, True, turnCounter)  # パス
      stateCpy = self.board.getState()
      placeableCells = self.__moveOrdering(placeableCells, color, turnCounter)
      self.board.put[placeableCells[0]](color)
      maxValue = value = -self.__negaScout(not color, height-1, -beta, -alpha, False, turnCounter+1)
      self.board.restoreState(stateCpy)
      if value >= beta:
        return value
      if value > alpha:
        alpha = value
      for pos in placeableCells[1:]:
        self.board.put[pos](color)
        value = -self.__negaScout(not color, height-1, (-alpha) - 1, -alpha, False, turnCounter+1)
        if value >= beta:
          self.board.restoreState(stateCpy)
          return value
        if value > alpha:
          alpha = value
          value = -self.__negaScout(not color, height-1, -beta, -alpha, False, turnCounter+1)
          if value >= beta:
            self.board.restoreState(stateCpy)
            return value
          if value > alpha:
            alpha = value
        maxValue = max(maxValue, value)
        self.board.restoreState(stateCpy)
      return maxValue
    elif height >= 3:
      placeableCells = self.board.placeableCells(color)
      if not len(placeableCells):
        if passed:
          return self.__evaluateLeaf(color, turnCounter) # 連続パスでゲーム終了 TODO
        return -self.__alphaBeta(not color, height, -beta, -alpha, True, turnCounter)  # パス
      placeableCells = self.__moveOrdering(placeableCells, color, turnCounter)
      stateCpy = self.board.getState()  # 盤面コピー
      maxValue = -othello.Config.INF
      for pos in placeableCells:
        self.board.put[pos](color)
        value = -self.__alphaBeta(not color, height-1, -beta, -alpha, False, turnCounter+1)
        self.board.restoreState(stateCpy)
        if value >= beta:
          return value  # カット
        if value > maxValue:
          alpha = max(alpha, value)
          maxValue = value
      return maxValue
    else:
      stateCpy = self.board.getState()  # 盤面コピー
      maxValue = -othello.Config.INF
      a = alpha
      count = 0
      for pos in self.board.emptyCells:
        if self.board.placeable[pos](color):
          self.board.put[pos](color)
          value = -self.__alphaBetaNoMO(not color, height - 1, -beta, -a, False, turnCounter+1)
          self.board.restoreState(stateCpy)
          if value >= beta:
            return value  # カット
          if value > maxValue:
            a = max(a, value)
            maxValue = value
          count += 1
      if not count:
        if passed:
          return self.__evaluateLeaf(color, turnCounter) # 連続パスでゲーム終了
        return -self.__alphaBeta(not color, height, -beta, -alpha, True, turnCounter)  # パス
      return maxValue
  """

  # <概要> http://uguisu.skr.jp/othello/alpha-beta.html
  # <引数> board:Board型, color:int(0~1), height:(1~MAX_SEARCH_HEIGHT), alpha:int, beta:int
  # <返値> int
  def __alphaBeta(self, color, height, alpha, beta, passed, turnCounter):
    if not height: # 設定した深さまでたどり着いたら再帰終了
      return self.__evaluateLeaf(color, turnCounter)

    if height >= 3:
      placeableCells = self.board.placeableCells(color)
      if not len(placeableCells):
        if passed:
          return self.__evaluateLeaf(color, turnCounter) # 連続パスでゲーム終了 TODO
        return -self.__alphaBeta(not color, height, -beta, -alpha, True, turnCounter)  # パス
      placeableCells = self.__moveOrdering(placeableCells, color, turnCounter)
      stateCpy = self.board.getState()  # 盤面コピー
      maxValue = -othello.Config.INF
      for pos in placeableCells:
        self.board.put[pos](color)
        value = -self.__alphaBeta(not color, height-1, -beta, -alpha, False, turnCounter+1)
        self.board.restoreState(stateCpy)
        if value >= beta:
          return value  # カット
        if value > maxValue:
          alpha = max(alpha, value)
          maxValue = value
      return maxValue

    stateCpy = self.board.getState()  # 盤面コピー
    maxValue = -othello.Config.INF
    a = alpha
    count = 0
    for pos in self.board.emptyCells:
      if self.board.placeable[pos](color):
        self.board.put[pos](color)
        value = -self.__alphaBetaNoMO(not color, height - 1, -beta, -a, False, turnCounter+1)
        self.board.restoreState(stateCpy)
        if value >= beta:
          return value  # カット
        if value > maxValue:
          a = max(a, value)
          maxValue = value
        count += 1
    if not count:
      if passed:
        return self.__evaluateLeaf(color, turnCounter) # 連続パスでゲーム終了
      return -self.__alphaBeta(not color, height, -beta, -alpha, True, turnCounter)  # パス
    return maxValue

  def __alphaBetaNoMO(self, color, height, alpha, beta, passed, turnCounter):
    if not height: # 設定した深さまでたどり着いたら再帰終了
      return self.__evaluateLeaf(color, turnCounter)
    stateCpy = self.board.getState()  # 盤面コピー
    maxValue = -othello.Config.INF
    a = alpha
    count = 0
    for pos in self.board.emptyCells:
      if self.board.placeable[pos](color):
        self.board.put[pos](color)
        value = -self.__alphaBetaNoMO(not color, height - 1, -beta, -a, False, turnCounter+1)
        self.board.restoreState(stateCpy)
        if value >= beta:
          return value  # カット
        if value > maxValue:
          a = max(a, value)
          maxValue = value
        count += 1
    if not count:
      if passed:
        return self.__evaluateLeaf(color, turnCounter) # 連続パスでゲーム終了
      return -self.__alphaBetaNoMO(not color, height, -beta, -alpha, True, turnCounter)  # パス
    return maxValue

  # <概要> 与えられた次手候補cellリストを評価値の見込みが高い順にソートする.
  #        これによってゲーム木探索中の枝刈り回数を増加させる.
  #        具体的には1手先の盤面を評価関数で評価した値を比較している.
  def __moveOrdering(self, cellPosList, color, turnCounter):
    stateCpy = self.board.getState()  # 盤面コピー
    values = [0] * len(cellPosList)
    for i, pos in enumerate(cellPosList):
      self.board.put[pos](color)
      values[i] = self.__evaluateLeaf(color, turnCounter+1)
      #values[i] = -self.__alphaBeta(not color, 2, -1024, 1024, False, turnCounter+1)
      self.board.restoreState(stateCpy)
    return [pos for value, pos in sorted(zip(values, cellPosList),reverse=True)]

  # <概要> 探索木のrootでのMoveOrdering関数
  #        // 深さ3の探索の評価値をもとにソートする
  #        通常のやつと同じ
  def __moveOrderingFirst(self, cellPosList, color, turnCounter):
    stateCpy = self.board.getState()  # 盤面コピー
    values = [0] * len(cellPosList)
    for i, pos in enumerate(cellPosList):
      self.board.put[pos](color)
      values[i] = self.__evaluateLeaf(color, turnCounter+1)
      #values[i] = -self.__alphaBeta(not color, 2, -1024, 1024, False, turnCounter+1)
      self.board.restoreState(stateCpy)
    return [pos for value, pos in sorted(zip(values, cellPosList),reverse=True)]

  """
  # <概要> http://uguisu.skr.jp/othello/5-1.html の位置重み付け + 確定石数差*8 + 置ける場所の数の差*4
  def __evaluateLeaf(self, color):
    res =  self.board.getEval(color)
    res += self.board.getSettled(color) << 3
    res += self.board.getMobility(color) << 1 # 着手可能候補数
    return res
  """

  # <概要> logistelloパターン+着手可能数差による評価
  def __evaluateLeaf(self, color, turnCounter):
    feature = self.board.getFeatures()
    stage = turnCounter / 4
    if color:
      return -(
        self.__weight[stage][0][feature[0]]+self.__weight[stage][0][feature[1]]+self.__weight[stage][0][feature[2]]+self.__weight[stage][0][feature[3]]+
        self.__weight[stage][1][feature[4]]+self.__weight[stage][1][feature[5]]+self.__weight[stage][1][feature[6]]+self.__weight[stage][1][feature[7]]+
        self.__weight[stage][2][feature[8]]+self.__weight[stage][2][feature[9]]+self.__weight[stage][2][feature[10]]+self.__weight[stage][2][feature[11]]+
        self.__weight[stage][3][feature[12]]+self.__weight[stage][3][feature[13]]+self.__weight[stage][3][feature[14]]+self.__weight[stage][3][feature[15]]+
        self.__weight[stage][4][feature[16]]+self.__weight[stage][4][feature[17]]+self.__weight[stage][4][feature[18]]+self.__weight[stage][4][feature[19]]+
        self.__weight[stage][5][feature[20]]+self.__weight[stage][5][feature[21]]+self.__weight[stage][5][feature[22]]+self.__weight[stage][5][feature[23]]+
        self.__weight[stage][6][feature[24]]+self.__weight[stage][6][feature[25]]+self.__weight[stage][6][feature[26]]+self.__weight[stage][6][feature[27]]+
        self.__weight[stage][7][feature[28]]+self.__weight[stage][7][feature[29]]+
        self.__weight[stage][8][feature[30]]+self.__weight[stage][8][feature[31]]+self.__weight[stage][8][feature[32]]+self.__weight[stage][8][feature[33]]+
        self.__weight[stage][9][feature[34]]+self.__weight[stage][9][feature[35]]+self.__weight[stage][9][feature[36]]+self.__weight[stage][9][feature[37]]+self.__weight[stage][9][feature[38]]+self.__weight[stage][9][feature[39]]+self.__weight[stage][9][feature[40]]+self.__weight[stage][9][feature[41]]+
        self.__weight[stage][10][feature[42]]+
        self.__weight[stage][10][feature[43]]+
        self.__weight[stage][10][feature[44]]+
        self.__weight[stage][10][feature[45]]+
        self.board.getMobility(0))
    else:
      return (
        self.__weight[stage][0][feature[0]]+self.__weight[stage][0][feature[1]]+self.__weight[stage][0][feature[2]]+self.__weight[stage][0][feature[3]]+
        self.__weight[stage][1][feature[4]]+self.__weight[stage][1][feature[5]]+self.__weight[stage][1][feature[6]]+self.__weight[stage][1][feature[7]]+
        self.__weight[stage][2][feature[8]]+self.__weight[stage][2][feature[9]]+self.__weight[stage][2][feature[10]]+self.__weight[stage][2][feature[11]]+
        self.__weight[stage][3][feature[12]]+self.__weight[stage][3][feature[13]]+self.__weight[stage][3][feature[14]]+self.__weight[stage][3][feature[15]]+
        self.__weight[stage][4][feature[16]]+self.__weight[stage][4][feature[17]]+self.__weight[stage][4][feature[18]]+self.__weight[stage][4][feature[19]]+
        self.__weight[stage][5][feature[20]]+self.__weight[stage][5][feature[21]]+self.__weight[stage][5][feature[22]]+self.__weight[stage][5][feature[23]]+
        self.__weight[stage][6][feature[24]]+self.__weight[stage][6][feature[25]]+self.__weight[stage][6][feature[26]]+self.__weight[stage][6][feature[27]]+
        self.__weight[stage][7][feature[28]]+self.__weight[stage][7][feature[29]]+
        self.__weight[stage][8][feature[30]]+self.__weight[stage][8][feature[31]]+self.__weight[stage][8][feature[32]]+self.__weight[stage][8][feature[33]]+
        self.__weight[stage][9][feature[34]]+self.__weight[stage][9][feature[35]]+self.__weight[stage][9][feature[36]]+self.__weight[stage][9][feature[37]]+self.__weight[stage][9][feature[38]]+self.__weight[stage][9][feature[39]]+self.__weight[stage][9][feature[40]]+self.__weight[stage][9][feature[41]]+
        self.__weight[stage][10][feature[42]]+
        self.__weight[stage][10][feature[43]]+
        self.__weight[stage][10][feature[44]]+
        self.__weight[stage][10][feature[45]]+
        self.board.getMobility(0))
  
  # <概要> 重みをロードする
  def __loadWeights(self):
    weight = [[[0 for i in range(MidGameBrain.PATTARNS[j])] for j in range(MidGameBrain.FEATURES)] for k in range(MidGameBrain.STAGES)]
    for stage in range(MidGameBrain.STAGES):
      f = open("./wei/w"+str(stage)+".txt", "r")
      for feature, line in enumerate(f):
        value = line.split(' ')
        for pattern in range(MidGameBrain.PATTARNS[feature]):
          weight[stage][feature][pattern] = float(value[pattern])
      f.close()
    return weight
