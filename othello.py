# -*- coding:utf-8 -*-

"""
  references:
    http://d.hatena.ne.jp/Megumi221/20081031/1225450482
"""

import pygame
from pygame.locals import *

class Config:
  CELL_WIDTH    = 100
  CELL_NUM      = 8
  WINDOW_WIDTH  = CELL_WIDTH * CELL_NUM
  WPOS          = CELL_WIDTH * (CELL_NUM - 1)

class Cell:
  EMPTY = 0
  BLACK = 1
  WHITE = 2
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.state = Cell.EMPTY

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
  def at(self, x, y):
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
  def takes(self, x, y):
    return 1
  def evaluate(self):
    return [7, 7]
  def placeable(self, x, y):
    if self.board.at(x, y) == Cell.EMPTY and self.takes(x, y) > 0:
      return True
    else:
      return False
  def placeableCells(self):
    return [cell for cell in self.board if placeable(cell.x, cell.y) ]

def main():
  pygame.init()
  screen = pygame.display.set_mode( (Config.WINDOW_WIDTH, Config.WINDOW_WIDTH) )
  screen.fill((0,0,0))
  pygame.display.set_caption('Othello')

  board = Board(screen)

  pygame.mouse.set_visible(True)
  turn = 0

  board.printBoard()

  while 1:
    if turn%2 == 1:
      xpos, ypos = board.evaluate()
      board.at(xpos, ypos).state = Cell.WHITE
      board.printBoard()
      pygame.display.flip()
      turn += 1
    for event in pygame.event.get():
      if (event.type == KEYDOWN and event.key == K_ESCAPE):
        return  # ESCAPEキーが押されたら終了
      if (event.type == MOUSEBUTTONDOWN and turn%2 == 0):
        xpos = int(pygame.mouse.get_pos()[0]/Config.CELL_WIDTH)
        ypos = int(pygame.mouse.get_pos()[1]/Config.CELL_WIDTH)
        board.at(xpos, ypos).state = Cell.BLACK
        board.printBoard()
        pygame.display.flip()
        turn += 1

if __name__ == "__main__":
  main()
