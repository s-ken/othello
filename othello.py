# -*- coding:utf-8 -*-

"""
  references:
    http://d.hatena.ne.jp/Megumi221/20081031/1225450482
"""

import pygame
from pygame.locals import *
import sys
import index

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
  PATTERNS_NUM      = 3 ** CELL_NUM
  HORI_OFFSET       = 0
  VERT_OFFSET       = CELL_NUM
  DIAG045_OFFSET    = VERT_OFFSET + CELL_NUM
  DIAG135_OFFSET    = DIAG045_OFFSET + CELL_NUM * 2 - 5
  MAX_SEARCH_HEIGHT  = 4
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
    self.__lines      = self.__initLines()
    self.__prevStates = None

  # <詳細> 範囲外への参照にはdummyCellを返す
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

  # <概要> 位置(x,y)にcolor色の駒を置いて得られる相手の駒数を返す
  # <引数> x:int(0~7), y:int(0~7), color:int(0~2)
  # <返値> int(0~6)
  def takes(self, x, y, color):
    return self.__takesHori(x, y, color) + self.__takesVert(x, y, color) + self.__takesDiag045(x, y, color) + self.__takesDiag135(x, y, color)
  
  # <概要> 位置(x,y)にcolor色の駒を置いて相手の駒を裏返す
  # <引数> x:int(0~7), y:int(0~7), color:int(0~2)
  def put(self, x, y, color):
    self.__flipDiag045(x, y, color) # 斜め45°方向を裏返す
    self.__flipDiag135(x, y, color) # 斜め135°方向を裏返す
    self.__flipHori(x, y, color)  # 水平方向を裏返す
    self.__flipVert(x, y, color)  # 垂直方向を裏返す
    self.at(x,y).state = color

  def placeable(self, x, y, color):
    if self.at(x, y).state == Cell.EMPTY and self.takes(x, y, color) > 0:
      return True
    else:
      return False
  def placeableCells(self, color):
    return [cell for cell in self.board if self.placeable(cell.x, cell.y, color) ]
  def storeStates(self):
    self.__prevStates = self.getStates()
  def loadStates(self):
    for cell, state in zip(self.board, self.__prevStates):
      cell.state = state
  def printResult(self):
    counter = [0, 0]
    for cell in self.board:
      if cell.state != Cell.EMPTY:
        counter[cell.state] += 1
    print "BLACK:", counter[Cell.BLACK], " WHITE:", counter[Cell.WHITE]
  def getStates(self):
    res = [None] * Config.CELL_NUM ** 2
    for i, cell in enumerate(self.board):
      res[i] = cell.state
    return res

  # <概要> メンバ変数__linesを初期化する
  def __initLines(self):
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

  # <概要> 位置(x,y)にcolor色の駒を置いたときに得られる水平方向の相手の駒の数を返す
  # <引数> x:int(0~7), y:int(0~7), color:int(0~2)
  # <返値> int(0~6)
  # <詳細> メンバ変数__linesを使用して処理を軽くしている.
  def __takesHori(self, x, y, color):
    return self.__index.takes(self.__lines[Config.HORI_OFFSET + y], x, color)
  def __takesVert(self, x, y, color):
    return self.__index.takes(self.__lines[Config.VERT_OFFSET + x], y, color)
  def __takesDiag045(self, x, y, color):
    sum = x + y
    if sum < 2 or sum > Config.CELL_NUM * 2 - 4:
      return 0
    return self.__index.takes(self.__lines[Config.DIAG045_OFFSET + sum - 2], y - max(0, sum - Config.CELL_NUM + 1), color)
  def __takesDiag135(self, x, y, color):
    dif = y - x
    if abs(dif) > Config.CELL_NUM - 3:
      return 0
    return self.__index.takes(self.__lines[Config.DIAG135_OFFSET + dif + Config.CELL_NUM - 3], y - max(0, dif), color)
  
  # <概要> 水平方向の相手の駒を裏返す
  # <引数> x:int(0~7), y:int(0~7), color:int(0~2)
  # <返値> int(0~6)
  # <詳細> メンバ変数__linesを使用して処理を軽くしている.
  #        __linesの要素のstateが書き換わる(=boardの中身が書き換わる)ので注意
  def __flipHori(self, x, y, color):
    self.__index.flip(self.__lines[Config.HORI_OFFSET + y], x, color)
  def __flipVert(self, x, y, color):
    self.__index.flip(self.__lines[Config.VERT_OFFSET + x], y, color)
  def __flipDiag045(self, x, y, color):
    sum = x + y
    if sum >= 2 and sum <= Config.CELL_NUM * 2 - 4:
      self.__index.flip(self.__lines[Config.DIAG045_OFFSET + sum - 2], y - max(0, sum - Config.CELL_NUM + 1), color)
  def __flipDiag135(self, x, y, color):
    dif = y - x
    if abs(dif) <= Config.CELL_NUM - 3:
      self.__index.flip(self.__lines[Config.DIAG135_OFFSET + dif + Config.CELL_NUM - 3], y - max(0, dif), color)


class Player(object):
  def __init__(self, board, color):
    self.board = board  # boardへの参照
    self.color = color  # 自分の色
  def takeTurn(self):
    raise NotImplementedError
  def canPut(self):
    return len(self.board.placeableCells(self.color)) > 0


class AI(Player):
  def __init__(self, board, color):
    super(AI, self).__init__(board, color)
    #self.__transpositionTable = None

  def __str__(self):
    return "AI"

  # <概要> 現盤面で打てる位置に対してそれぞれNegaMax関数を呼び出し,
  #        その値が最大となる位置を返す.
  def __evaluate(self):
    #self.__transpositionTable = {}  # 置換表を空に
    statesCpy = self.board.getStates()  # stateをコピー
    placeableCells = self.board.placeableCells(self.color)
    maxValue = -Config.INF
    placedCell = None
    for placeableCell in placeableCells:
      self.board.put(placeableCell.x, placeableCell.y, self.color)
      value = -self.__alphaBeta(not color, Config.MAX_SEARCH_HEIGHT, maxValue, Config.INF)
      if value > maxValue:
        maxValue = value
        placedCell = placeableCell
      for cell, state in zip(self.board.board, statesCpy):
        cell.state = state
    return [placedCell.x, placedCell.y]

  # <概要> http://uguisu.skr.jp/othello/alpha-beta.html
  # <引数> board:Board型, color:int(0~1), height:(1~MAX_SEARCH_HEIGHT), alpha:int, beta:int
  # <返値> int
  def __alphaBeta(self, color, height, alpha, beta):
    if not height: # 設定した深さまでたどり着いたら再帰終了
      return self.__evaluateLeaf(color)
    placeableCells = self.board.placeableCells(color)
    if not len(placeableCells):  # パス発生or試合終了でも再帰終了
      return self.__evaluateLeaf(color)
    statesCpy = self.board.getStates()
    #key = tuple(statesCpy)
    #if key in self.__transpositionTable:
    #  return self.__transpositionTable[key]
    for placeableCell in placeableCells:
      self.board.put(placeableCell.x, placeableCell.y, color)
      alpha = max(alpha, -self.__alphaBeta(not color, height - 1, -beta, -alpha))
      if alpha >= beta:
        return alpha  # カット
      for cell, state in zip(self.board.board, statesCpy):
        cell.state = state
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

  def takeTurn(self):
    x, y = self.__evaluate()
    self.board.put(x, y, self.color)  # 位置(xpos,ypos)に駒を置く
  

class You(Player):
  def __init__(self, board, color):
    super(You, self).__init__(board, color)
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
            return
          else:
            print "ERROR: You cannot put here."   # クリック地点が置けない場所ならループ継続


class UndoRequest(Exception):
  def __init__(self): 0


class Game:
  def __init__(self):
    pygame.init()
    self.__screen     = pygame.display.set_mode( (Config.WINDOW_WIDTH, Config.WINDOW_WIDTH) )
    self.__board      = Board(self.__screen)
    self.__turn       = Cell.BLACK
    self.__passedFlag = False
    self.__player     = [None] * 2
    self.__player[Config.AI_COLOR]      = AI(self.__board, Config.AI_COLOR)
    self.__player[not Config.AI_COLOR]  = You(self.__board, not Config.AI_COLOR)
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