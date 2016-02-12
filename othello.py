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
    self.board = [[Cell(i,j) for j in range(Config.CELL_NUM)] for i in range(Config.CELL_NUM)]
    self.empty_img  = pygame.image.load('empty.png').convert()
    self.black_img  = pygame.image.load('black.png').convert()
    self.white_img  = pygame.image.load('white.png').convert()
    self.empty_rect = self.empty_img.get_rect()
    self.black_rect = self.empty_img.get_rect()
    self.white_rect = self.empty_img.get_rect()
    self.screen     = screen
    print self.board[0][1].x
  def printBoard(self):
    for i in xrange(0, Config.WPOS+1, Config.CELL_WIDTH):
      x = i/Config.CELL_WIDTH 
      for j in xrange(0, Config.WPOS+1, Config.CELL_WIDTH):
        y = j/Config.CELL_WIDTH
        if self.board[x][y].state == Cell.EMPTY:
          self.screen.blit(self.empty_img, self.empty_rect.move(i,j))
        if self.board[x][y].state == Cell.BLACK:
          self.screen.blit(self.black_img, self.black_rect.move(i,j))
        if self.board[x][y].state == Cell.WHITE:
          self.screen.blit(self.white_img, self.white_rect.move(i,j))
    pygame.display.flip()
  def evaluate(self):
    return [7, 7]
  def getPlaceableCells(self):
    placeable = []

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
      board.board[xpos][ypos].state = Cell.WHITE
      board.printBoard()
      pygame.display.flip()
      turn += 1
    for event in pygame.event.get():
      if (event.type == KEYDOWN and event.key == K_ESCAPE):
        return  # ESCAPEキーが押されたら終了
      if (event.type == MOUSEBUTTONDOWN and turn%2 == 0):
        xpos = int(pygame.mouse.get_pos()[0]/Config.CELL_WIDTH)
        ypos = int(pygame.mouse.get_pos()[1]/Config.CELL_WIDTH)
        board.board[xpos][ypos].state = Cell.BLACK
        board.printBoard()
        pygame.display.flip()
        turn += 1

if __name__ == "__main__":
  main()
