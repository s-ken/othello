# -*- coding:utf-8 -*-

import pygame
import othello
import index

class Board:
  def __init__(self):
    pygame.init()
    self.__screen     = pygame.display.set_mode( (othello.Config.WINDOW_WIDTH, othello.Config.WINDOW_WIDTH) )
    self.empty_img    = pygame.image.load('empty.png').convert()
    self.black_img    = pygame.image.load('black.png').convert()
    self.white_img    = pygame.image.load('white.png').convert()
    self.empty_rect   = self.empty_img.get_rect()
    self.black_rect   = self.empty_img.get_rect()
    self.white_rect   = self.empty_img.get_rect()
    self.__screen.fill((0,0,0))
    pygame.display.set_caption('Othello')
    pygame.mouse.set_visible(True)
    self.board 	      = [6560] * 64
    self.__emptyCells = range(othello.Config.CELL_NUM ** 2) # 空マスのインデックスリスト. placeableCells()で使用する
    self.__index      = index.Index()
    self.__referenceContainer = self.__initReferenceContainer() # サイズは64
    self.put(3 + (3 << 3), othello.Config.WHITE)
    self.modifyEmptyCells(3 + (3 << 3))
    self.put(3 + (4 << 3), othello.Config.BLACK)
    self.modifyEmptyCells(3 + (4 << 3))
    self.put(4 + (3 << 3), othello.Config.BLACK)
    self.modifyEmptyCells(4 + (3 << 3))
    self.put(4 + (4 << 3), othello.Config.WHITE)
    self.modifyEmptyCells(4 + (4 << 3))
    self.__prevStates = None

  def at(self, x, y):
    return (self.board[y] % (3 ** (x + 1))) / (3 ** x)

  def printBoard(self): # TODO
    for x in range(othello.Config.CELL_NUM):
      for y in range(othello.Config.CELL_NUM):
        xy = (x*othello.Config.CELL_WIDTH, y*othello.Config.CELL_WIDTH)
        state = self.at(x, y)
        if state == othello.Config.EMPTY:
          self.__screen.blit(self.empty_img, self.empty_rect.move(xy))
        if state == othello.Config.BLACK:
          self.__screen.blit(self.black_img, self.black_rect.move(xy))
        if state == othello.Config.WHITE:
          self.__screen.blit(self.white_img, self.white_rect.move(xy))
    pygame.display.flip()

  # <概要> 駒の数をプリントする
  def printResult(self):
    counter = [0, 0]
    for x in range(othello.Config.CELL_NUM):
      for y in range(othello.Config.CELL_NUM):
        state = self.at(x, y)
        if state != othello.Config.EMPTY:
          counter[state] += 1
    print "BLACK:", counter[othello.Config.BLACK], " WHITE:", counter[othello.Config.WHITE]

  # <概要> 位置(x,y)にcolor色の駒を置いて得られる相手の駒数を返す
  # <引数> pos:int(0~63), color:int(0~2)
  # <返値> int(0~6)
  def takes(self, pos, color):
    container = self.__referenceContainer[pos]
    res = ( self.__index.takes(self.board[container[0][0]], container[0][1], color)
          + self.__index.takes(self.board[container[1][0]], container[1][1], color) )
    if container[2][0] >= 0:
      res += self.__index.takes(self.board[container[2][0]], container[2][1], color)
    if container[3][0] >= 0:
      res += self.__index.takes(self.board[container[3][0]], container[3][1], color)
    return res

  # <概要> 位置(x,y)にcolor色の駒を置いて相手の駒を裏返す
  # <引数> pos:int(0~63), color:int(0~2)
  def put(self, pos, color):
    container = self.__referenceContainer[pos]
    # 水平方向flip
    self.board[container[0][0]], fliped = self.__index.flipLine(self.board[container[0][0]], container[0][1], color) # 水平方向
    for cont in self.__referenceContainer[pos+fliped[0] : pos] + self.__referenceContainer[pos+1 : pos+fliped[1]+1]:
      self.board[cont[1][0]] = self.__index.flipCell(self.board[cont[1][0]], cont[1][1])  # 垂直方向
      if cont[2][0] >= 0:
        self.board[cont[2][0]] = self.__index.flipCell(self.board[cont[2][0]], cont[2][1])  # 斜め045方向
      if cont[3][0] >= 0:
        self.board[cont[3][0]] = self.__index.flipCell(self.board[cont[3][0]], cont[3][1])  # 斜め135方向
    # 垂直方向flip
    self.board[container[1][0]], fliped = self.__index.flipLine(self.board[container[1][0]], container[1][1], color) # 垂直方向
    for cont in self.__referenceContainer[pos+(fliped[0]<<3) : pos : 8] + self.__referenceContainer[pos+8 : pos+(fliped[1]<<3)+1 : 8]:
      self.board[cont[0][0]] = self.__index.flipCell(self.board[cont[0][0]], cont[0][1])  # 水平方向
      if cont[2][0] >= 0:
        self.board[cont[2][0]] = self.__index.flipCell(self.board[cont[2][0]], cont[2][1]) # 斜め045方向
      if cont[3][0] >= 0:
        self.board[cont[3][0]] = self.__index.flipCell(self.board[cont[3][0]], cont[3][1]) # 斜め135方向
    # 斜め045方向flip
    if container[2][0] >= 0:
      self.board[container[2][0]], fliped = self.__index.flipLine(self.board[container[2][0]], container[2][1], color) # 斜め045方向
      for idx in [pos-x+(x<<3) for x in range(fliped[0],1)[:-1]] + [pos-x+(x<<3) for x in range(fliped[1]+1)[1:]]:
        cont = self.__referenceContainer[idx]
        self.board[cont[0][0]] = self.__index.flipCell(self.board[cont[0][0]], cont[0][1])  # 水平方向
        self.board[cont[1][0]] = self.__index.flipCell(self.board[cont[1][0]], cont[1][1])  # 垂直方向
        if cont[3][0] >= 0:
          self.board[cont[3][0]] = self.__index.flipCell(self.board[cont[3][0]], cont[3][1]) # 斜め135方向
    # 斜め135方向flip
    if container[3][0] >= 0:
      self.board[container[3][0]], fliped = self.__index.flipLine(self.board[container[3][0]], container[3][1], color) # 斜め045方向
      for idx in [pos+x+(x<<3) for x in range(fliped[0],1)[:-1]] + [pos+x+(x<<3) for x in range(fliped[1]+1)[1:]]:
        cont = self.__referenceContainer[idx]
        self.board[cont[0][0]] = self.__index.flipCell(self.board[cont[0][0]], cont[0][1])  # 水平方向
        self.board[cont[1][0]] = self.__index.flipCell(self.board[cont[1][0]], cont[1][1])  # 垂直方向
        if cont[2][0] >= 0:
          self.board[cont[2][0]] = self.__index.flipCell(self.board[cont[2][0]], cont[2][1]) # 斜め045方向

  def placeable(self, pos, color):
    container = self.__referenceContainer[pos]
    if self.__index.takes(self.board[container[0][0]], container[0][1], color):
      return True
    if self.__index.takes(self.board[container[1][0]], container[1][1], color):
      return True
    if container[2][0] >= 0:
      if self.__index.takes(self.board[container[2][0]], container[2][1], color):
        return True
    if container[3][0] >= 0:
      if self.__index.takes(self.board[container[3][0]], container[3][1], color):
        return True
    return False

  def placeableCells(self, color):
    return [cellPos for cellPos in self.__emptyCells if self.placeable(cellPos, color) ]

  # ==================== Undo 関連 =====================
  def storeStates(self):
    self.__prevStates = list(self.board)

  def loadStates(self):
    self.board = self.__prevStates
  # ==================================================

  # <概要> 空マスリストの更新
  # <詳細> 本来ならこの処理をput()に入れてしまいたいところだが
  #        put()はゲーム木の探索過程で何度も呼び出されるため,ちょっとそれきつい感じ.
  #        ということでpublicな関数にしてPlayerのtakeTurn()内のput() <-実際の盤面に駒が置かれる
  #        のあとにこれを呼び出すことにした
  def modifyEmptyCells(self, pos):
    self.__emptyCells.remove(pos)

  # ======================================== ReferenceContainer 初期化関連 ========================================
  def __initReferenceContainer(self):
    HORI_OFFSET       = 0
    VERT_OFFSET       = othello.Config.CELL_NUM
    DIAG045_OFFSET    = VERT_OFFSET + othello.Config.CELL_NUM
    DIAG135_OFFSET    = DIAG045_OFFSET + othello.Config.CELL_NUM * 2 - 5
    res = [None] * othello.Config.CELL_NUM ** 2
    for i in range(othello.Config.CELL_NUM ** 2):
      x = i % othello.Config.CELL_NUM
      y = i / othello.Config.CELL_NUM
      horiLineIndex = HORI_OFFSET + y
      horiPos       = x
      vertLineIndex = VERT_OFFSET + x
      vertPos       = y
      diag045LineIndex = -1
      diag045Pos       = -1
      if 2 <= x + y <= othello.Config.CELL_NUM * 2 - 4: # サイズが3以上(flipが発生する)
        diag045LineIndex = DIAG045_OFFSET + x + y - 2
        diag045Pos       = y - max(0, x + y - othello.Config.CELL_NUM + 1)
      diag135LineIndex = -1
      diag135Pos       = -1
      if abs(y - x) <= othello.Config.CELL_NUM - 3: # サイズが3以上(flipが発生する)
        diag135LineIndex = DIAG135_OFFSET + y - x + othello.Config.CELL_NUM - 3
        diag135Pos       = y - max(0, y - x)
      res[i] = ((horiLineIndex, horiPos), (vertLineIndex, vertPos), (diag045LineIndex, diag045Pos), (diag135LineIndex, diag135Pos))
    return res
  # ==========================================================================================================
