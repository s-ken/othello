# -*- coding:utf-8 -*-

import othello
#import transPositionTable # 使うとむしろ遅くなる

class AI():
  def __init__(self, board, color, openingBook):
    self.board = board  # boardへの参照
    self.color = color  # 自分の色
    self.openingBook = openingBook
    self.__brain = BookBrain(board, color, openingBook)
    self.__middleBrain  = AlphaBetaBrain(board, color, othello.Config.MAX_SEARCH_HEIGHT, midGameEval, midGameMV)
    self.__endBrain     = AlphaBetaBrain(board, color, othello.Config.INF, endGameEval, endGameMV)
    self.__turnCounter  = color

  def canPut(self):
    return len(self.board.placeableCells(self.color)) > 0

  def __str__(self):
    return "AI"

  def takeTurn(self):
    if not self.__brain.isValid() or self.__turnCounter >= othello.Config.LAST_PHASE:
      self.__changeBrain()
      print "change"
    pos = self.__brain.evaluate()
    self.board.put[pos](self.color)  # 位置(x,y)に駒を置く
    self.board.modifyEmptyCells(pos) # 空マスリストの更新
    self.__turnCounter += 2

  def __changeBrain(self):
    if self.__brain is self.__middleBrain:
      self.__brain = self.__endBrain
    else:
      self.__brain = self.__middleBrain


class Brain(object):
  def __init__(self, board, color):
    self.board = board  # boardへの参照
    self.color = color  # 自分の色
  def evaluate(self): 0
  def isValid(self):  0

class BookBrain(Brain):
  def __init__(self, board, color, openingBook):
    super(BookBrain, self).__init__(board, color)
    self.__openingBook = openingBook

  # <概要> OpeningBookを参照して次の手を返す
  def evaluate(self):
    x, y = self.__openingBook.readBook()
    return x + y * 8

  def isValid(self):
    return self.__openingBook.isValid()

# ========================= AlphaBeta法に基づく探索 ========================
# ゲーム木の葉での盤面評価関数evaluateLeaf()
# 探索過程でのノードの探索順序のソート関数moveOrdering() をコンストラクタ引数で与える
class AlphaBetaBrain(Brain):
  def __init__(self, board, color, searchHeight, evaluateLeaf, moveOrdering):
    super(AlphaBetaBrain, self).__init__(board, color)
    self.__valid = True
    self.cutCounter = 0
    #self.__transpositionTable = None
    self.__searchHeight = searchHeight  # 探索木の高さ
    self.__evaluateLeaf = evaluateLeaf  # 関数ポインタ
    self.__moveOrdering = moveOrdering  # 関数ポインタ

  # <概要> 現盤面で打てる位置に対してそれぞれ評価関数を呼び出し,
  #        その値が最大となる位置を返す.
  def evaluate(self):
    self.cutCounter = 0
    #self.__transpositionTable = transPositionTable.TranspositionTable()
    placeableCells = self.board.placeableCells(self.color)
    maxValue = -othello.Config.INF
    for placeableCell in placeableCells:
      value = self.__evalateCell(placeableCell) # cellを評価
      if value > maxValue:
        maxValue = value
        res = placeableCell
    print "cut:",self.cutCounter
   # print "col:",self.__transpositionTable.collision
    return res

  def isValid(self):  # TODO
    return self.__valid

  # <概要> 与えられたcellに駒を置いた場合の評価値を返す
  def __evalateCell(self, cellPos):
    stateCpy = self.board.getState()  # 盤面コピー
    self.board.put[cellPos](self.color)
    res = -self.__alphaBeta(not self.color, self.__searchHeight-1, -othello.Config.INF, othello.Config.INF, False)
    self.board.restoreState(stateCpy)
    return res

  # <概要> http://uguisu.skr.jp/othello/alpha-beta.html
  # <引数> board:Board型, color:int(0~1), height:(1~MAX_SEARCH_HEIGHT), alpha:int, beta:int
  # <返値> int
  def __alphaBeta(self, color, height, alpha, beta, passed):
    if not height: # 設定した深さまでたどり着いたら再帰終了
      return self.__evaluateLeaf(self.board, color)
    placeableCells = self.board.placeableCells(color)
    if not len(placeableCells):
      if passed:
        return self.__evaluateLeaf(self.board, color) # ゲーム終了
      return -self.__alphaBeta(not color, height, -beta, -alpha, True)  # パス
    if not len(placeableCells):  # パス発生or試合終了でも再帰終了
      return self.__evaluateLeaf(self.board, color)
    #placeableCells = self.__moveOrdering(self.board, placeableCells, color)
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
        self.cutCounter += 1
        return value  # カット
      if value > maxValue:
        a = max(a, value)
        maxValue = value
    return maxValue

# <概要> 与えられた次手候補cellリストを評価値の見込みが高い順にソートする
#        これによってゲーム木探索中の枝刈り回数を増加させる
def midGameMV(board, cellPosList, color):
  return cellPosList

# <概要> 相手の置ける場所が少なくなる順にソート
def endGameMV(board, cellPosList ,color):
  stateCpy = self.board.getState()  # 盤面コピー
  values = [0] * len(cellPosList)
  for i, pos in enumerate(cellPosList):
    self.board.put[pos](color)
    values[i] = board.getMobility(not color)
    self.board.restoreState(stateCpy)
  return [pos for value, pos in sorted(zip(values, cellPosList))]


 # <概要> てきとーに http://uguisu.skr.jp/othello/5-1.html の重み付け + 置ける場所の数の差*4
def midGameEval(board, color):
  res =  board.getEval(color)
  res += board.getSettled(color) << 3
  res += board.getMobility(color) << 2 # 着手可能候補数
  return res

# <概要> 石差で評価
def endGameEval(board, color):
  return board.getDifference(color)