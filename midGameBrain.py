# -*- coding:utf-8 -*-

import othello
import transPositionTable

# 中盤
# 探索:AlphaBeta, 盤面評価:位置+着手可能手数+確定石数, MoveOrdering:1手先の盤面評価値

class MidGameBrain():
  STAGES   = 60/4
  FEATURES = 11
  PATTARNS = [3**8]*3 + [3**4, 3**5, 3**6, 3**7, 3**8] + [3**10]*2 + [3**9]  

  def __init__(self, board, color, weight):
    self.board = board  # boardへの参照
    self.color = color  # 自分の色
    #self.__transpositionTable = None
    if weight is None:
      self.__weight = self.__loadWeights()
    else:
      self.__weight = weight  # Logistello重み
    self.__stage = None    # 盤面評価関数で使用する重みのステージ

  # <概要> 現盤面で打てる位置に対してそれぞれ評価関数を呼び出し,
  #        その値が最大となる位置を返す.
  def evaluate(self, turnCounter):
    # 探索関数にturnCounterを渡してincするのはだるいので,
    # turnCounter+探索木の高さ から盤面評価関数が呼び出された時点での盤面でのstageを計算してしまう。
    # 途中パスでゲーム終了してしまうような場合には誤った値となるが、まぁそれはいいとする。
    self.__stage = (turnCounter + othello.Config.MID_HEIGHT) / 4
    #self.__transpositionTable = transPositionTable.TranspositionTable()
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
    return res

  def isValid(self, turnCounter):
    return turnCounter < othello.Config.LAST_PHASE

  def setWeight(self, weight):
    self.__weight = weight

  def __negaScout(self, color, height, alpha, beta, passed):
    placeableCells = self.board.placeableCells(color)
    if not len(placeableCells):
      if passed:
        return self.__evaluateLeaf(color) # 連続パスでゲーム終了 TODO
      return -self.__negaScout(not color, height, -beta, -alpha, True)  # パス
    stateCpy = self.board.getState()
    if height >= 3:
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
        return self.__evaluateLeaf(color) # 連続パスでゲーム終了 TODO
      return -self.__alphaBeta(not color, height, -beta, -alpha, True)  # パス
    if height >= 3:
      placeableCells = self.__moveOrdering(placeableCells, color)
    stateCpy = self.board.getState()  # 盤面コピー
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

  """
  # <概要> http://uguisu.skr.jp/othello/5-1.html の位置重み付け + 確定石数差*8 + 置ける場所の数の差*4
  def __evaluateLeaf(self, color):
    res =  self.board.getEval(color)
    res += self.board.getSettled(color) << 3
    res += self.board.getMobility(color) << 1 # 着手可能候補数
    return res
  """

  # <概要> logistelloパターン+着手可能数差による評価
  def __evaluateLeaf(self, color):
    feature = self.board.getFeatures()
    if color:
      return -(
        self.__weight[self.__stage][0][feature[0]]+self.__weight[self.__stage][0][feature[1]]+self.__weight[self.__stage][0][feature[2]]+self.__weight[self.__stage][0][feature[3]]+
        self.__weight[self.__stage][1][feature[4]]+self.__weight[self.__stage][1][feature[5]]+self.__weight[self.__stage][1][feature[6]]+self.__weight[self.__stage][1][feature[7]]+
        self.__weight[self.__stage][2][feature[8]]+self.__weight[self.__stage][2][feature[9]]+self.__weight[self.__stage][2][feature[10]]+self.__weight[self.__stage][2][feature[11]]+
        self.__weight[self.__stage][3][feature[12]]+self.__weight[self.__stage][3][feature[13]]+self.__weight[self.__stage][3][feature[14]]+self.__weight[self.__stage][3][feature[15]]+
        self.__weight[self.__stage][4][feature[16]]+self.__weight[self.__stage][4][feature[17]]+self.__weight[self.__stage][4][feature[18]]+self.__weight[self.__stage][4][feature[19]]+
        self.__weight[self.__stage][5][feature[20]]+self.__weight[self.__stage][5][feature[21]]+self.__weight[self.__stage][5][feature[22]]+self.__weight[self.__stage][5][feature[23]]+
        self.__weight[self.__stage][6][feature[24]]+self.__weight[self.__stage][6][feature[25]]+self.__weight[self.__stage][6][feature[26]]+self.__weight[self.__stage][6][feature[27]]+
        self.__weight[self.__stage][7][feature[28]]+self.__weight[self.__stage][7][feature[29]]+
        self.__weight[self.__stage][8][feature[30]]+self.__weight[self.__stage][8][feature[31]]+self.__weight[self.__stage][8][feature[32]]+self.__weight[self.__stage][8][feature[33]]+
        self.__weight[self.__stage][9][feature[34]]+self.__weight[self.__stage][9][feature[35]]+self.__weight[self.__stage][9][feature[36]]+self.__weight[self.__stage][9][feature[37]]+self.__weight[self.__stage][9][feature[38]]+self.__weight[self.__stage][9][feature[39]]+self.__weight[self.__stage][9][feature[40]]+self.__weight[self.__stage][9][feature[41]]+
        self.__weight[self.__stage][10][feature[42]]+
        self.__weight[self.__stage][10][feature[43]]+
        self.__weight[self.__stage][10][feature[44]]+
        self.__weight[self.__stage][10][feature[45]]+
        self.board.getMobility(0))
    else:
      return (
        self.__weight[self.__stage][0][feature[0]]+self.__weight[self.__stage][0][feature[1]]+self.__weight[self.__stage][0][feature[2]]+self.__weight[self.__stage][0][feature[3]]+
        self.__weight[self.__stage][1][feature[4]]+self.__weight[self.__stage][1][feature[5]]+self.__weight[self.__stage][1][feature[6]]+self.__weight[self.__stage][1][feature[7]]+
        self.__weight[self.__stage][2][feature[8]]+self.__weight[self.__stage][2][feature[9]]+self.__weight[self.__stage][2][feature[10]]+self.__weight[self.__stage][2][feature[11]]+
        self.__weight[self.__stage][3][feature[12]]+self.__weight[self.__stage][3][feature[13]]+self.__weight[self.__stage][3][feature[14]]+self.__weight[self.__stage][3][feature[15]]+
        self.__weight[self.__stage][4][feature[16]]+self.__weight[self.__stage][4][feature[17]]+self.__weight[self.__stage][4][feature[18]]+self.__weight[self.__stage][4][feature[19]]+
        self.__weight[self.__stage][5][feature[20]]+self.__weight[self.__stage][5][feature[21]]+self.__weight[self.__stage][5][feature[22]]+self.__weight[self.__stage][5][feature[23]]+
        self.__weight[self.__stage][6][feature[24]]+self.__weight[self.__stage][6][feature[25]]+self.__weight[self.__stage][6][feature[26]]+self.__weight[self.__stage][6][feature[27]]+
        self.__weight[self.__stage][7][feature[28]]+self.__weight[self.__stage][7][feature[29]]+
        self.__weight[self.__stage][8][feature[30]]+self.__weight[self.__stage][8][feature[31]]+self.__weight[self.__stage][8][feature[32]]+self.__weight[self.__stage][8][feature[33]]+
        self.__weight[self.__stage][9][feature[34]]+self.__weight[self.__stage][9][feature[35]]+self.__weight[self.__stage][9][feature[36]]+self.__weight[self.__stage][9][feature[37]]+self.__weight[self.__stage][9][feature[38]]+self.__weight[self.__stage][9][feature[39]]+self.__weight[self.__stage][9][feature[40]]+self.__weight[self.__stage][9][feature[41]]+
        self.__weight[self.__stage][10][feature[42]]+
        self.__weight[self.__stage][10][feature[43]]+
        self.__weight[self.__stage][10][feature[44]]+
        self.__weight[self.__stage][10][feature[45]]+
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
