# -*- coding:utf-8 -*-

"""
  references:
    http://d.hatena.ne.jp/Megumi221/20081031/1225450482
"""

import pygame
from pygame.locals import *

class Cell:
  BLACK = 0
  WHITE = 1
  EMPTY = 2
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.state = Cell.EMPTY
  def __mul__(self, other):
    return self.state * other
    
class Config:
  CELL_WIDTH    = 100
  CELL_NUM      = 8
  WINDOW_WIDTH  = CELL_WIDTH * CELL_NUM
  WPOS          = CELL_WIDTH * (CELL_NUM - 1)
  AI_COLOR      = Cell.WHITE
  PATTERNS_NUM    = 3 ** CELL_NUM
  HORI_OFFSET     = 0
  VERT_OFFSET     = CELL_NUM
  DIAG045_OFFSET  = VERT_OFFSET + CELL_NUM
  DIAG135_OFFSET  = DIAG045_OFFSET + CELL_NUM * 2 - 5

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
    self.__index      = Index()
    self.__dummyCell  = Cell(-1, -1)
    self.__lines      = self.__initLines()
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
  def takes(self, x, y, color):
    return self.__takesHori(x, y, color) + self.__takesVert(x, y, color) + self.__takesDiag045(x, y, color) + self.__takesDiag135(x, y, color)
  def put(self, x, y, color):
    self.__reverseDiag045(x, y, color)
    self.at(x, y).state = Cell.EMPTY
    self.__reverseDiag135(x, y, color)
    self.at(x, y).state = Cell.EMPTY
    self.__reverseHori(x, y, color)
    self.at(x, y).state = Cell.EMPTY
    self.__reverseVert(x, y, color)
    return True
  def placeable(self, x, y, color):
    if self.at(x, y).state == Cell.EMPTY and self.takes(x, y, color) > 0:
      return True
    else:
      return False
  def placeableCells(self, color):
    return [cell for cell in self.board if self.placeable(cell.x, cell.y, color) ]
  def __initLines(self):
    return self.__getHoriLines() + self.__getVertLines() + self.__getDiag045Lines() + self.__getDiag135Lines()
  def __getHoriLines(self):
    res = [[] for i in range(Config.CELL_NUM)]
    for y in range(Config.CELL_NUM):
      res[y] = self.board[y*Config.CELL_NUM:(y+1)*Config.CELL_NUM]
    return res
  def __getVertLines(self):
    res = [[] for i in range(Config.CELL_NUM)]
    for x in range(Config.CELL_NUM):
      res[x] = self.board[x :: Config.CELL_NUM]
    return res
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
  def __reverseHori(self, x, y, color):
    self.__index.reverse(self.__lines[Config.HORI_OFFSET + y], x, color)
  def __reverseVert(self, x, y, color):
    self.__index.reverse(self.__lines[Config.VERT_OFFSET + x], y, color)
  def __reverseDiag045(self, x, y, color):
    sum = x + y
    if sum >= 2 and sum <= Config.CELL_NUM * 2 - 4:
      self.__index.reverse(self.__lines[Config.DIAG045_OFFSET + sum - 2], y - max(0, sum - Config.CELL_NUM + 1), color)
  def __reverseDiag135(self, x, y, color):
    dif = y - x
    if abs(dif) <= Config.CELL_NUM - 3:
      self.__index.reverse(self.__lines[Config.DIAG135_OFFSET + dif + Config.CELL_NUM - 3], y - max(0, dif), color)

class Index:
  class Element:
    def __init__(self):
      self.to = -1
      self.takes = 0
  def __init__(self):
    self.__matrix = [[[Index.Element(), Index.Element()] for i in range(Config.CELL_NUM)] for j in range(Config.PATTERNS_NUM)]
    for code in range(Config.PATTERNS_NUM):
      self.__initRow(code)
  def __initRow(self, code):
    line = [Cell(0, 0) for i in range(Config.CELL_NUM)]
    Index.__decode(code, line)
    for x in range(Config.CELL_NUM):
     if line[x].state != Cell.EMPTY:
      continue
     self.__initElement(code, x, line)
  def __initElement(self, i, j, line):
    for color in [Cell.BLACK, Cell.WHITE]:
      lineCpy = [Cell(0, 0) for k in range(Config.CELL_NUM)]
      for (cellCpy, cell) in zip(lineCpy, line):
        cellCpy.state = cell.state
      lineCpy[j].state = color
      takesLeft  = Index.__reverseLine(lineCpy[:j][::-1], color)
      takesRight = Index.__reverseLine(lineCpy[j+1:], color)
      self.__matrix[i][j][color].to    = Index.__encode(lineCpy)
      self.__matrix[i][j][color].takes = takesLeft + takesRight
  @classmethod
  def __decode(cls, code, line):
    for i in range(Config.CELL_NUM)[::-1]:
      line[i].state = code / 3 ** i
      code %= 3 ** i
  @classmethod
  def __encode(cls, line):
    res = 0
    for i, c in enumerate(line):
      res += c * 3 ** i
    return res
  @classmethod
  def __reverseLine(cls, line, color):
    for i, c in enumerate(line):
      if c.state == Cell.EMPTY:
        return 0
      if c.state == color:
        for d in line[:i]:
          d.state = color
        return i
    return 0
  def takes(self, line, x, color):
    return self.__matrix[Index.__encode(line)][x][color].takes
  def reverse(self, line, x, color):
    Index.__decode(self.__matrix[Index.__encode(line)][x][color].to, line)

class AI:
  def __init__(self, board, color):
    self.__board = board
    self.__color = color
  def __evaluate(self):
    placeableCells = self.__board.placeableCells(self.__color)
    return [placeableCells[0].x, placeableCells[0].y]
  def put(self):
    x, y = self.__evaluate()
    self.__board.put(x, y, self.__color)
  def canPut(self):
    return len(self.__board.placeableCells(self.__color)) > 0

class You:
  def __init__(self, board, color):
    self.__board = board
    self.__color = color
  def put(self, x, y):
    if not self.__board.placeable(x, y, self.__color):
      print "ERROR: You cannot put here." 
      return False
    self.__board.put(x, y, self.__color)
    return True
  def canPut(self):
    return len(self.__board.placeableCells(self.__color)) > 0

def main():
  pygame.init()
  screen = pygame.display.set_mode( (Config.WINDOW_WIDTH, Config.WINDOW_WIDTH) )
  screen.fill((0,0,0))
  pygame.display.set_caption('Othello')
  board = Board(screen)
  ai = AI(board, Config.AI_COLOR)
  you = You(board, not Config.AI_COLOR)
  pygame.mouse.set_visible(True)
  turn = 0
  board.printBoard()
  while 1:
    if turn%2 == Config.AI_COLOR:
      ai.put()
      board.printBoard()
      pygame.display.flip()
      turn += 1
    for event in pygame.event.get():
      if (event.type == KEYDOWN and event.key == K_ESCAPE):
        return  # ESCAPEキーが押されたら終了
      if (event.type == MOUSEBUTTONDOWN and turn%2 != Config.AI_COLOR):
        xpos = int(pygame.mouse.get_pos()[0]/Config.CELL_WIDTH)
        ypos = int(pygame.mouse.get_pos()[1]/Config.CELL_WIDTH)
        if you.put(xpos, ypos):
          board.printBoard()
          pygame.display.flip()
          turn += 1

if __name__ == "__main__":
  main()
