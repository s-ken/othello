# -*- coding:utf-8 -*-
# BitBoard :
# 2つの64bitの整数値で表現されたボード.
# 盤面の処理をbit演算で実装できるため高速.
# 詳しくは,
# http://starlancer.org/~is2004/owiki/wiki.cgi?action=ATTACH&file=othello%2E12%2E1%2E2%2Eppt&page=%A4%CA%A4%F3%A4%C7%A4%E2%A5%BB%A5%DF%A5%CA%A1%BC
# とか,Wikipediaとか.
import pygame
import othello

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
    self.black        = (1 << (4 + 3 * 8)) + (1 << (3 + 4 * 8));
    self.white        = (1 << (3 + 3 * 8)) + (1 << (4 + 4 * 8));
    self.__prevState  = None

  def at(self, x, y):
    mask = 1 << (x + y * 8)
    if self.black & mask:
      return othello.Config.BLACK
    if self.white & mask:
      return othello.Config.WHITE
    return othello.Config.EMPTY

  def printBoard(self):
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

  # <概要> 位置posにcolor色の駒を置いて得られる相手の駒数を返す
  # <引数> pos:int(0~63), color:int(0~1){othello.Config.BLACK,WHITE}
  # <返値> int(0~6)
  def takes(self, pos, color): # TODO
    pat = self.__getTakePattern(pos, color)
    count = (pat & int('0x5555555555555555', 16)) + ((pat >> 1)& int('0x5555555555555555',16))
    count = (count & int('0x3333333333333333', 16)) + ((count >> 2)　& int('0x3333333333333333', 16))
    count = (count & int('0x0f0f0f0f0f0f0f0f', 16)) + ((count >> 4)　& int('0x0f0f0f0f0f0f0f0f', 16))
    count = (count & int('0x00ff00ff00ff00ff', 16)) + ((count >> 8)　& int('0x00ff00ff00ff00ff', 16))
    count = (count & int('0x0000ffff0000ffff', 16)) + ((count >> 16)　& int('0x0000ffff0000ffff', 16))
    count = (count & int('0x00000000ffffffff', 16)) + ((count >> 32)　& int('0x00000000ffffffff', 16))
    return count

  # <概要> 位置posにcolor色の駒を置いて相手の駒を裏返す
  # <引数> pos:int(0~63), color:int(0~1){othello.Config.BLACK,WHITE}
  def put(self, pos, color): # TODO
    pat = self.__getTakePattern(pos, color)
    posbit = 1 << (63 - pos)
    if color == 0:
      self.black ^= posbit|pat
      self.white ^= pat
    else:
      self.white ^= posbit|pat
      self.black ^= pat


  def __getTakePattern(self, pos, color):
    posbit = 1 << (63 - pos)
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
      pat_tmp = (posbit >> i)
      i+=1
    if ((posbit >> i) & me) != 0:
      pat |= pat_tmp

    #左方向
    i = 1
    pat_tmp = 0
    mask = int('0x7e7e7e7e7e7e7e7e', 16)
    while ((posbit << i) & mask & enemy) != 0 :
      pat_tmp = (posbit << i)
      i+=1
    if ((posbit << i) & me) != 0:
      pat |= pat_tmp

    #上方向
    i = 1
    pat_tmp = 0
    mask = int('0x00ffffffffffff00', 16)
    while ((posbit << 8*i) & mask & enemy) != 0 :
      pat_tmp = (posbit << 8*i)
      i+=1
    if ((posbit << 8*i) & me) != 0:
      pat |= pat_tmp

    #下方向
    i = 1
    pat_tmp = 0
    mask = int('0x00ffffffffffff00', 16)
    while ((posbit >> 8*i) & mask & enemy) != 0 :
      pat_tmp = (posbit >> 8*i)
      i+=1
    if ((posbit >> 8*i) & me) != 0:
      pat |= pat_tmp

    #右上方向
    i = 1
    pat_tmp = 0
    mask = int('0x007e7e7e7e7e7e00', 16)
    while ((posbit << 7*i) & mask & enemy) != 0 :
      pat_tmp = (posbit << 7*i)
      i+=1
    if ((posbit << 7*i) & me) != 0:
      pat |= pat_tmp

    #左上方向
    i = 1
    pat_tmp = 0
    mask = int('0x007e7e7e7e7e7e00', 16)
    while ((posbit << 9*i) & mask & enemy) != 0 :
      pat_tmp = (posbit << 9*i)
      i+=1
    if ((posbit << 9*i) & me) != 0:
      pat |= pat_tmp

    #右下方向
    i = 1
    pat_tmp = 0
    mask = int('0x007e7e7e7e7e7e00', 16)
    while ((posbit >> 9*i) & mask & enemy) != 0 :
      pat_tmp = (posbit >> 9*i)
      i+=1
    if ((posbit >> 9*i) & me) != 0:
      pat |= pat_tmp

    #左下方向
    i = 1
    pat_tmp = 0
    mask = int('0x007e7e7e7e7e7e00', 16)
    while ((posbit >> 7*i) & mask & enemy) != 0 :
      pat_tmp = (posbit >> 7*i)
      i+=1
    if ((posbit >> 7*i) & me) != 0:
      pat |= pat_tmp

    return pat

  # <概要> 位置posにcolor色の駒を置けるか否かを返す
  # <引数> pos:int(0~63), color:int(0~1){othello.Config.BLACK,WHITE}
  # <返値> bool
  def placeable(self, pos, color): # TODO
    cellPos = self.placeblleCells(color)
    return pos in cellPos

    #<概要>color色の駒を置くことができる場所を返す
    #<引数>color:int(0~1){othello.Config.BLACK,WHITE}
    #<返り値>list(size:64)
  def placeableCells(self, color): # TODO
  cellPos = [0]*64
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
      t |= mask & (me << 1)
    valid = blank & (t << 1)

    #左方向
    mask = enemy & int('0x7e7e7e7e7e7e7e7e', 16)
    t = mask & (me >> 1)
    for i in range(5):
      t |= mask & (me >> 1)
    valid |= blank & (t >> 1)

    #上方向
    mask = enemy & int('0x00ffffffffffff00', 16)
    t = mask & (me << 8)
    for i in range(5):
      t |= mask & (me << 8)
    valid |= blank & (t << 8)

    #下方向
    mask = enemy & int('0x00ffffffffffff00', 16)
    t = mask & (me >> 8)
    for i in range(5):
      t |= mask & (me >> 8)
    valid |= blank & (t >> 8)

    #右上方向
    mask = enemy & int('0x007e7e7e7e7e7e00', 16)
    t = mask & (me << 7)
    for i in range(5):
      t |= mask & (me << 7)
    valid |= blank & (t << 7)

    #左上方向
    mask = enemy & int('0x007e7e7e7e7e7e00', 16)
    t = mask & (me << 9)
    for i in range(5):
      t |= mask & (me << 9)
    valid |= blank & (t << 9)

    #右下方向
    mask = enemy & int('0x007e7e7e7e7e7e00', 16)
    t = mask & (me >> 9)
    for i in range(5):
      t |= mask & (me >> 9)
    valid |= blank & (t >> 9)

    #左下方向
    mask = enemy & int('0x007e7e7e7e7e7e00', 16)
    t = mask & (me >> 7)
    for i in range(5):
      t |= mask & (me >> 7)
    valid |= blank & (t >> 7)

    for i in range(64):
      if valid & 1:
        cellPos[63-i] = 1
      valid >>= 1
    return cellPos


  # ==================== Undo 関連 =====================
  def getState(self):
    return [self.black, self.white]

  def restoreState(self, state):
    self.black = state[0]
    self.white = state[1]

  def storeState(self):
    self.__prevState = self.getState()

  def loadState(self):
    self.restoreState(self.__prevState)
  # ==================================================
