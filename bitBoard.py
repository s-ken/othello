# -*- coding:utf-8 -*-
# BitBoard :
# 2つの64bitの整数値で表現されたボード.
# 盤面の処理をbit演算で実装できるため高速.
# 詳しくは,
# http://starlancer.org/~is2004/owiki/wiki.cgi?action=ATTACH&file=othello%2E12%2E1%2E2%2Eppt&page=%A4%CA%A4%F3%A4%C7%A4%E2%A5%BB%A5%DF%A5%CA%A1%BC
# とか,Wikipediaとか.
import pygame
import othello

class BitBoard:
  def __init__(self, visible):
    if visible:
      pygame.init()
      self.__screen     = pygame.display.set_mode( (othello.Config.WINDOW_WIDTH, othello.Config.WINDOW_WIDTH) )
      self.empty_img    = pygame.image.load('img/empty.png').convert()
      self.black_img    = pygame.image.load('img/black.png').convert()
      self.white_img    = pygame.image.load('img/white.png').convert()
      self.puttedBlack_img    = pygame.image.load('img/puttedBlack.png').convert()
      self.puttedWhite_img    = pygame.image.load('img/puttedWhite.png').convert()
      self.placeable_img= pygame.image.load('img/placeable.png').convert()
      self.empty_rect   = self.empty_img.get_rect()
      self.black_rect   = self.empty_img.get_rect()
      self.white_rect   = self.empty_img.get_rect()
      self.__screen.fill((0,0,0))
      pygame.display.set_caption('Othello')
      pygame.mouse.set_visible(True)
    self.INITIAL_STATE = ((1 << (4 + 3 * 8)) + (1 << (3 + 4 * 8)), (1 << (3 + 3 * 8)) + (1 << (4 + 4 * 8)))
    self.INITIAL_EMPCELL = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,29,30,31,32,33,34,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63]
    self.init()

  def init(self):
    self.black = self.INITIAL_STATE[0]
    self.white = self.INITIAL_STATE[1]
    self.emptyCells = list(self.INITIAL_EMPCELL)
    self.__prevState  = None
    self.__prevEmptyCells = None

  def setState(self, cells, emptyCells):
    self.black = 0
    self.white = 0
    for pos,cell in enumerate(cells):
      if cell == 0:
        self.black += (1 << pos)
      elif cell == 1:
        self.white += (1 << pos)
    self.emptyCells = list(emptyCells)

  # <概要> 空マスリストの更新
  def modifyEmptyCells(self, pos):
    self.emptyCells.remove(pos)

  def at(self, x, y):
    mask = 1 << (x + y * 8)
    if self.black & mask:
      return othello.Config.BLACK
    if self.white & mask:
      return othello.Config.WHITE
    return othello.Config.EMPTY

  def printBoard(self, puttedPos, turn):
    for x in range(othello.Config.CELL_NUM):
      for y in range(othello.Config.CELL_NUM):
        xy = (x*othello.Config.CELL_WIDTH, y*othello.Config.CELL_WIDTH)
        state = self.at(x, y)
        if state == othello.Config.EMPTY:
          if self.placeable(x+y*8,turn):
            self.__screen.blit(self.placeable_img, self.empty_rect.move(xy))
          else:
            self.__screen.blit(self.empty_img, self.empty_rect.move(xy))
        if state == othello.Config.BLACK:
          if x+y*8 == puttedPos:
            self.__screen.blit(self.puttedBlack_img, self.black_rect.move(xy))
          else:
            self.__screen.blit(self.black_img, self.black_rect.move(xy))
        if state == othello.Config.WHITE:
          if x+y*8 == puttedPos:
            self.__screen.blit(self.puttedWhite_img, self.black_rect.move(xy))
          else:
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

  # <概要> 位置posにcolor色の駒を置いて得られる相手の駒数を返す
  # <引数> pos:int(0~63), color:int(0~1){othello.Config.BLACK,WHITE}
  # <返値> int(0~6)
  def takes(self, pos, color): # TODO
    pat = self.__getTakePattern(pos, color)
    count = (pat & int('0x5555555555555555', 16)) + ((pat >> 1) & int('0x5555555555555555',16))
    count = (count & int('0x3333333333333333', 16)) + ((count >> 2) & int('0x3333333333333333', 16))
    count = (count & int('0x0f0f0f0f0f0f0f0f', 16)) + ((count >> 4) & int('0x0f0f0f0f0f0f0f0f', 16))
    count = (count & int('0x00ff00ff00ff00ff', 16)) + ((count >> 8) & int('0x00ff00ff00ff00ff', 16))
    count = (count & int('0x0000ffff0000ffff', 16)) + ((count >> 16) & int('0x0000ffff0000ffff', 16))
    count = (count & int('0x00000000ffffffff', 16)) + ((count >> 32) & int('0x00000000ffffffff', 16))
    return count

  # <概要> 位置posにcolor色の駒を置いて相手の駒を裏返す
  # <引数> pos:int(0~63), color:int(0~1){othello.Config.BLACK,WHITE}
  def put(self, pos, color): # TODO
    pat = self.__getTakePattern(pos, color)
    posbit = 1 << pos
    if color == 0:
      self.black ^= posbit|pat
      self.white ^= pat
    else:
      self.white ^= posbit|pat
      self.black ^= pat

  def __getTakePattern(self, pos, color):
    posbit = 1 << pos
    if color == 0:
      me = self.black
      enemy = self.white
    else:
      enemy = self.black
      me = self.white

    pat = 0
    #右方向
    i = 1
    pat_tmp = 0
    mask = int('0x7e7e7e7e7e7e7e7e', 16)
    while ((posbit >> i) & mask & enemy) != 0 :
      pat_tmp |= (posbit >> i)
      i+=1
    if ((posbit >> i) & me) != 0:
      pat |= pat_tmp

    #左方向
    i = 1
    pat_tmp = 0
    mask = int('0x7e7e7e7e7e7e7e7e', 16)
    while ((posbit << i) & mask & enemy) != 0 :
      pat_tmp |= (posbit << i)
      i+=1
    if ((posbit << i) & me) != 0:
      pat |= pat_tmp

    #上方向
    i = 1
    pat_tmp = 0
    mask = int('0x00ffffffffffff00', 16)
    while ((posbit << 8*i) & mask & enemy) != 0 :
      pat_tmp |= (posbit << 8*i)
      i+=1
    if ((posbit << 8*i) & me) != 0:
      pat |= pat_tmp

    #下方向
    i = 1
    pat_tmp = 0
    mask = int('0x00ffffffffffff00', 16)
    while ((posbit >> 8*i) & mask & enemy) != 0 :
      pat_tmp |= (posbit >> 8*i)
      i+=1
    if ((posbit >> 8*i) & me) != 0:
      pat |= pat_tmp

    #右上方向
    i = 1
    pat_tmp = 0
    mask = int('0x007e7e7e7e7e7e00', 16)
    while ((posbit << 7*i) & mask & enemy) != 0 :
      pat_tmp |= (posbit << 7*i)
      i+=1
    if ((posbit << 7*i) & me) != 0:
      pat |= pat_tmp

    #左上方向
    i = 1
    pat_tmp = 0
    mask = int('0x007e7e7e7e7e7e00', 16)
    while ((posbit << 9*i) & mask & enemy) != 0 :
      pat_tmp |= (posbit << 9*i)
      i+=1
    if ((posbit << 9*i) & me) != 0:
      pat |= pat_tmp

    #右下方向
    i = 1
    pat_tmp = 0
    mask = int('0x007e7e7e7e7e7e00', 16)
    while ((posbit >> 9*i) & mask & enemy) != 0 :
      pat_tmp |= (posbit >> 9*i)
      i+=1
    if ((posbit >> 9*i) & me) != 0:
      pat |= pat_tmp

    #左下方向
    i = 1
    pat_tmp = 0
    mask = int('0x007e7e7e7e7e7e00', 16)
    while ((posbit >> 7*i) & mask & enemy) != 0 :
      pat_tmp |= (posbit >> 7*i)
      i+=1
    if ((posbit >> 7*i) & me) != 0:
      pat |= pat_tmp

    return pat

  # <概要> 位置posにcolor色の駒を置けるか否かを返す
  # <引数> pos:int(0~63), color:int(0~1){othello.Config.BLACK,WHITE}
  # <返値> bool
  def placeable(self, pos, color): # TODO
    cellPos = self.placeableCells(color)
    return pos in cellPos

    #<概要>color色の駒を置くことができる場所を返す
    #<引数>color:int(0~1){othello.Config.BLACK,WHITE}
    #<返り値>list(size:64)
  def placeableCells(self, color): # TODO
    cellPos = []
    if color == 0:
      me = self.black
      enemy = self.white
    else:
      enemy = self.black
      me = self.white
    blank = ~(self.black | self.white)
    #右方向
    mask = enemy & int('0x7e7e7e7e7e7e7e7e', 16)
    t = mask & (me << 1)
    for i in range(5):
      t |= mask & (t << 1)
    valid = blank & (t << 1)

    #左方向
    mask = enemy & int('0x7e7e7e7e7e7e7e7e', 16)
    t = mask & (me >> 1)
    for i in range(5):
      t |= mask & (t >> 1)
    valid |= blank & (t >> 1)

    #上方向
    mask = enemy & int('0x00ffffffffffff00', 16)
    t = mask & (me << 8)
    for i in range(5):
      t |= mask & (t << 8)
    valid |= blank & (t << 8)

    #下方向
    mask = enemy & int('0x00ffffffffffff00', 16)
    t = mask & (me >> 8)
    for i in range(5):
      t |= mask & (t >> 8)
    valid |= blank & (t >> 8)

    #右上方向
    mask = enemy & int('0x007e7e7e7e7e7e00', 16)
    t = mask & (me << 7)
    for i in range(5):
      t |= mask & (t << 7)
    valid |= blank & (t << 7)

    #左上方向
    mask = enemy & int('0x007e7e7e7e7e7e00', 16)
    t = mask & (me << 9)
    for i in range(5):
      t |= mask & (t << 9)
    valid |= blank & (t << 9)

    #右下方向
    mask = enemy & int('0x007e7e7e7e7e7e00', 16)
    t = mask & (me >> 9)
    for i in range(5):
      t |= mask & (t >> 9)
    valid |= blank & (t >> 9)

    #左下方向
    mask = enemy & int('0x007e7e7e7e7e7e00', 16)
    t = mask & (me >> 7)
    for i in range(5):
      t |= mask & (t >> 7)
    valid |= blank & (t >> 7)

    for i in self.emptyCells:
      if valid & (1<<i):
        cellPos.append(i)
      #valid >>= 1
    return cellPos

  def placeableCellsNum(self, color):
    if color == 0:
      me = self.black
      enemy = self.white
    else:
      enemy = self.black
      me = self.white
    blank = ~(self.black | self.white)
    #右方向
    mask = enemy & int('0x7e7e7e7e7e7e7e7e', 16)
    t = mask & (me << 1)
    for i in range(5):
      t |= mask & (t << 1)
    valid = blank & (t << 1)

    #左方向
    mask = enemy & int('0x7e7e7e7e7e7e7e7e', 16)
    t = mask & (me >> 1)
    for i in range(5):
      t |= mask & (t >> 1)
    valid |= blank & (t >> 1)

    #上方向
    mask = enemy & int('0x00ffffffffffff00', 16)
    t = mask & (me << 8)
    for i in range(5):
      t |= mask & (t << 8)
    valid |= blank & (t << 8)

    #下方向
    mask = enemy & int('0x00ffffffffffff00', 16)
    t = mask & (me >> 8)
    for i in range(5):
      t |= mask & (t >> 8)
    valid |= blank & (t >> 8)

    #右上方向
    mask = enemy & int('0x007e7e7e7e7e7e00', 16)
    t = mask & (me << 7)
    for i in range(5):
      t |= mask & (t << 7)
    valid |= blank & (t << 7)

    #左上方向
    mask = enemy & int('0x007e7e7e7e7e7e00', 16)
    t = mask & (me << 9)
    for i in range(5):
      t |= mask & (t << 9)
    valid |= blank & (t << 9)

    #右下方向
    mask = enemy & int('0x007e7e7e7e7e7e00', 16)
    t = mask & (me >> 9)
    for i in range(5):
      t |= mask & (t >> 9)
    valid |= blank & (t >> 9)

    #左下方向
    mask = enemy & int('0x007e7e7e7e7e7e00', 16)
    t = mask & (me >> 7)
    for i in range(5):
      t |= mask & (t >> 7)
    valid |= blank & (t >> 7)

    return bin(valid).count("1")

  # ==================== Undo 関連 =====================
  def getState(self):
    return [self.black, self.white]

  def restoreState(self, state):
    self.black = state[0]
    self.white = state[1]

  def storeState(self):
    self.__prevState = self.getState()
    self.__prevEmptyCells = list(self.emptyCells)

  def loadState(self):
    self.restoreState(self.__prevState)
    self.emptyCells = self.__prevEmptyCells
  # ==================================================

  def getDifference(self, color):
    res = bin(self.black).count("1") - bin(self.white).count("1")
    if color:
      return -res
    else:
      return res
