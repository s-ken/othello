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
    return 0

  # <概要> 位置posにcolor色の駒を置いて相手の駒を裏返す
  # <引数> pos:int(0~63), color:int(0~1){othello.Config.BLACK,WHITE}
  def put(self, pos, color): # TODO
    return

  # <概要> 位置posにcolor色の駒を置けるか否かを返す
  # <引数> pos:int(0~63), color:int(0~1){othello.Config.BLACK,WHITE}
  # <返値> bool
  def placeable(self, pos, color): # TODO
    return True

  def placeableCells(self, color): # TODO
    return [cellPos for cellPos in range(64) if self.placeable(cellPos, color) ]

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
