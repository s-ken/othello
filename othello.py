# -*- coding:utf-8 -*-

"""
  references:
    http://d.hatena.ne.jp/Megumi221/20081031/1225450482
"""

import pygame
from pygame.locals import *
import sys
import index
import book

class Cell:
  BLACK = 0
  WHITE = 1
  EMPTY = 2
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.state = Cell.EMPTY
  def __mul__(self, other): # Index.__encode()用
    return self.state * other

    
class Config:
  CELL_WIDTH    = 100
  CELL_NUM      = 8
  WINDOW_WIDTH  = CELL_WIDTH * CELL_NUM
  WPOS          = CELL_WIDTH * (CELL_NUM - 1)
  AI_COLOR      = Cell.WHITE
  MAX_SEARCH_HEIGHT = 4 # ゲーム木の高さ
  INF = 1024
  WEIGHTS = (  30, -12,  0, -1, -1,  0, -12,  30,
              -12, -15, -3, -3, -3, -3, -15, -12,
                0,  -3,  0, -1, -1,  0,  -3,   0,
               -1,  -3, -1, -1, -1, -1,  -3,  -1,
               -1,  -3, -1, -1, -1, -1,  -3,  -1,
                0,  -3,  0, -1, -1,  0,  -3,   0,
              -12, -15, -3, -3, -3, -3, -15, -12,
               30, -12,  0, -1, -1,  0, -12,  30
            )
  MIDDLE_PHASE = 20
  LAST_PHASE = 40


# 特定のマスにかかる縦横斜めの4つのCell列と,そのそれぞれの列の内でのマスの位置を格納するクラス
# takes(),put()で使用される
class ReferenceContainer:
  def __init__(self, horiLine, horiPos, vertLine, vertPos, diag045Line, diag045Pos, diag135Line, diag135Pos):
    self.line = (horiLine, vertLine, diag045Line, diag135Line)
    self.pos  = (horiPos, vertPos, diag045Pos, diag135Pos)


class Board:
  def __init__(self, screen):
    self.board = [ Cell(i%Config.CELL_NUM,i/Config.CELL_NUM) for i in range(Config.CELL_NUM**2) ]
    self.at(3,3).state = Cell.WHITE
    self.at(3,4).state = Cell.BLACK
    self.at(4,3).state = Cell.BLACK
    self.at(4,4).state = Cell.WHITE
    self.empty_img  = pygame.image.load('empty.png').convert()
    self.black_img  = pygame.image.load('black.png').convert()
    self.white_img  = pygame.image.load('white.png').convert()
    self.empty_rect = self.empty_img.get_rect()
    self.black_rect = self.empty_img.get_rect()
    self.white_rect = self.empty_img.get_rect()
    self.screen     = screen
    self.__index      = index.Index()
    self.__dummyCell  = Cell(-1, -1)  # at()での範囲外のマスへの参照用
    self.__prevStates = None
    self.__referenceContainer = self.__initReferenceContainer() # サイズは64
    self.__emptyCells = [cell for cell in self.board] # 空マスのリスト. placeableCells()で使用する
    self.modifyEmptyCells(3, 3)
    self.modifyEmptyCells(3, 4)
    self.modifyEmptyCells(4, 3)
    self.modifyEmptyCells(4, 4)

  # <詳細> 範囲外への参照にはdummyCellを返す
  #        (範囲外への参照は__getDiagXXXLines()中で
  #        サイズが8未満の斜めのCell列を得るときに発生する)
  def at(self, x, y):
    if x < 0 or x >= Config.CELL_NUM or y < 0 or y >= Config.CELL_NUM:
      return self.__dummyCell
    return self.board[x+y*Config.CELL_NUM]

  def printBoard(self):
    for i, cell in enumerate(self.board):
      xy = (i%Config.CELL_NUM*Config.CELL_WIDTH ,i/Config.CELL_NUM*Config.CELL_WIDTH)
      if cell.state == Cell.EMPTY:
        self.screen.blit(self.empty_img, self.empty_rect.move(xy))
      if cell.state == Cell.BLACK:
        self.screen.blit(self.black_img, self.black_rect.move(xy))
      if cell.state == Cell.WHITE:
        self.screen.blit(self.white_img, self.white_rect.move(xy))
    pygame.display.flip()

  # <概要> 駒の数をプリントする 
  def printResult(self):
    counter = [0, 0]
    for cell in self.board:
      if cell.state != Cell.EMPTY:
        counter[cell.state] += 1
    print "BLACK:", counter[Cell.BLACK], " WHITE:", counter[Cell.WHITE]

  # <概要> 位置(x,y)にcolor色の駒を置いて得られる相手の駒数を返す
  # <引数> x:int(0~7), y:int(0~7), color:int(0~2)
  # <返値> int(0~6)
  def takes(self, x, y, color):
    container = self.__referenceContainer[x + y * Config.CELL_NUM]
    res = 0
    for i in range(4):
      if container.pos[i] >= 0:
        res += self.__index.takes(container.line[i], container.pos[i], color)
    return res
  
  # <概要> 位置(x,y)にcolor色の駒を置いて相手の駒を裏返す
  # <引数> x:int(0~7), y:int(0~7), color:int(0~2)
  def put(self, x, y, color):
    container = self.__referenceContainer[x + y * Config.CELL_NUM]
    for i in range(4):
      if container.pos[i] >= 0:
        self.__index.flip(container.line[i], container.pos[i], color)
    self.at(x,y).state = color

  def placeable(self, x, y, color):
    if self.at(x, y).state == Cell.EMPTY and self.takes(x, y, color) > 0:
      return True
    else:
      return False

  def placeableCells(self, color):
    return [cell for cell in self.__emptyCells if self.placeable(cell.x, cell.y, color) ]

  # ==================== Undo 関連 =====================
  def storeStates(self):
    self.__prevStates = self.getStates()

  def loadStates(self):
    restoreStates(self.__prevStates)

  # <概要> 現盤面のstateを返す
  #        AIのゲーム木探索での盤面保存にも使用している
  def getStates(self):
    res = [None] * Config.CELL_NUM ** 2
    for i, cell in enumerate(self.board):
      res[i] = cell.state
    return res

  # <概要> 盤面復元用の関数
  #        AIのゲーム木探索での盤面復元にも使用している
  def restoreStates(self, states):
    for cell, state in zip(self.board, states): # 盤面復元
        cell.state = state
  # ==================================================

  # <概要> 空マスリストの更新
  # <詳細> 本来ならこの処理をput()に入れてしまいたいところだが
  #        put()はゲーム木の探索過程で何度も呼び出されるため,ちょっとそれきつい感じ.
  #        ということでpublicな関数にしてPlayerのtakeTurn()内のput() <-実際の盤面に駒が置かれる
  #        のあとにこれを呼び出すことにした
  def modifyEmptyCells(self, x, y):
    self.__emptyCells.remove(self.at(x,y))

  # ======================================== ReferenceContainer 初期化関連 ========================================
  def __initReferenceContainer(self):
    HORI_OFFSET       = 0
    VERT_OFFSET       = Config.CELL_NUM
    DIAG045_OFFSET    = VERT_OFFSET + Config.CELL_NUM
    DIAG135_OFFSET    = DIAG045_OFFSET + Config.CELL_NUM * 2 - 5
    lines = self.__getLines()
    res = [None] * Config.CELL_NUM ** 2
    for i in range(Config.CELL_NUM ** 2):
      x = i % Config.CELL_NUM
      y = i / Config.CELL_NUM
      horiLine = lines[HORI_OFFSET + y]
      horiPos  = x
      vertLine = lines[VERT_OFFSET + x]
      vertPos  = y
      diag045Line = None
      diag045Pos  = -1
      if 2 <= x + y <= Config.CELL_NUM * 2 - 4: # サイズが3以上(flipが発生する)
        diag045Line = lines[DIAG045_OFFSET + x + y - 2]
        diag045Pos  = y - max(0, x + y - Config.CELL_NUM + 1)
      diag135Line = None
      diag135Pos  = -1
      if abs(y - x) <= Config.CELL_NUM - 3: # サイズが3以上(flipが発生する)
        diag135Line = lines[DIAG135_OFFSET + y - x + Config.CELL_NUM - 3]
        diag135Pos  = y - max(0, y - x)
      res[i] = ReferenceContainer(horiLine, horiPos, vertLine, vertPos, diag045Line, diag045Pos, diag135Line, diag135Pos)
    return res

  def __getLines(self):
    return self.__getHoriLines() + self.__getVertLines() + self.__getDiag045Lines() + self.__getDiag135Lines()
  
  # <概要> 水平方向のCell型ListからなるListを返す
  # <返値> (Cell型List[8])型List[8]
  def __getHoriLines(self):
    res = [[] for i in range(Config.CELL_NUM)]
    for y in range(Config.CELL_NUM):
      res[y] = self.board[y*Config.CELL_NUM:(y+1)*Config.CELL_NUM]
    return res

  # <概要> 垂直方向のCell型ListからなるListを返す
  # <返値> (Cell型List[8])型List[8]
  def __getVertLines(self):
    res = [[] for i in range(Config.CELL_NUM)]
    for x in range(Config.CELL_NUM):
      res[x] = self.board[x :: Config.CELL_NUM]
    return res

  # <概要> 斜め45°方向のCell型ListからなるListを返す
  # <返値> (Cell型List)型List[11]
  # <詳細> 返値の各要素のCell型Listの長さは,順に
  #        3,4,5,6,7,8,7,6,5,4,3 である
  #        長さ1,2のものは駒が裏返ることがないので省く
  def __getDiag045Lines(self):
    res = [[] for i in range(Config.CELL_NUM * 2 - 5)]
    for i in range(Config.CELL_NUM * 2 - 5):
      x = min(Config.CELL_NUM - 1, i + 2)
      y = max(0, i + 3 - Config.CELL_NUM)
      for j in range(Config.CELL_NUM):
        res[i].append(self.at(x, y))
        x -= 1
        y += 1
    return res

  # <概要> 斜め135°方向のCell型ListからなるListを返す
  # <返値> (Cell型List)型List[11]
  def __getDiag135Lines(self):
    res = [[] for i in range(Config.CELL_NUM * 2 - 5)]
    for i in range(Config.CELL_NUM * 2 - 5):
      x = max(0, Config.CELL_NUM - 1 - (i + 2))
      y = max(0, i + 3 - Config.CELL_NUM)
      for j in range(Config.CELL_NUM):
        res[i].append(self.at(x, y))
        x += 1
        y += 1
    return res
  # ==========================================================================================================


class Player(object):
  def __init__(self, board, color, openingBook):
    self.board = board  # boardへの参照
    self.color = color  # 自分の色
    self.openingBook = openingBook
  def takeTurn(self):
    raise NotImplementedError
  def canPut(self):
    return len(self.board.placeableCells(self.color)) > 0


class AI(Player):
  def __init__(self, board, color, openingBook):
    super(AI, self).__init__(board, color, openingBook)
    #self.__transpositionTable = None
    self.__turnCounter = color

  def __str__(self):
    return "AI"

  # <概要> 現盤面で打てる位置に対してそれぞれ評価関数を呼び出し,
  #        その値が最大となる位置を返す.
  def __evaluate(self):
    #self.__transpositionTable = {}  # 置換表を空に
    placeableCells = self.board.placeableCells(self.color)
    maxValue = -Config.INF
    for placeableCell in placeableCells:
      value = self.__evalateCell(placeableCell) # cellを評価
      if value > maxValue:
        maxValue = value
        res = placeableCell
    return (res.x, res.y)

  # <概要> 与えられたcellに駒を置いた場合の評価値を返す
  #        序盤中盤終盤ごとに評価関数を割当てている
  def __evalateCell(self, cell):
    statesCpy = self.board.getStates()  # 盤面コピー
    if self.__turnCounter < Config.MIDDLE_PHASE: # 序盤
      self.board.put(cell.x, cell.y, self.color)
      res = -self.__alphaBeta(not self.color, Config.MAX_SEARCH_HEIGHT, -Config.INF, Config.INF)
    elif Config.MIDDLE_PHASE <= self.__turnCounter < Config.LAST_PHASE:  # 中盤
      self.board.put(cell.x, cell.y, self.color)
      res = -self.__alphaBeta(not self.color, Config.MAX_SEARCH_HEIGHT, -Config.INF, Config.INF)
    else: # 終盤
      self.board.put(cell.x, cell.y, self.color)
      res = -self.__alphaBeta(not self.color, Config.MAX_SEARCH_HEIGHT, -Config.INF, Config.INF)
    self.board.restoreStates(statesCpy)
    return res

  # <概要> http://uguisu.skr.jp/othello/alpha-beta.html
  # <引数> board:Board型, color:int(0~1), height:(1~MAX_SEARCH_HEIGHT), alpha:int, beta:int
  # <返値> int
  def __alphaBeta(self, color, height, alpha, beta):
    if not height: # 設定した深さまでたどり着いたら再帰終了
      return self.__evaluateLeaf(color)
    placeableCells = self.board.placeableCells(color)
    if not len(placeableCells):  # パス発生or試合終了でも再帰終了
      return self.__evaluateLeaf(color)
    placeableCells = self.__moveOrdering(placeableCells)
    statesCpy = self.board.getStates()
    #key = tuple(statesCpy)
    #if key in self.__transpositionTable:
    #  return self.__transpositionTable[key]
    for placeableCell in placeableCells:
      self.board.put(placeableCell.x, placeableCell.y, color)
      alpha = max(alpha, -self.__alphaBeta(not color, height - 1, -beta, -alpha))
      if alpha >= beta:
        return alpha  # カット
      self.board.restoreStates(statesCpy)
    #self.__transpositionTable[key] = alpha
    return alpha

  # <概要> てきとーに http://uguisu.skr.jp/othello/5-1.html の重み付け
  def __evaluateLeaf(self, color):
    res = 0
    for cell, weight in zip(self.board.board, Config.WEIGHTS):
      if cell.state == color:
        res += weight
      elif cell.state == (not color):
        res -= weight
    return res

  # <概要> 与えられた次手候補cellリストを評価値の見込みが高い順にソートする
  #        これによってゲーム木探索中の枝刈り回数を増加させる
  def __moveOrdering(self, cells):  # TODO
    return cells

  def takeTurn(self):
    if self.openingBook.isValid():  # 現状定石通りのゲーム進行なら...
      x, y = self.openingBook.readBook()
    else:
      x, y = self.__evaluate()
    self.board.put(x, y, self.color)  # 位置(xpos,ypos)に駒を置く
    self.board.modifyEmptyCells(x, y)
    self.__turnCounter += 2
  

class You(Player):
  def __init__(self, board, color, openingBook):
    super(You, self).__init__(board, color, openingBook)
  def __str__(self):
    return "You"
  def takeTurn(self):
    while 1:
      for event in pygame.event.get():
        if (event.type == KEYDOWN and event.key == K_ESCAPE):
          sys.exit()  # ESCAPEキーが押されたら終了
        if (event.type == KEYDOWN and event.key == K_BACKSPACE):
          raise UndoRequest() # BACKSPACEキーが押されたらUndo
        if (event.type == MOUSEBUTTONDOWN):
          xpos = int(pygame.mouse.get_pos()[0]/Config.CELL_WIDTH)
          ypos = int(pygame.mouse.get_pos()[1]/Config.CELL_WIDTH)
          if self.board.placeable(xpos, ypos, self.color):
            self.board.storeStates()   # boardの要素のstateを書き換える前に,各stateを保存する
            self.board.put(xpos, ypos, self.color)  # 位置(xpos,ypos)に駒を置く
            self.board.modifyEmptyCells(xpos, ypos)
            if self.openingBook.isValid():
              self.openingBook.proceed(xpos, ypos)  # 定石通りかどうかチェック
            return
          else:
            print "ERROR: You cannot put here."   # クリック地点が置けない場所ならループ継続


class UndoRequest(Exception):
  def __init__(self): 0


class TranspositionTable:
  def __init__(self):
    self.__table = [[0, 0] for i in range(Config.TABLE_SIZE)]  # 窓幅を格納(min, max)

  @classmethod
  def __hash(self, board):
    res = 0
    for i, cell in enumerate(board.board):
      res += (cell.state * 3 ** (i % Config.CELL_NUM)) * 17 ** (i / Config.CELL_NUM)
      res %= Config.TABLE_SIZE
    return res


class Game:
  def __init__(self):
    pygame.init()
    self.__screen     = pygame.display.set_mode( (Config.WINDOW_WIDTH, Config.WINDOW_WIDTH) )
    self.__board      = Board(self.__screen)
    self.__turn       = Cell.BLACK
    self.__passedFlag = False
    self.__openingBook = book.OpeningBook()
    self.__player     = [None] * 2
    self.__player[Config.AI_COLOR]      = AI(self.__board, Config.AI_COLOR, self.__openingBook)
    self.__player[not Config.AI_COLOR]  = You(self.__board, not Config.AI_COLOR, self.__openingBook)
    self.__screen.fill((0,0,0))
    pygame.display.set_caption('Othello')
    pygame.mouse.set_visible(True)
  def run(self):
    while 1:
      self.__printBoard()
      if self.__player[self.__turn%2].canPut():  # 置ける場所があればTrue
        try:
          self.__player[self.__turn%2].takeTurn() # 俺のターン
          self.__passedFlag = False
        except UndoRequest:
          self.__undo()
          continue
      else:     
        print self.__player[self.__turn%2], " passed."
        if self.__passedFlag:  # 二人ともパス->終了
          return
        self.__passedFlag = True
      self.__turn += 1
  def output(self):
    self.__board.printResult()
  def __printBoard(self):
    self.__board.printBoard()
    pygame.display.flip()
  def __undo(self):
    self.__board.loadStates()


def main():
  game = Game()
  game.run()
  game.output()

if __name__ == "__main__":
  main()