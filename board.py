# -*- coding:utf-8 -*-

import pygame
import othello
import index

class Board:
  def __init__(self):
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

    self.board 	      = [6560] * 38
    self.__emptyCells = range(othello.Config.CELL_NUM ** 2) # 空マスのインデックスリスト. placeableCells()で使用する
    self.__index      = index.Index()
    self.put = [  self.putAt0,self.putAt1,self.putAt2,self.putAt3,self.putAt4,self.putAt5,self.putAt6,self.putAt7,
                  self.putAt8,self.putAt9,self.putAt10,self.putAt11,self.putAt12,self.putAt13,self.putAt14,self.putAt15,
                  self.putAt16,self.putAt17,self.putAt18,self.putAt19,self.putAt20,self.putAt21,self.putAt22,self.putAt23,
                  self.putAt24,self.putAt25,self.putAt26,self.putAt27,self.putAt28,self.putAt29,self.putAt30,self.putAt31,
                  self.putAt32,self.putAt33,self.putAt34,self.putAt35,self.putAt36,self.putAt37,self.putAt38,self.putAt39,
                  self.putAt40,self.putAt41,self.putAt42,self.putAt43,self.putAt44,self.putAt45,self.putAt46,self.putAt47,
                  self.putAt48,self.putAt49,self.putAt50,self.putAt51,self.putAt52,self.putAt53,self.putAt54,self.putAt55,
                  self.putAt56,self.putAt57,self.putAt58,self.putAt59,self.putAt60,self.putAt61,self.putAt62,self.putAt63]
    self.placeable = [  self.placeable0,self.placeable1,self.placeable2,self.placeable3,self.placeable4,self.placeable5,self.placeable6,self.placeable7,
                        self.placeable8,self.placeable9,self.placeable10,self.placeable11,self.placeable12,self.placeable13,self.placeable14,self.placeable15,
                        self.placeable16,self.placeable17,self.placeable18,self.placeable19,self.placeable20,self.placeable21,self.placeable22,self.placeable23,
                        self.placeable24,self.placeable25,self.placeable26,self.placeable27,self.placeable28,self.placeable29,self.placeable30,self.placeable31,
                        self.placeable32,self.placeable33,self.placeable34,self.placeable35,self.placeable36,self.placeable37,self.placeable38,self.placeable39,
                        self.placeable40,self.placeable41,self.placeable42,self.placeable43,self.placeable44,self.placeable45,self.placeable46,self.placeable47,
                        self.placeable48,self.placeable49,self.placeable50,self.placeable51,self.placeable52,self.placeable53,self.placeable54,self.placeable55,
                        self.placeable56,self.placeable57,self.placeable58,self.placeable59,self.placeable60,self.placeable61,self.placeable62,self.placeable63]    
    self.takes = [  self.takes0,self.takes1,self.takes2,self.takes3,self.takes4,self.takes5,self.takes6,self.takes7,
                    self.takes8,self.takes9,self.takes10,self.takes11,self.takes12,self.takes13,self.takes14,self.takes15,
                    self.takes16,self.takes17,self.takes18,self.takes19,self.takes20,self.takes21,self.takes22,self.takes23,
                    self.takes24,self.takes25,self.takes26,self.takes27,self.takes28,self.takes29,self.takes30,self.takes31,
                    self.takes32,self.takes33,self.takes34,self.takes35,self.takes36,self.takes37,self.takes38,self.takes39,
                    self.takes40,self.takes41,self.takes42,self.takes43,self.takes44,self.takes45,self.takes46,self.takes47,
                    self.takes48,self.takes49,self.takes50,self.takes51,self.takes52,self.takes53,self.takes54,self.takes55,
                    self.takes56,self.takes57,self.takes58,self.takes59,self.takes60,self.takes61,self.takes62,self.takes63]
    self.put[3 + (3 << 3)](othello.Config.WHITE)
    self.modifyEmptyCells(3 + (3 << 3))
    self.put[3 + (4 << 3)](othello.Config.BLACK)
    self.modifyEmptyCells(3 + (4 << 3))
    self.put[4 + (3 << 3)](othello.Config.BLACK)
    self.modifyEmptyCells(4 + (3 << 3))
    self.put[4 + (4 << 3)](othello.Config.WHITE)
    self.modifyEmptyCells(4 + (4 << 3))
    self.__prevState = None   # Undo用
    self.__prevEmptyCells = None
    
  def at(self, x, y):
    return (self.board[y] % (3 ** (x + 1))) / (3 ** x)

  def printBoard(self, puttedPos, turn): # TODO
    for x in range(othello.Config.CELL_NUM):
      for y in range(othello.Config.CELL_NUM):
        xy = (x*othello.Config.CELL_WIDTH, y*othello.Config.CELL_WIDTH)
        state = self.at(x, y)
        if state == othello.Config.EMPTY:
          if self.placeable[x+y*8](turn):
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

  def placeableCells(self, color):
    return [cellPos for cellPos in self.__emptyCells if self.placeable[cellPos](color) ]
  
  def placeableCellsNum(self, color):
    res = 0
    for cellPos in self.__emptyCells:
      if self.placeable[cellPos](color):
        res += 1
    return res

  # ==================== 評価関数関連 ====================
  def getEval(self, color):
    res = 0
    for i, code in enumerate(self.board[:8]):
      res += self.__index.getEval(i, code, color)
    return res

  def getSettled(self, color):
    return (self.__index.getSettled(self.board[0],color) + self.__index.getSettled(self.board[7],color) +
            self.__index.getSettled(self.board[8],color) + self.__index.getSettled(self.board[15],color))

  def getMobility(self, color):
    res = 0
    for code in self.board:
      res += self.__index.getMobility(code, color)
    return res

  def getDifference(self, color):
    res = 0
    for code in self.board[:8]:
      res += self.__index.getDifference(code, color)
    return res
  # ==================================================

  # ==================== Undo 関連 =====================
  def getState(self):
    return list(self.board)

  def restoreState(self, state):
    self.board = list(state)

  def storeState(self):
    self.__prevState = self.getState()
    self.__prevEmptyCells = list(self.__emptyCells)

  def loadState(self):
    self.restoreState(self.__prevState)
    self.__emptyCells = self.__prevEmptyCells
  # ==================================================

  # <概要> 空マスリストの更新
  # <詳細> 本来ならこの処理をput()に入れてしまいたいところだが
  #        put()はゲーム木の探索過程で何度も呼び出されるため,ちょっとそれきつい感じ.
  #        ということでpublicな関数にしてPlayerのtakeTurn()内のput() <-実際の盤面に駒が置かれる
  #        のあとにこれを呼び出すことにした
  def modifyEmptyCells(self, pos):
    self.__emptyCells.remove(pos)



  # 以下マス毎のputとplaceableとtakes関数. 関数ポインタのリストの該当位置に格納して使用される
  def takes0(self, color):
    return self.__index.takes(self.board[0],0,color)+self.__index.takes(self.board[8],0,color)+self.__index.takes(self.board[32],0,color)
  def takes1(self, color):
    return self.__index.takes(self.board[0],1,color)+self.__index.takes(self.board[9],0,color)+self.__index.takes(self.board[31],0,color)
  def takes2(self, color):
    return self.__index.takes(self.board[0],2,color)+self.__index.takes(self.board[10],0,color)+self.__index.takes(self.board[16],0,color)+self.__index.takes(self.board[30],0,color)
  def takes3(self, color):
    return self.__index.takes(self.board[0],3,color)+self.__index.takes(self.board[11],0,color)+self.__index.takes(self.board[17],0,color)+self.__index.takes(self.board[29],0,color)
  def takes4(self, color):
    return self.__index.takes(self.board[0],4,color)+self.__index.takes(self.board[12],0,color)+self.__index.takes(self.board[18],0,color)+self.__index.takes(self.board[28],0,color)
  def takes5(self, color):
    return self.__index.takes(self.board[0],5,color)+self.__index.takes(self.board[13],0,color)+self.__index.takes(self.board[19],0,color)+self.__index.takes(self.board[27],0,color)
  def takes6(self, color):
    return self.__index.takes(self.board[0],6,color)+self.__index.takes(self.board[14],0,color)+self.__index.takes(self.board[20],0,color)
  def takes7(self, color):
    return self.__index.takes(self.board[0],7,color)+self.__index.takes(self.board[15],0,color)+self.__index.takes(self.board[21],0,color)
  def takes8(self, color):
    return self.__index.takes(self.board[1],0,color)+self.__index.takes(self.board[8],1,color)+self.__index.takes(self.board[33],0,color)
  def takes9(self, color):
    return self.__index.takes(self.board[1],1,color)+self.__index.takes(self.board[9],1,color)+self.__index.takes(self.board[16],1,color)+self.__index.takes(self.board[32],1,color)
  def takes10(self, color):
    return self.__index.takes(self.board[1],2,color)+self.__index.takes(self.board[10],1,color)+self.__index.takes(self.board[17],1,color)+self.__index.takes(self.board[31],1,color)
  def takes11(self, color):
    return self.__index.takes(self.board[1],3,color)+self.__index.takes(self.board[11],1,color)+self.__index.takes(self.board[18],1,color)+self.__index.takes(self.board[30],1,color)
  def takes12(self, color):
    return self.__index.takes(self.board[1],4,color)+self.__index.takes(self.board[12],1,color)+self.__index.takes(self.board[19],1,color)+self.__index.takes(self.board[29],1,color)
  def takes13(self, color):
    return self.__index.takes(self.board[1],5,color)+self.__index.takes(self.board[13],1,color)+self.__index.takes(self.board[20],1,color)+self.__index.takes(self.board[28],1,color)
  def takes14(self, color):
    return self.__index.takes(self.board[1],6,color)+self.__index.takes(self.board[14],1,color)+self.__index.takes(self.board[21],1,color)+self.__index.takes(self.board[27],1,color)
  def takes15(self, color):
    return self.__index.takes(self.board[1],7,color)+self.__index.takes(self.board[15],1,color)+self.__index.takes(self.board[22],0,color)
  def takes16(self, color):
    return self.__index.takes(self.board[2],0,color)+self.__index.takes(self.board[8],2,color)+self.__index.takes(self.board[16],2,color)+self.__index.takes(self.board[34],0,color)
  def takes17(self, color):
    return self.__index.takes(self.board[2],1,color)+self.__index.takes(self.board[9],2,color)+self.__index.takes(self.board[17],2,color)+self.__index.takes(self.board[33],1,color)
  def takes18(self, color):
    return self.__index.takes(self.board[2],2,color)+self.__index.takes(self.board[10],2,color)+self.__index.takes(self.board[18],2,color)+self.__index.takes(self.board[32],2,color)
  def takes19(self, color):
    return self.__index.takes(self.board[2],3,color)+self.__index.takes(self.board[11],2,color)+self.__index.takes(self.board[19],2,color)+self.__index.takes(self.board[31],2,color)
  def takes20(self, color):
    return self.__index.takes(self.board[2],4,color)+self.__index.takes(self.board[12],2,color)+self.__index.takes(self.board[20],2,color)+self.__index.takes(self.board[30],2,color)
  def takes21(self, color):
    return self.__index.takes(self.board[2],5,color)+self.__index.takes(self.board[13],2,color)+self.__index.takes(self.board[21],2,color)+self.__index.takes(self.board[29],2,color)
  def takes22(self, color):
    return self.__index.takes(self.board[2],6,color)+self.__index.takes(self.board[14],2,color)+self.__index.takes(self.board[22],1,color)+self.__index.takes(self.board[28],2,color)
  def takes23(self, color):
    return self.__index.takes(self.board[2],7,color)+self.__index.takes(self.board[15],2,color)+self.__index.takes(self.board[23],0,color)+self.__index.takes(self.board[27],2,color)
  def takes24(self, color):
    return self.__index.takes(self.board[3],0,color)+self.__index.takes(self.board[8],3,color)+self.__index.takes(self.board[17],3,color)+self.__index.takes(self.board[35],0,color)
  def takes25(self, color):
    return self.__index.takes(self.board[3],1,color)+self.__index.takes(self.board[9],3,color)+self.__index.takes(self.board[18],3,color)+self.__index.takes(self.board[34],1,color)
  def takes26(self, color):
    return self.__index.takes(self.board[3],2,color)+self.__index.takes(self.board[10],3,color)+self.__index.takes(self.board[19],3,color)+self.__index.takes(self.board[33],2,color)
  def takes27(self, color):
    return self.__index.takes(self.board[3],3,color)+self.__index.takes(self.board[11],3,color)+self.__index.takes(self.board[20],3,color)+self.__index.takes(self.board[32],3,color)
  def takes28(self, color):
    return self.__index.takes(self.board[3],4,color)+self.__index.takes(self.board[12],3,color)+self.__index.takes(self.board[21],3,color)+self.__index.takes(self.board[31],3,color)
  def takes29(self, color):
    return self.__index.takes(self.board[3],5,color)+self.__index.takes(self.board[13],3,color)+self.__index.takes(self.board[22],2,color)+self.__index.takes(self.board[30],3,color)
  def takes30(self, color):
    return self.__index.takes(self.board[3],6,color)+self.__index.takes(self.board[14],3,color)+self.__index.takes(self.board[23],1,color)+self.__index.takes(self.board[29],3,color)
  def takes31(self, color):
    return self.__index.takes(self.board[3],7,color)+self.__index.takes(self.board[15],3,color)+self.__index.takes(self.board[24],0,color)+self.__index.takes(self.board[28],3,color)
  def takes32(self, color):
    return self.__index.takes(self.board[4],0,color)+self.__index.takes(self.board[8],4,color)+self.__index.takes(self.board[18],4,color)+self.__index.takes(self.board[36],0,color)
  def takes33(self, color):
    return self.__index.takes(self.board[4],1,color)+self.__index.takes(self.board[9],4,color)+self.__index.takes(self.board[19],4,color)+self.__index.takes(self.board[35],1,color)
  def takes34(self, color):
    return self.__index.takes(self.board[4],2,color)+self.__index.takes(self.board[10],4,color)+self.__index.takes(self.board[20],4,color)+self.__index.takes(self.board[34],2,color)
  def takes35(self, color):
    return self.__index.takes(self.board[4],3,color)+self.__index.takes(self.board[11],4,color)+self.__index.takes(self.board[21],4,color)+self.__index.takes(self.board[33],3,color)
  def takes36(self, color):
    return self.__index.takes(self.board[4],4,color)+self.__index.takes(self.board[12],4,color)+self.__index.takes(self.board[22],3,color)+self.__index.takes(self.board[32],4,color)
  def takes37(self, color):
    return self.__index.takes(self.board[4],5,color)+self.__index.takes(self.board[13],4,color)+self.__index.takes(self.board[23],2,color)+self.__index.takes(self.board[31],4,color)
  def takes38(self, color):
    return self.__index.takes(self.board[4],6,color)+self.__index.takes(self.board[14],4,color)+self.__index.takes(self.board[24],1,color)+self.__index.takes(self.board[30],4,color)
  def takes39(self, color):
    return self.__index.takes(self.board[4],7,color)+self.__index.takes(self.board[15],4,color)+self.__index.takes(self.board[25],0,color)+self.__index.takes(self.board[29],4,color)
  def takes40(self, color):
    return self.__index.takes(self.board[5],0,color)+self.__index.takes(self.board[8],5,color)+self.__index.takes(self.board[19],5,color)+self.__index.takes(self.board[37],0,color)
  def takes41(self, color):
    return self.__index.takes(self.board[5],1,color)+self.__index.takes(self.board[9],5,color)+self.__index.takes(self.board[20],5,color)+self.__index.takes(self.board[36],1,color)
  def takes42(self, color):
    return self.__index.takes(self.board[5],2,color)+self.__index.takes(self.board[10],5,color)+self.__index.takes(self.board[21],5,color)+self.__index.takes(self.board[35],2,color)
  def takes43(self, color):
    return self.__index.takes(self.board[5],3,color)+self.__index.takes(self.board[11],5,color)+self.__index.takes(self.board[22],4,color)+self.__index.takes(self.board[34],3,color)
  def takes44(self, color):
    return self.__index.takes(self.board[5],4,color)+self.__index.takes(self.board[12],5,color)+self.__index.takes(self.board[23],3,color)+self.__index.takes(self.board[33],4,color)
  def takes45(self, color):
    return self.__index.takes(self.board[5],5,color)+self.__index.takes(self.board[13],5,color)+self.__index.takes(self.board[24],2,color)+self.__index.takes(self.board[32],5,color)
  def takes46(self, color):
    return self.__index.takes(self.board[5],6,color)+self.__index.takes(self.board[14],5,color)+self.__index.takes(self.board[25],1,color)+self.__index.takes(self.board[31],5,color)
  def takes47(self, color):
    return self.__index.takes(self.board[5],7,color)+self.__index.takes(self.board[15],5,color)+self.__index.takes(self.board[26],0,color)+self.__index.takes(self.board[30],5,color)
  def takes48(self, color):
    return self.__index.takes(self.board[6],0,color)+self.__index.takes(self.board[8],6,color)+self.__index.takes(self.board[20],6,color)
  def takes49(self, color):
    return self.__index.takes(self.board[6],1,color)+self.__index.takes(self.board[9],6,color)+self.__index.takes(self.board[21],6,color)+self.__index.takes(self.board[37],1,color)
  def takes50(self, color):
    return self.__index.takes(self.board[6],2,color)+self.__index.takes(self.board[10],6,color)+self.__index.takes(self.board[22],5,color)+self.__index.takes(self.board[36],2,color)
  def takes51(self, color):
    return self.__index.takes(self.board[6],3,color)+self.__index.takes(self.board[11],6,color)+self.__index.takes(self.board[23],4,color)+self.__index.takes(self.board[35],3,color)
  def takes52(self, color):
    return self.__index.takes(self.board[6],4,color)+self.__index.takes(self.board[12],6,color)+self.__index.takes(self.board[24],3,color)+self.__index.takes(self.board[34],4,color)
  def takes53(self, color):
    return self.__index.takes(self.board[6],5,color)+self.__index.takes(self.board[13],6,color)+self.__index.takes(self.board[25],2,color)+self.__index.takes(self.board[33],5,color)
  def takes54(self, color):
    return self.__index.takes(self.board[6],6,color)+self.__index.takes(self.board[14],6,color)+self.__index.takes(self.board[26],1,color)+self.__index.takes(self.board[32],6,color)
  def takes55(self, color):
    return self.__index.takes(self.board[6],7,color)+self.__index.takes(self.board[15],6,color)+self.__index.takes(self.board[31],6,color)
  def takes56(self, color):
    return self.__index.takes(self.board[7],0,color)+self.__index.takes(self.board[8],7,color)+self.__index.takes(self.board[21],7,color)
  def takes57(self, color):
    return self.__index.takes(self.board[7],1,color)+self.__index.takes(self.board[9],7,color)+self.__index.takes(self.board[22],6,color)
  def takes58(self, color):
    return self.__index.takes(self.board[7],2,color)+self.__index.takes(self.board[10],7,color)+self.__index.takes(self.board[23],5,color)+self.__index.takes(self.board[37],2,color)
  def takes59(self, color):
    return self.__index.takes(self.board[7],3,color)+self.__index.takes(self.board[11],7,color)+self.__index.takes(self.board[24],4,color)+self.__index.takes(self.board[36],3,color)
  def takes60(self, color):
    return self.__index.takes(self.board[7],4,color)+self.__index.takes(self.board[12],7,color)+self.__index.takes(self.board[25],3,color)+self.__index.takes(self.board[35],4,color)
  def takes61(self, color):
    return self.__index.takes(self.board[7],5,color)+self.__index.takes(self.board[13],7,color)+self.__index.takes(self.board[26],2,color)+self.__index.takes(self.board[34],5,color)
  def takes62(self, color):
    return self.__index.takes(self.board[7],6,color)+self.__index.takes(self.board[14],7,color)+self.__index.takes(self.board[33],6,color)
  def takes63(self, color):
    return self.__index.takes(self.board[7],7,color)+self.__index.takes(self.board[15],7,color)+self.__index.takes(self.board[32],7,color)

  def placeable0(self, color):
    if self.__index.takes(self.board[0],0,color) or self.__index.takes(self.board[8],0,color) or self.__index.takes(self.board[32],0,color):
      return True
    return False
  def placeable1(self, color):
    if self.__index.takes(self.board[0],1,color) or self.__index.takes(self.board[9],0,color) or self.__index.takes(self.board[31],0,color):
      return True
    return False
  def placeable2(self, color):
    if self.__index.takes(self.board[0],2,color) or self.__index.takes(self.board[10],0,color) or self.__index.takes(self.board[16],0,color) or self.__index.takes(self.board[30],0,color):
      return True
    return False
  def placeable3(self, color):
    if self.__index.takes(self.board[0],3,color) or self.__index.takes(self.board[11],0,color) or self.__index.takes(self.board[17],0,color) or self.__index.takes(self.board[29],0,color):
      return True
    return False
  def placeable4(self, color):
    if self.__index.takes(self.board[0],4,color) or self.__index.takes(self.board[12],0,color) or self.__index.takes(self.board[18],0,color) or self.__index.takes(self.board[28],0,color):
      return True
    return False
  def placeable5(self, color):
    if self.__index.takes(self.board[0],5,color) or self.__index.takes(self.board[13],0,color) or self.__index.takes(self.board[19],0,color) or self.__index.takes(self.board[27],0,color):
      return True
    return False
  def placeable6(self, color):
    if self.__index.takes(self.board[0],6,color) or self.__index.takes(self.board[14],0,color) or self.__index.takes(self.board[20],0,color):
      return True
    return False
  def placeable7(self, color):
    if self.__index.takes(self.board[0],7,color) or self.__index.takes(self.board[15],0,color) or self.__index.takes(self.board[21],0,color):
      return True
    return False
  def placeable8(self, color):
    if self.__index.takes(self.board[1],0,color) or self.__index.takes(self.board[8],1,color) or self.__index.takes(self.board[33],0,color):
      return True
    return False
  def placeable9(self, color):
    if self.__index.takes(self.board[1],1,color) or self.__index.takes(self.board[9],1,color) or self.__index.takes(self.board[16],1,color) or self.__index.takes(self.board[32],1,color):
      return True
    return False
  def placeable10(self, color):
    if self.__index.takes(self.board[1],2,color) or self.__index.takes(self.board[10],1,color) or self.__index.takes(self.board[17],1,color) or self.__index.takes(self.board[31],1,color):
      return True
    return False
  def placeable11(self, color):
    if self.__index.takes(self.board[1],3,color) or self.__index.takes(self.board[11],1,color) or self.__index.takes(self.board[18],1,color) or self.__index.takes(self.board[30],1,color):
      return True
    return False
  def placeable12(self, color):
    if self.__index.takes(self.board[1],4,color) or self.__index.takes(self.board[12],1,color) or self.__index.takes(self.board[19],1,color) or self.__index.takes(self.board[29],1,color):
      return True
    return False
  def placeable13(self, color):
    if self.__index.takes(self.board[1],5,color) or self.__index.takes(self.board[13],1,color) or self.__index.takes(self.board[20],1,color) or self.__index.takes(self.board[28],1,color):
      return True
    return False
  def placeable14(self, color):
    if self.__index.takes(self.board[1],6,color) or self.__index.takes(self.board[14],1,color) or self.__index.takes(self.board[21],1,color) or self.__index.takes(self.board[27],1,color):
      return True
    return False
  def placeable15(self, color):
    if self.__index.takes(self.board[1],7,color) or self.__index.takes(self.board[15],1,color) or self.__index.takes(self.board[22],0,color):
      return True
    return False
  def placeable16(self, color):
    if self.__index.takes(self.board[2],0,color) or self.__index.takes(self.board[8],2,color) or self.__index.takes(self.board[16],2,color) or self.__index.takes(self.board[34],0,color):
      return True
    return False
  def placeable17(self, color):
    if self.__index.takes(self.board[2],1,color) or self.__index.takes(self.board[9],2,color) or self.__index.takes(self.board[17],2,color) or self.__index.takes(self.board[33],1,color):
      return True
    return False
  def placeable18(self, color):
    if self.__index.takes(self.board[2],2,color) or self.__index.takes(self.board[10],2,color) or self.__index.takes(self.board[18],2,color) or self.__index.takes(self.board[32],2,color):
      return True
    return False
  def placeable19(self, color):
    if self.__index.takes(self.board[2],3,color) or self.__index.takes(self.board[11],2,color) or self.__index.takes(self.board[19],2,color) or self.__index.takes(self.board[31],2,color):
      return True
    return False
  def placeable20(self, color):
    if self.__index.takes(self.board[2],4,color) or self.__index.takes(self.board[12],2,color) or self.__index.takes(self.board[20],2,color) or self.__index.takes(self.board[30],2,color):
      return True
    return False
  def placeable21(self, color):
    if self.__index.takes(self.board[2],5,color) or self.__index.takes(self.board[13],2,color) or self.__index.takes(self.board[21],2,color) or self.__index.takes(self.board[29],2,color):
      return True
    return False
  def placeable22(self, color):
    if self.__index.takes(self.board[2],6,color) or self.__index.takes(self.board[14],2,color) or self.__index.takes(self.board[22],1,color) or self.__index.takes(self.board[28],2,color):
      return True
    return False
  def placeable23(self, color):
    if self.__index.takes(self.board[2],7,color) or self.__index.takes(self.board[15],2,color) or self.__index.takes(self.board[23],0,color) or self.__index.takes(self.board[27],2,color):
      return True
    return False
  def placeable24(self, color):
    if self.__index.takes(self.board[3],0,color) or self.__index.takes(self.board[8],3,color) or self.__index.takes(self.board[17],3,color) or self.__index.takes(self.board[35],0,color):
      return True
    return False
  def placeable25(self, color):
    if self.__index.takes(self.board[3],1,color) or self.__index.takes(self.board[9],3,color) or self.__index.takes(self.board[18],3,color) or self.__index.takes(self.board[34],1,color):
      return True
    return False
  def placeable26(self, color):
    if self.__index.takes(self.board[3],2,color) or self.__index.takes(self.board[10],3,color) or self.__index.takes(self.board[19],3,color) or self.__index.takes(self.board[33],2,color):
      return True
    return False
  def placeable27(self, color):
    if self.__index.takes(self.board[3],3,color) or self.__index.takes(self.board[11],3,color) or self.__index.takes(self.board[20],3,color) or self.__index.takes(self.board[32],3,color):
      return True
    return False
  def placeable28(self, color):
    if self.__index.takes(self.board[3],4,color) or self.__index.takes(self.board[12],3,color) or self.__index.takes(self.board[21],3,color) or self.__index.takes(self.board[31],3,color):
      return True
    return False
  def placeable29(self, color):
    if self.__index.takes(self.board[3],5,color) or self.__index.takes(self.board[13],3,color) or self.__index.takes(self.board[22],2,color) or self.__index.takes(self.board[30],3,color):
      return True
    return False
  def placeable30(self, color):
    if self.__index.takes(self.board[3],6,color) or self.__index.takes(self.board[14],3,color) or self.__index.takes(self.board[23],1,color) or self.__index.takes(self.board[29],3,color):
      return True
    return False
  def placeable31(self, color):
    if self.__index.takes(self.board[3],7,color) or self.__index.takes(self.board[15],3,color) or self.__index.takes(self.board[24],0,color) or self.__index.takes(self.board[28],3,color):
      return True
    return False
  def placeable32(self, color):
    if self.__index.takes(self.board[4],0,color) or self.__index.takes(self.board[8],4,color) or self.__index.takes(self.board[18],4,color) or self.__index.takes(self.board[36],0,color):
      return True
    return False
  def placeable33(self, color):
    if self.__index.takes(self.board[4],1,color) or self.__index.takes(self.board[9],4,color) or self.__index.takes(self.board[19],4,color) or self.__index.takes(self.board[35],1,color):
      return True
    return False
  def placeable34(self, color):
    if self.__index.takes(self.board[4],2,color) or self.__index.takes(self.board[10],4,color) or self.__index.takes(self.board[20],4,color) or self.__index.takes(self.board[34],2,color):
      return True
    return False
  def placeable35(self, color):
    if self.__index.takes(self.board[4],3,color) or self.__index.takes(self.board[11],4,color) or self.__index.takes(self.board[21],4,color) or self.__index.takes(self.board[33],3,color):
      return True
    return False
  def placeable36(self, color):
    if self.__index.takes(self.board[4],4,color) or self.__index.takes(self.board[12],4,color) or self.__index.takes(self.board[22],3,color) or self.__index.takes(self.board[32],4,color):
      return True
    return False
  def placeable37(self, color):
    if self.__index.takes(self.board[4],5,color) or self.__index.takes(self.board[13],4,color) or self.__index.takes(self.board[23],2,color) or self.__index.takes(self.board[31],4,color):
      return True
    return False
  def placeable38(self, color):
    if self.__index.takes(self.board[4],6,color) or self.__index.takes(self.board[14],4,color) or self.__index.takes(self.board[24],1,color) or self.__index.takes(self.board[30],4,color):
      return True
    return False
  def placeable39(self, color):
    if self.__index.takes(self.board[4],7,color) or self.__index.takes(self.board[15],4,color) or self.__index.takes(self.board[25],0,color) or self.__index.takes(self.board[29],4,color):
      return True
    return False
  def placeable40(self, color):
    if self.__index.takes(self.board[5],0,color) or self.__index.takes(self.board[8],5,color) or self.__index.takes(self.board[19],5,color) or self.__index.takes(self.board[37],0,color):
      return True
    return False
  def placeable41(self, color):
    if self.__index.takes(self.board[5],1,color) or self.__index.takes(self.board[9],5,color) or self.__index.takes(self.board[20],5,color) or self.__index.takes(self.board[36],1,color):
      return True
    return False
  def placeable42(self, color):
    if self.__index.takes(self.board[5],2,color) or self.__index.takes(self.board[10],5,color) or self.__index.takes(self.board[21],5,color) or self.__index.takes(self.board[35],2,color):
      return True
    return False
  def placeable43(self, color):
    if self.__index.takes(self.board[5],3,color) or self.__index.takes(self.board[11],5,color) or self.__index.takes(self.board[22],4,color) or self.__index.takes(self.board[34],3,color):
      return True
    return False
  def placeable44(self, color):
    if self.__index.takes(self.board[5],4,color) or self.__index.takes(self.board[12],5,color) or self.__index.takes(self.board[23],3,color) or self.__index.takes(self.board[33],4,color):
      return True
    return False
  def placeable45(self, color):
    if self.__index.takes(self.board[5],5,color) or self.__index.takes(self.board[13],5,color) or self.__index.takes(self.board[24],2,color) or self.__index.takes(self.board[32],5,color):
      return True
    return False
  def placeable46(self, color):
    if self.__index.takes(self.board[5],6,color) or self.__index.takes(self.board[14],5,color) or self.__index.takes(self.board[25],1,color) or self.__index.takes(self.board[31],5,color):
      return True
    return False
  def placeable47(self, color):
    if self.__index.takes(self.board[5],7,color) or self.__index.takes(self.board[15],5,color) or self.__index.takes(self.board[26],0,color) or self.__index.takes(self.board[30],5,color):
      return True
    return False
  def placeable48(self, color):
    if self.__index.takes(self.board[6],0,color) or self.__index.takes(self.board[8],6,color) or self.__index.takes(self.board[20],6,color):
      return True
    return False
  def placeable49(self, color):
    if self.__index.takes(self.board[6],1,color) or self.__index.takes(self.board[9],6,color) or self.__index.takes(self.board[21],6,color) or self.__index.takes(self.board[37],1,color):
      return True
    return False
  def placeable50(self, color):
    if self.__index.takes(self.board[6],2,color) or self.__index.takes(self.board[10],6,color) or self.__index.takes(self.board[22],5,color) or self.__index.takes(self.board[36],2,color):
      return True
    return False
  def placeable51(self, color):
    if self.__index.takes(self.board[6],3,color) or self.__index.takes(self.board[11],6,color) or self.__index.takes(self.board[23],4,color) or self.__index.takes(self.board[35],3,color):
      return True
    return False
  def placeable52(self, color):
    if self.__index.takes(self.board[6],4,color) or self.__index.takes(self.board[12],6,color) or self.__index.takes(self.board[24],3,color) or self.__index.takes(self.board[34],4,color):
      return True
    return False
  def placeable53(self, color):
    if self.__index.takes(self.board[6],5,color) or self.__index.takes(self.board[13],6,color) or self.__index.takes(self.board[25],2,color) or self.__index.takes(self.board[33],5,color):
      return True
    return False
  def placeable54(self, color):
    if self.__index.takes(self.board[6],6,color) or self.__index.takes(self.board[14],6,color) or self.__index.takes(self.board[26],1,color) or self.__index.takes(self.board[32],6,color):
      return True
    return False
  def placeable55(self, color):
    if self.__index.takes(self.board[6],7,color) or self.__index.takes(self.board[15],6,color) or self.__index.takes(self.board[31],6,color):
      return True
    return False
  def placeable56(self, color):
    if self.__index.takes(self.board[7],0,color) or self.__index.takes(self.board[8],7,color) or self.__index.takes(self.board[21],7,color):
      return True
    return False
  def placeable57(self, color):
    if self.__index.takes(self.board[7],1,color) or self.__index.takes(self.board[9],7,color) or self.__index.takes(self.board[22],6,color):
      return True
    return False
  def placeable58(self, color):
    if self.__index.takes(self.board[7],2,color) or self.__index.takes(self.board[10],7,color) or self.__index.takes(self.board[23],5,color) or self.__index.takes(self.board[37],2,color):
      return True
    return False
  def placeable59(self, color):
    if self.__index.takes(self.board[7],3,color) or self.__index.takes(self.board[11],7,color) or self.__index.takes(self.board[24],4,color) or self.__index.takes(self.board[36],3,color):
      return True
    return False
  def placeable60(self, color):
    if self.__index.takes(self.board[7],4,color) or self.__index.takes(self.board[12],7,color) or self.__index.takes(self.board[25],3,color) or self.__index.takes(self.board[35],4,color):
      return True
    return False
  def placeable61(self, color):
    if self.__index.takes(self.board[7],5,color) or self.__index.takes(self.board[13],7,color) or self.__index.takes(self.board[26],2,color) or self.__index.takes(self.board[34],5,color):
      return True
    return False
  def placeable62(self, color):
    if self.__index.takes(self.board[7],6,color) or self.__index.takes(self.board[14],7,color) or self.__index.takes(self.board[33],6,color):
      return True
    return False
  def placeable63(self, color):
    if self.__index.takes(self.board[7],7,color) or self.__index.takes(self.board[15],7,color) or self.__index.takes(self.board[32],7,color):
      return True
    return False

  def putAt0(self, color):
    self.board[0],fliped = self.__index.flipLine(self.board[0],0,color)
    if fliped[1] >= 1:
      self.board[9] = self.__index.flipDisk(self.board[9],0)
      self.board[31] = self.__index.flipDisk(self.board[31],0)
      if fliped[1] >= 2:
        self.board[10] = self.__index.flipDisk(self.board[10],0)
        self.board[16] = self.__index.flipDisk(self.board[16],0)
        self.board[30] = self.__index.flipDisk(self.board[30],0)
        if fliped[1] >= 3:
          self.board[11] = self.__index.flipDisk(self.board[11],0)
          self.board[17] = self.__index.flipDisk(self.board[17],0)
          self.board[29] = self.__index.flipDisk(self.board[29],0)
          if fliped[1] >= 4:
            self.board[12] = self.__index.flipDisk(self.board[12],0)
            self.board[18] = self.__index.flipDisk(self.board[18],0)
            self.board[28] = self.__index.flipDisk(self.board[28],0)
            if fliped[1] >= 5:
              self.board[13] = self.__index.flipDisk(self.board[13],0)
              self.board[19] = self.__index.flipDisk(self.board[19],0)
              self.board[27] = self.__index.flipDisk(self.board[27],0)
              if fliped[1] >= 6:
                self.board[14] = self.__index.flipDisk(self.board[14],0)
                self.board[20] = self.__index.flipDisk(self.board[20],0)
    self.board[8],fliped = self.__index.flipLine(self.board[8],0,color)
    if fliped[1] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],0);
      self.board[33] = self.__index.flipDisk(self.board[33],0);
      if fliped[1] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],0);
        self.board[16] = self.__index.flipDisk(self.board[16],2);
        self.board[34] = self.__index.flipDisk(self.board[34],0);
        if fliped[1] >= 3:
          self.board[3] = self.__index.flipDisk(self.board[3],0);
          self.board[17] = self.__index.flipDisk(self.board[17],3);
          self.board[35] = self.__index.flipDisk(self.board[35],0);
          if fliped[1] >= 4:
            self.board[4] = self.__index.flipDisk(self.board[4],0);
            self.board[18] = self.__index.flipDisk(self.board[18],4);
            self.board[36] = self.__index.flipDisk(self.board[36],0);
            if fliped[1] >= 5:
              self.board[5] = self.__index.flipDisk(self.board[5],0);
              self.board[19] = self.__index.flipDisk(self.board[19],5);
              self.board[37] = self.__index.flipDisk(self.board[37],0);
              if fliped[1] >= 6:
                self.board[6] = self.__index.flipDisk(self.board[6],0);
                self.board[20] = self.__index.flipDisk(self.board[20],6);
    self.board[32],fliped = self.__index.flipLine(self.board[32],0,color);
    if fliped[1] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],1);
      self.board[9] = self.__index.flipDisk(self.board[9],1);
      self.board[16] = self.__index.flipDisk(self.board[16],1);
      if fliped[1] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],2);
        self.board[10] = self.__index.flipDisk(self.board[10],2);
        self.board[18] = self.__index.flipDisk(self.board[18],2);
        if fliped[1] >= 3:
          self.board[3] = self.__index.flipDisk(self.board[3],3);
          self.board[11] = self.__index.flipDisk(self.board[11],3);
          self.board[20] = self.__index.flipDisk(self.board[20],3);
          if fliped[1] >= 4:
            self.board[4] = self.__index.flipDisk(self.board[4],4);
            self.board[12] = self.__index.flipDisk(self.board[12],4);
            self.board[22] = self.__index.flipDisk(self.board[22],3);
            if fliped[1] >= 5:
              self.board[5] = self.__index.flipDisk(self.board[5],5);
              self.board[13] = self.__index.flipDisk(self.board[13],5);
              self.board[24] = self.__index.flipDisk(self.board[24],2);
              if fliped[1] >= 6:
                self.board[6] = self.__index.flipDisk(self.board[6],6);
                self.board[14] = self.__index.flipDisk(self.board[14],6);
                self.board[26] = self.__index.flipDisk(self.board[26],1);
  def putAt1(self, color):
    self.board[0],fliped = self.__index.flipLine(self.board[0],1,color)
    if fliped[1] >= 1:
      self.board[10] = self.__index.flipDisk(self.board[10],0)
      self.board[16] = self.__index.flipDisk(self.board[16],0)
      self.board[30] = self.__index.flipDisk(self.board[30],0)
      if fliped[1] >= 2:
        self.board[11] = self.__index.flipDisk(self.board[11],0)
        self.board[17] = self.__index.flipDisk(self.board[17],0)
        self.board[29] = self.__index.flipDisk(self.board[29],0)
        if fliped[1] >= 3:
          self.board[12] = self.__index.flipDisk(self.board[12],0)
          self.board[18] = self.__index.flipDisk(self.board[18],0)
          self.board[28] = self.__index.flipDisk(self.board[28],0)
          if fliped[1] >= 4:
            self.board[13] = self.__index.flipDisk(self.board[13],0)
            self.board[19] = self.__index.flipDisk(self.board[19],0)
            self.board[27] = self.__index.flipDisk(self.board[27],0)
            if fliped[1] >= 5:
              self.board[14] = self.__index.flipDisk(self.board[14],0)
              self.board[20] = self.__index.flipDisk(self.board[20],0)
    self.board[9],fliped = self.__index.flipLine(self.board[9],0,color)
    if fliped[1] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],1);
      self.board[16] = self.__index.flipDisk(self.board[16],1);
      self.board[32] = self.__index.flipDisk(self.board[32],1);
      if fliped[1] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],1);
        self.board[17] = self.__index.flipDisk(self.board[17],2);
        self.board[33] = self.__index.flipDisk(self.board[33],1);
        if fliped[1] >= 3:
          self.board[3] = self.__index.flipDisk(self.board[3],1);
          self.board[18] = self.__index.flipDisk(self.board[18],3);
          self.board[34] = self.__index.flipDisk(self.board[34],1);
          if fliped[1] >= 4:
            self.board[4] = self.__index.flipDisk(self.board[4],1);
            self.board[19] = self.__index.flipDisk(self.board[19],4);
            self.board[35] = self.__index.flipDisk(self.board[35],1);
            if fliped[1] >= 5:
              self.board[5] = self.__index.flipDisk(self.board[5],1);
              self.board[20] = self.__index.flipDisk(self.board[20],5);
              self.board[36] = self.__index.flipDisk(self.board[36],1);
              if fliped[1] >= 6:
                self.board[6] = self.__index.flipDisk(self.board[6],1);
                self.board[21] = self.__index.flipDisk(self.board[21],6);
                self.board[37] = self.__index.flipDisk(self.board[37],1);
    self.board[31],fliped = self.__index.flipLine(self.board[31],0,color);
    if fliped[1] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],2);
      self.board[10] = self.__index.flipDisk(self.board[10],1);
      self.board[17] = self.__index.flipDisk(self.board[17],1);
      if fliped[1] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],3);
        self.board[11] = self.__index.flipDisk(self.board[11],2);
        self.board[19] = self.__index.flipDisk(self.board[19],2);
        if fliped[1] >= 3:
          self.board[3] = self.__index.flipDisk(self.board[3],4);
          self.board[12] = self.__index.flipDisk(self.board[12],3);
          self.board[21] = self.__index.flipDisk(self.board[21],3);
          if fliped[1] >= 4:
            self.board[4] = self.__index.flipDisk(self.board[4],5);
            self.board[13] = self.__index.flipDisk(self.board[13],4);
            self.board[23] = self.__index.flipDisk(self.board[23],2);
            if fliped[1] >= 5:
              self.board[5] = self.__index.flipDisk(self.board[5],6);
              self.board[14] = self.__index.flipDisk(self.board[14],5);
              self.board[25] = self.__index.flipDisk(self.board[25],1);
  def putAt2(self, color):
    self.board[0],fliped = self.__index.flipLine(self.board[0],2,color)
    if fliped[0] >= 1:
      self.board[9] = self.__index.flipDisk(self.board[9],0)
      self.board[31] = self.__index.flipDisk(self.board[31],0)
    if fliped[1] >= 1:
      self.board[11] = self.__index.flipDisk(self.board[11],0)
      self.board[17] = self.__index.flipDisk(self.board[17],0)
      self.board[29] = self.__index.flipDisk(self.board[29],0)
      if fliped[1] >= 2:
        self.board[12] = self.__index.flipDisk(self.board[12],0)
        self.board[18] = self.__index.flipDisk(self.board[18],0)
        self.board[28] = self.__index.flipDisk(self.board[28],0)
        if fliped[1] >= 3:
          self.board[13] = self.__index.flipDisk(self.board[13],0)
          self.board[19] = self.__index.flipDisk(self.board[19],0)
          self.board[27] = self.__index.flipDisk(self.board[27],0)
          if fliped[1] >= 4:
            self.board[14] = self.__index.flipDisk(self.board[14],0)
            self.board[20] = self.__index.flipDisk(self.board[20],0)
    self.board[10],fliped = self.__index.flipLine(self.board[10],0,color)
    if fliped[1] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],2);
      self.board[17] = self.__index.flipDisk(self.board[17],1);
      self.board[31] = self.__index.flipDisk(self.board[31],1);
      if fliped[1] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],2);
        self.board[18] = self.__index.flipDisk(self.board[18],2);
        self.board[32] = self.__index.flipDisk(self.board[32],2);
        if fliped[1] >= 3:
          self.board[3] = self.__index.flipDisk(self.board[3],2);
          self.board[19] = self.__index.flipDisk(self.board[19],3);
          self.board[33] = self.__index.flipDisk(self.board[33],2);
          if fliped[1] >= 4:
            self.board[4] = self.__index.flipDisk(self.board[4],2);
            self.board[20] = self.__index.flipDisk(self.board[20],4);
            self.board[34] = self.__index.flipDisk(self.board[34],2);
            if fliped[1] >= 5:
              self.board[5] = self.__index.flipDisk(self.board[5],2);
              self.board[21] = self.__index.flipDisk(self.board[21],5);
              self.board[35] = self.__index.flipDisk(self.board[35],2);
              if fliped[1] >= 6:
                self.board[6] = self.__index.flipDisk(self.board[6],2);
                self.board[22] = self.__index.flipDisk(self.board[22],5);
                self.board[36] = self.__index.flipDisk(self.board[36],2);
    self.board[16],fliped = self.__index.flipLine(self.board[16],0,color);
    if fliped[1] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],1);
      self.board[9] = self.__index.flipDisk(self.board[9],1);
      self.board[32] = self.__index.flipDisk(self.board[32],1);
    self.board[30],fliped = self.__index.flipLine(self.board[30],0,color);
    if fliped[1] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],3);
      self.board[11] = self.__index.flipDisk(self.board[11],1);
      self.board[18] = self.__index.flipDisk(self.board[18],1);
      if fliped[1] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],4);
        self.board[12] = self.__index.flipDisk(self.board[12],2);
        self.board[20] = self.__index.flipDisk(self.board[20],2);
        if fliped[1] >= 3:
          self.board[3] = self.__index.flipDisk(self.board[3],5);
          self.board[13] = self.__index.flipDisk(self.board[13],3);
          self.board[22] = self.__index.flipDisk(self.board[22],2);
          if fliped[1] >= 4:
            self.board[4] = self.__index.flipDisk(self.board[4],6);
            self.board[14] = self.__index.flipDisk(self.board[14],4);
            self.board[24] = self.__index.flipDisk(self.board[24],1);
  def putAt3(self, color):
    self.board[0],fliped = self.__index.flipLine(self.board[0],3,color)
    if fliped[0] >= 1:
      self.board[10] = self.__index.flipDisk(self.board[10],0)
      self.board[16] = self.__index.flipDisk(self.board[16],0)
      self.board[30] = self.__index.flipDisk(self.board[30],0)
      if fliped[0] >= 2:
        self.board[9] = self.__index.flipDisk(self.board[9],0)
        self.board[31] = self.__index.flipDisk(self.board[31],0)
    if fliped[1] >= 1:
      self.board[12] = self.__index.flipDisk(self.board[12],0)
      self.board[18] = self.__index.flipDisk(self.board[18],0)
      self.board[28] = self.__index.flipDisk(self.board[28],0)
      if fliped[1] >= 2:
        self.board[13] = self.__index.flipDisk(self.board[13],0)
        self.board[19] = self.__index.flipDisk(self.board[19],0)
        self.board[27] = self.__index.flipDisk(self.board[27],0)
        if fliped[1] >= 3:
          self.board[14] = self.__index.flipDisk(self.board[14],0)
          self.board[20] = self.__index.flipDisk(self.board[20],0)
    self.board[11],fliped = self.__index.flipLine(self.board[11],0,color)
    if fliped[1] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],3);
      self.board[18] = self.__index.flipDisk(self.board[18],1);
      self.board[30] = self.__index.flipDisk(self.board[30],1);
      if fliped[1] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],3);
        self.board[19] = self.__index.flipDisk(self.board[19],2);
        self.board[31] = self.__index.flipDisk(self.board[31],2);
        if fliped[1] >= 3:
          self.board[3] = self.__index.flipDisk(self.board[3],3);
          self.board[20] = self.__index.flipDisk(self.board[20],3);
          self.board[32] = self.__index.flipDisk(self.board[32],3);
          if fliped[1] >= 4:
            self.board[4] = self.__index.flipDisk(self.board[4],3);
            self.board[21] = self.__index.flipDisk(self.board[21],4);
            self.board[33] = self.__index.flipDisk(self.board[33],3);
            if fliped[1] >= 5:
              self.board[5] = self.__index.flipDisk(self.board[5],3);
              self.board[22] = self.__index.flipDisk(self.board[22],4);
              self.board[34] = self.__index.flipDisk(self.board[34],3);
              if fliped[1] >= 6:
                self.board[6] = self.__index.flipDisk(self.board[6],3);
                self.board[23] = self.__index.flipDisk(self.board[23],4);
                self.board[35] = self.__index.flipDisk(self.board[35],3);
    self.board[17],fliped = self.__index.flipLine(self.board[17],0,color);
    if fliped[1] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],2);
      self.board[10] = self.__index.flipDisk(self.board[10],1);
      self.board[31] = self.__index.flipDisk(self.board[31],1);
      if fliped[1] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],1);
        self.board[9] = self.__index.flipDisk(self.board[9],2);
        self.board[33] = self.__index.flipDisk(self.board[33],1);
    self.board[29],fliped = self.__index.flipLine(self.board[29],0,color);
    if fliped[1] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],4);
      self.board[12] = self.__index.flipDisk(self.board[12],1);
      self.board[19] = self.__index.flipDisk(self.board[19],1);
      if fliped[1] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],5);
        self.board[13] = self.__index.flipDisk(self.board[13],2);
        self.board[21] = self.__index.flipDisk(self.board[21],2);
        if fliped[1] >= 3:
          self.board[3] = self.__index.flipDisk(self.board[3],6);
          self.board[14] = self.__index.flipDisk(self.board[14],3);
          self.board[23] = self.__index.flipDisk(self.board[23],1);
  def putAt4(self, color):
    self.board[0],fliped = self.__index.flipLine(self.board[0],4,color)
    if fliped[0] >= 1:
      self.board[11] = self.__index.flipDisk(self.board[11],0)
      self.board[17] = self.__index.flipDisk(self.board[17],0)
      self.board[29] = self.__index.flipDisk(self.board[29],0)
      if fliped[0] >= 2:
        self.board[10] = self.__index.flipDisk(self.board[10],0)
        self.board[16] = self.__index.flipDisk(self.board[16],0)
        self.board[30] = self.__index.flipDisk(self.board[30],0)
        if fliped[0] >= 3:
          self.board[9] = self.__index.flipDisk(self.board[9],0)
          self.board[31] = self.__index.flipDisk(self.board[31],0)
    if fliped[1] >= 1:
      self.board[13] = self.__index.flipDisk(self.board[13],0)
      self.board[19] = self.__index.flipDisk(self.board[19],0)
      self.board[27] = self.__index.flipDisk(self.board[27],0)
      if fliped[1] >= 2:
        self.board[14] = self.__index.flipDisk(self.board[14],0)
        self.board[20] = self.__index.flipDisk(self.board[20],0)
    self.board[12],fliped = self.__index.flipLine(self.board[12],0,color)
    if fliped[1] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],4);
      self.board[19] = self.__index.flipDisk(self.board[19],1);
      self.board[29] = self.__index.flipDisk(self.board[29],1);
      if fliped[1] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],4);
        self.board[20] = self.__index.flipDisk(self.board[20],2);
        self.board[30] = self.__index.flipDisk(self.board[30],2);
        if fliped[1] >= 3:
          self.board[3] = self.__index.flipDisk(self.board[3],4);
          self.board[21] = self.__index.flipDisk(self.board[21],3);
          self.board[31] = self.__index.flipDisk(self.board[31],3);
          if fliped[1] >= 4:
            self.board[4] = self.__index.flipDisk(self.board[4],4);
            self.board[22] = self.__index.flipDisk(self.board[22],3);
            self.board[32] = self.__index.flipDisk(self.board[32],4);
            if fliped[1] >= 5:
              self.board[5] = self.__index.flipDisk(self.board[5],4);
              self.board[23] = self.__index.flipDisk(self.board[23],3);
              self.board[33] = self.__index.flipDisk(self.board[33],4);
              if fliped[1] >= 6:
                self.board[6] = self.__index.flipDisk(self.board[6],4);
                self.board[24] = self.__index.flipDisk(self.board[24],3);
                self.board[34] = self.__index.flipDisk(self.board[34],4);
    self.board[18],fliped = self.__index.flipLine(self.board[18],0,color);
    if fliped[1] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],3);
      self.board[11] = self.__index.flipDisk(self.board[11],1);
      self.board[30] = self.__index.flipDisk(self.board[30],1);
      if fliped[1] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],2);
        self.board[10] = self.__index.flipDisk(self.board[10],2);
        self.board[32] = self.__index.flipDisk(self.board[32],2);
        if fliped[1] >= 3:
          self.board[3] = self.__index.flipDisk(self.board[3],1);
          self.board[9] = self.__index.flipDisk(self.board[9],3);
          self.board[34] = self.__index.flipDisk(self.board[34],1);
    self.board[28],fliped = self.__index.flipLine(self.board[28],0,color);
    if fliped[1] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],5);
      self.board[13] = self.__index.flipDisk(self.board[13],1);
      self.board[20] = self.__index.flipDisk(self.board[20],1);
      if fliped[1] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],6);
        self.board[14] = self.__index.flipDisk(self.board[14],2);
        self.board[22] = self.__index.flipDisk(self.board[22],1);
  def putAt5(self, color):
    self.board[0],fliped = self.__index.flipLine(self.board[0],5,color)
    if fliped[0] >= 1:
      self.board[12] = self.__index.flipDisk(self.board[12],0)
      self.board[18] = self.__index.flipDisk(self.board[18],0)
      self.board[28] = self.__index.flipDisk(self.board[28],0)
      if fliped[0] >= 2:
        self.board[11] = self.__index.flipDisk(self.board[11],0)
        self.board[17] = self.__index.flipDisk(self.board[17],0)
        self.board[29] = self.__index.flipDisk(self.board[29],0)
        if fliped[0] >= 3:
          self.board[10] = self.__index.flipDisk(self.board[10],0)
          self.board[16] = self.__index.flipDisk(self.board[16],0)
          self.board[30] = self.__index.flipDisk(self.board[30],0)
          if fliped[0] >= 4:
            self.board[9] = self.__index.flipDisk(self.board[9],0)
            self.board[31] = self.__index.flipDisk(self.board[31],0)
    if fliped[1] >= 1:
      self.board[14] = self.__index.flipDisk(self.board[14],0)
      self.board[20] = self.__index.flipDisk(self.board[20],0)
    self.board[13],fliped = self.__index.flipLine(self.board[13],0,color)
    if fliped[1] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],5);
      self.board[20] = self.__index.flipDisk(self.board[20],1);
      self.board[28] = self.__index.flipDisk(self.board[28],1);
      if fliped[1] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],5);
        self.board[21] = self.__index.flipDisk(self.board[21],2);
        self.board[29] = self.__index.flipDisk(self.board[29],2);
        if fliped[1] >= 3:
          self.board[3] = self.__index.flipDisk(self.board[3],5);
          self.board[22] = self.__index.flipDisk(self.board[22],2);
          self.board[30] = self.__index.flipDisk(self.board[30],3);
          if fliped[1] >= 4:
            self.board[4] = self.__index.flipDisk(self.board[4],5);
            self.board[23] = self.__index.flipDisk(self.board[23],2);
            self.board[31] = self.__index.flipDisk(self.board[31],4);
            if fliped[1] >= 5:
              self.board[5] = self.__index.flipDisk(self.board[5],5);
              self.board[24] = self.__index.flipDisk(self.board[24],2);
              self.board[32] = self.__index.flipDisk(self.board[32],5);
              if fliped[1] >= 6:
                self.board[6] = self.__index.flipDisk(self.board[6],5);
                self.board[25] = self.__index.flipDisk(self.board[25],2);
                self.board[33] = self.__index.flipDisk(self.board[33],5);
    self.board[19],fliped = self.__index.flipLine(self.board[19],0,color);
    if fliped[1] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],4);
      self.board[12] = self.__index.flipDisk(self.board[12],1);
      self.board[29] = self.__index.flipDisk(self.board[29],1);
      if fliped[1] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],3);
        self.board[11] = self.__index.flipDisk(self.board[11],2);
        self.board[31] = self.__index.flipDisk(self.board[31],2);
        if fliped[1] >= 3:
          self.board[3] = self.__index.flipDisk(self.board[3],2);
          self.board[10] = self.__index.flipDisk(self.board[10],3);
          self.board[33] = self.__index.flipDisk(self.board[33],2);
          if fliped[1] >= 4:
            self.board[4] = self.__index.flipDisk(self.board[4],1);
            self.board[9] = self.__index.flipDisk(self.board[9],4);
            self.board[35] = self.__index.flipDisk(self.board[35],1);
    self.board[27],fliped = self.__index.flipLine(self.board[27],0,color);
    if fliped[1] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],6);
      self.board[14] = self.__index.flipDisk(self.board[14],1);
      self.board[21] = self.__index.flipDisk(self.board[21],1);
  def putAt6(self, color):
    self.board[0],fliped = self.__index.flipLine(self.board[0],6,color)
    if fliped[0] >= 1:
      self.board[13] = self.__index.flipDisk(self.board[13],0)
      self.board[19] = self.__index.flipDisk(self.board[19],0)
      self.board[27] = self.__index.flipDisk(self.board[27],0)
      if fliped[0] >= 2:
        self.board[12] = self.__index.flipDisk(self.board[12],0)
        self.board[18] = self.__index.flipDisk(self.board[18],0)
        self.board[28] = self.__index.flipDisk(self.board[28],0)
        if fliped[0] >= 3:
          self.board[11] = self.__index.flipDisk(self.board[11],0)
          self.board[17] = self.__index.flipDisk(self.board[17],0)
          self.board[29] = self.__index.flipDisk(self.board[29],0)
          if fliped[0] >= 4:
            self.board[10] = self.__index.flipDisk(self.board[10],0)
            self.board[16] = self.__index.flipDisk(self.board[16],0)
            self.board[30] = self.__index.flipDisk(self.board[30],0)
            if fliped[0] >= 5:
              self.board[9] = self.__index.flipDisk(self.board[9],0)
              self.board[31] = self.__index.flipDisk(self.board[31],0)
    self.board[14],fliped = self.__index.flipLine(self.board[14],0,color)
    if fliped[1] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],6);
      self.board[21] = self.__index.flipDisk(self.board[21],1);
      self.board[27] = self.__index.flipDisk(self.board[27],1);
      if fliped[1] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],6);
        self.board[22] = self.__index.flipDisk(self.board[22],1);
        self.board[28] = self.__index.flipDisk(self.board[28],2);
        if fliped[1] >= 3:
          self.board[3] = self.__index.flipDisk(self.board[3],6);
          self.board[23] = self.__index.flipDisk(self.board[23],1);
          self.board[29] = self.__index.flipDisk(self.board[29],3);
          if fliped[1] >= 4:
            self.board[4] = self.__index.flipDisk(self.board[4],6);
            self.board[24] = self.__index.flipDisk(self.board[24],1);
            self.board[30] = self.__index.flipDisk(self.board[30],4);
            if fliped[1] >= 5:
              self.board[5] = self.__index.flipDisk(self.board[5],6);
              self.board[25] = self.__index.flipDisk(self.board[25],1);
              self.board[31] = self.__index.flipDisk(self.board[31],5);
              if fliped[1] >= 6:
                self.board[6] = self.__index.flipDisk(self.board[6],6);
                self.board[26] = self.__index.flipDisk(self.board[26],1);
                self.board[32] = self.__index.flipDisk(self.board[32],6);
    self.board[20],fliped = self.__index.flipLine(self.board[20],0,color);
    if fliped[1] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],5);
      self.board[13] = self.__index.flipDisk(self.board[13],1);
      self.board[28] = self.__index.flipDisk(self.board[28],1);
      if fliped[1] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],4);
        self.board[12] = self.__index.flipDisk(self.board[12],2);
        self.board[30] = self.__index.flipDisk(self.board[30],2);
        if fliped[1] >= 3:
          self.board[3] = self.__index.flipDisk(self.board[3],3);
          self.board[11] = self.__index.flipDisk(self.board[11],3);
          self.board[32] = self.__index.flipDisk(self.board[32],3);
          if fliped[1] >= 4:
            self.board[4] = self.__index.flipDisk(self.board[4],2);
            self.board[10] = self.__index.flipDisk(self.board[10],4);
            self.board[34] = self.__index.flipDisk(self.board[34],2);
            if fliped[1] >= 5:
              self.board[5] = self.__index.flipDisk(self.board[5],1);
              self.board[9] = self.__index.flipDisk(self.board[9],5);
              self.board[36] = self.__index.flipDisk(self.board[36],1);
  def putAt7(self, color):
    self.board[0],fliped = self.__index.flipLine(self.board[0],7,color)
    if fliped[0] >= 1:
      self.board[14] = self.__index.flipDisk(self.board[14],0)
      self.board[20] = self.__index.flipDisk(self.board[20],0)
      if fliped[0] >= 2:
        self.board[13] = self.__index.flipDisk(self.board[13],0)
        self.board[19] = self.__index.flipDisk(self.board[19],0)
        self.board[27] = self.__index.flipDisk(self.board[27],0)
        if fliped[0] >= 3:
          self.board[12] = self.__index.flipDisk(self.board[12],0)
          self.board[18] = self.__index.flipDisk(self.board[18],0)
          self.board[28] = self.__index.flipDisk(self.board[28],0)
          if fliped[0] >= 4:
            self.board[11] = self.__index.flipDisk(self.board[11],0)
            self.board[17] = self.__index.flipDisk(self.board[17],0)
            self.board[29] = self.__index.flipDisk(self.board[29],0)
            if fliped[0] >= 5:
              self.board[10] = self.__index.flipDisk(self.board[10],0)
              self.board[16] = self.__index.flipDisk(self.board[16],0)
              self.board[30] = self.__index.flipDisk(self.board[30],0)
              if fliped[0] >= 6:
                self.board[9] = self.__index.flipDisk(self.board[9],0)
                self.board[31] = self.__index.flipDisk(self.board[31],0)
    self.board[15],fliped = self.__index.flipLine(self.board[15],0,color)
    if fliped[1] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],7);
      self.board[22] = self.__index.flipDisk(self.board[22],0);
      if fliped[1] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],7);
        self.board[23] = self.__index.flipDisk(self.board[23],0);
        self.board[27] = self.__index.flipDisk(self.board[27],2);
        if fliped[1] >= 3:
          self.board[3] = self.__index.flipDisk(self.board[3],7);
          self.board[24] = self.__index.flipDisk(self.board[24],0);
          self.board[28] = self.__index.flipDisk(self.board[28],3);
          if fliped[1] >= 4:
            self.board[4] = self.__index.flipDisk(self.board[4],7);
            self.board[25] = self.__index.flipDisk(self.board[25],0);
            self.board[29] = self.__index.flipDisk(self.board[29],4);
            if fliped[1] >= 5:
              self.board[5] = self.__index.flipDisk(self.board[5],7);
              self.board[26] = self.__index.flipDisk(self.board[26],0);
              self.board[30] = self.__index.flipDisk(self.board[30],5);
              if fliped[1] >= 6:
                self.board[6] = self.__index.flipDisk(self.board[6],7);
                self.board[31] = self.__index.flipDisk(self.board[31],6);
    self.board[21],fliped = self.__index.flipLine(self.board[21],0,color);
    if fliped[1] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],6);
      self.board[14] = self.__index.flipDisk(self.board[14],1);
      self.board[27] = self.__index.flipDisk(self.board[27],1);
      if fliped[1] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],5);
        self.board[13] = self.__index.flipDisk(self.board[13],2);
        self.board[29] = self.__index.flipDisk(self.board[29],2);
        if fliped[1] >= 3:
          self.board[3] = self.__index.flipDisk(self.board[3],4);
          self.board[12] = self.__index.flipDisk(self.board[12],3);
          self.board[31] = self.__index.flipDisk(self.board[31],3);
          if fliped[1] >= 4:
            self.board[4] = self.__index.flipDisk(self.board[4],3);
            self.board[11] = self.__index.flipDisk(self.board[11],4);
            self.board[33] = self.__index.flipDisk(self.board[33],3);
            if fliped[1] >= 5:
              self.board[5] = self.__index.flipDisk(self.board[5],2);
              self.board[10] = self.__index.flipDisk(self.board[10],5);
              self.board[35] = self.__index.flipDisk(self.board[35],2);
              if fliped[1] >= 6:
                self.board[6] = self.__index.flipDisk(self.board[6],1);
                self.board[9] = self.__index.flipDisk(self.board[9],6);
                self.board[37] = self.__index.flipDisk(self.board[37],1);
  def putAt8(self, color):
    self.board[1],fliped = self.__index.flipLine(self.board[1],0,color)
    if fliped[1] >= 1:
      self.board[9] = self.__index.flipDisk(self.board[9],1)
      self.board[16] = self.__index.flipDisk(self.board[16],1)
      self.board[32] = self.__index.flipDisk(self.board[32],1)
      if fliped[1] >= 2:
        self.board[10] = self.__index.flipDisk(self.board[10],1)
        self.board[17] = self.__index.flipDisk(self.board[17],1)
        self.board[31] = self.__index.flipDisk(self.board[31],1)
        if fliped[1] >= 3:
          self.board[11] = self.__index.flipDisk(self.board[11],1)
          self.board[18] = self.__index.flipDisk(self.board[18],1)
          self.board[30] = self.__index.flipDisk(self.board[30],1)
          if fliped[1] >= 4:
            self.board[12] = self.__index.flipDisk(self.board[12],1)
            self.board[19] = self.__index.flipDisk(self.board[19],1)
            self.board[29] = self.__index.flipDisk(self.board[29],1)
            if fliped[1] >= 5:
              self.board[13] = self.__index.flipDisk(self.board[13],1)
              self.board[20] = self.__index.flipDisk(self.board[20],1)
              self.board[28] = self.__index.flipDisk(self.board[28],1)
              if fliped[1] >= 6:
                self.board[14] = self.__index.flipDisk(self.board[14],1)
                self.board[21] = self.__index.flipDisk(self.board[21],1)
                self.board[27] = self.__index.flipDisk(self.board[27],1)
    self.board[8],fliped = self.__index.flipLine(self.board[8],1,color)
    if fliped[1] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],0);
      self.board[16] = self.__index.flipDisk(self.board[16],2);
      self.board[34] = self.__index.flipDisk(self.board[34],0);
      if fliped[1] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],0);
        self.board[17] = self.__index.flipDisk(self.board[17],3);
        self.board[35] = self.__index.flipDisk(self.board[35],0);
        if fliped[1] >= 3:
          self.board[4] = self.__index.flipDisk(self.board[4],0);
          self.board[18] = self.__index.flipDisk(self.board[18],4);
          self.board[36] = self.__index.flipDisk(self.board[36],0);
          if fliped[1] >= 4:
            self.board[5] = self.__index.flipDisk(self.board[5],0);
            self.board[19] = self.__index.flipDisk(self.board[19],5);
            self.board[37] = self.__index.flipDisk(self.board[37],0);
            if fliped[1] >= 5:
              self.board[6] = self.__index.flipDisk(self.board[6],0);
              self.board[20] = self.__index.flipDisk(self.board[20],6);
    self.board[33],fliped = self.__index.flipLine(self.board[33],0,color);
    if fliped[1] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],1);
      self.board[9] = self.__index.flipDisk(self.board[9],2);
      self.board[17] = self.__index.flipDisk(self.board[17],2);
      if fliped[1] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],2);
        self.board[10] = self.__index.flipDisk(self.board[10],3);
        self.board[19] = self.__index.flipDisk(self.board[19],3);
        if fliped[1] >= 3:
          self.board[4] = self.__index.flipDisk(self.board[4],3);
          self.board[11] = self.__index.flipDisk(self.board[11],4);
          self.board[21] = self.__index.flipDisk(self.board[21],4);
          if fliped[1] >= 4:
            self.board[5] = self.__index.flipDisk(self.board[5],4);
            self.board[12] = self.__index.flipDisk(self.board[12],5);
            self.board[23] = self.__index.flipDisk(self.board[23],3);
            if fliped[1] >= 5:
              self.board[6] = self.__index.flipDisk(self.board[6],5);
              self.board[13] = self.__index.flipDisk(self.board[13],6);
              self.board[25] = self.__index.flipDisk(self.board[25],2);
  def putAt9(self, color):
    self.board[1],fliped = self.__index.flipLine(self.board[1],1,color)
    if fliped[1] >= 1:
      self.board[10] = self.__index.flipDisk(self.board[10],1)
      self.board[17] = self.__index.flipDisk(self.board[17],1)
      self.board[31] = self.__index.flipDisk(self.board[31],1)
      if fliped[1] >= 2:
        self.board[11] = self.__index.flipDisk(self.board[11],1)
        self.board[18] = self.__index.flipDisk(self.board[18],1)
        self.board[30] = self.__index.flipDisk(self.board[30],1)
        if fliped[1] >= 3:
          self.board[12] = self.__index.flipDisk(self.board[12],1)
          self.board[19] = self.__index.flipDisk(self.board[19],1)
          self.board[29] = self.__index.flipDisk(self.board[29],1)
          if fliped[1] >= 4:
            self.board[13] = self.__index.flipDisk(self.board[13],1)
            self.board[20] = self.__index.flipDisk(self.board[20],1)
            self.board[28] = self.__index.flipDisk(self.board[28],1)
            if fliped[1] >= 5:
              self.board[14] = self.__index.flipDisk(self.board[14],1)
              self.board[21] = self.__index.flipDisk(self.board[21],1)
              self.board[27] = self.__index.flipDisk(self.board[27],1)
    self.board[9],fliped = self.__index.flipLine(self.board[9],1,color)
    if fliped[1] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],1);
      self.board[17] = self.__index.flipDisk(self.board[17],2);
      self.board[33] = self.__index.flipDisk(self.board[33],1);
      if fliped[1] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],1);
        self.board[18] = self.__index.flipDisk(self.board[18],3);
        self.board[34] = self.__index.flipDisk(self.board[34],1);
        if fliped[1] >= 3:
          self.board[4] = self.__index.flipDisk(self.board[4],1);
          self.board[19] = self.__index.flipDisk(self.board[19],4);
          self.board[35] = self.__index.flipDisk(self.board[35],1);
          if fliped[1] >= 4:
            self.board[5] = self.__index.flipDisk(self.board[5],1);
            self.board[20] = self.__index.flipDisk(self.board[20],5);
            self.board[36] = self.__index.flipDisk(self.board[36],1);
            if fliped[1] >= 5:
              self.board[6] = self.__index.flipDisk(self.board[6],1);
              self.board[21] = self.__index.flipDisk(self.board[21],6);
              self.board[37] = self.__index.flipDisk(self.board[37],1);
    self.board[16],fliped = self.__index.flipLine(self.board[16],1,color);
    self.board[32],fliped = self.__index.flipLine(self.board[32],1,color);
    if fliped[1] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],2);
      self.board[10] = self.__index.flipDisk(self.board[10],2);
      self.board[18] = self.__index.flipDisk(self.board[18],2);
      if fliped[1] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],3);
        self.board[11] = self.__index.flipDisk(self.board[11],3);
        self.board[20] = self.__index.flipDisk(self.board[20],3);
        if fliped[1] >= 3:
          self.board[4] = self.__index.flipDisk(self.board[4],4);
          self.board[12] = self.__index.flipDisk(self.board[12],4);
          self.board[22] = self.__index.flipDisk(self.board[22],3);
          if fliped[1] >= 4:
            self.board[5] = self.__index.flipDisk(self.board[5],5);
            self.board[13] = self.__index.flipDisk(self.board[13],5);
            self.board[24] = self.__index.flipDisk(self.board[24],2);
            if fliped[1] >= 5:
              self.board[6] = self.__index.flipDisk(self.board[6],6);
              self.board[14] = self.__index.flipDisk(self.board[14],6);
              self.board[26] = self.__index.flipDisk(self.board[26],1);
  def putAt10(self, color):
    self.board[1],fliped = self.__index.flipLine(self.board[1],2,color)
    if fliped[0] >= 1:
      self.board[9] = self.__index.flipDisk(self.board[9],1)
      self.board[16] = self.__index.flipDisk(self.board[16],1)
      self.board[32] = self.__index.flipDisk(self.board[32],1)
    if fliped[1] >= 1:
      self.board[11] = self.__index.flipDisk(self.board[11],1)
      self.board[18] = self.__index.flipDisk(self.board[18],1)
      self.board[30] = self.__index.flipDisk(self.board[30],1)
      if fliped[1] >= 2:
        self.board[12] = self.__index.flipDisk(self.board[12],1)
        self.board[19] = self.__index.flipDisk(self.board[19],1)
        self.board[29] = self.__index.flipDisk(self.board[29],1)
        if fliped[1] >= 3:
          self.board[13] = self.__index.flipDisk(self.board[13],1)
          self.board[20] = self.__index.flipDisk(self.board[20],1)
          self.board[28] = self.__index.flipDisk(self.board[28],1)
          if fliped[1] >= 4:
            self.board[14] = self.__index.flipDisk(self.board[14],1)
            self.board[21] = self.__index.flipDisk(self.board[21],1)
            self.board[27] = self.__index.flipDisk(self.board[27],1)
    self.board[10],fliped = self.__index.flipLine(self.board[10],1,color)
    if fliped[1] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],2);
      self.board[18] = self.__index.flipDisk(self.board[18],2);
      self.board[32] = self.__index.flipDisk(self.board[32],2);
      if fliped[1] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],2);
        self.board[19] = self.__index.flipDisk(self.board[19],3);
        self.board[33] = self.__index.flipDisk(self.board[33],2);
        if fliped[1] >= 3:
          self.board[4] = self.__index.flipDisk(self.board[4],2);
          self.board[20] = self.__index.flipDisk(self.board[20],4);
          self.board[34] = self.__index.flipDisk(self.board[34],2);
          if fliped[1] >= 4:
            self.board[5] = self.__index.flipDisk(self.board[5],2);
            self.board[21] = self.__index.flipDisk(self.board[21],5);
            self.board[35] = self.__index.flipDisk(self.board[35],2);
            if fliped[1] >= 5:
              self.board[6] = self.__index.flipDisk(self.board[6],2);
              self.board[22] = self.__index.flipDisk(self.board[22],5);
              self.board[36] = self.__index.flipDisk(self.board[36],2);
    self.board[17],fliped = self.__index.flipLine(self.board[17],1,color);
    if fliped[1] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],1);
      self.board[9] = self.__index.flipDisk(self.board[9],2);
      self.board[33] = self.__index.flipDisk(self.board[33],1);
    self.board[31],fliped = self.__index.flipLine(self.board[31],1,color);
    if fliped[1] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],3);
      self.board[11] = self.__index.flipDisk(self.board[11],2);
      self.board[19] = self.__index.flipDisk(self.board[19],2);
      if fliped[1] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],4);
        self.board[12] = self.__index.flipDisk(self.board[12],3);
        self.board[21] = self.__index.flipDisk(self.board[21],3);
        if fliped[1] >= 3:
          self.board[4] = self.__index.flipDisk(self.board[4],5);
          self.board[13] = self.__index.flipDisk(self.board[13],4);
          self.board[23] = self.__index.flipDisk(self.board[23],2);
          if fliped[1] >= 4:
            self.board[5] = self.__index.flipDisk(self.board[5],6);
            self.board[14] = self.__index.flipDisk(self.board[14],5);
            self.board[25] = self.__index.flipDisk(self.board[25],1);
  def putAt11(self, color):
    self.board[1],fliped = self.__index.flipLine(self.board[1],3,color)
    if fliped[0] >= 1:
      self.board[10] = self.__index.flipDisk(self.board[10],1)
      self.board[17] = self.__index.flipDisk(self.board[17],1)
      self.board[31] = self.__index.flipDisk(self.board[31],1)
      if fliped[0] >= 2:
        self.board[9] = self.__index.flipDisk(self.board[9],1)
        self.board[16] = self.__index.flipDisk(self.board[16],1)
        self.board[32] = self.__index.flipDisk(self.board[32],1)
    if fliped[1] >= 1:
      self.board[12] = self.__index.flipDisk(self.board[12],1)
      self.board[19] = self.__index.flipDisk(self.board[19],1)
      self.board[29] = self.__index.flipDisk(self.board[29],1)
      if fliped[1] >= 2:
        self.board[13] = self.__index.flipDisk(self.board[13],1)
        self.board[20] = self.__index.flipDisk(self.board[20],1)
        self.board[28] = self.__index.flipDisk(self.board[28],1)
        if fliped[1] >= 3:
          self.board[14] = self.__index.flipDisk(self.board[14],1)
          self.board[21] = self.__index.flipDisk(self.board[21],1)
          self.board[27] = self.__index.flipDisk(self.board[27],1)
    self.board[11],fliped = self.__index.flipLine(self.board[11],1,color)
    if fliped[1] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],3);
      self.board[19] = self.__index.flipDisk(self.board[19],2);
      self.board[31] = self.__index.flipDisk(self.board[31],2);
      if fliped[1] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],3);
        self.board[20] = self.__index.flipDisk(self.board[20],3);
        self.board[32] = self.__index.flipDisk(self.board[32],3);
        if fliped[1] >= 3:
          self.board[4] = self.__index.flipDisk(self.board[4],3);
          self.board[21] = self.__index.flipDisk(self.board[21],4);
          self.board[33] = self.__index.flipDisk(self.board[33],3);
          if fliped[1] >= 4:
            self.board[5] = self.__index.flipDisk(self.board[5],3);
            self.board[22] = self.__index.flipDisk(self.board[22],4);
            self.board[34] = self.__index.flipDisk(self.board[34],3);
            if fliped[1] >= 5:
              self.board[6] = self.__index.flipDisk(self.board[6],3);
              self.board[23] = self.__index.flipDisk(self.board[23],4);
              self.board[35] = self.__index.flipDisk(self.board[35],3);
    self.board[18],fliped = self.__index.flipLine(self.board[18],1,color);
    if fliped[1] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],2);
      self.board[10] = self.__index.flipDisk(self.board[10],2);
      self.board[32] = self.__index.flipDisk(self.board[32],2);
      if fliped[1] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],1);
        self.board[9] = self.__index.flipDisk(self.board[9],3);
        self.board[34] = self.__index.flipDisk(self.board[34],1);
    self.board[30],fliped = self.__index.flipLine(self.board[30],1,color);
    if fliped[1] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],4);
      self.board[12] = self.__index.flipDisk(self.board[12],2);
      self.board[20] = self.__index.flipDisk(self.board[20],2);
      if fliped[1] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],5);
        self.board[13] = self.__index.flipDisk(self.board[13],3);
        self.board[22] = self.__index.flipDisk(self.board[22],2);
        if fliped[1] >= 3:
          self.board[4] = self.__index.flipDisk(self.board[4],6);
          self.board[14] = self.__index.flipDisk(self.board[14],4);
          self.board[24] = self.__index.flipDisk(self.board[24],1);
  def putAt12(self, color):
    self.board[1],fliped = self.__index.flipLine(self.board[1],4,color)
    if fliped[0] >= 1:
      self.board[11] = self.__index.flipDisk(self.board[11],1)
      self.board[18] = self.__index.flipDisk(self.board[18],1)
      self.board[30] = self.__index.flipDisk(self.board[30],1)
      if fliped[0] >= 2:
        self.board[10] = self.__index.flipDisk(self.board[10],1)
        self.board[17] = self.__index.flipDisk(self.board[17],1)
        self.board[31] = self.__index.flipDisk(self.board[31],1)
        if fliped[0] >= 3:
          self.board[9] = self.__index.flipDisk(self.board[9],1)
          self.board[16] = self.__index.flipDisk(self.board[16],1)
          self.board[32] = self.__index.flipDisk(self.board[32],1)
    if fliped[1] >= 1:
      self.board[13] = self.__index.flipDisk(self.board[13],1)
      self.board[20] = self.__index.flipDisk(self.board[20],1)
      self.board[28] = self.__index.flipDisk(self.board[28],1)
      if fliped[1] >= 2:
        self.board[14] = self.__index.flipDisk(self.board[14],1)
        self.board[21] = self.__index.flipDisk(self.board[21],1)
        self.board[27] = self.__index.flipDisk(self.board[27],1)
    self.board[12],fliped = self.__index.flipLine(self.board[12],1,color)
    if fliped[1] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],4);
      self.board[20] = self.__index.flipDisk(self.board[20],2);
      self.board[30] = self.__index.flipDisk(self.board[30],2);
      if fliped[1] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],4);
        self.board[21] = self.__index.flipDisk(self.board[21],3);
        self.board[31] = self.__index.flipDisk(self.board[31],3);
        if fliped[1] >= 3:
          self.board[4] = self.__index.flipDisk(self.board[4],4);
          self.board[22] = self.__index.flipDisk(self.board[22],3);
          self.board[32] = self.__index.flipDisk(self.board[32],4);
          if fliped[1] >= 4:
            self.board[5] = self.__index.flipDisk(self.board[5],4);
            self.board[23] = self.__index.flipDisk(self.board[23],3);
            self.board[33] = self.__index.flipDisk(self.board[33],4);
            if fliped[1] >= 5:
              self.board[6] = self.__index.flipDisk(self.board[6],4);
              self.board[24] = self.__index.flipDisk(self.board[24],3);
              self.board[34] = self.__index.flipDisk(self.board[34],4);
    self.board[19],fliped = self.__index.flipLine(self.board[19],1,color);
    if fliped[1] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],3);
      self.board[11] = self.__index.flipDisk(self.board[11],2);
      self.board[31] = self.__index.flipDisk(self.board[31],2);
      if fliped[1] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],2);
        self.board[10] = self.__index.flipDisk(self.board[10],3);
        self.board[33] = self.__index.flipDisk(self.board[33],2);
        if fliped[1] >= 3:
          self.board[4] = self.__index.flipDisk(self.board[4],1);
          self.board[9] = self.__index.flipDisk(self.board[9],4);
          self.board[35] = self.__index.flipDisk(self.board[35],1);
    self.board[29],fliped = self.__index.flipLine(self.board[29],1,color);
    if fliped[1] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],5);
      self.board[13] = self.__index.flipDisk(self.board[13],2);
      self.board[21] = self.__index.flipDisk(self.board[21],2);
      if fliped[1] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],6);
        self.board[14] = self.__index.flipDisk(self.board[14],3);
        self.board[23] = self.__index.flipDisk(self.board[23],1);
  def putAt13(self, color):
    self.board[1],fliped = self.__index.flipLine(self.board[1],5,color)
    if fliped[0] >= 1:
      self.board[12] = self.__index.flipDisk(self.board[12],1)
      self.board[19] = self.__index.flipDisk(self.board[19],1)
      self.board[29] = self.__index.flipDisk(self.board[29],1)
      if fliped[0] >= 2:
        self.board[11] = self.__index.flipDisk(self.board[11],1)
        self.board[18] = self.__index.flipDisk(self.board[18],1)
        self.board[30] = self.__index.flipDisk(self.board[30],1)
        if fliped[0] >= 3:
          self.board[10] = self.__index.flipDisk(self.board[10],1)
          self.board[17] = self.__index.flipDisk(self.board[17],1)
          self.board[31] = self.__index.flipDisk(self.board[31],1)
          if fliped[0] >= 4:
            self.board[9] = self.__index.flipDisk(self.board[9],1)
            self.board[16] = self.__index.flipDisk(self.board[16],1)
            self.board[32] = self.__index.flipDisk(self.board[32],1)
    if fliped[1] >= 1:
      self.board[14] = self.__index.flipDisk(self.board[14],1)
      self.board[21] = self.__index.flipDisk(self.board[21],1)
      self.board[27] = self.__index.flipDisk(self.board[27],1)
    self.board[13],fliped = self.__index.flipLine(self.board[13],1,color)
    if fliped[1] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],5);
      self.board[21] = self.__index.flipDisk(self.board[21],2);
      self.board[29] = self.__index.flipDisk(self.board[29],2);
      if fliped[1] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],5);
        self.board[22] = self.__index.flipDisk(self.board[22],2);
        self.board[30] = self.__index.flipDisk(self.board[30],3);
        if fliped[1] >= 3:
          self.board[4] = self.__index.flipDisk(self.board[4],5);
          self.board[23] = self.__index.flipDisk(self.board[23],2);
          self.board[31] = self.__index.flipDisk(self.board[31],4);
          if fliped[1] >= 4:
            self.board[5] = self.__index.flipDisk(self.board[5],5);
            self.board[24] = self.__index.flipDisk(self.board[24],2);
            self.board[32] = self.__index.flipDisk(self.board[32],5);
            if fliped[1] >= 5:
              self.board[6] = self.__index.flipDisk(self.board[6],5);
              self.board[25] = self.__index.flipDisk(self.board[25],2);
              self.board[33] = self.__index.flipDisk(self.board[33],5);
    self.board[20],fliped = self.__index.flipLine(self.board[20],1,color);
    if fliped[1] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],4);
      self.board[12] = self.__index.flipDisk(self.board[12],2);
      self.board[30] = self.__index.flipDisk(self.board[30],2);
      if fliped[1] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],3);
        self.board[11] = self.__index.flipDisk(self.board[11],3);
        self.board[32] = self.__index.flipDisk(self.board[32],3);
        if fliped[1] >= 3:
          self.board[4] = self.__index.flipDisk(self.board[4],2);
          self.board[10] = self.__index.flipDisk(self.board[10],4);
          self.board[34] = self.__index.flipDisk(self.board[34],2);
          if fliped[1] >= 4:
            self.board[5] = self.__index.flipDisk(self.board[5],1);
            self.board[9] = self.__index.flipDisk(self.board[9],5);
            self.board[36] = self.__index.flipDisk(self.board[36],1);
    self.board[28],fliped = self.__index.flipLine(self.board[28],1,color);
    if fliped[1] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],6);
      self.board[14] = self.__index.flipDisk(self.board[14],2);
      self.board[22] = self.__index.flipDisk(self.board[22],1);
  def putAt14(self, color):
    self.board[1],fliped = self.__index.flipLine(self.board[1],6,color)
    if fliped[0] >= 1:
      self.board[13] = self.__index.flipDisk(self.board[13],1)
      self.board[20] = self.__index.flipDisk(self.board[20],1)
      self.board[28] = self.__index.flipDisk(self.board[28],1)
      if fliped[0] >= 2:
        self.board[12] = self.__index.flipDisk(self.board[12],1)
        self.board[19] = self.__index.flipDisk(self.board[19],1)
        self.board[29] = self.__index.flipDisk(self.board[29],1)
        if fliped[0] >= 3:
          self.board[11] = self.__index.flipDisk(self.board[11],1)
          self.board[18] = self.__index.flipDisk(self.board[18],1)
          self.board[30] = self.__index.flipDisk(self.board[30],1)
          if fliped[0] >= 4:
            self.board[10] = self.__index.flipDisk(self.board[10],1)
            self.board[17] = self.__index.flipDisk(self.board[17],1)
            self.board[31] = self.__index.flipDisk(self.board[31],1)
            if fliped[0] >= 5:
              self.board[9] = self.__index.flipDisk(self.board[9],1)
              self.board[16] = self.__index.flipDisk(self.board[16],1)
              self.board[32] = self.__index.flipDisk(self.board[32],1)
    self.board[14],fliped = self.__index.flipLine(self.board[14],1,color)
    if fliped[1] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],6);
      self.board[22] = self.__index.flipDisk(self.board[22],1);
      self.board[28] = self.__index.flipDisk(self.board[28],2);
      if fliped[1] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],6);
        self.board[23] = self.__index.flipDisk(self.board[23],1);
        self.board[29] = self.__index.flipDisk(self.board[29],3);
        if fliped[1] >= 3:
          self.board[4] = self.__index.flipDisk(self.board[4],6);
          self.board[24] = self.__index.flipDisk(self.board[24],1);
          self.board[30] = self.__index.flipDisk(self.board[30],4);
          if fliped[1] >= 4:
            self.board[5] = self.__index.flipDisk(self.board[5],6);
            self.board[25] = self.__index.flipDisk(self.board[25],1);
            self.board[31] = self.__index.flipDisk(self.board[31],5);
            if fliped[1] >= 5:
              self.board[6] = self.__index.flipDisk(self.board[6],6);
              self.board[26] = self.__index.flipDisk(self.board[26],1);
              self.board[32] = self.__index.flipDisk(self.board[32],6);
    self.board[21],fliped = self.__index.flipLine(self.board[21],1,color);
    if fliped[1] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],5);
      self.board[13] = self.__index.flipDisk(self.board[13],2);
      self.board[29] = self.__index.flipDisk(self.board[29],2);
      if fliped[1] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],4);
        self.board[12] = self.__index.flipDisk(self.board[12],3);
        self.board[31] = self.__index.flipDisk(self.board[31],3);
        if fliped[1] >= 3:
          self.board[4] = self.__index.flipDisk(self.board[4],3);
          self.board[11] = self.__index.flipDisk(self.board[11],4);
          self.board[33] = self.__index.flipDisk(self.board[33],3);
          if fliped[1] >= 4:
            self.board[5] = self.__index.flipDisk(self.board[5],2);
            self.board[10] = self.__index.flipDisk(self.board[10],5);
            self.board[35] = self.__index.flipDisk(self.board[35],2);
            if fliped[1] >= 5:
              self.board[6] = self.__index.flipDisk(self.board[6],1);
              self.board[9] = self.__index.flipDisk(self.board[9],6);
              self.board[37] = self.__index.flipDisk(self.board[37],1);
    self.board[27],fliped = self.__index.flipLine(self.board[27],1,color);
  def putAt15(self, color):
    self.board[1],fliped = self.__index.flipLine(self.board[1],7,color)
    if fliped[0] >= 1:
      self.board[14] = self.__index.flipDisk(self.board[14],1)
      self.board[21] = self.__index.flipDisk(self.board[21],1)
      self.board[27] = self.__index.flipDisk(self.board[27],1)
      if fliped[0] >= 2:
        self.board[13] = self.__index.flipDisk(self.board[13],1)
        self.board[20] = self.__index.flipDisk(self.board[20],1)
        self.board[28] = self.__index.flipDisk(self.board[28],1)
        if fliped[0] >= 3:
          self.board[12] = self.__index.flipDisk(self.board[12],1)
          self.board[19] = self.__index.flipDisk(self.board[19],1)
          self.board[29] = self.__index.flipDisk(self.board[29],1)
          if fliped[0] >= 4:
            self.board[11] = self.__index.flipDisk(self.board[11],1)
            self.board[18] = self.__index.flipDisk(self.board[18],1)
            self.board[30] = self.__index.flipDisk(self.board[30],1)
            if fliped[0] >= 5:
              self.board[10] = self.__index.flipDisk(self.board[10],1)
              self.board[17] = self.__index.flipDisk(self.board[17],1)
              self.board[31] = self.__index.flipDisk(self.board[31],1)
              if fliped[0] >= 6:
                self.board[9] = self.__index.flipDisk(self.board[9],1)
                self.board[16] = self.__index.flipDisk(self.board[16],1)
                self.board[32] = self.__index.flipDisk(self.board[32],1)
    self.board[15],fliped = self.__index.flipLine(self.board[15],1,color)
    if fliped[1] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],7);
      self.board[23] = self.__index.flipDisk(self.board[23],0);
      self.board[27] = self.__index.flipDisk(self.board[27],2);
      if fliped[1] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],7);
        self.board[24] = self.__index.flipDisk(self.board[24],0);
        self.board[28] = self.__index.flipDisk(self.board[28],3);
        if fliped[1] >= 3:
          self.board[4] = self.__index.flipDisk(self.board[4],7);
          self.board[25] = self.__index.flipDisk(self.board[25],0);
          self.board[29] = self.__index.flipDisk(self.board[29],4);
          if fliped[1] >= 4:
            self.board[5] = self.__index.flipDisk(self.board[5],7);
            self.board[26] = self.__index.flipDisk(self.board[26],0);
            self.board[30] = self.__index.flipDisk(self.board[30],5);
            if fliped[1] >= 5:
              self.board[6] = self.__index.flipDisk(self.board[6],7);
              self.board[31] = self.__index.flipDisk(self.board[31],6);
    self.board[22],fliped = self.__index.flipLine(self.board[22],0,color);
    if fliped[1] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],6);
      self.board[14] = self.__index.flipDisk(self.board[14],2);
      self.board[28] = self.__index.flipDisk(self.board[28],2);
      if fliped[1] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],5);
        self.board[13] = self.__index.flipDisk(self.board[13],3);
        self.board[30] = self.__index.flipDisk(self.board[30],3);
        if fliped[1] >= 3:
          self.board[4] = self.__index.flipDisk(self.board[4],4);
          self.board[12] = self.__index.flipDisk(self.board[12],4);
          self.board[32] = self.__index.flipDisk(self.board[32],4);
          if fliped[1] >= 4:
            self.board[5] = self.__index.flipDisk(self.board[5],3);
            self.board[11] = self.__index.flipDisk(self.board[11],5);
            self.board[34] = self.__index.flipDisk(self.board[34],3);
            if fliped[1] >= 5:
              self.board[6] = self.__index.flipDisk(self.board[6],2);
              self.board[10] = self.__index.flipDisk(self.board[10],6);
              self.board[36] = self.__index.flipDisk(self.board[36],2);
  def putAt16(self, color):
    self.board[2],fliped = self.__index.flipLine(self.board[2],0,color)
    if fliped[1] >= 1:
      self.board[9] = self.__index.flipDisk(self.board[9],2)
      self.board[17] = self.__index.flipDisk(self.board[17],2)
      self.board[33] = self.__index.flipDisk(self.board[33],1)
      if fliped[1] >= 2:
        self.board[10] = self.__index.flipDisk(self.board[10],2)
        self.board[18] = self.__index.flipDisk(self.board[18],2)
        self.board[32] = self.__index.flipDisk(self.board[32],2)
        if fliped[1] >= 3:
          self.board[11] = self.__index.flipDisk(self.board[11],2)
          self.board[19] = self.__index.flipDisk(self.board[19],2)
          self.board[31] = self.__index.flipDisk(self.board[31],2)
          if fliped[1] >= 4:
            self.board[12] = self.__index.flipDisk(self.board[12],2)
            self.board[20] = self.__index.flipDisk(self.board[20],2)
            self.board[30] = self.__index.flipDisk(self.board[30],2)
            if fliped[1] >= 5:
              self.board[13] = self.__index.flipDisk(self.board[13],2)
              self.board[21] = self.__index.flipDisk(self.board[21],2)
              self.board[29] = self.__index.flipDisk(self.board[29],2)
              if fliped[1] >= 6:
                self.board[14] = self.__index.flipDisk(self.board[14],2)
                self.board[22] = self.__index.flipDisk(self.board[22],1)
                self.board[28] = self.__index.flipDisk(self.board[28],2)
    self.board[8],fliped = self.__index.flipLine(self.board[8],2,color)
    if fliped[0] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],0);
      self.board[33] = self.__index.flipDisk(self.board[33],0);
    if fliped[1] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],0);
      self.board[17] = self.__index.flipDisk(self.board[17],3);
      self.board[35] = self.__index.flipDisk(self.board[35],0);
      if fliped[1] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],0);
        self.board[18] = self.__index.flipDisk(self.board[18],4);
        self.board[36] = self.__index.flipDisk(self.board[36],0);
        if fliped[1] >= 3:
          self.board[5] = self.__index.flipDisk(self.board[5],0);
          self.board[19] = self.__index.flipDisk(self.board[19],5);
          self.board[37] = self.__index.flipDisk(self.board[37],0);
          if fliped[1] >= 4:
            self.board[6] = self.__index.flipDisk(self.board[6],0);
            self.board[20] = self.__index.flipDisk(self.board[20],6);
    self.board[16],fliped = self.__index.flipLine(self.board[16],2,color);
    if fliped[0] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],1);
      self.board[9] = self.__index.flipDisk(self.board[9],1);
      self.board[32] = self.__index.flipDisk(self.board[32],1);
    self.board[34],fliped = self.__index.flipLine(self.board[34],0,color);
    if fliped[1] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],1);
      self.board[9] = self.__index.flipDisk(self.board[9],3);
      self.board[18] = self.__index.flipDisk(self.board[18],3);
      if fliped[1] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],2);
        self.board[10] = self.__index.flipDisk(self.board[10],4);
        self.board[20] = self.__index.flipDisk(self.board[20],4);
        if fliped[1] >= 3:
          self.board[5] = self.__index.flipDisk(self.board[5],3);
          self.board[11] = self.__index.flipDisk(self.board[11],5);
          self.board[22] = self.__index.flipDisk(self.board[22],4);
          if fliped[1] >= 4:
            self.board[6] = self.__index.flipDisk(self.board[6],4);
            self.board[12] = self.__index.flipDisk(self.board[12],6);
            self.board[24] = self.__index.flipDisk(self.board[24],3);
  def putAt17(self, color):
    self.board[2],fliped = self.__index.flipLine(self.board[2],1,color)
    if fliped[1] >= 1:
      self.board[10] = self.__index.flipDisk(self.board[10],2)
      self.board[18] = self.__index.flipDisk(self.board[18],2)
      self.board[32] = self.__index.flipDisk(self.board[32],2)
      if fliped[1] >= 2:
        self.board[11] = self.__index.flipDisk(self.board[11],2)
        self.board[19] = self.__index.flipDisk(self.board[19],2)
        self.board[31] = self.__index.flipDisk(self.board[31],2)
        if fliped[1] >= 3:
          self.board[12] = self.__index.flipDisk(self.board[12],2)
          self.board[20] = self.__index.flipDisk(self.board[20],2)
          self.board[30] = self.__index.flipDisk(self.board[30],2)
          if fliped[1] >= 4:
            self.board[13] = self.__index.flipDisk(self.board[13],2)
            self.board[21] = self.__index.flipDisk(self.board[21],2)
            self.board[29] = self.__index.flipDisk(self.board[29],2)
            if fliped[1] >= 5:
              self.board[14] = self.__index.flipDisk(self.board[14],2)
              self.board[22] = self.__index.flipDisk(self.board[22],1)
              self.board[28] = self.__index.flipDisk(self.board[28],2)
    self.board[9],fliped = self.__index.flipLine(self.board[9],2,color)
    if fliped[0] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],1);
      self.board[16] = self.__index.flipDisk(self.board[16],1);
      self.board[32] = self.__index.flipDisk(self.board[32],1);
    if fliped[1] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],1);
      self.board[18] = self.__index.flipDisk(self.board[18],3);
      self.board[34] = self.__index.flipDisk(self.board[34],1);
      if fliped[1] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],1);
        self.board[19] = self.__index.flipDisk(self.board[19],4);
        self.board[35] = self.__index.flipDisk(self.board[35],1);
        if fliped[1] >= 3:
          self.board[5] = self.__index.flipDisk(self.board[5],1);
          self.board[20] = self.__index.flipDisk(self.board[20],5);
          self.board[36] = self.__index.flipDisk(self.board[36],1);
          if fliped[1] >= 4:
            self.board[6] = self.__index.flipDisk(self.board[6],1);
            self.board[21] = self.__index.flipDisk(self.board[21],6);
            self.board[37] = self.__index.flipDisk(self.board[37],1);
    self.board[17],fliped = self.__index.flipLine(self.board[17],2,color);
    if fliped[0] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],2);
      self.board[10] = self.__index.flipDisk(self.board[10],1);
      self.board[31] = self.__index.flipDisk(self.board[31],1);
    self.board[33],fliped = self.__index.flipLine(self.board[33],1,color);
    if fliped[1] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],2);
      self.board[10] = self.__index.flipDisk(self.board[10],3);
      self.board[19] = self.__index.flipDisk(self.board[19],3);
      if fliped[1] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],3);
        self.board[11] = self.__index.flipDisk(self.board[11],4);
        self.board[21] = self.__index.flipDisk(self.board[21],4);
        if fliped[1] >= 3:
          self.board[5] = self.__index.flipDisk(self.board[5],4);
          self.board[12] = self.__index.flipDisk(self.board[12],5);
          self.board[23] = self.__index.flipDisk(self.board[23],3);
          if fliped[1] >= 4:
            self.board[6] = self.__index.flipDisk(self.board[6],5);
            self.board[13] = self.__index.flipDisk(self.board[13],6);
            self.board[25] = self.__index.flipDisk(self.board[25],2);
  def putAt18(self, color):
    self.board[2],fliped = self.__index.flipLine(self.board[2],2,color)
    if fliped[0] >= 1:
      self.board[9] = self.__index.flipDisk(self.board[9],2)
      self.board[17] = self.__index.flipDisk(self.board[17],2)
      self.board[33] = self.__index.flipDisk(self.board[33],1)
    if fliped[1] >= 1:
      self.board[11] = self.__index.flipDisk(self.board[11],2)
      self.board[19] = self.__index.flipDisk(self.board[19],2)
      self.board[31] = self.__index.flipDisk(self.board[31],2)
      if fliped[1] >= 2:
        self.board[12] = self.__index.flipDisk(self.board[12],2)
        self.board[20] = self.__index.flipDisk(self.board[20],2)
        self.board[30] = self.__index.flipDisk(self.board[30],2)
        if fliped[1] >= 3:
          self.board[13] = self.__index.flipDisk(self.board[13],2)
          self.board[21] = self.__index.flipDisk(self.board[21],2)
          self.board[29] = self.__index.flipDisk(self.board[29],2)
          if fliped[1] >= 4:
            self.board[14] = self.__index.flipDisk(self.board[14],2)
            self.board[22] = self.__index.flipDisk(self.board[22],1)
            self.board[28] = self.__index.flipDisk(self.board[28],2)
    self.board[10],fliped = self.__index.flipLine(self.board[10],2,color)
    if fliped[0] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],2);
      self.board[17] = self.__index.flipDisk(self.board[17],1);
      self.board[31] = self.__index.flipDisk(self.board[31],1);
    if fliped[1] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],2);
      self.board[19] = self.__index.flipDisk(self.board[19],3);
      self.board[33] = self.__index.flipDisk(self.board[33],2);
      if fliped[1] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],2);
        self.board[20] = self.__index.flipDisk(self.board[20],4);
        self.board[34] = self.__index.flipDisk(self.board[34],2);
        if fliped[1] >= 3:
          self.board[5] = self.__index.flipDisk(self.board[5],2);
          self.board[21] = self.__index.flipDisk(self.board[21],5);
          self.board[35] = self.__index.flipDisk(self.board[35],2);
          if fliped[1] >= 4:
            self.board[6] = self.__index.flipDisk(self.board[6],2);
            self.board[22] = self.__index.flipDisk(self.board[22],5);
            self.board[36] = self.__index.flipDisk(self.board[36],2);
    self.board[18],fliped = self.__index.flipLine(self.board[18],2,color);
    if fliped[0] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],3);
      self.board[11] = self.__index.flipDisk(self.board[11],1);
      self.board[30] = self.__index.flipDisk(self.board[30],1);
    if fliped[1] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],1);
      self.board[9] = self.__index.flipDisk(self.board[9],3);
      self.board[34] = self.__index.flipDisk(self.board[34],1);
    self.board[32],fliped = self.__index.flipLine(self.board[32],2,color);
    if fliped[0] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],1);
      self.board[9] = self.__index.flipDisk(self.board[9],1);
      self.board[16] = self.__index.flipDisk(self.board[16],1);
    if fliped[1] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],3);
      self.board[11] = self.__index.flipDisk(self.board[11],3);
      self.board[20] = self.__index.flipDisk(self.board[20],3);
      if fliped[1] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],4);
        self.board[12] = self.__index.flipDisk(self.board[12],4);
        self.board[22] = self.__index.flipDisk(self.board[22],3);
        if fliped[1] >= 3:
          self.board[5] = self.__index.flipDisk(self.board[5],5);
          self.board[13] = self.__index.flipDisk(self.board[13],5);
          self.board[24] = self.__index.flipDisk(self.board[24],2);
          if fliped[1] >= 4:
            self.board[6] = self.__index.flipDisk(self.board[6],6);
            self.board[14] = self.__index.flipDisk(self.board[14],6);
            self.board[26] = self.__index.flipDisk(self.board[26],1);
  def putAt19(self, color):
    self.board[2],fliped = self.__index.flipLine(self.board[2],3,color)
    if fliped[0] >= 1:
      self.board[10] = self.__index.flipDisk(self.board[10],2)
      self.board[18] = self.__index.flipDisk(self.board[18],2)
      self.board[32] = self.__index.flipDisk(self.board[32],2)
      if fliped[0] >= 2:
        self.board[9] = self.__index.flipDisk(self.board[9],2)
        self.board[17] = self.__index.flipDisk(self.board[17],2)
        self.board[33] = self.__index.flipDisk(self.board[33],1)
    if fliped[1] >= 1:
      self.board[12] = self.__index.flipDisk(self.board[12],2)
      self.board[20] = self.__index.flipDisk(self.board[20],2)
      self.board[30] = self.__index.flipDisk(self.board[30],2)
      if fliped[1] >= 2:
        self.board[13] = self.__index.flipDisk(self.board[13],2)
        self.board[21] = self.__index.flipDisk(self.board[21],2)
        self.board[29] = self.__index.flipDisk(self.board[29],2)
        if fliped[1] >= 3:
          self.board[14] = self.__index.flipDisk(self.board[14],2)
          self.board[22] = self.__index.flipDisk(self.board[22],1)
          self.board[28] = self.__index.flipDisk(self.board[28],2)
    self.board[11],fliped = self.__index.flipLine(self.board[11],2,color)
    if fliped[0] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],3);
      self.board[18] = self.__index.flipDisk(self.board[18],1);
      self.board[30] = self.__index.flipDisk(self.board[30],1);
    if fliped[1] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],3);
      self.board[20] = self.__index.flipDisk(self.board[20],3);
      self.board[32] = self.__index.flipDisk(self.board[32],3);
      if fliped[1] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],3);
        self.board[21] = self.__index.flipDisk(self.board[21],4);
        self.board[33] = self.__index.flipDisk(self.board[33],3);
        if fliped[1] >= 3:
          self.board[5] = self.__index.flipDisk(self.board[5],3);
          self.board[22] = self.__index.flipDisk(self.board[22],4);
          self.board[34] = self.__index.flipDisk(self.board[34],3);
          if fliped[1] >= 4:
            self.board[6] = self.__index.flipDisk(self.board[6],3);
            self.board[23] = self.__index.flipDisk(self.board[23],4);
            self.board[35] = self.__index.flipDisk(self.board[35],3);
    self.board[19],fliped = self.__index.flipLine(self.board[19],2,color);
    if fliped[0] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],4);
      self.board[12] = self.__index.flipDisk(self.board[12],1);
      self.board[29] = self.__index.flipDisk(self.board[29],1);
    if fliped[1] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],2);
      self.board[10] = self.__index.flipDisk(self.board[10],3);
      self.board[33] = self.__index.flipDisk(self.board[33],2);
      if fliped[1] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],1);
        self.board[9] = self.__index.flipDisk(self.board[9],4);
        self.board[35] = self.__index.flipDisk(self.board[35],1);
    self.board[31],fliped = self.__index.flipLine(self.board[31],2,color);
    if fliped[0] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],2);
      self.board[10] = self.__index.flipDisk(self.board[10],1);
      self.board[17] = self.__index.flipDisk(self.board[17],1);
    if fliped[1] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],4);
      self.board[12] = self.__index.flipDisk(self.board[12],3);
      self.board[21] = self.__index.flipDisk(self.board[21],3);
      if fliped[1] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],5);
        self.board[13] = self.__index.flipDisk(self.board[13],4);
        self.board[23] = self.__index.flipDisk(self.board[23],2);
        if fliped[1] >= 3:
          self.board[5] = self.__index.flipDisk(self.board[5],6);
          self.board[14] = self.__index.flipDisk(self.board[14],5);
          self.board[25] = self.__index.flipDisk(self.board[25],1);
  def putAt20(self, color):
    self.board[2],fliped = self.__index.flipLine(self.board[2],4,color)
    if fliped[0] >= 1:
      self.board[11] = self.__index.flipDisk(self.board[11],2)
      self.board[19] = self.__index.flipDisk(self.board[19],2)
      self.board[31] = self.__index.flipDisk(self.board[31],2)
      if fliped[0] >= 2:
        self.board[10] = self.__index.flipDisk(self.board[10],2)
        self.board[18] = self.__index.flipDisk(self.board[18],2)
        self.board[32] = self.__index.flipDisk(self.board[32],2)
        if fliped[0] >= 3:
          self.board[9] = self.__index.flipDisk(self.board[9],2)
          self.board[17] = self.__index.flipDisk(self.board[17],2)
          self.board[33] = self.__index.flipDisk(self.board[33],1)
    if fliped[1] >= 1:
      self.board[13] = self.__index.flipDisk(self.board[13],2)
      self.board[21] = self.__index.flipDisk(self.board[21],2)
      self.board[29] = self.__index.flipDisk(self.board[29],2)
      if fliped[1] >= 2:
        self.board[14] = self.__index.flipDisk(self.board[14],2)
        self.board[22] = self.__index.flipDisk(self.board[22],1)
        self.board[28] = self.__index.flipDisk(self.board[28],2)
    self.board[12],fliped = self.__index.flipLine(self.board[12],2,color)
    if fliped[0] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],4);
      self.board[19] = self.__index.flipDisk(self.board[19],1);
      self.board[29] = self.__index.flipDisk(self.board[29],1);
    if fliped[1] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],4);
      self.board[21] = self.__index.flipDisk(self.board[21],3);
      self.board[31] = self.__index.flipDisk(self.board[31],3);
      if fliped[1] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],4);
        self.board[22] = self.__index.flipDisk(self.board[22],3);
        self.board[32] = self.__index.flipDisk(self.board[32],4);
        if fliped[1] >= 3:
          self.board[5] = self.__index.flipDisk(self.board[5],4);
          self.board[23] = self.__index.flipDisk(self.board[23],3);
          self.board[33] = self.__index.flipDisk(self.board[33],4);
          if fliped[1] >= 4:
            self.board[6] = self.__index.flipDisk(self.board[6],4);
            self.board[24] = self.__index.flipDisk(self.board[24],3);
            self.board[34] = self.__index.flipDisk(self.board[34],4);
    self.board[20],fliped = self.__index.flipLine(self.board[20],2,color);
    if fliped[0] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],5);
      self.board[13] = self.__index.flipDisk(self.board[13],1);
      self.board[28] = self.__index.flipDisk(self.board[28],1);
    if fliped[1] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],3);
      self.board[11] = self.__index.flipDisk(self.board[11],3);
      self.board[32] = self.__index.flipDisk(self.board[32],3);
      if fliped[1] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],2);
        self.board[10] = self.__index.flipDisk(self.board[10],4);
        self.board[34] = self.__index.flipDisk(self.board[34],2);
        if fliped[1] >= 3:
          self.board[5] = self.__index.flipDisk(self.board[5],1);
          self.board[9] = self.__index.flipDisk(self.board[9],5);
          self.board[36] = self.__index.flipDisk(self.board[36],1);
    self.board[30],fliped = self.__index.flipLine(self.board[30],2,color);
    if fliped[0] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],3);
      self.board[11] = self.__index.flipDisk(self.board[11],1);
      self.board[18] = self.__index.flipDisk(self.board[18],1);
    if fliped[1] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],5);
      self.board[13] = self.__index.flipDisk(self.board[13],3);
      self.board[22] = self.__index.flipDisk(self.board[22],2);
      if fliped[1] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],6);
        self.board[14] = self.__index.flipDisk(self.board[14],4);
        self.board[24] = self.__index.flipDisk(self.board[24],1);
  def putAt21(self, color):
    self.board[2],fliped = self.__index.flipLine(self.board[2],5,color)
    if fliped[0] >= 1:
      self.board[12] = self.__index.flipDisk(self.board[12],2)
      self.board[20] = self.__index.flipDisk(self.board[20],2)
      self.board[30] = self.__index.flipDisk(self.board[30],2)
      if fliped[0] >= 2:
        self.board[11] = self.__index.flipDisk(self.board[11],2)
        self.board[19] = self.__index.flipDisk(self.board[19],2)
        self.board[31] = self.__index.flipDisk(self.board[31],2)
        if fliped[0] >= 3:
          self.board[10] = self.__index.flipDisk(self.board[10],2)
          self.board[18] = self.__index.flipDisk(self.board[18],2)
          self.board[32] = self.__index.flipDisk(self.board[32],2)
          if fliped[0] >= 4:
            self.board[9] = self.__index.flipDisk(self.board[9],2)
            self.board[17] = self.__index.flipDisk(self.board[17],2)
            self.board[33] = self.__index.flipDisk(self.board[33],1)
    if fliped[1] >= 1:
      self.board[14] = self.__index.flipDisk(self.board[14],2)
      self.board[22] = self.__index.flipDisk(self.board[22],1)
      self.board[28] = self.__index.flipDisk(self.board[28],2)
    self.board[13],fliped = self.__index.flipLine(self.board[13],2,color)
    if fliped[0] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],5);
      self.board[20] = self.__index.flipDisk(self.board[20],1);
      self.board[28] = self.__index.flipDisk(self.board[28],1);
    if fliped[1] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],5);
      self.board[22] = self.__index.flipDisk(self.board[22],2);
      self.board[30] = self.__index.flipDisk(self.board[30],3);
      if fliped[1] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],5);
        self.board[23] = self.__index.flipDisk(self.board[23],2);
        self.board[31] = self.__index.flipDisk(self.board[31],4);
        if fliped[1] >= 3:
          self.board[5] = self.__index.flipDisk(self.board[5],5);
          self.board[24] = self.__index.flipDisk(self.board[24],2);
          self.board[32] = self.__index.flipDisk(self.board[32],5);
          if fliped[1] >= 4:
            self.board[6] = self.__index.flipDisk(self.board[6],5);
            self.board[25] = self.__index.flipDisk(self.board[25],2);
            self.board[33] = self.__index.flipDisk(self.board[33],5);
    self.board[21],fliped = self.__index.flipLine(self.board[21],2,color);
    if fliped[0] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],6);
      self.board[14] = self.__index.flipDisk(self.board[14],1);
      self.board[27] = self.__index.flipDisk(self.board[27],1);
    if fliped[1] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],4);
      self.board[12] = self.__index.flipDisk(self.board[12],3);
      self.board[31] = self.__index.flipDisk(self.board[31],3);
      if fliped[1] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],3);
        self.board[11] = self.__index.flipDisk(self.board[11],4);
        self.board[33] = self.__index.flipDisk(self.board[33],3);
        if fliped[1] >= 3:
          self.board[5] = self.__index.flipDisk(self.board[5],2);
          self.board[10] = self.__index.flipDisk(self.board[10],5);
          self.board[35] = self.__index.flipDisk(self.board[35],2);
          if fliped[1] >= 4:
            self.board[6] = self.__index.flipDisk(self.board[6],1);
            self.board[9] = self.__index.flipDisk(self.board[9],6);
            self.board[37] = self.__index.flipDisk(self.board[37],1);
    self.board[29],fliped = self.__index.flipLine(self.board[29],2,color);
    if fliped[0] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],4);
      self.board[12] = self.__index.flipDisk(self.board[12],1);
      self.board[19] = self.__index.flipDisk(self.board[19],1);
    if fliped[1] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],6);
      self.board[14] = self.__index.flipDisk(self.board[14],3);
      self.board[23] = self.__index.flipDisk(self.board[23],1);
  def putAt22(self, color):
    self.board[2],fliped = self.__index.flipLine(self.board[2],6,color)
    if fliped[0] >= 1:
      self.board[13] = self.__index.flipDisk(self.board[13],2)
      self.board[21] = self.__index.flipDisk(self.board[21],2)
      self.board[29] = self.__index.flipDisk(self.board[29],2)
      if fliped[0] >= 2:
        self.board[12] = self.__index.flipDisk(self.board[12],2)
        self.board[20] = self.__index.flipDisk(self.board[20],2)
        self.board[30] = self.__index.flipDisk(self.board[30],2)
        if fliped[0] >= 3:
          self.board[11] = self.__index.flipDisk(self.board[11],2)
          self.board[19] = self.__index.flipDisk(self.board[19],2)
          self.board[31] = self.__index.flipDisk(self.board[31],2)
          if fliped[0] >= 4:
            self.board[10] = self.__index.flipDisk(self.board[10],2)
            self.board[18] = self.__index.flipDisk(self.board[18],2)
            self.board[32] = self.__index.flipDisk(self.board[32],2)
            if fliped[0] >= 5:
              self.board[9] = self.__index.flipDisk(self.board[9],2)
              self.board[17] = self.__index.flipDisk(self.board[17],2)
              self.board[33] = self.__index.flipDisk(self.board[33],1)
    self.board[14],fliped = self.__index.flipLine(self.board[14],2,color)
    if fliped[0] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],6);
      self.board[21] = self.__index.flipDisk(self.board[21],1);
      self.board[27] = self.__index.flipDisk(self.board[27],1);
    if fliped[1] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],6);
      self.board[23] = self.__index.flipDisk(self.board[23],1);
      self.board[29] = self.__index.flipDisk(self.board[29],3);
      if fliped[1] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],6);
        self.board[24] = self.__index.flipDisk(self.board[24],1);
        self.board[30] = self.__index.flipDisk(self.board[30],4);
        if fliped[1] >= 3:
          self.board[5] = self.__index.flipDisk(self.board[5],6);
          self.board[25] = self.__index.flipDisk(self.board[25],1);
          self.board[31] = self.__index.flipDisk(self.board[31],5);
          if fliped[1] >= 4:
            self.board[6] = self.__index.flipDisk(self.board[6],6);
            self.board[26] = self.__index.flipDisk(self.board[26],1);
            self.board[32] = self.__index.flipDisk(self.board[32],6);
    self.board[22],fliped = self.__index.flipLine(self.board[22],1,color);
    if fliped[1] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],5);
      self.board[13] = self.__index.flipDisk(self.board[13],3);
      self.board[30] = self.__index.flipDisk(self.board[30],3);
      if fliped[1] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],4);
        self.board[12] = self.__index.flipDisk(self.board[12],4);
        self.board[32] = self.__index.flipDisk(self.board[32],4);
        if fliped[1] >= 3:
          self.board[5] = self.__index.flipDisk(self.board[5],3);
          self.board[11] = self.__index.flipDisk(self.board[11],5);
          self.board[34] = self.__index.flipDisk(self.board[34],3);
          if fliped[1] >= 4:
            self.board[6] = self.__index.flipDisk(self.board[6],2);
            self.board[10] = self.__index.flipDisk(self.board[10],6);
            self.board[36] = self.__index.flipDisk(self.board[36],2);
    self.board[28],fliped = self.__index.flipLine(self.board[28],2,color);
    if fliped[0] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],5);
      self.board[13] = self.__index.flipDisk(self.board[13],1);
      self.board[20] = self.__index.flipDisk(self.board[20],1);
  def putAt23(self, color):
    self.board[2],fliped = self.__index.flipLine(self.board[2],7,color)
    if fliped[0] >= 1:
      self.board[14] = self.__index.flipDisk(self.board[14],2)
      self.board[22] = self.__index.flipDisk(self.board[22],1)
      self.board[28] = self.__index.flipDisk(self.board[28],2)
      if fliped[0] >= 2:
        self.board[13] = self.__index.flipDisk(self.board[13],2)
        self.board[21] = self.__index.flipDisk(self.board[21],2)
        self.board[29] = self.__index.flipDisk(self.board[29],2)
        if fliped[0] >= 3:
          self.board[12] = self.__index.flipDisk(self.board[12],2)
          self.board[20] = self.__index.flipDisk(self.board[20],2)
          self.board[30] = self.__index.flipDisk(self.board[30],2)
          if fliped[0] >= 4:
            self.board[11] = self.__index.flipDisk(self.board[11],2)
            self.board[19] = self.__index.flipDisk(self.board[19],2)
            self.board[31] = self.__index.flipDisk(self.board[31],2)
            if fliped[0] >= 5:
              self.board[10] = self.__index.flipDisk(self.board[10],2)
              self.board[18] = self.__index.flipDisk(self.board[18],2)
              self.board[32] = self.__index.flipDisk(self.board[32],2)
              if fliped[0] >= 6:
                self.board[9] = self.__index.flipDisk(self.board[9],2)
                self.board[17] = self.__index.flipDisk(self.board[17],2)
                self.board[33] = self.__index.flipDisk(self.board[33],1)
    self.board[15],fliped = self.__index.flipLine(self.board[15],2,color)
    if fliped[0] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],7);
      self.board[22] = self.__index.flipDisk(self.board[22],0);
    if fliped[1] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],7);
      self.board[24] = self.__index.flipDisk(self.board[24],0);
      self.board[28] = self.__index.flipDisk(self.board[28],3);
      if fliped[1] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],7);
        self.board[25] = self.__index.flipDisk(self.board[25],0);
        self.board[29] = self.__index.flipDisk(self.board[29],4);
        if fliped[1] >= 3:
          self.board[5] = self.__index.flipDisk(self.board[5],7);
          self.board[26] = self.__index.flipDisk(self.board[26],0);
          self.board[30] = self.__index.flipDisk(self.board[30],5);
          if fliped[1] >= 4:
            self.board[6] = self.__index.flipDisk(self.board[6],7);
            self.board[31] = self.__index.flipDisk(self.board[31],6);
    self.board[23],fliped = self.__index.flipLine(self.board[23],0,color);
    if fliped[1] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],6);
      self.board[14] = self.__index.flipDisk(self.board[14],3);
      self.board[29] = self.__index.flipDisk(self.board[29],3);
      if fliped[1] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],5);
        self.board[13] = self.__index.flipDisk(self.board[13],4);
        self.board[31] = self.__index.flipDisk(self.board[31],4);
        if fliped[1] >= 3:
          self.board[5] = self.__index.flipDisk(self.board[5],4);
          self.board[12] = self.__index.flipDisk(self.board[12],5);
          self.board[33] = self.__index.flipDisk(self.board[33],4);
          if fliped[1] >= 4:
            self.board[6] = self.__index.flipDisk(self.board[6],3);
            self.board[11] = self.__index.flipDisk(self.board[11],6);
            self.board[35] = self.__index.flipDisk(self.board[35],3);
    self.board[27],fliped = self.__index.flipLine(self.board[27],2,color);
    if fliped[0] >= 1:
      self.board[1] = self.__index.flipDisk(self.board[1],6);
      self.board[14] = self.__index.flipDisk(self.board[14],1);
      self.board[21] = self.__index.flipDisk(self.board[21],1);
  def putAt24(self, color):
    self.board[3],fliped = self.__index.flipLine(self.board[3],0,color)
    if fliped[1] >= 1:
      self.board[9] = self.__index.flipDisk(self.board[9],3)
      self.board[18] = self.__index.flipDisk(self.board[18],3)
      self.board[34] = self.__index.flipDisk(self.board[34],1)
      if fliped[1] >= 2:
        self.board[10] = self.__index.flipDisk(self.board[10],3)
        self.board[19] = self.__index.flipDisk(self.board[19],3)
        self.board[33] = self.__index.flipDisk(self.board[33],2)
        if fliped[1] >= 3:
          self.board[11] = self.__index.flipDisk(self.board[11],3)
          self.board[20] = self.__index.flipDisk(self.board[20],3)
          self.board[32] = self.__index.flipDisk(self.board[32],3)
          if fliped[1] >= 4:
            self.board[12] = self.__index.flipDisk(self.board[12],3)
            self.board[21] = self.__index.flipDisk(self.board[21],3)
            self.board[31] = self.__index.flipDisk(self.board[31],3)
            if fliped[1] >= 5:
              self.board[13] = self.__index.flipDisk(self.board[13],3)
              self.board[22] = self.__index.flipDisk(self.board[22],2)
              self.board[30] = self.__index.flipDisk(self.board[30],3)
              if fliped[1] >= 6:
                self.board[14] = self.__index.flipDisk(self.board[14],3)
                self.board[23] = self.__index.flipDisk(self.board[23],1)
                self.board[29] = self.__index.flipDisk(self.board[29],3)
    self.board[8],fliped = self.__index.flipLine(self.board[8],3,color)
    if fliped[0] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],0);
      self.board[16] = self.__index.flipDisk(self.board[16],2);
      self.board[34] = self.__index.flipDisk(self.board[34],0);
      if fliped[0] >= 2:
        self.board[1] = self.__index.flipDisk(self.board[1],0);
        self.board[33] = self.__index.flipDisk(self.board[33],0);
    if fliped[1] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],0);
      self.board[18] = self.__index.flipDisk(self.board[18],4);
      self.board[36] = self.__index.flipDisk(self.board[36],0);
      if fliped[1] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],0);
        self.board[19] = self.__index.flipDisk(self.board[19],5);
        self.board[37] = self.__index.flipDisk(self.board[37],0);
        if fliped[1] >= 3:
          self.board[6] = self.__index.flipDisk(self.board[6],0);
          self.board[20] = self.__index.flipDisk(self.board[20],6);
    self.board[17],fliped = self.__index.flipLine(self.board[17],3,color);
    if fliped[0] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],1);
      self.board[9] = self.__index.flipDisk(self.board[9],2);
      self.board[33] = self.__index.flipDisk(self.board[33],1);
      if fliped[0] >= 2:
        self.board[1] = self.__index.flipDisk(self.board[1],2);
        self.board[10] = self.__index.flipDisk(self.board[10],1);
        self.board[31] = self.__index.flipDisk(self.board[31],1);
    self.board[35],fliped = self.__index.flipLine(self.board[35],0,color);
    if fliped[1] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],1);
      self.board[9] = self.__index.flipDisk(self.board[9],4);
      self.board[19] = self.__index.flipDisk(self.board[19],4);
      if fliped[1] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],2);
        self.board[10] = self.__index.flipDisk(self.board[10],5);
        self.board[21] = self.__index.flipDisk(self.board[21],5);
        if fliped[1] >= 3:
          self.board[6] = self.__index.flipDisk(self.board[6],3);
          self.board[11] = self.__index.flipDisk(self.board[11],6);
          self.board[23] = self.__index.flipDisk(self.board[23],4);
  def putAt25(self, color):
    self.board[3],fliped = self.__index.flipLine(self.board[3],1,color)
    if fliped[1] >= 1:
      self.board[10] = self.__index.flipDisk(self.board[10],3)
      self.board[19] = self.__index.flipDisk(self.board[19],3)
      self.board[33] = self.__index.flipDisk(self.board[33],2)
      if fliped[1] >= 2:
        self.board[11] = self.__index.flipDisk(self.board[11],3)
        self.board[20] = self.__index.flipDisk(self.board[20],3)
        self.board[32] = self.__index.flipDisk(self.board[32],3)
        if fliped[1] >= 3:
          self.board[12] = self.__index.flipDisk(self.board[12],3)
          self.board[21] = self.__index.flipDisk(self.board[21],3)
          self.board[31] = self.__index.flipDisk(self.board[31],3)
          if fliped[1] >= 4:
            self.board[13] = self.__index.flipDisk(self.board[13],3)
            self.board[22] = self.__index.flipDisk(self.board[22],2)
            self.board[30] = self.__index.flipDisk(self.board[30],3)
            if fliped[1] >= 5:
              self.board[14] = self.__index.flipDisk(self.board[14],3)
              self.board[23] = self.__index.flipDisk(self.board[23],1)
              self.board[29] = self.__index.flipDisk(self.board[29],3)
    self.board[9],fliped = self.__index.flipLine(self.board[9],3,color)
    if fliped[0] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],1);
      self.board[17] = self.__index.flipDisk(self.board[17],2);
      self.board[33] = self.__index.flipDisk(self.board[33],1);
      if fliped[0] >= 2:
        self.board[1] = self.__index.flipDisk(self.board[1],1);
        self.board[16] = self.__index.flipDisk(self.board[16],1);
        self.board[32] = self.__index.flipDisk(self.board[32],1);
    if fliped[1] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],1);
      self.board[19] = self.__index.flipDisk(self.board[19],4);
      self.board[35] = self.__index.flipDisk(self.board[35],1);
      if fliped[1] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],1);
        self.board[20] = self.__index.flipDisk(self.board[20],5);
        self.board[36] = self.__index.flipDisk(self.board[36],1);
        if fliped[1] >= 3:
          self.board[6] = self.__index.flipDisk(self.board[6],1);
          self.board[21] = self.__index.flipDisk(self.board[21],6);
          self.board[37] = self.__index.flipDisk(self.board[37],1);
    self.board[18],fliped = self.__index.flipLine(self.board[18],3,color);
    if fliped[0] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],2);
      self.board[10] = self.__index.flipDisk(self.board[10],2);
      self.board[32] = self.__index.flipDisk(self.board[32],2);
      if fliped[0] >= 2:
        self.board[1] = self.__index.flipDisk(self.board[1],3);
        self.board[11] = self.__index.flipDisk(self.board[11],1);
        self.board[30] = self.__index.flipDisk(self.board[30],1);
    self.board[34],fliped = self.__index.flipLine(self.board[34],1,color);
    if fliped[1] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],2);
      self.board[10] = self.__index.flipDisk(self.board[10],4);
      self.board[20] = self.__index.flipDisk(self.board[20],4);
      if fliped[1] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],3);
        self.board[11] = self.__index.flipDisk(self.board[11],5);
        self.board[22] = self.__index.flipDisk(self.board[22],4);
        if fliped[1] >= 3:
          self.board[6] = self.__index.flipDisk(self.board[6],4);
          self.board[12] = self.__index.flipDisk(self.board[12],6);
          self.board[24] = self.__index.flipDisk(self.board[24],3);
  def putAt26(self, color):
    self.board[3],fliped = self.__index.flipLine(self.board[3],2,color)
    if fliped[0] >= 1:
      self.board[9] = self.__index.flipDisk(self.board[9],3)
      self.board[18] = self.__index.flipDisk(self.board[18],3)
      self.board[34] = self.__index.flipDisk(self.board[34],1)
    if fliped[1] >= 1:
      self.board[11] = self.__index.flipDisk(self.board[11],3)
      self.board[20] = self.__index.flipDisk(self.board[20],3)
      self.board[32] = self.__index.flipDisk(self.board[32],3)
      if fliped[1] >= 2:
        self.board[12] = self.__index.flipDisk(self.board[12],3)
        self.board[21] = self.__index.flipDisk(self.board[21],3)
        self.board[31] = self.__index.flipDisk(self.board[31],3)
        if fliped[1] >= 3:
          self.board[13] = self.__index.flipDisk(self.board[13],3)
          self.board[22] = self.__index.flipDisk(self.board[22],2)
          self.board[30] = self.__index.flipDisk(self.board[30],3)
          if fliped[1] >= 4:
            self.board[14] = self.__index.flipDisk(self.board[14],3)
            self.board[23] = self.__index.flipDisk(self.board[23],1)
            self.board[29] = self.__index.flipDisk(self.board[29],3)
    self.board[10],fliped = self.__index.flipLine(self.board[10],3,color)
    if fliped[0] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],2);
      self.board[18] = self.__index.flipDisk(self.board[18],2);
      self.board[32] = self.__index.flipDisk(self.board[32],2);
      if fliped[0] >= 2:
        self.board[1] = self.__index.flipDisk(self.board[1],2);
        self.board[17] = self.__index.flipDisk(self.board[17],1);
        self.board[31] = self.__index.flipDisk(self.board[31],1);
    if fliped[1] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],2);
      self.board[20] = self.__index.flipDisk(self.board[20],4);
      self.board[34] = self.__index.flipDisk(self.board[34],2);
      if fliped[1] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],2);
        self.board[21] = self.__index.flipDisk(self.board[21],5);
        self.board[35] = self.__index.flipDisk(self.board[35],2);
        if fliped[1] >= 3:
          self.board[6] = self.__index.flipDisk(self.board[6],2);
          self.board[22] = self.__index.flipDisk(self.board[22],5);
          self.board[36] = self.__index.flipDisk(self.board[36],2);
    self.board[19],fliped = self.__index.flipLine(self.board[19],3,color);
    if fliped[0] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],3);
      self.board[11] = self.__index.flipDisk(self.board[11],2);
      self.board[31] = self.__index.flipDisk(self.board[31],2);
      if fliped[0] >= 2:
        self.board[1] = self.__index.flipDisk(self.board[1],4);
        self.board[12] = self.__index.flipDisk(self.board[12],1);
        self.board[29] = self.__index.flipDisk(self.board[29],1);
    if fliped[1] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],1);
      self.board[9] = self.__index.flipDisk(self.board[9],4);
      self.board[35] = self.__index.flipDisk(self.board[35],1);
    self.board[33],fliped = self.__index.flipLine(self.board[33],2,color);
    if fliped[0] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],1);
      self.board[9] = self.__index.flipDisk(self.board[9],2);
      self.board[17] = self.__index.flipDisk(self.board[17],2);
    if fliped[1] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],3);
      self.board[11] = self.__index.flipDisk(self.board[11],4);
      self.board[21] = self.__index.flipDisk(self.board[21],4);
      if fliped[1] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],4);
        self.board[12] = self.__index.flipDisk(self.board[12],5);
        self.board[23] = self.__index.flipDisk(self.board[23],3);
        if fliped[1] >= 3:
          self.board[6] = self.__index.flipDisk(self.board[6],5);
          self.board[13] = self.__index.flipDisk(self.board[13],6);
          self.board[25] = self.__index.flipDisk(self.board[25],2);
  def putAt27(self, color):
    self.board[3],fliped = self.__index.flipLine(self.board[3],3,color)
    if fliped[0] >= 1:
      self.board[10] = self.__index.flipDisk(self.board[10],3)
      self.board[19] = self.__index.flipDisk(self.board[19],3)
      self.board[33] = self.__index.flipDisk(self.board[33],2)
      if fliped[0] >= 2:
        self.board[9] = self.__index.flipDisk(self.board[9],3)
        self.board[18] = self.__index.flipDisk(self.board[18],3)
        self.board[34] = self.__index.flipDisk(self.board[34],1)
    if fliped[1] >= 1:
      self.board[12] = self.__index.flipDisk(self.board[12],3)
      self.board[21] = self.__index.flipDisk(self.board[21],3)
      self.board[31] = self.__index.flipDisk(self.board[31],3)
      if fliped[1] >= 2:
        self.board[13] = self.__index.flipDisk(self.board[13],3)
        self.board[22] = self.__index.flipDisk(self.board[22],2)
        self.board[30] = self.__index.flipDisk(self.board[30],3)
        if fliped[1] >= 3:
          self.board[14] = self.__index.flipDisk(self.board[14],3)
          self.board[23] = self.__index.flipDisk(self.board[23],1)
          self.board[29] = self.__index.flipDisk(self.board[29],3)
    self.board[11],fliped = self.__index.flipLine(self.board[11],3,color)
    if fliped[0] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],3);
      self.board[19] = self.__index.flipDisk(self.board[19],2);
      self.board[31] = self.__index.flipDisk(self.board[31],2);
      if fliped[0] >= 2:
        self.board[1] = self.__index.flipDisk(self.board[1],3);
        self.board[18] = self.__index.flipDisk(self.board[18],1);
        self.board[30] = self.__index.flipDisk(self.board[30],1);
    if fliped[1] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],3);
      self.board[21] = self.__index.flipDisk(self.board[21],4);
      self.board[33] = self.__index.flipDisk(self.board[33],3);
      if fliped[1] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],3);
        self.board[22] = self.__index.flipDisk(self.board[22],4);
        self.board[34] = self.__index.flipDisk(self.board[34],3);
        if fliped[1] >= 3:
          self.board[6] = self.__index.flipDisk(self.board[6],3);
          self.board[23] = self.__index.flipDisk(self.board[23],4);
          self.board[35] = self.__index.flipDisk(self.board[35],3);
    self.board[20],fliped = self.__index.flipLine(self.board[20],3,color);
    if fliped[0] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],4);
      self.board[12] = self.__index.flipDisk(self.board[12],2);
      self.board[30] = self.__index.flipDisk(self.board[30],2);
      if fliped[0] >= 2:
        self.board[1] = self.__index.flipDisk(self.board[1],5);
        self.board[13] = self.__index.flipDisk(self.board[13],1);
        self.board[28] = self.__index.flipDisk(self.board[28],1);
    if fliped[1] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],2);
      self.board[10] = self.__index.flipDisk(self.board[10],4);
      self.board[34] = self.__index.flipDisk(self.board[34],2);
      if fliped[1] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],1);
        self.board[9] = self.__index.flipDisk(self.board[9],5);
        self.board[36] = self.__index.flipDisk(self.board[36],1);
    self.board[32],fliped = self.__index.flipLine(self.board[32],3,color);
    if fliped[0] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],2);
      self.board[10] = self.__index.flipDisk(self.board[10],2);
      self.board[18] = self.__index.flipDisk(self.board[18],2);
      if fliped[0] >= 2:
        self.board[1] = self.__index.flipDisk(self.board[1],1);
        self.board[9] = self.__index.flipDisk(self.board[9],1);
        self.board[16] = self.__index.flipDisk(self.board[16],1);
    if fliped[1] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],4);
      self.board[12] = self.__index.flipDisk(self.board[12],4);
      self.board[22] = self.__index.flipDisk(self.board[22],3);
      if fliped[1] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],5);
        self.board[13] = self.__index.flipDisk(self.board[13],5);
        self.board[24] = self.__index.flipDisk(self.board[24],2);
        if fliped[1] >= 3:
          self.board[6] = self.__index.flipDisk(self.board[6],6);
          self.board[14] = self.__index.flipDisk(self.board[14],6);
          self.board[26] = self.__index.flipDisk(self.board[26],1);
  def putAt28(self, color):
    self.board[3],fliped = self.__index.flipLine(self.board[3],4,color)
    if fliped[0] >= 1:
      self.board[11] = self.__index.flipDisk(self.board[11],3)
      self.board[20] = self.__index.flipDisk(self.board[20],3)
      self.board[32] = self.__index.flipDisk(self.board[32],3)
      if fliped[0] >= 2:
        self.board[10] = self.__index.flipDisk(self.board[10],3)
        self.board[19] = self.__index.flipDisk(self.board[19],3)
        self.board[33] = self.__index.flipDisk(self.board[33],2)
        if fliped[0] >= 3:
          self.board[9] = self.__index.flipDisk(self.board[9],3)
          self.board[18] = self.__index.flipDisk(self.board[18],3)
          self.board[34] = self.__index.flipDisk(self.board[34],1)
    if fliped[1] >= 1:
      self.board[13] = self.__index.flipDisk(self.board[13],3)
      self.board[22] = self.__index.flipDisk(self.board[22],2)
      self.board[30] = self.__index.flipDisk(self.board[30],3)
      if fliped[1] >= 2:
        self.board[14] = self.__index.flipDisk(self.board[14],3)
        self.board[23] = self.__index.flipDisk(self.board[23],1)
        self.board[29] = self.__index.flipDisk(self.board[29],3)
    self.board[12],fliped = self.__index.flipLine(self.board[12],3,color)
    if fliped[0] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],4);
      self.board[20] = self.__index.flipDisk(self.board[20],2);
      self.board[30] = self.__index.flipDisk(self.board[30],2);
      if fliped[0] >= 2:
        self.board[1] = self.__index.flipDisk(self.board[1],4);
        self.board[19] = self.__index.flipDisk(self.board[19],1);
        self.board[29] = self.__index.flipDisk(self.board[29],1);
    if fliped[1] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],4);
      self.board[22] = self.__index.flipDisk(self.board[22],3);
      self.board[32] = self.__index.flipDisk(self.board[32],4);
      if fliped[1] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],4);
        self.board[23] = self.__index.flipDisk(self.board[23],3);
        self.board[33] = self.__index.flipDisk(self.board[33],4);
        if fliped[1] >= 3:
          self.board[6] = self.__index.flipDisk(self.board[6],4);
          self.board[24] = self.__index.flipDisk(self.board[24],3);
          self.board[34] = self.__index.flipDisk(self.board[34],4);
    self.board[21],fliped = self.__index.flipLine(self.board[21],3,color);
    if fliped[0] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],5);
      self.board[13] = self.__index.flipDisk(self.board[13],2);
      self.board[29] = self.__index.flipDisk(self.board[29],2);
      if fliped[0] >= 2:
        self.board[1] = self.__index.flipDisk(self.board[1],6);
        self.board[14] = self.__index.flipDisk(self.board[14],1);
        self.board[27] = self.__index.flipDisk(self.board[27],1);
    if fliped[1] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],3);
      self.board[11] = self.__index.flipDisk(self.board[11],4);
      self.board[33] = self.__index.flipDisk(self.board[33],3);
      if fliped[1] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],2);
        self.board[10] = self.__index.flipDisk(self.board[10],5);
        self.board[35] = self.__index.flipDisk(self.board[35],2);
        if fliped[1] >= 3:
          self.board[6] = self.__index.flipDisk(self.board[6],1);
          self.board[9] = self.__index.flipDisk(self.board[9],6);
          self.board[37] = self.__index.flipDisk(self.board[37],1);
    self.board[31],fliped = self.__index.flipLine(self.board[31],3,color);
    if fliped[0] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],3);
      self.board[11] = self.__index.flipDisk(self.board[11],2);
      self.board[19] = self.__index.flipDisk(self.board[19],2);
      if fliped[0] >= 2:
        self.board[1] = self.__index.flipDisk(self.board[1],2);
        self.board[10] = self.__index.flipDisk(self.board[10],1);
        self.board[17] = self.__index.flipDisk(self.board[17],1);
    if fliped[1] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],5);
      self.board[13] = self.__index.flipDisk(self.board[13],4);
      self.board[23] = self.__index.flipDisk(self.board[23],2);
      if fliped[1] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],6);
        self.board[14] = self.__index.flipDisk(self.board[14],5);
        self.board[25] = self.__index.flipDisk(self.board[25],1);
  def putAt29(self, color):
    self.board[3],fliped = self.__index.flipLine(self.board[3],5,color)
    if fliped[0] >= 1:
      self.board[12] = self.__index.flipDisk(self.board[12],3)
      self.board[21] = self.__index.flipDisk(self.board[21],3)
      self.board[31] = self.__index.flipDisk(self.board[31],3)
      if fliped[0] >= 2:
        self.board[11] = self.__index.flipDisk(self.board[11],3)
        self.board[20] = self.__index.flipDisk(self.board[20],3)
        self.board[32] = self.__index.flipDisk(self.board[32],3)
        if fliped[0] >= 3:
          self.board[10] = self.__index.flipDisk(self.board[10],3)
          self.board[19] = self.__index.flipDisk(self.board[19],3)
          self.board[33] = self.__index.flipDisk(self.board[33],2)
          if fliped[0] >= 4:
            self.board[9] = self.__index.flipDisk(self.board[9],3)
            self.board[18] = self.__index.flipDisk(self.board[18],3)
            self.board[34] = self.__index.flipDisk(self.board[34],1)
    if fliped[1] >= 1:
      self.board[14] = self.__index.flipDisk(self.board[14],3)
      self.board[23] = self.__index.flipDisk(self.board[23],1)
      self.board[29] = self.__index.flipDisk(self.board[29],3)
    self.board[13],fliped = self.__index.flipLine(self.board[13],3,color)
    if fliped[0] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],5);
      self.board[21] = self.__index.flipDisk(self.board[21],2);
      self.board[29] = self.__index.flipDisk(self.board[29],2);
      if fliped[0] >= 2:
        self.board[1] = self.__index.flipDisk(self.board[1],5);
        self.board[20] = self.__index.flipDisk(self.board[20],1);
        self.board[28] = self.__index.flipDisk(self.board[28],1);
    if fliped[1] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],5);
      self.board[23] = self.__index.flipDisk(self.board[23],2);
      self.board[31] = self.__index.flipDisk(self.board[31],4);
      if fliped[1] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],5);
        self.board[24] = self.__index.flipDisk(self.board[24],2);
        self.board[32] = self.__index.flipDisk(self.board[32],5);
        if fliped[1] >= 3:
          self.board[6] = self.__index.flipDisk(self.board[6],5);
          self.board[25] = self.__index.flipDisk(self.board[25],2);
          self.board[33] = self.__index.flipDisk(self.board[33],5);
    self.board[22],fliped = self.__index.flipLine(self.board[22],2,color);
    if fliped[0] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],6);
      self.board[14] = self.__index.flipDisk(self.board[14],2);
      self.board[28] = self.__index.flipDisk(self.board[28],2);
    if fliped[1] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],4);
      self.board[12] = self.__index.flipDisk(self.board[12],4);
      self.board[32] = self.__index.flipDisk(self.board[32],4);
      if fliped[1] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],3);
        self.board[11] = self.__index.flipDisk(self.board[11],5);
        self.board[34] = self.__index.flipDisk(self.board[34],3);
        if fliped[1] >= 3:
          self.board[6] = self.__index.flipDisk(self.board[6],2);
          self.board[10] = self.__index.flipDisk(self.board[10],6);
          self.board[36] = self.__index.flipDisk(self.board[36],2);
    self.board[30],fliped = self.__index.flipLine(self.board[30],3,color);
    if fliped[0] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],4);
      self.board[12] = self.__index.flipDisk(self.board[12],2);
      self.board[20] = self.__index.flipDisk(self.board[20],2);
      if fliped[0] >= 2:
        self.board[1] = self.__index.flipDisk(self.board[1],3);
        self.board[11] = self.__index.flipDisk(self.board[11],1);
        self.board[18] = self.__index.flipDisk(self.board[18],1);
    if fliped[1] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],6);
      self.board[14] = self.__index.flipDisk(self.board[14],4);
      self.board[24] = self.__index.flipDisk(self.board[24],1);
  def putAt30(self, color):
    self.board[3],fliped = self.__index.flipLine(self.board[3],6,color)
    if fliped[0] >= 1:
      self.board[13] = self.__index.flipDisk(self.board[13],3)
      self.board[22] = self.__index.flipDisk(self.board[22],2)
      self.board[30] = self.__index.flipDisk(self.board[30],3)
      if fliped[0] >= 2:
        self.board[12] = self.__index.flipDisk(self.board[12],3)
        self.board[21] = self.__index.flipDisk(self.board[21],3)
        self.board[31] = self.__index.flipDisk(self.board[31],3)
        if fliped[0] >= 3:
          self.board[11] = self.__index.flipDisk(self.board[11],3)
          self.board[20] = self.__index.flipDisk(self.board[20],3)
          self.board[32] = self.__index.flipDisk(self.board[32],3)
          if fliped[0] >= 4:
            self.board[10] = self.__index.flipDisk(self.board[10],3)
            self.board[19] = self.__index.flipDisk(self.board[19],3)
            self.board[33] = self.__index.flipDisk(self.board[33],2)
            if fliped[0] >= 5:
              self.board[9] = self.__index.flipDisk(self.board[9],3)
              self.board[18] = self.__index.flipDisk(self.board[18],3)
              self.board[34] = self.__index.flipDisk(self.board[34],1)
    self.board[14],fliped = self.__index.flipLine(self.board[14],3,color)
    if fliped[0] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],6);
      self.board[22] = self.__index.flipDisk(self.board[22],1);
      self.board[28] = self.__index.flipDisk(self.board[28],2);
      if fliped[0] >= 2:
        self.board[1] = self.__index.flipDisk(self.board[1],6);
        self.board[21] = self.__index.flipDisk(self.board[21],1);
        self.board[27] = self.__index.flipDisk(self.board[27],1);
    if fliped[1] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],6);
      self.board[24] = self.__index.flipDisk(self.board[24],1);
      self.board[30] = self.__index.flipDisk(self.board[30],4);
      if fliped[1] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],6);
        self.board[25] = self.__index.flipDisk(self.board[25],1);
        self.board[31] = self.__index.flipDisk(self.board[31],5);
        if fliped[1] >= 3:
          self.board[6] = self.__index.flipDisk(self.board[6],6);
          self.board[26] = self.__index.flipDisk(self.board[26],1);
          self.board[32] = self.__index.flipDisk(self.board[32],6);
    self.board[23],fliped = self.__index.flipLine(self.board[23],1,color);
    if fliped[1] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],5);
      self.board[13] = self.__index.flipDisk(self.board[13],4);
      self.board[31] = self.__index.flipDisk(self.board[31],4);
      if fliped[1] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],4);
        self.board[12] = self.__index.flipDisk(self.board[12],5);
        self.board[33] = self.__index.flipDisk(self.board[33],4);
        if fliped[1] >= 3:
          self.board[6] = self.__index.flipDisk(self.board[6],3);
          self.board[11] = self.__index.flipDisk(self.board[11],6);
          self.board[35] = self.__index.flipDisk(self.board[35],3);
    self.board[29],fliped = self.__index.flipLine(self.board[29],3,color);
    if fliped[0] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],5);
      self.board[13] = self.__index.flipDisk(self.board[13],2);
      self.board[21] = self.__index.flipDisk(self.board[21],2);
      if fliped[0] >= 2:
        self.board[1] = self.__index.flipDisk(self.board[1],4);
        self.board[12] = self.__index.flipDisk(self.board[12],1);
        self.board[19] = self.__index.flipDisk(self.board[19],1);
  def putAt31(self, color):
    self.board[3],fliped = self.__index.flipLine(self.board[3],7,color)
    if fliped[0] >= 1:
      self.board[14] = self.__index.flipDisk(self.board[14],3)
      self.board[23] = self.__index.flipDisk(self.board[23],1)
      self.board[29] = self.__index.flipDisk(self.board[29],3)
      if fliped[0] >= 2:
        self.board[13] = self.__index.flipDisk(self.board[13],3)
        self.board[22] = self.__index.flipDisk(self.board[22],2)
        self.board[30] = self.__index.flipDisk(self.board[30],3)
        if fliped[0] >= 3:
          self.board[12] = self.__index.flipDisk(self.board[12],3)
          self.board[21] = self.__index.flipDisk(self.board[21],3)
          self.board[31] = self.__index.flipDisk(self.board[31],3)
          if fliped[0] >= 4:
            self.board[11] = self.__index.flipDisk(self.board[11],3)
            self.board[20] = self.__index.flipDisk(self.board[20],3)
            self.board[32] = self.__index.flipDisk(self.board[32],3)
            if fliped[0] >= 5:
              self.board[10] = self.__index.flipDisk(self.board[10],3)
              self.board[19] = self.__index.flipDisk(self.board[19],3)
              self.board[33] = self.__index.flipDisk(self.board[33],2)
              if fliped[0] >= 6:
                self.board[9] = self.__index.flipDisk(self.board[9],3)
                self.board[18] = self.__index.flipDisk(self.board[18],3)
                self.board[34] = self.__index.flipDisk(self.board[34],1)
    self.board[15],fliped = self.__index.flipLine(self.board[15],3,color)
    if fliped[0] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],7);
      self.board[23] = self.__index.flipDisk(self.board[23],0);
      self.board[27] = self.__index.flipDisk(self.board[27],2);
      if fliped[0] >= 2:
        self.board[1] = self.__index.flipDisk(self.board[1],7);
        self.board[22] = self.__index.flipDisk(self.board[22],0);
    if fliped[1] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],7);
      self.board[25] = self.__index.flipDisk(self.board[25],0);
      self.board[29] = self.__index.flipDisk(self.board[29],4);
      if fliped[1] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],7);
        self.board[26] = self.__index.flipDisk(self.board[26],0);
        self.board[30] = self.__index.flipDisk(self.board[30],5);
        if fliped[1] >= 3:
          self.board[6] = self.__index.flipDisk(self.board[6],7);
          self.board[31] = self.__index.flipDisk(self.board[31],6);
    self.board[24],fliped = self.__index.flipLine(self.board[24],0,color);
    if fliped[1] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],6);
      self.board[14] = self.__index.flipDisk(self.board[14],4);
      self.board[30] = self.__index.flipDisk(self.board[30],4);
      if fliped[1] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],5);
        self.board[13] = self.__index.flipDisk(self.board[13],5);
        self.board[32] = self.__index.flipDisk(self.board[32],5);
        if fliped[1] >= 3:
          self.board[6] = self.__index.flipDisk(self.board[6],4);
          self.board[12] = self.__index.flipDisk(self.board[12],6);
          self.board[34] = self.__index.flipDisk(self.board[34],4);
    self.board[28],fliped = self.__index.flipLine(self.board[28],3,color);
    if fliped[0] >= 1:
      self.board[2] = self.__index.flipDisk(self.board[2],6);
      self.board[14] = self.__index.flipDisk(self.board[14],2);
      self.board[22] = self.__index.flipDisk(self.board[22],1);
      if fliped[0] >= 2:
        self.board[1] = self.__index.flipDisk(self.board[1],5);
        self.board[13] = self.__index.flipDisk(self.board[13],1);
        self.board[20] = self.__index.flipDisk(self.board[20],1);
  def putAt32(self, color):
    self.board[4],fliped = self.__index.flipLine(self.board[4],0,color)
    if fliped[1] >= 1:
      self.board[9] = self.__index.flipDisk(self.board[9],4)
      self.board[19] = self.__index.flipDisk(self.board[19],4)
      self.board[35] = self.__index.flipDisk(self.board[35],1)
      if fliped[1] >= 2:
        self.board[10] = self.__index.flipDisk(self.board[10],4)
        self.board[20] = self.__index.flipDisk(self.board[20],4)
        self.board[34] = self.__index.flipDisk(self.board[34],2)
        if fliped[1] >= 3:
          self.board[11] = self.__index.flipDisk(self.board[11],4)
          self.board[21] = self.__index.flipDisk(self.board[21],4)
          self.board[33] = self.__index.flipDisk(self.board[33],3)
          if fliped[1] >= 4:
            self.board[12] = self.__index.flipDisk(self.board[12],4)
            self.board[22] = self.__index.flipDisk(self.board[22],3)
            self.board[32] = self.__index.flipDisk(self.board[32],4)
            if fliped[1] >= 5:
              self.board[13] = self.__index.flipDisk(self.board[13],4)
              self.board[23] = self.__index.flipDisk(self.board[23],2)
              self.board[31] = self.__index.flipDisk(self.board[31],4)
              if fliped[1] >= 6:
                self.board[14] = self.__index.flipDisk(self.board[14],4)
                self.board[24] = self.__index.flipDisk(self.board[24],1)
                self.board[30] = self.__index.flipDisk(self.board[30],4)
    self.board[8],fliped = self.__index.flipLine(self.board[8],4,color)
    if fliped[0] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],0);
      self.board[17] = self.__index.flipDisk(self.board[17],3);
      self.board[35] = self.__index.flipDisk(self.board[35],0);
      if fliped[0] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],0);
        self.board[16] = self.__index.flipDisk(self.board[16],2);
        self.board[34] = self.__index.flipDisk(self.board[34],0);
        if fliped[0] >= 3:
          self.board[1] = self.__index.flipDisk(self.board[1],0);
          self.board[33] = self.__index.flipDisk(self.board[33],0);
    if fliped[1] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],0);
      self.board[19] = self.__index.flipDisk(self.board[19],5);
      self.board[37] = self.__index.flipDisk(self.board[37],0);
      if fliped[1] >= 2:
        self.board[6] = self.__index.flipDisk(self.board[6],0);
        self.board[20] = self.__index.flipDisk(self.board[20],6);
    self.board[18],fliped = self.__index.flipLine(self.board[18],4,color);
    if fliped[0] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],1);
      self.board[9] = self.__index.flipDisk(self.board[9],3);
      self.board[34] = self.__index.flipDisk(self.board[34],1);
      if fliped[0] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],2);
        self.board[10] = self.__index.flipDisk(self.board[10],2);
        self.board[32] = self.__index.flipDisk(self.board[32],2);
        if fliped[0] >= 3:
          self.board[1] = self.__index.flipDisk(self.board[1],3);
          self.board[11] = self.__index.flipDisk(self.board[11],1);
          self.board[30] = self.__index.flipDisk(self.board[30],1);
    self.board[36],fliped = self.__index.flipLine(self.board[36],0,color);
    if fliped[1] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],1);
      self.board[9] = self.__index.flipDisk(self.board[9],5);
      self.board[20] = self.__index.flipDisk(self.board[20],5);
      if fliped[1] >= 2:
        self.board[6] = self.__index.flipDisk(self.board[6],2);
        self.board[10] = self.__index.flipDisk(self.board[10],6);
        self.board[22] = self.__index.flipDisk(self.board[22],5);
  def putAt33(self, color):
    self.board[4],fliped = self.__index.flipLine(self.board[4],1,color)
    if fliped[1] >= 1:
      self.board[10] = self.__index.flipDisk(self.board[10],4)
      self.board[20] = self.__index.flipDisk(self.board[20],4)
      self.board[34] = self.__index.flipDisk(self.board[34],2)
      if fliped[1] >= 2:
        self.board[11] = self.__index.flipDisk(self.board[11],4)
        self.board[21] = self.__index.flipDisk(self.board[21],4)
        self.board[33] = self.__index.flipDisk(self.board[33],3)
        if fliped[1] >= 3:
          self.board[12] = self.__index.flipDisk(self.board[12],4)
          self.board[22] = self.__index.flipDisk(self.board[22],3)
          self.board[32] = self.__index.flipDisk(self.board[32],4)
          if fliped[1] >= 4:
            self.board[13] = self.__index.flipDisk(self.board[13],4)
            self.board[23] = self.__index.flipDisk(self.board[23],2)
            self.board[31] = self.__index.flipDisk(self.board[31],4)
            if fliped[1] >= 5:
              self.board[14] = self.__index.flipDisk(self.board[14],4)
              self.board[24] = self.__index.flipDisk(self.board[24],1)
              self.board[30] = self.__index.flipDisk(self.board[30],4)
    self.board[9],fliped = self.__index.flipLine(self.board[9],4,color)
    if fliped[0] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],1);
      self.board[18] = self.__index.flipDisk(self.board[18],3);
      self.board[34] = self.__index.flipDisk(self.board[34],1);
      if fliped[0] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],1);
        self.board[17] = self.__index.flipDisk(self.board[17],2);
        self.board[33] = self.__index.flipDisk(self.board[33],1);
        if fliped[0] >= 3:
          self.board[1] = self.__index.flipDisk(self.board[1],1);
          self.board[16] = self.__index.flipDisk(self.board[16],1);
          self.board[32] = self.__index.flipDisk(self.board[32],1);
    if fliped[1] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],1);
      self.board[20] = self.__index.flipDisk(self.board[20],5);
      self.board[36] = self.__index.flipDisk(self.board[36],1);
      if fliped[1] >= 2:
        self.board[6] = self.__index.flipDisk(self.board[6],1);
        self.board[21] = self.__index.flipDisk(self.board[21],6);
        self.board[37] = self.__index.flipDisk(self.board[37],1);
    self.board[19],fliped = self.__index.flipLine(self.board[19],4,color);
    if fliped[0] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],2);
      self.board[10] = self.__index.flipDisk(self.board[10],3);
      self.board[33] = self.__index.flipDisk(self.board[33],2);
      if fliped[0] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],3);
        self.board[11] = self.__index.flipDisk(self.board[11],2);
        self.board[31] = self.__index.flipDisk(self.board[31],2);
        if fliped[0] >= 3:
          self.board[1] = self.__index.flipDisk(self.board[1],4);
          self.board[12] = self.__index.flipDisk(self.board[12],1);
          self.board[29] = self.__index.flipDisk(self.board[29],1);
    self.board[35],fliped = self.__index.flipLine(self.board[35],1,color);
    if fliped[1] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],2);
      self.board[10] = self.__index.flipDisk(self.board[10],5);
      self.board[21] = self.__index.flipDisk(self.board[21],5);
      if fliped[1] >= 2:
        self.board[6] = self.__index.flipDisk(self.board[6],3);
        self.board[11] = self.__index.flipDisk(self.board[11],6);
        self.board[23] = self.__index.flipDisk(self.board[23],4);
  def putAt34(self, color):
    self.board[4],fliped = self.__index.flipLine(self.board[4],2,color)
    if fliped[0] >= 1:
      self.board[9] = self.__index.flipDisk(self.board[9],4)
      self.board[19] = self.__index.flipDisk(self.board[19],4)
      self.board[35] = self.__index.flipDisk(self.board[35],1)
    if fliped[1] >= 1:
      self.board[11] = self.__index.flipDisk(self.board[11],4)
      self.board[21] = self.__index.flipDisk(self.board[21],4)
      self.board[33] = self.__index.flipDisk(self.board[33],3)
      if fliped[1] >= 2:
        self.board[12] = self.__index.flipDisk(self.board[12],4)
        self.board[22] = self.__index.flipDisk(self.board[22],3)
        self.board[32] = self.__index.flipDisk(self.board[32],4)
        if fliped[1] >= 3:
          self.board[13] = self.__index.flipDisk(self.board[13],4)
          self.board[23] = self.__index.flipDisk(self.board[23],2)
          self.board[31] = self.__index.flipDisk(self.board[31],4)
          if fliped[1] >= 4:
            self.board[14] = self.__index.flipDisk(self.board[14],4)
            self.board[24] = self.__index.flipDisk(self.board[24],1)
            self.board[30] = self.__index.flipDisk(self.board[30],4)
    self.board[10],fliped = self.__index.flipLine(self.board[10],4,color)
    if fliped[0] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],2);
      self.board[19] = self.__index.flipDisk(self.board[19],3);
      self.board[33] = self.__index.flipDisk(self.board[33],2);
      if fliped[0] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],2);
        self.board[18] = self.__index.flipDisk(self.board[18],2);
        self.board[32] = self.__index.flipDisk(self.board[32],2);
        if fliped[0] >= 3:
          self.board[1] = self.__index.flipDisk(self.board[1],2);
          self.board[17] = self.__index.flipDisk(self.board[17],1);
          self.board[31] = self.__index.flipDisk(self.board[31],1);
    if fliped[1] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],2);
      self.board[21] = self.__index.flipDisk(self.board[21],5);
      self.board[35] = self.__index.flipDisk(self.board[35],2);
      if fliped[1] >= 2:
        self.board[6] = self.__index.flipDisk(self.board[6],2);
        self.board[22] = self.__index.flipDisk(self.board[22],5);
        self.board[36] = self.__index.flipDisk(self.board[36],2);
    self.board[20],fliped = self.__index.flipLine(self.board[20],4,color);
    if fliped[0] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],3);
      self.board[11] = self.__index.flipDisk(self.board[11],3);
      self.board[32] = self.__index.flipDisk(self.board[32],3);
      if fliped[0] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],4);
        self.board[12] = self.__index.flipDisk(self.board[12],2);
        self.board[30] = self.__index.flipDisk(self.board[30],2);
        if fliped[0] >= 3:
          self.board[1] = self.__index.flipDisk(self.board[1],5);
          self.board[13] = self.__index.flipDisk(self.board[13],1);
          self.board[28] = self.__index.flipDisk(self.board[28],1);
    if fliped[1] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],1);
      self.board[9] = self.__index.flipDisk(self.board[9],5);
      self.board[36] = self.__index.flipDisk(self.board[36],1);
    self.board[34],fliped = self.__index.flipLine(self.board[34],2,color);
    if fliped[0] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],1);
      self.board[9] = self.__index.flipDisk(self.board[9],3);
      self.board[18] = self.__index.flipDisk(self.board[18],3);
    if fliped[1] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],3);
      self.board[11] = self.__index.flipDisk(self.board[11],5);
      self.board[22] = self.__index.flipDisk(self.board[22],4);
      if fliped[1] >= 2:
        self.board[6] = self.__index.flipDisk(self.board[6],4);
        self.board[12] = self.__index.flipDisk(self.board[12],6);
        self.board[24] = self.__index.flipDisk(self.board[24],3);
  def putAt35(self, color):
    self.board[4],fliped = self.__index.flipLine(self.board[4],3,color)
    if fliped[0] >= 1:
      self.board[10] = self.__index.flipDisk(self.board[10],4)
      self.board[20] = self.__index.flipDisk(self.board[20],4)
      self.board[34] = self.__index.flipDisk(self.board[34],2)
      if fliped[0] >= 2:
        self.board[9] = self.__index.flipDisk(self.board[9],4)
        self.board[19] = self.__index.flipDisk(self.board[19],4)
        self.board[35] = self.__index.flipDisk(self.board[35],1)
    if fliped[1] >= 1:
      self.board[12] = self.__index.flipDisk(self.board[12],4)
      self.board[22] = self.__index.flipDisk(self.board[22],3)
      self.board[32] = self.__index.flipDisk(self.board[32],4)
      if fliped[1] >= 2:
        self.board[13] = self.__index.flipDisk(self.board[13],4)
        self.board[23] = self.__index.flipDisk(self.board[23],2)
        self.board[31] = self.__index.flipDisk(self.board[31],4)
        if fliped[1] >= 3:
          self.board[14] = self.__index.flipDisk(self.board[14],4)
          self.board[24] = self.__index.flipDisk(self.board[24],1)
          self.board[30] = self.__index.flipDisk(self.board[30],4)
    self.board[11],fliped = self.__index.flipLine(self.board[11],4,color)
    if fliped[0] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],3);
      self.board[20] = self.__index.flipDisk(self.board[20],3);
      self.board[32] = self.__index.flipDisk(self.board[32],3);
      if fliped[0] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],3);
        self.board[19] = self.__index.flipDisk(self.board[19],2);
        self.board[31] = self.__index.flipDisk(self.board[31],2);
        if fliped[0] >= 3:
          self.board[1] = self.__index.flipDisk(self.board[1],3);
          self.board[18] = self.__index.flipDisk(self.board[18],1);
          self.board[30] = self.__index.flipDisk(self.board[30],1);
    if fliped[1] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],3);
      self.board[22] = self.__index.flipDisk(self.board[22],4);
      self.board[34] = self.__index.flipDisk(self.board[34],3);
      if fliped[1] >= 2:
        self.board[6] = self.__index.flipDisk(self.board[6],3);
        self.board[23] = self.__index.flipDisk(self.board[23],4);
        self.board[35] = self.__index.flipDisk(self.board[35],3);
    self.board[21],fliped = self.__index.flipLine(self.board[21],4,color);
    if fliped[0] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],4);
      self.board[12] = self.__index.flipDisk(self.board[12],3);
      self.board[31] = self.__index.flipDisk(self.board[31],3);
      if fliped[0] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],5);
        self.board[13] = self.__index.flipDisk(self.board[13],2);
        self.board[29] = self.__index.flipDisk(self.board[29],2);
        if fliped[0] >= 3:
          self.board[1] = self.__index.flipDisk(self.board[1],6);
          self.board[14] = self.__index.flipDisk(self.board[14],1);
          self.board[27] = self.__index.flipDisk(self.board[27],1);
    if fliped[1] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],2);
      self.board[10] = self.__index.flipDisk(self.board[10],5);
      self.board[35] = self.__index.flipDisk(self.board[35],2);
      if fliped[1] >= 2:
        self.board[6] = self.__index.flipDisk(self.board[6],1);
        self.board[9] = self.__index.flipDisk(self.board[9],6);
        self.board[37] = self.__index.flipDisk(self.board[37],1);
    self.board[33],fliped = self.__index.flipLine(self.board[33],3,color);
    if fliped[0] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],2);
      self.board[10] = self.__index.flipDisk(self.board[10],3);
      self.board[19] = self.__index.flipDisk(self.board[19],3);
      if fliped[0] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],1);
        self.board[9] = self.__index.flipDisk(self.board[9],2);
        self.board[17] = self.__index.flipDisk(self.board[17],2);
    if fliped[1] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],4);
      self.board[12] = self.__index.flipDisk(self.board[12],5);
      self.board[23] = self.__index.flipDisk(self.board[23],3);
      if fliped[1] >= 2:
        self.board[6] = self.__index.flipDisk(self.board[6],5);
        self.board[13] = self.__index.flipDisk(self.board[13],6);
        self.board[25] = self.__index.flipDisk(self.board[25],2);
  def putAt36(self, color):
    self.board[4],fliped = self.__index.flipLine(self.board[4],4,color)
    if fliped[0] >= 1:
      self.board[11] = self.__index.flipDisk(self.board[11],4)
      self.board[21] = self.__index.flipDisk(self.board[21],4)
      self.board[33] = self.__index.flipDisk(self.board[33],3)
      if fliped[0] >= 2:
        self.board[10] = self.__index.flipDisk(self.board[10],4)
        self.board[20] = self.__index.flipDisk(self.board[20],4)
        self.board[34] = self.__index.flipDisk(self.board[34],2)
        if fliped[0] >= 3:
          self.board[9] = self.__index.flipDisk(self.board[9],4)
          self.board[19] = self.__index.flipDisk(self.board[19],4)
          self.board[35] = self.__index.flipDisk(self.board[35],1)
    if fliped[1] >= 1:
      self.board[13] = self.__index.flipDisk(self.board[13],4)
      self.board[23] = self.__index.flipDisk(self.board[23],2)
      self.board[31] = self.__index.flipDisk(self.board[31],4)
      if fliped[1] >= 2:
        self.board[14] = self.__index.flipDisk(self.board[14],4)
        self.board[24] = self.__index.flipDisk(self.board[24],1)
        self.board[30] = self.__index.flipDisk(self.board[30],4)
    self.board[12],fliped = self.__index.flipLine(self.board[12],4,color)
    if fliped[0] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],4);
      self.board[21] = self.__index.flipDisk(self.board[21],3);
      self.board[31] = self.__index.flipDisk(self.board[31],3);
      if fliped[0] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],4);
        self.board[20] = self.__index.flipDisk(self.board[20],2);
        self.board[30] = self.__index.flipDisk(self.board[30],2);
        if fliped[0] >= 3:
          self.board[1] = self.__index.flipDisk(self.board[1],4);
          self.board[19] = self.__index.flipDisk(self.board[19],1);
          self.board[29] = self.__index.flipDisk(self.board[29],1);
    if fliped[1] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],4);
      self.board[23] = self.__index.flipDisk(self.board[23],3);
      self.board[33] = self.__index.flipDisk(self.board[33],4);
      if fliped[1] >= 2:
        self.board[6] = self.__index.flipDisk(self.board[6],4);
        self.board[24] = self.__index.flipDisk(self.board[24],3);
        self.board[34] = self.__index.flipDisk(self.board[34],4);
    self.board[22],fliped = self.__index.flipLine(self.board[22],3,color);
    if fliped[0] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],5);
      self.board[13] = self.__index.flipDisk(self.board[13],3);
      self.board[30] = self.__index.flipDisk(self.board[30],3);
      if fliped[0] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],6);
        self.board[14] = self.__index.flipDisk(self.board[14],2);
        self.board[28] = self.__index.flipDisk(self.board[28],2);
    if fliped[1] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],3);
      self.board[11] = self.__index.flipDisk(self.board[11],5);
      self.board[34] = self.__index.flipDisk(self.board[34],3);
      if fliped[1] >= 2:
        self.board[6] = self.__index.flipDisk(self.board[6],2);
        self.board[10] = self.__index.flipDisk(self.board[10],6);
        self.board[36] = self.__index.flipDisk(self.board[36],2);
    self.board[32],fliped = self.__index.flipLine(self.board[32],4,color);
    if fliped[0] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],3);
      self.board[11] = self.__index.flipDisk(self.board[11],3);
      self.board[20] = self.__index.flipDisk(self.board[20],3);
      if fliped[0] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],2);
        self.board[10] = self.__index.flipDisk(self.board[10],2);
        self.board[18] = self.__index.flipDisk(self.board[18],2);
        if fliped[0] >= 3:
          self.board[1] = self.__index.flipDisk(self.board[1],1);
          self.board[9] = self.__index.flipDisk(self.board[9],1);
          self.board[16] = self.__index.flipDisk(self.board[16],1);
    if fliped[1] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],5);
      self.board[13] = self.__index.flipDisk(self.board[13],5);
      self.board[24] = self.__index.flipDisk(self.board[24],2);
      if fliped[1] >= 2:
        self.board[6] = self.__index.flipDisk(self.board[6],6);
        self.board[14] = self.__index.flipDisk(self.board[14],6);
        self.board[26] = self.__index.flipDisk(self.board[26],1);
  def putAt37(self, color):
    self.board[4],fliped = self.__index.flipLine(self.board[4],5,color)
    if fliped[0] >= 1:
      self.board[12] = self.__index.flipDisk(self.board[12],4)
      self.board[22] = self.__index.flipDisk(self.board[22],3)
      self.board[32] = self.__index.flipDisk(self.board[32],4)
      if fliped[0] >= 2:
        self.board[11] = self.__index.flipDisk(self.board[11],4)
        self.board[21] = self.__index.flipDisk(self.board[21],4)
        self.board[33] = self.__index.flipDisk(self.board[33],3)
        if fliped[0] >= 3:
          self.board[10] = self.__index.flipDisk(self.board[10],4)
          self.board[20] = self.__index.flipDisk(self.board[20],4)
          self.board[34] = self.__index.flipDisk(self.board[34],2)
          if fliped[0] >= 4:
            self.board[9] = self.__index.flipDisk(self.board[9],4)
            self.board[19] = self.__index.flipDisk(self.board[19],4)
            self.board[35] = self.__index.flipDisk(self.board[35],1)
    if fliped[1] >= 1:
      self.board[14] = self.__index.flipDisk(self.board[14],4)
      self.board[24] = self.__index.flipDisk(self.board[24],1)
      self.board[30] = self.__index.flipDisk(self.board[30],4)
    self.board[13],fliped = self.__index.flipLine(self.board[13],4,color)
    if fliped[0] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],5);
      self.board[22] = self.__index.flipDisk(self.board[22],2);
      self.board[30] = self.__index.flipDisk(self.board[30],3);
      if fliped[0] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],5);
        self.board[21] = self.__index.flipDisk(self.board[21],2);
        self.board[29] = self.__index.flipDisk(self.board[29],2);
        if fliped[0] >= 3:
          self.board[1] = self.__index.flipDisk(self.board[1],5);
          self.board[20] = self.__index.flipDisk(self.board[20],1);
          self.board[28] = self.__index.flipDisk(self.board[28],1);
    if fliped[1] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],5);
      self.board[24] = self.__index.flipDisk(self.board[24],2);
      self.board[32] = self.__index.flipDisk(self.board[32],5);
      if fliped[1] >= 2:
        self.board[6] = self.__index.flipDisk(self.board[6],5);
        self.board[25] = self.__index.flipDisk(self.board[25],2);
        self.board[33] = self.__index.flipDisk(self.board[33],5);
    self.board[23],fliped = self.__index.flipLine(self.board[23],2,color);
    if fliped[0] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],6);
      self.board[14] = self.__index.flipDisk(self.board[14],3);
      self.board[29] = self.__index.flipDisk(self.board[29],3);
    if fliped[1] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],4);
      self.board[12] = self.__index.flipDisk(self.board[12],5);
      self.board[33] = self.__index.flipDisk(self.board[33],4);
      if fliped[1] >= 2:
        self.board[6] = self.__index.flipDisk(self.board[6],3);
        self.board[11] = self.__index.flipDisk(self.board[11],6);
        self.board[35] = self.__index.flipDisk(self.board[35],3);
    self.board[31],fliped = self.__index.flipLine(self.board[31],4,color);
    if fliped[0] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],4);
      self.board[12] = self.__index.flipDisk(self.board[12],3);
      self.board[21] = self.__index.flipDisk(self.board[21],3);
      if fliped[0] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],3);
        self.board[11] = self.__index.flipDisk(self.board[11],2);
        self.board[19] = self.__index.flipDisk(self.board[19],2);
        if fliped[0] >= 3:
          self.board[1] = self.__index.flipDisk(self.board[1],2);
          self.board[10] = self.__index.flipDisk(self.board[10],1);
          self.board[17] = self.__index.flipDisk(self.board[17],1);
    if fliped[1] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],6);
      self.board[14] = self.__index.flipDisk(self.board[14],5);
      self.board[25] = self.__index.flipDisk(self.board[25],1);
  def putAt38(self, color):
    self.board[4],fliped = self.__index.flipLine(self.board[4],6,color)
    if fliped[0] >= 1:
      self.board[13] = self.__index.flipDisk(self.board[13],4)
      self.board[23] = self.__index.flipDisk(self.board[23],2)
      self.board[31] = self.__index.flipDisk(self.board[31],4)
      if fliped[0] >= 2:
        self.board[12] = self.__index.flipDisk(self.board[12],4)
        self.board[22] = self.__index.flipDisk(self.board[22],3)
        self.board[32] = self.__index.flipDisk(self.board[32],4)
        if fliped[0] >= 3:
          self.board[11] = self.__index.flipDisk(self.board[11],4)
          self.board[21] = self.__index.flipDisk(self.board[21],4)
          self.board[33] = self.__index.flipDisk(self.board[33],3)
          if fliped[0] >= 4:
            self.board[10] = self.__index.flipDisk(self.board[10],4)
            self.board[20] = self.__index.flipDisk(self.board[20],4)
            self.board[34] = self.__index.flipDisk(self.board[34],2)
            if fliped[0] >= 5:
              self.board[9] = self.__index.flipDisk(self.board[9],4)
              self.board[19] = self.__index.flipDisk(self.board[19],4)
              self.board[35] = self.__index.flipDisk(self.board[35],1)
    self.board[14],fliped = self.__index.flipLine(self.board[14],4,color)
    if fliped[0] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],6);
      self.board[23] = self.__index.flipDisk(self.board[23],1);
      self.board[29] = self.__index.flipDisk(self.board[29],3);
      if fliped[0] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],6);
        self.board[22] = self.__index.flipDisk(self.board[22],1);
        self.board[28] = self.__index.flipDisk(self.board[28],2);
        if fliped[0] >= 3:
          self.board[1] = self.__index.flipDisk(self.board[1],6);
          self.board[21] = self.__index.flipDisk(self.board[21],1);
          self.board[27] = self.__index.flipDisk(self.board[27],1);
    if fliped[1] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],6);
      self.board[25] = self.__index.flipDisk(self.board[25],1);
      self.board[31] = self.__index.flipDisk(self.board[31],5);
      if fliped[1] >= 2:
        self.board[6] = self.__index.flipDisk(self.board[6],6);
        self.board[26] = self.__index.flipDisk(self.board[26],1);
        self.board[32] = self.__index.flipDisk(self.board[32],6);
    self.board[24],fliped = self.__index.flipLine(self.board[24],1,color);
    if fliped[1] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],5);
      self.board[13] = self.__index.flipDisk(self.board[13],5);
      self.board[32] = self.__index.flipDisk(self.board[32],5);
      if fliped[1] >= 2:
        self.board[6] = self.__index.flipDisk(self.board[6],4);
        self.board[12] = self.__index.flipDisk(self.board[12],6);
        self.board[34] = self.__index.flipDisk(self.board[34],4);
    self.board[30],fliped = self.__index.flipLine(self.board[30],4,color);
    if fliped[0] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],5);
      self.board[13] = self.__index.flipDisk(self.board[13],3);
      self.board[22] = self.__index.flipDisk(self.board[22],2);
      if fliped[0] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],4);
        self.board[12] = self.__index.flipDisk(self.board[12],2);
        self.board[20] = self.__index.flipDisk(self.board[20],2);
        if fliped[0] >= 3:
          self.board[1] = self.__index.flipDisk(self.board[1],3);
          self.board[11] = self.__index.flipDisk(self.board[11],1);
          self.board[18] = self.__index.flipDisk(self.board[18],1);
  def putAt39(self, color):
    self.board[4],fliped = self.__index.flipLine(self.board[4],7,color)
    if fliped[0] >= 1:
      self.board[14] = self.__index.flipDisk(self.board[14],4)
      self.board[24] = self.__index.flipDisk(self.board[24],1)
      self.board[30] = self.__index.flipDisk(self.board[30],4)
      if fliped[0] >= 2:
        self.board[13] = self.__index.flipDisk(self.board[13],4)
        self.board[23] = self.__index.flipDisk(self.board[23],2)
        self.board[31] = self.__index.flipDisk(self.board[31],4)
        if fliped[0] >= 3:
          self.board[12] = self.__index.flipDisk(self.board[12],4)
          self.board[22] = self.__index.flipDisk(self.board[22],3)
          self.board[32] = self.__index.flipDisk(self.board[32],4)
          if fliped[0] >= 4:
            self.board[11] = self.__index.flipDisk(self.board[11],4)
            self.board[21] = self.__index.flipDisk(self.board[21],4)
            self.board[33] = self.__index.flipDisk(self.board[33],3)
            if fliped[0] >= 5:
              self.board[10] = self.__index.flipDisk(self.board[10],4)
              self.board[20] = self.__index.flipDisk(self.board[20],4)
              self.board[34] = self.__index.flipDisk(self.board[34],2)
              if fliped[0] >= 6:
                self.board[9] = self.__index.flipDisk(self.board[9],4)
                self.board[19] = self.__index.flipDisk(self.board[19],4)
                self.board[35] = self.__index.flipDisk(self.board[35],1)
    self.board[15],fliped = self.__index.flipLine(self.board[15],4,color)
    if fliped[0] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],7);
      self.board[24] = self.__index.flipDisk(self.board[24],0);
      self.board[28] = self.__index.flipDisk(self.board[28],3);
      if fliped[0] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],7);
        self.board[23] = self.__index.flipDisk(self.board[23],0);
        self.board[27] = self.__index.flipDisk(self.board[27],2);
        if fliped[0] >= 3:
          self.board[1] = self.__index.flipDisk(self.board[1],7);
          self.board[22] = self.__index.flipDisk(self.board[22],0);
    if fliped[1] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],7);
      self.board[26] = self.__index.flipDisk(self.board[26],0);
      self.board[30] = self.__index.flipDisk(self.board[30],5);
      if fliped[1] >= 2:
        self.board[6] = self.__index.flipDisk(self.board[6],7);
        self.board[31] = self.__index.flipDisk(self.board[31],6);
    self.board[25],fliped = self.__index.flipLine(self.board[25],0,color);
    if fliped[1] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],6);
      self.board[14] = self.__index.flipDisk(self.board[14],5);
      self.board[31] = self.__index.flipDisk(self.board[31],5);
      if fliped[1] >= 2:
        self.board[6] = self.__index.flipDisk(self.board[6],5);
        self.board[13] = self.__index.flipDisk(self.board[13],6);
        self.board[33] = self.__index.flipDisk(self.board[33],5);
    self.board[29],fliped = self.__index.flipLine(self.board[29],4,color);
    if fliped[0] >= 1:
      self.board[3] = self.__index.flipDisk(self.board[3],6);
      self.board[14] = self.__index.flipDisk(self.board[14],3);
      self.board[23] = self.__index.flipDisk(self.board[23],1);
      if fliped[0] >= 2:
        self.board[2] = self.__index.flipDisk(self.board[2],5);
        self.board[13] = self.__index.flipDisk(self.board[13],2);
        self.board[21] = self.__index.flipDisk(self.board[21],2);
        if fliped[0] >= 3:
          self.board[1] = self.__index.flipDisk(self.board[1],4);
          self.board[12] = self.__index.flipDisk(self.board[12],1);
          self.board[19] = self.__index.flipDisk(self.board[19],1);
  def putAt40(self, color):
    self.board[5],fliped = self.__index.flipLine(self.board[5],0,color)
    if fliped[1] >= 1:
      self.board[9] = self.__index.flipDisk(self.board[9],5)
      self.board[20] = self.__index.flipDisk(self.board[20],5)
      self.board[36] = self.__index.flipDisk(self.board[36],1)
      if fliped[1] >= 2:
        self.board[10] = self.__index.flipDisk(self.board[10],5)
        self.board[21] = self.__index.flipDisk(self.board[21],5)
        self.board[35] = self.__index.flipDisk(self.board[35],2)
        if fliped[1] >= 3:
          self.board[11] = self.__index.flipDisk(self.board[11],5)
          self.board[22] = self.__index.flipDisk(self.board[22],4)
          self.board[34] = self.__index.flipDisk(self.board[34],3)
          if fliped[1] >= 4:
            self.board[12] = self.__index.flipDisk(self.board[12],5)
            self.board[23] = self.__index.flipDisk(self.board[23],3)
            self.board[33] = self.__index.flipDisk(self.board[33],4)
            if fliped[1] >= 5:
              self.board[13] = self.__index.flipDisk(self.board[13],5)
              self.board[24] = self.__index.flipDisk(self.board[24],2)
              self.board[32] = self.__index.flipDisk(self.board[32],5)
              if fliped[1] >= 6:
                self.board[14] = self.__index.flipDisk(self.board[14],5)
                self.board[25] = self.__index.flipDisk(self.board[25],1)
                self.board[31] = self.__index.flipDisk(self.board[31],5)
    self.board[8],fliped = self.__index.flipLine(self.board[8],5,color)
    if fliped[0] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],0);
      self.board[18] = self.__index.flipDisk(self.board[18],4);
      self.board[36] = self.__index.flipDisk(self.board[36],0);
      if fliped[0] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],0);
        self.board[17] = self.__index.flipDisk(self.board[17],3);
        self.board[35] = self.__index.flipDisk(self.board[35],0);
        if fliped[0] >= 3:
          self.board[2] = self.__index.flipDisk(self.board[2],0);
          self.board[16] = self.__index.flipDisk(self.board[16],2);
          self.board[34] = self.__index.flipDisk(self.board[34],0);
          if fliped[0] >= 4:
            self.board[1] = self.__index.flipDisk(self.board[1],0);
            self.board[33] = self.__index.flipDisk(self.board[33],0);
    if fliped[1] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],0);
      self.board[20] = self.__index.flipDisk(self.board[20],6);
    self.board[19],fliped = self.__index.flipLine(self.board[19],5,color);
    if fliped[0] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],1);
      self.board[9] = self.__index.flipDisk(self.board[9],4);
      self.board[35] = self.__index.flipDisk(self.board[35],1);
      if fliped[0] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],2);
        self.board[10] = self.__index.flipDisk(self.board[10],3);
        self.board[33] = self.__index.flipDisk(self.board[33],2);
        if fliped[0] >= 3:
          self.board[2] = self.__index.flipDisk(self.board[2],3);
          self.board[11] = self.__index.flipDisk(self.board[11],2);
          self.board[31] = self.__index.flipDisk(self.board[31],2);
          if fliped[0] >= 4:
            self.board[1] = self.__index.flipDisk(self.board[1],4);
            self.board[12] = self.__index.flipDisk(self.board[12],1);
            self.board[29] = self.__index.flipDisk(self.board[29],1);
    self.board[37],fliped = self.__index.flipLine(self.board[37],0,color);
    if fliped[1] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],1);
      self.board[9] = self.__index.flipDisk(self.board[9],6);
      self.board[21] = self.__index.flipDisk(self.board[21],6);
  def putAt41(self, color):
    self.board[5],fliped = self.__index.flipLine(self.board[5],1,color)
    if fliped[1] >= 1:
      self.board[10] = self.__index.flipDisk(self.board[10],5)
      self.board[21] = self.__index.flipDisk(self.board[21],5)
      self.board[35] = self.__index.flipDisk(self.board[35],2)
      if fliped[1] >= 2:
        self.board[11] = self.__index.flipDisk(self.board[11],5)
        self.board[22] = self.__index.flipDisk(self.board[22],4)
        self.board[34] = self.__index.flipDisk(self.board[34],3)
        if fliped[1] >= 3:
          self.board[12] = self.__index.flipDisk(self.board[12],5)
          self.board[23] = self.__index.flipDisk(self.board[23],3)
          self.board[33] = self.__index.flipDisk(self.board[33],4)
          if fliped[1] >= 4:
            self.board[13] = self.__index.flipDisk(self.board[13],5)
            self.board[24] = self.__index.flipDisk(self.board[24],2)
            self.board[32] = self.__index.flipDisk(self.board[32],5)
            if fliped[1] >= 5:
              self.board[14] = self.__index.flipDisk(self.board[14],5)
              self.board[25] = self.__index.flipDisk(self.board[25],1)
              self.board[31] = self.__index.flipDisk(self.board[31],5)
    self.board[9],fliped = self.__index.flipLine(self.board[9],5,color)
    if fliped[0] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],1);
      self.board[19] = self.__index.flipDisk(self.board[19],4);
      self.board[35] = self.__index.flipDisk(self.board[35],1);
      if fliped[0] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],1);
        self.board[18] = self.__index.flipDisk(self.board[18],3);
        self.board[34] = self.__index.flipDisk(self.board[34],1);
        if fliped[0] >= 3:
          self.board[2] = self.__index.flipDisk(self.board[2],1);
          self.board[17] = self.__index.flipDisk(self.board[17],2);
          self.board[33] = self.__index.flipDisk(self.board[33],1);
          if fliped[0] >= 4:
            self.board[1] = self.__index.flipDisk(self.board[1],1);
            self.board[16] = self.__index.flipDisk(self.board[16],1);
            self.board[32] = self.__index.flipDisk(self.board[32],1);
    if fliped[1] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],1);
      self.board[21] = self.__index.flipDisk(self.board[21],6);
      self.board[37] = self.__index.flipDisk(self.board[37],1);
    self.board[20],fliped = self.__index.flipLine(self.board[20],5,color);
    if fliped[0] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],2);
      self.board[10] = self.__index.flipDisk(self.board[10],4);
      self.board[34] = self.__index.flipDisk(self.board[34],2);
      if fliped[0] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],3);
        self.board[11] = self.__index.flipDisk(self.board[11],3);
        self.board[32] = self.__index.flipDisk(self.board[32],3);
        if fliped[0] >= 3:
          self.board[2] = self.__index.flipDisk(self.board[2],4);
          self.board[12] = self.__index.flipDisk(self.board[12],2);
          self.board[30] = self.__index.flipDisk(self.board[30],2);
          if fliped[0] >= 4:
            self.board[1] = self.__index.flipDisk(self.board[1],5);
            self.board[13] = self.__index.flipDisk(self.board[13],1);
            self.board[28] = self.__index.flipDisk(self.board[28],1);
    self.board[36],fliped = self.__index.flipLine(self.board[36],1,color);
    if fliped[1] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],2);
      self.board[10] = self.__index.flipDisk(self.board[10],6);
      self.board[22] = self.__index.flipDisk(self.board[22],5);
  def putAt42(self, color):
    self.board[5],fliped = self.__index.flipLine(self.board[5],2,color)
    if fliped[0] >= 1:
      self.board[9] = self.__index.flipDisk(self.board[9],5)
      self.board[20] = self.__index.flipDisk(self.board[20],5)
      self.board[36] = self.__index.flipDisk(self.board[36],1)
    if fliped[1] >= 1:
      self.board[11] = self.__index.flipDisk(self.board[11],5)
      self.board[22] = self.__index.flipDisk(self.board[22],4)
      self.board[34] = self.__index.flipDisk(self.board[34],3)
      if fliped[1] >= 2:
        self.board[12] = self.__index.flipDisk(self.board[12],5)
        self.board[23] = self.__index.flipDisk(self.board[23],3)
        self.board[33] = self.__index.flipDisk(self.board[33],4)
        if fliped[1] >= 3:
          self.board[13] = self.__index.flipDisk(self.board[13],5)
          self.board[24] = self.__index.flipDisk(self.board[24],2)
          self.board[32] = self.__index.flipDisk(self.board[32],5)
          if fliped[1] >= 4:
            self.board[14] = self.__index.flipDisk(self.board[14],5)
            self.board[25] = self.__index.flipDisk(self.board[25],1)
            self.board[31] = self.__index.flipDisk(self.board[31],5)
    self.board[10],fliped = self.__index.flipLine(self.board[10],5,color)
    if fliped[0] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],2);
      self.board[20] = self.__index.flipDisk(self.board[20],4);
      self.board[34] = self.__index.flipDisk(self.board[34],2);
      if fliped[0] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],2);
        self.board[19] = self.__index.flipDisk(self.board[19],3);
        self.board[33] = self.__index.flipDisk(self.board[33],2);
        if fliped[0] >= 3:
          self.board[2] = self.__index.flipDisk(self.board[2],2);
          self.board[18] = self.__index.flipDisk(self.board[18],2);
          self.board[32] = self.__index.flipDisk(self.board[32],2);
          if fliped[0] >= 4:
            self.board[1] = self.__index.flipDisk(self.board[1],2);
            self.board[17] = self.__index.flipDisk(self.board[17],1);
            self.board[31] = self.__index.flipDisk(self.board[31],1);
    if fliped[1] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],2);
      self.board[22] = self.__index.flipDisk(self.board[22],5);
      self.board[36] = self.__index.flipDisk(self.board[36],2);
    self.board[21],fliped = self.__index.flipLine(self.board[21],5,color);
    if fliped[0] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],3);
      self.board[11] = self.__index.flipDisk(self.board[11],4);
      self.board[33] = self.__index.flipDisk(self.board[33],3);
      if fliped[0] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],4);
        self.board[12] = self.__index.flipDisk(self.board[12],3);
        self.board[31] = self.__index.flipDisk(self.board[31],3);
        if fliped[0] >= 3:
          self.board[2] = self.__index.flipDisk(self.board[2],5);
          self.board[13] = self.__index.flipDisk(self.board[13],2);
          self.board[29] = self.__index.flipDisk(self.board[29],2);
          if fliped[0] >= 4:
            self.board[1] = self.__index.flipDisk(self.board[1],6);
            self.board[14] = self.__index.flipDisk(self.board[14],1);
            self.board[27] = self.__index.flipDisk(self.board[27],1);
    if fliped[1] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],1);
      self.board[9] = self.__index.flipDisk(self.board[9],6);
      self.board[37] = self.__index.flipDisk(self.board[37],1);
    self.board[35],fliped = self.__index.flipLine(self.board[35],2,color);
    if fliped[0] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],1);
      self.board[9] = self.__index.flipDisk(self.board[9],4);
      self.board[19] = self.__index.flipDisk(self.board[19],4);
    if fliped[1] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],3);
      self.board[11] = self.__index.flipDisk(self.board[11],6);
      self.board[23] = self.__index.flipDisk(self.board[23],4);
  def putAt43(self, color):
    self.board[5],fliped = self.__index.flipLine(self.board[5],3,color)
    if fliped[0] >= 1:
      self.board[10] = self.__index.flipDisk(self.board[10],5)
      self.board[21] = self.__index.flipDisk(self.board[21],5)
      self.board[35] = self.__index.flipDisk(self.board[35],2)
      if fliped[0] >= 2:
        self.board[9] = self.__index.flipDisk(self.board[9],5)
        self.board[20] = self.__index.flipDisk(self.board[20],5)
        self.board[36] = self.__index.flipDisk(self.board[36],1)
    if fliped[1] >= 1:
      self.board[12] = self.__index.flipDisk(self.board[12],5)
      self.board[23] = self.__index.flipDisk(self.board[23],3)
      self.board[33] = self.__index.flipDisk(self.board[33],4)
      if fliped[1] >= 2:
        self.board[13] = self.__index.flipDisk(self.board[13],5)
        self.board[24] = self.__index.flipDisk(self.board[24],2)
        self.board[32] = self.__index.flipDisk(self.board[32],5)
        if fliped[1] >= 3:
          self.board[14] = self.__index.flipDisk(self.board[14],5)
          self.board[25] = self.__index.flipDisk(self.board[25],1)
          self.board[31] = self.__index.flipDisk(self.board[31],5)
    self.board[11],fliped = self.__index.flipLine(self.board[11],5,color)
    if fliped[0] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],3);
      self.board[21] = self.__index.flipDisk(self.board[21],4);
      self.board[33] = self.__index.flipDisk(self.board[33],3);
      if fliped[0] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],3);
        self.board[20] = self.__index.flipDisk(self.board[20],3);
        self.board[32] = self.__index.flipDisk(self.board[32],3);
        if fliped[0] >= 3:
          self.board[2] = self.__index.flipDisk(self.board[2],3);
          self.board[19] = self.__index.flipDisk(self.board[19],2);
          self.board[31] = self.__index.flipDisk(self.board[31],2);
          if fliped[0] >= 4:
            self.board[1] = self.__index.flipDisk(self.board[1],3);
            self.board[18] = self.__index.flipDisk(self.board[18],1);
            self.board[30] = self.__index.flipDisk(self.board[30],1);
    if fliped[1] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],3);
      self.board[23] = self.__index.flipDisk(self.board[23],4);
      self.board[35] = self.__index.flipDisk(self.board[35],3);
    self.board[22],fliped = self.__index.flipLine(self.board[22],4,color);
    if fliped[0] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],4);
      self.board[12] = self.__index.flipDisk(self.board[12],4);
      self.board[32] = self.__index.flipDisk(self.board[32],4);
      if fliped[0] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],5);
        self.board[13] = self.__index.flipDisk(self.board[13],3);
        self.board[30] = self.__index.flipDisk(self.board[30],3);
        if fliped[0] >= 3:
          self.board[2] = self.__index.flipDisk(self.board[2],6);
          self.board[14] = self.__index.flipDisk(self.board[14],2);
          self.board[28] = self.__index.flipDisk(self.board[28],2);
    if fliped[1] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],2);
      self.board[10] = self.__index.flipDisk(self.board[10],6);
      self.board[36] = self.__index.flipDisk(self.board[36],2);
    self.board[34],fliped = self.__index.flipLine(self.board[34],3,color);
    if fliped[0] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],2);
      self.board[10] = self.__index.flipDisk(self.board[10],4);
      self.board[20] = self.__index.flipDisk(self.board[20],4);
      if fliped[0] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],1);
        self.board[9] = self.__index.flipDisk(self.board[9],3);
        self.board[18] = self.__index.flipDisk(self.board[18],3);
    if fliped[1] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],4);
      self.board[12] = self.__index.flipDisk(self.board[12],6);
      self.board[24] = self.__index.flipDisk(self.board[24],3);
  def putAt44(self, color):
    self.board[5],fliped = self.__index.flipLine(self.board[5],4,color)
    if fliped[0] >= 1:
      self.board[11] = self.__index.flipDisk(self.board[11],5)
      self.board[22] = self.__index.flipDisk(self.board[22],4)
      self.board[34] = self.__index.flipDisk(self.board[34],3)
      if fliped[0] >= 2:
        self.board[10] = self.__index.flipDisk(self.board[10],5)
        self.board[21] = self.__index.flipDisk(self.board[21],5)
        self.board[35] = self.__index.flipDisk(self.board[35],2)
        if fliped[0] >= 3:
          self.board[9] = self.__index.flipDisk(self.board[9],5)
          self.board[20] = self.__index.flipDisk(self.board[20],5)
          self.board[36] = self.__index.flipDisk(self.board[36],1)
    if fliped[1] >= 1:
      self.board[13] = self.__index.flipDisk(self.board[13],5)
      self.board[24] = self.__index.flipDisk(self.board[24],2)
      self.board[32] = self.__index.flipDisk(self.board[32],5)
      if fliped[1] >= 2:
        self.board[14] = self.__index.flipDisk(self.board[14],5)
        self.board[25] = self.__index.flipDisk(self.board[25],1)
        self.board[31] = self.__index.flipDisk(self.board[31],5)
    self.board[12],fliped = self.__index.flipLine(self.board[12],5,color)
    if fliped[0] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],4);
      self.board[22] = self.__index.flipDisk(self.board[22],3);
      self.board[32] = self.__index.flipDisk(self.board[32],4);
      if fliped[0] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],4);
        self.board[21] = self.__index.flipDisk(self.board[21],3);
        self.board[31] = self.__index.flipDisk(self.board[31],3);
        if fliped[0] >= 3:
          self.board[2] = self.__index.flipDisk(self.board[2],4);
          self.board[20] = self.__index.flipDisk(self.board[20],2);
          self.board[30] = self.__index.flipDisk(self.board[30],2);
          if fliped[0] >= 4:
            self.board[1] = self.__index.flipDisk(self.board[1],4);
            self.board[19] = self.__index.flipDisk(self.board[19],1);
            self.board[29] = self.__index.flipDisk(self.board[29],1);
    if fliped[1] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],4);
      self.board[24] = self.__index.flipDisk(self.board[24],3);
      self.board[34] = self.__index.flipDisk(self.board[34],4);
    self.board[23],fliped = self.__index.flipLine(self.board[23],3,color);
    if fliped[0] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],5);
      self.board[13] = self.__index.flipDisk(self.board[13],4);
      self.board[31] = self.__index.flipDisk(self.board[31],4);
      if fliped[0] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],6);
        self.board[14] = self.__index.flipDisk(self.board[14],3);
        self.board[29] = self.__index.flipDisk(self.board[29],3);
    if fliped[1] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],3);
      self.board[11] = self.__index.flipDisk(self.board[11],6);
      self.board[35] = self.__index.flipDisk(self.board[35],3);
    self.board[33],fliped = self.__index.flipLine(self.board[33],4,color);
    if fliped[0] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],3);
      self.board[11] = self.__index.flipDisk(self.board[11],4);
      self.board[21] = self.__index.flipDisk(self.board[21],4);
      if fliped[0] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],2);
        self.board[10] = self.__index.flipDisk(self.board[10],3);
        self.board[19] = self.__index.flipDisk(self.board[19],3);
        if fliped[0] >= 3:
          self.board[2] = self.__index.flipDisk(self.board[2],1);
          self.board[9] = self.__index.flipDisk(self.board[9],2);
          self.board[17] = self.__index.flipDisk(self.board[17],2);
    if fliped[1] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],5);
      self.board[13] = self.__index.flipDisk(self.board[13],6);
      self.board[25] = self.__index.flipDisk(self.board[25],2);
  def putAt45(self, color):
    self.board[5],fliped = self.__index.flipLine(self.board[5],5,color)
    if fliped[0] >= 1:
      self.board[12] = self.__index.flipDisk(self.board[12],5)
      self.board[23] = self.__index.flipDisk(self.board[23],3)
      self.board[33] = self.__index.flipDisk(self.board[33],4)
      if fliped[0] >= 2:
        self.board[11] = self.__index.flipDisk(self.board[11],5)
        self.board[22] = self.__index.flipDisk(self.board[22],4)
        self.board[34] = self.__index.flipDisk(self.board[34],3)
        if fliped[0] >= 3:
          self.board[10] = self.__index.flipDisk(self.board[10],5)
          self.board[21] = self.__index.flipDisk(self.board[21],5)
          self.board[35] = self.__index.flipDisk(self.board[35],2)
          if fliped[0] >= 4:
            self.board[9] = self.__index.flipDisk(self.board[9],5)
            self.board[20] = self.__index.flipDisk(self.board[20],5)
            self.board[36] = self.__index.flipDisk(self.board[36],1)
    if fliped[1] >= 1:
      self.board[14] = self.__index.flipDisk(self.board[14],5)
      self.board[25] = self.__index.flipDisk(self.board[25],1)
      self.board[31] = self.__index.flipDisk(self.board[31],5)
    self.board[13],fliped = self.__index.flipLine(self.board[13],5,color)
    if fliped[0] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],5);
      self.board[23] = self.__index.flipDisk(self.board[23],2);
      self.board[31] = self.__index.flipDisk(self.board[31],4);
      if fliped[0] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],5);
        self.board[22] = self.__index.flipDisk(self.board[22],2);
        self.board[30] = self.__index.flipDisk(self.board[30],3);
        if fliped[0] >= 3:
          self.board[2] = self.__index.flipDisk(self.board[2],5);
          self.board[21] = self.__index.flipDisk(self.board[21],2);
          self.board[29] = self.__index.flipDisk(self.board[29],2);
          if fliped[0] >= 4:
            self.board[1] = self.__index.flipDisk(self.board[1],5);
            self.board[20] = self.__index.flipDisk(self.board[20],1);
            self.board[28] = self.__index.flipDisk(self.board[28],1);
    if fliped[1] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],5);
      self.board[25] = self.__index.flipDisk(self.board[25],2);
      self.board[33] = self.__index.flipDisk(self.board[33],5);
    self.board[24],fliped = self.__index.flipLine(self.board[24],2,color);
    if fliped[0] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],6);
      self.board[14] = self.__index.flipDisk(self.board[14],4);
      self.board[30] = self.__index.flipDisk(self.board[30],4);
    if fliped[1] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],4);
      self.board[12] = self.__index.flipDisk(self.board[12],6);
      self.board[34] = self.__index.flipDisk(self.board[34],4);
    self.board[32],fliped = self.__index.flipLine(self.board[32],5,color);
    if fliped[0] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],4);
      self.board[12] = self.__index.flipDisk(self.board[12],4);
      self.board[22] = self.__index.flipDisk(self.board[22],3);
      if fliped[0] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],3);
        self.board[11] = self.__index.flipDisk(self.board[11],3);
        self.board[20] = self.__index.flipDisk(self.board[20],3);
        if fliped[0] >= 3:
          self.board[2] = self.__index.flipDisk(self.board[2],2);
          self.board[10] = self.__index.flipDisk(self.board[10],2);
          self.board[18] = self.__index.flipDisk(self.board[18],2);
          if fliped[0] >= 4:
            self.board[1] = self.__index.flipDisk(self.board[1],1);
            self.board[9] = self.__index.flipDisk(self.board[9],1);
            self.board[16] = self.__index.flipDisk(self.board[16],1);
    if fliped[1] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],6);
      self.board[14] = self.__index.flipDisk(self.board[14],6);
      self.board[26] = self.__index.flipDisk(self.board[26],1);
  def putAt46(self, color):
    self.board[5],fliped = self.__index.flipLine(self.board[5],6,color)
    if fliped[0] >= 1:
      self.board[13] = self.__index.flipDisk(self.board[13],5)
      self.board[24] = self.__index.flipDisk(self.board[24],2)
      self.board[32] = self.__index.flipDisk(self.board[32],5)
      if fliped[0] >= 2:
        self.board[12] = self.__index.flipDisk(self.board[12],5)
        self.board[23] = self.__index.flipDisk(self.board[23],3)
        self.board[33] = self.__index.flipDisk(self.board[33],4)
        if fliped[0] >= 3:
          self.board[11] = self.__index.flipDisk(self.board[11],5)
          self.board[22] = self.__index.flipDisk(self.board[22],4)
          self.board[34] = self.__index.flipDisk(self.board[34],3)
          if fliped[0] >= 4:
            self.board[10] = self.__index.flipDisk(self.board[10],5)
            self.board[21] = self.__index.flipDisk(self.board[21],5)
            self.board[35] = self.__index.flipDisk(self.board[35],2)
            if fliped[0] >= 5:
              self.board[9] = self.__index.flipDisk(self.board[9],5)
              self.board[20] = self.__index.flipDisk(self.board[20],5)
              self.board[36] = self.__index.flipDisk(self.board[36],1)
    self.board[14],fliped = self.__index.flipLine(self.board[14],5,color)
    if fliped[0] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],6);
      self.board[24] = self.__index.flipDisk(self.board[24],1);
      self.board[30] = self.__index.flipDisk(self.board[30],4);
      if fliped[0] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],6);
        self.board[23] = self.__index.flipDisk(self.board[23],1);
        self.board[29] = self.__index.flipDisk(self.board[29],3);
        if fliped[0] >= 3:
          self.board[2] = self.__index.flipDisk(self.board[2],6);
          self.board[22] = self.__index.flipDisk(self.board[22],1);
          self.board[28] = self.__index.flipDisk(self.board[28],2);
          if fliped[0] >= 4:
            self.board[1] = self.__index.flipDisk(self.board[1],6);
            self.board[21] = self.__index.flipDisk(self.board[21],1);
            self.board[27] = self.__index.flipDisk(self.board[27],1);
    if fliped[1] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],6);
      self.board[26] = self.__index.flipDisk(self.board[26],1);
      self.board[32] = self.__index.flipDisk(self.board[32],6);
    self.board[25],fliped = self.__index.flipLine(self.board[25],1,color);
    if fliped[1] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],5);
      self.board[13] = self.__index.flipDisk(self.board[13],6);
      self.board[33] = self.__index.flipDisk(self.board[33],5);
    self.board[31],fliped = self.__index.flipLine(self.board[31],5,color);
    if fliped[0] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],5);
      self.board[13] = self.__index.flipDisk(self.board[13],4);
      self.board[23] = self.__index.flipDisk(self.board[23],2);
      if fliped[0] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],4);
        self.board[12] = self.__index.flipDisk(self.board[12],3);
        self.board[21] = self.__index.flipDisk(self.board[21],3);
        if fliped[0] >= 3:
          self.board[2] = self.__index.flipDisk(self.board[2],3);
          self.board[11] = self.__index.flipDisk(self.board[11],2);
          self.board[19] = self.__index.flipDisk(self.board[19],2);
          if fliped[0] >= 4:
            self.board[1] = self.__index.flipDisk(self.board[1],2);
            self.board[10] = self.__index.flipDisk(self.board[10],1);
            self.board[17] = self.__index.flipDisk(self.board[17],1);
  def putAt47(self, color):
    self.board[5],fliped = self.__index.flipLine(self.board[5],7,color)
    if fliped[0] >= 1:
      self.board[14] = self.__index.flipDisk(self.board[14],5)
      self.board[25] = self.__index.flipDisk(self.board[25],1)
      self.board[31] = self.__index.flipDisk(self.board[31],5)
      if fliped[0] >= 2:
        self.board[13] = self.__index.flipDisk(self.board[13],5)
        self.board[24] = self.__index.flipDisk(self.board[24],2)
        self.board[32] = self.__index.flipDisk(self.board[32],5)
        if fliped[0] >= 3:
          self.board[12] = self.__index.flipDisk(self.board[12],5)
          self.board[23] = self.__index.flipDisk(self.board[23],3)
          self.board[33] = self.__index.flipDisk(self.board[33],4)
          if fliped[0] >= 4:
            self.board[11] = self.__index.flipDisk(self.board[11],5)
            self.board[22] = self.__index.flipDisk(self.board[22],4)
            self.board[34] = self.__index.flipDisk(self.board[34],3)
            if fliped[0] >= 5:
              self.board[10] = self.__index.flipDisk(self.board[10],5)
              self.board[21] = self.__index.flipDisk(self.board[21],5)
              self.board[35] = self.__index.flipDisk(self.board[35],2)
              if fliped[0] >= 6:
                self.board[9] = self.__index.flipDisk(self.board[9],5)
                self.board[20] = self.__index.flipDisk(self.board[20],5)
                self.board[36] = self.__index.flipDisk(self.board[36],1)
    self.board[15],fliped = self.__index.flipLine(self.board[15],5,color)
    if fliped[0] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],7);
      self.board[25] = self.__index.flipDisk(self.board[25],0);
      self.board[29] = self.__index.flipDisk(self.board[29],4);
      if fliped[0] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],7);
        self.board[24] = self.__index.flipDisk(self.board[24],0);
        self.board[28] = self.__index.flipDisk(self.board[28],3);
        if fliped[0] >= 3:
          self.board[2] = self.__index.flipDisk(self.board[2],7);
          self.board[23] = self.__index.flipDisk(self.board[23],0);
          self.board[27] = self.__index.flipDisk(self.board[27],2);
          if fliped[0] >= 4:
            self.board[1] = self.__index.flipDisk(self.board[1],7);
            self.board[22] = self.__index.flipDisk(self.board[22],0);
    if fliped[1] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],7);
      self.board[31] = self.__index.flipDisk(self.board[31],6);
    self.board[26],fliped = self.__index.flipLine(self.board[26],0,color);
    if fliped[1] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],6);
      self.board[14] = self.__index.flipDisk(self.board[14],6);
      self.board[32] = self.__index.flipDisk(self.board[32],6);
    self.board[30],fliped = self.__index.flipLine(self.board[30],5,color);
    if fliped[0] >= 1:
      self.board[4] = self.__index.flipDisk(self.board[4],6);
      self.board[14] = self.__index.flipDisk(self.board[14],4);
      self.board[24] = self.__index.flipDisk(self.board[24],1);
      if fliped[0] >= 2:
        self.board[3] = self.__index.flipDisk(self.board[3],5);
        self.board[13] = self.__index.flipDisk(self.board[13],3);
        self.board[22] = self.__index.flipDisk(self.board[22],2);
        if fliped[0] >= 3:
          self.board[2] = self.__index.flipDisk(self.board[2],4);
          self.board[12] = self.__index.flipDisk(self.board[12],2);
          self.board[20] = self.__index.flipDisk(self.board[20],2);
          if fliped[0] >= 4:
            self.board[1] = self.__index.flipDisk(self.board[1],3);
            self.board[11] = self.__index.flipDisk(self.board[11],1);
            self.board[18] = self.__index.flipDisk(self.board[18],1);
  def putAt48(self, color):
    self.board[6],fliped = self.__index.flipLine(self.board[6],0,color)
    if fliped[1] >= 1:
      self.board[9] = self.__index.flipDisk(self.board[9],6)
      self.board[21] = self.__index.flipDisk(self.board[21],6)
      self.board[37] = self.__index.flipDisk(self.board[37],1)
      if fliped[1] >= 2:
        self.board[10] = self.__index.flipDisk(self.board[10],6)
        self.board[22] = self.__index.flipDisk(self.board[22],5)
        self.board[36] = self.__index.flipDisk(self.board[36],2)
        if fliped[1] >= 3:
          self.board[11] = self.__index.flipDisk(self.board[11],6)
          self.board[23] = self.__index.flipDisk(self.board[23],4)
          self.board[35] = self.__index.flipDisk(self.board[35],3)
          if fliped[1] >= 4:
            self.board[12] = self.__index.flipDisk(self.board[12],6)
            self.board[24] = self.__index.flipDisk(self.board[24],3)
            self.board[34] = self.__index.flipDisk(self.board[34],4)
            if fliped[1] >= 5:
              self.board[13] = self.__index.flipDisk(self.board[13],6)
              self.board[25] = self.__index.flipDisk(self.board[25],2)
              self.board[33] = self.__index.flipDisk(self.board[33],5)
              if fliped[1] >= 6:
                self.board[14] = self.__index.flipDisk(self.board[14],6)
                self.board[26] = self.__index.flipDisk(self.board[26],1)
                self.board[32] = self.__index.flipDisk(self.board[32],6)
    self.board[8],fliped = self.__index.flipLine(self.board[8],6,color)
    if fliped[0] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],0);
      self.board[19] = self.__index.flipDisk(self.board[19],5);
      self.board[37] = self.__index.flipDisk(self.board[37],0);
      if fliped[0] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],0);
        self.board[18] = self.__index.flipDisk(self.board[18],4);
        self.board[36] = self.__index.flipDisk(self.board[36],0);
        if fliped[0] >= 3:
          self.board[3] = self.__index.flipDisk(self.board[3],0);
          self.board[17] = self.__index.flipDisk(self.board[17],3);
          self.board[35] = self.__index.flipDisk(self.board[35],0);
          if fliped[0] >= 4:
            self.board[2] = self.__index.flipDisk(self.board[2],0);
            self.board[16] = self.__index.flipDisk(self.board[16],2);
            self.board[34] = self.__index.flipDisk(self.board[34],0);
            if fliped[0] >= 5:
              self.board[1] = self.__index.flipDisk(self.board[1],0);
              self.board[33] = self.__index.flipDisk(self.board[33],0);
    self.board[20],fliped = self.__index.flipLine(self.board[20],6,color);
    if fliped[0] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],1);
      self.board[9] = self.__index.flipDisk(self.board[9],5);
      self.board[36] = self.__index.flipDisk(self.board[36],1);
      if fliped[0] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],2);
        self.board[10] = self.__index.flipDisk(self.board[10],4);
        self.board[34] = self.__index.flipDisk(self.board[34],2);
        if fliped[0] >= 3:
          self.board[3] = self.__index.flipDisk(self.board[3],3);
          self.board[11] = self.__index.flipDisk(self.board[11],3);
          self.board[32] = self.__index.flipDisk(self.board[32],3);
          if fliped[0] >= 4:
            self.board[2] = self.__index.flipDisk(self.board[2],4);
            self.board[12] = self.__index.flipDisk(self.board[12],2);
            self.board[30] = self.__index.flipDisk(self.board[30],2);
            if fliped[0] >= 5:
              self.board[1] = self.__index.flipDisk(self.board[1],5);
              self.board[13] = self.__index.flipDisk(self.board[13],1);
              self.board[28] = self.__index.flipDisk(self.board[28],1);
  def putAt49(self, color):
    self.board[6],fliped = self.__index.flipLine(self.board[6],1,color)
    if fliped[1] >= 1:
      self.board[10] = self.__index.flipDisk(self.board[10],6)
      self.board[22] = self.__index.flipDisk(self.board[22],5)
      self.board[36] = self.__index.flipDisk(self.board[36],2)
      if fliped[1] >= 2:
        self.board[11] = self.__index.flipDisk(self.board[11],6)
        self.board[23] = self.__index.flipDisk(self.board[23],4)
        self.board[35] = self.__index.flipDisk(self.board[35],3)
        if fliped[1] >= 3:
          self.board[12] = self.__index.flipDisk(self.board[12],6)
          self.board[24] = self.__index.flipDisk(self.board[24],3)
          self.board[34] = self.__index.flipDisk(self.board[34],4)
          if fliped[1] >= 4:
            self.board[13] = self.__index.flipDisk(self.board[13],6)
            self.board[25] = self.__index.flipDisk(self.board[25],2)
            self.board[33] = self.__index.flipDisk(self.board[33],5)
            if fliped[1] >= 5:
              self.board[14] = self.__index.flipDisk(self.board[14],6)
              self.board[26] = self.__index.flipDisk(self.board[26],1)
              self.board[32] = self.__index.flipDisk(self.board[32],6)
    self.board[9],fliped = self.__index.flipLine(self.board[9],6,color)
    if fliped[0] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],1);
      self.board[20] = self.__index.flipDisk(self.board[20],5);
      self.board[36] = self.__index.flipDisk(self.board[36],1);
      if fliped[0] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],1);
        self.board[19] = self.__index.flipDisk(self.board[19],4);
        self.board[35] = self.__index.flipDisk(self.board[35],1);
        if fliped[0] >= 3:
          self.board[3] = self.__index.flipDisk(self.board[3],1);
          self.board[18] = self.__index.flipDisk(self.board[18],3);
          self.board[34] = self.__index.flipDisk(self.board[34],1);
          if fliped[0] >= 4:
            self.board[2] = self.__index.flipDisk(self.board[2],1);
            self.board[17] = self.__index.flipDisk(self.board[17],2);
            self.board[33] = self.__index.flipDisk(self.board[33],1);
            if fliped[0] >= 5:
              self.board[1] = self.__index.flipDisk(self.board[1],1);
              self.board[16] = self.__index.flipDisk(self.board[16],1);
              self.board[32] = self.__index.flipDisk(self.board[32],1);
    self.board[21],fliped = self.__index.flipLine(self.board[21],6,color);
    if fliped[0] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],2);
      self.board[10] = self.__index.flipDisk(self.board[10],5);
      self.board[35] = self.__index.flipDisk(self.board[35],2);
      if fliped[0] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],3);
        self.board[11] = self.__index.flipDisk(self.board[11],4);
        self.board[33] = self.__index.flipDisk(self.board[33],3);
        if fliped[0] >= 3:
          self.board[3] = self.__index.flipDisk(self.board[3],4);
          self.board[12] = self.__index.flipDisk(self.board[12],3);
          self.board[31] = self.__index.flipDisk(self.board[31],3);
          if fliped[0] >= 4:
            self.board[2] = self.__index.flipDisk(self.board[2],5);
            self.board[13] = self.__index.flipDisk(self.board[13],2);
            self.board[29] = self.__index.flipDisk(self.board[29],2);
            if fliped[0] >= 5:
              self.board[1] = self.__index.flipDisk(self.board[1],6);
              self.board[14] = self.__index.flipDisk(self.board[14],1);
              self.board[27] = self.__index.flipDisk(self.board[27],1);
    self.board[37],fliped = self.__index.flipLine(self.board[37],1,color);
  def putAt50(self, color):
    self.board[6],fliped = self.__index.flipLine(self.board[6],2,color)
    if fliped[0] >= 1:
      self.board[9] = self.__index.flipDisk(self.board[9],6)
      self.board[21] = self.__index.flipDisk(self.board[21],6)
      self.board[37] = self.__index.flipDisk(self.board[37],1)
    if fliped[1] >= 1:
      self.board[11] = self.__index.flipDisk(self.board[11],6)
      self.board[23] = self.__index.flipDisk(self.board[23],4)
      self.board[35] = self.__index.flipDisk(self.board[35],3)
      if fliped[1] >= 2:
        self.board[12] = self.__index.flipDisk(self.board[12],6)
        self.board[24] = self.__index.flipDisk(self.board[24],3)
        self.board[34] = self.__index.flipDisk(self.board[34],4)
        if fliped[1] >= 3:
          self.board[13] = self.__index.flipDisk(self.board[13],6)
          self.board[25] = self.__index.flipDisk(self.board[25],2)
          self.board[33] = self.__index.flipDisk(self.board[33],5)
          if fliped[1] >= 4:
            self.board[14] = self.__index.flipDisk(self.board[14],6)
            self.board[26] = self.__index.flipDisk(self.board[26],1)
            self.board[32] = self.__index.flipDisk(self.board[32],6)
    self.board[10],fliped = self.__index.flipLine(self.board[10],6,color)
    if fliped[0] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],2);
      self.board[21] = self.__index.flipDisk(self.board[21],5);
      self.board[35] = self.__index.flipDisk(self.board[35],2);
      if fliped[0] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],2);
        self.board[20] = self.__index.flipDisk(self.board[20],4);
        self.board[34] = self.__index.flipDisk(self.board[34],2);
        if fliped[0] >= 3:
          self.board[3] = self.__index.flipDisk(self.board[3],2);
          self.board[19] = self.__index.flipDisk(self.board[19],3);
          self.board[33] = self.__index.flipDisk(self.board[33],2);
          if fliped[0] >= 4:
            self.board[2] = self.__index.flipDisk(self.board[2],2);
            self.board[18] = self.__index.flipDisk(self.board[18],2);
            self.board[32] = self.__index.flipDisk(self.board[32],2);
            if fliped[0] >= 5:
              self.board[1] = self.__index.flipDisk(self.board[1],2);
              self.board[17] = self.__index.flipDisk(self.board[17],1);
              self.board[31] = self.__index.flipDisk(self.board[31],1);
    self.board[22],fliped = self.__index.flipLine(self.board[22],5,color);
    if fliped[0] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],3);
      self.board[11] = self.__index.flipDisk(self.board[11],5);
      self.board[34] = self.__index.flipDisk(self.board[34],3);
      if fliped[0] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],4);
        self.board[12] = self.__index.flipDisk(self.board[12],4);
        self.board[32] = self.__index.flipDisk(self.board[32],4);
        if fliped[0] >= 3:
          self.board[3] = self.__index.flipDisk(self.board[3],5);
          self.board[13] = self.__index.flipDisk(self.board[13],3);
          self.board[30] = self.__index.flipDisk(self.board[30],3);
          if fliped[0] >= 4:
            self.board[2] = self.__index.flipDisk(self.board[2],6);
            self.board[14] = self.__index.flipDisk(self.board[14],2);
            self.board[28] = self.__index.flipDisk(self.board[28],2);
    self.board[36],fliped = self.__index.flipLine(self.board[36],2,color);
    if fliped[0] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],1);
      self.board[9] = self.__index.flipDisk(self.board[9],5);
      self.board[20] = self.__index.flipDisk(self.board[20],5);
  def putAt51(self, color):
    self.board[6],fliped = self.__index.flipLine(self.board[6],3,color)
    if fliped[0] >= 1:
      self.board[10] = self.__index.flipDisk(self.board[10],6)
      self.board[22] = self.__index.flipDisk(self.board[22],5)
      self.board[36] = self.__index.flipDisk(self.board[36],2)
      if fliped[0] >= 2:
        self.board[9] = self.__index.flipDisk(self.board[9],6)
        self.board[21] = self.__index.flipDisk(self.board[21],6)
        self.board[37] = self.__index.flipDisk(self.board[37],1)
    if fliped[1] >= 1:
      self.board[12] = self.__index.flipDisk(self.board[12],6)
      self.board[24] = self.__index.flipDisk(self.board[24],3)
      self.board[34] = self.__index.flipDisk(self.board[34],4)
      if fliped[1] >= 2:
        self.board[13] = self.__index.flipDisk(self.board[13],6)
        self.board[25] = self.__index.flipDisk(self.board[25],2)
        self.board[33] = self.__index.flipDisk(self.board[33],5)
        if fliped[1] >= 3:
          self.board[14] = self.__index.flipDisk(self.board[14],6)
          self.board[26] = self.__index.flipDisk(self.board[26],1)
          self.board[32] = self.__index.flipDisk(self.board[32],6)
    self.board[11],fliped = self.__index.flipLine(self.board[11],6,color)
    if fliped[0] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],3);
      self.board[22] = self.__index.flipDisk(self.board[22],4);
      self.board[34] = self.__index.flipDisk(self.board[34],3);
      if fliped[0] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],3);
        self.board[21] = self.__index.flipDisk(self.board[21],4);
        self.board[33] = self.__index.flipDisk(self.board[33],3);
        if fliped[0] >= 3:
          self.board[3] = self.__index.flipDisk(self.board[3],3);
          self.board[20] = self.__index.flipDisk(self.board[20],3);
          self.board[32] = self.__index.flipDisk(self.board[32],3);
          if fliped[0] >= 4:
            self.board[2] = self.__index.flipDisk(self.board[2],3);
            self.board[19] = self.__index.flipDisk(self.board[19],2);
            self.board[31] = self.__index.flipDisk(self.board[31],2);
            if fliped[0] >= 5:
              self.board[1] = self.__index.flipDisk(self.board[1],3);
              self.board[18] = self.__index.flipDisk(self.board[18],1);
              self.board[30] = self.__index.flipDisk(self.board[30],1);
    self.board[23],fliped = self.__index.flipLine(self.board[23],4,color);
    if fliped[0] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],4);
      self.board[12] = self.__index.flipDisk(self.board[12],5);
      self.board[33] = self.__index.flipDisk(self.board[33],4);
      if fliped[0] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],5);
        self.board[13] = self.__index.flipDisk(self.board[13],4);
        self.board[31] = self.__index.flipDisk(self.board[31],4);
        if fliped[0] >= 3:
          self.board[3] = self.__index.flipDisk(self.board[3],6);
          self.board[14] = self.__index.flipDisk(self.board[14],3);
          self.board[29] = self.__index.flipDisk(self.board[29],3);
    self.board[35],fliped = self.__index.flipLine(self.board[35],3,color);
    if fliped[0] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],2);
      self.board[10] = self.__index.flipDisk(self.board[10],5);
      self.board[21] = self.__index.flipDisk(self.board[21],5);
      if fliped[0] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],1);
        self.board[9] = self.__index.flipDisk(self.board[9],4);
        self.board[19] = self.__index.flipDisk(self.board[19],4);
  def putAt52(self, color):
    self.board[6],fliped = self.__index.flipLine(self.board[6],4,color)
    if fliped[0] >= 1:
      self.board[11] = self.__index.flipDisk(self.board[11],6)
      self.board[23] = self.__index.flipDisk(self.board[23],4)
      self.board[35] = self.__index.flipDisk(self.board[35],3)
      if fliped[0] >= 2:
        self.board[10] = self.__index.flipDisk(self.board[10],6)
        self.board[22] = self.__index.flipDisk(self.board[22],5)
        self.board[36] = self.__index.flipDisk(self.board[36],2)
        if fliped[0] >= 3:
          self.board[9] = self.__index.flipDisk(self.board[9],6)
          self.board[21] = self.__index.flipDisk(self.board[21],6)
          self.board[37] = self.__index.flipDisk(self.board[37],1)
    if fliped[1] >= 1:
      self.board[13] = self.__index.flipDisk(self.board[13],6)
      self.board[25] = self.__index.flipDisk(self.board[25],2)
      self.board[33] = self.__index.flipDisk(self.board[33],5)
      if fliped[1] >= 2:
        self.board[14] = self.__index.flipDisk(self.board[14],6)
        self.board[26] = self.__index.flipDisk(self.board[26],1)
        self.board[32] = self.__index.flipDisk(self.board[32],6)
    self.board[12],fliped = self.__index.flipLine(self.board[12],6,color)
    if fliped[0] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],4);
      self.board[23] = self.__index.flipDisk(self.board[23],3);
      self.board[33] = self.__index.flipDisk(self.board[33],4);
      if fliped[0] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],4);
        self.board[22] = self.__index.flipDisk(self.board[22],3);
        self.board[32] = self.__index.flipDisk(self.board[32],4);
        if fliped[0] >= 3:
          self.board[3] = self.__index.flipDisk(self.board[3],4);
          self.board[21] = self.__index.flipDisk(self.board[21],3);
          self.board[31] = self.__index.flipDisk(self.board[31],3);
          if fliped[0] >= 4:
            self.board[2] = self.__index.flipDisk(self.board[2],4);
            self.board[20] = self.__index.flipDisk(self.board[20],2);
            self.board[30] = self.__index.flipDisk(self.board[30],2);
            if fliped[0] >= 5:
              self.board[1] = self.__index.flipDisk(self.board[1],4);
              self.board[19] = self.__index.flipDisk(self.board[19],1);
              self.board[29] = self.__index.flipDisk(self.board[29],1);
    self.board[24],fliped = self.__index.flipLine(self.board[24],3,color);
    if fliped[0] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],5);
      self.board[13] = self.__index.flipDisk(self.board[13],5);
      self.board[32] = self.__index.flipDisk(self.board[32],5);
      if fliped[0] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],6);
        self.board[14] = self.__index.flipDisk(self.board[14],4);
        self.board[30] = self.__index.flipDisk(self.board[30],4);
    self.board[34],fliped = self.__index.flipLine(self.board[34],4,color);
    if fliped[0] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],3);
      self.board[11] = self.__index.flipDisk(self.board[11],5);
      self.board[22] = self.__index.flipDisk(self.board[22],4);
      if fliped[0] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],2);
        self.board[10] = self.__index.flipDisk(self.board[10],4);
        self.board[20] = self.__index.flipDisk(self.board[20],4);
        if fliped[0] >= 3:
          self.board[3] = self.__index.flipDisk(self.board[3],1);
          self.board[9] = self.__index.flipDisk(self.board[9],3);
          self.board[18] = self.__index.flipDisk(self.board[18],3);
  def putAt53(self, color):
    self.board[6],fliped = self.__index.flipLine(self.board[6],5,color)
    if fliped[0] >= 1:
      self.board[12] = self.__index.flipDisk(self.board[12],6)
      self.board[24] = self.__index.flipDisk(self.board[24],3)
      self.board[34] = self.__index.flipDisk(self.board[34],4)
      if fliped[0] >= 2:
        self.board[11] = self.__index.flipDisk(self.board[11],6)
        self.board[23] = self.__index.flipDisk(self.board[23],4)
        self.board[35] = self.__index.flipDisk(self.board[35],3)
        if fliped[0] >= 3:
          self.board[10] = self.__index.flipDisk(self.board[10],6)
          self.board[22] = self.__index.flipDisk(self.board[22],5)
          self.board[36] = self.__index.flipDisk(self.board[36],2)
          if fliped[0] >= 4:
            self.board[9] = self.__index.flipDisk(self.board[9],6)
            self.board[21] = self.__index.flipDisk(self.board[21],6)
            self.board[37] = self.__index.flipDisk(self.board[37],1)
    if fliped[1] >= 1:
      self.board[14] = self.__index.flipDisk(self.board[14],6)
      self.board[26] = self.__index.flipDisk(self.board[26],1)
      self.board[32] = self.__index.flipDisk(self.board[32],6)
    self.board[13],fliped = self.__index.flipLine(self.board[13],6,color)
    if fliped[0] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],5);
      self.board[24] = self.__index.flipDisk(self.board[24],2);
      self.board[32] = self.__index.flipDisk(self.board[32],5);
      if fliped[0] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],5);
        self.board[23] = self.__index.flipDisk(self.board[23],2);
        self.board[31] = self.__index.flipDisk(self.board[31],4);
        if fliped[0] >= 3:
          self.board[3] = self.__index.flipDisk(self.board[3],5);
          self.board[22] = self.__index.flipDisk(self.board[22],2);
          self.board[30] = self.__index.flipDisk(self.board[30],3);
          if fliped[0] >= 4:
            self.board[2] = self.__index.flipDisk(self.board[2],5);
            self.board[21] = self.__index.flipDisk(self.board[21],2);
            self.board[29] = self.__index.flipDisk(self.board[29],2);
            if fliped[0] >= 5:
              self.board[1] = self.__index.flipDisk(self.board[1],5);
              self.board[20] = self.__index.flipDisk(self.board[20],1);
              self.board[28] = self.__index.flipDisk(self.board[28],1);
    self.board[25],fliped = self.__index.flipLine(self.board[25],2,color);
    if fliped[0] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],6);
      self.board[14] = self.__index.flipDisk(self.board[14],5);
      self.board[31] = self.__index.flipDisk(self.board[31],5);
    self.board[33],fliped = self.__index.flipLine(self.board[33],5,color);
    if fliped[0] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],4);
      self.board[12] = self.__index.flipDisk(self.board[12],5);
      self.board[23] = self.__index.flipDisk(self.board[23],3);
      if fliped[0] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],3);
        self.board[11] = self.__index.flipDisk(self.board[11],4);
        self.board[21] = self.__index.flipDisk(self.board[21],4);
        if fliped[0] >= 3:
          self.board[3] = self.__index.flipDisk(self.board[3],2);
          self.board[10] = self.__index.flipDisk(self.board[10],3);
          self.board[19] = self.__index.flipDisk(self.board[19],3);
          if fliped[0] >= 4:
            self.board[2] = self.__index.flipDisk(self.board[2],1);
            self.board[9] = self.__index.flipDisk(self.board[9],2);
            self.board[17] = self.__index.flipDisk(self.board[17],2);
  def putAt54(self, color):
    self.board[6],fliped = self.__index.flipLine(self.board[6],6,color)
    if fliped[0] >= 1:
      self.board[13] = self.__index.flipDisk(self.board[13],6)
      self.board[25] = self.__index.flipDisk(self.board[25],2)
      self.board[33] = self.__index.flipDisk(self.board[33],5)
      if fliped[0] >= 2:
        self.board[12] = self.__index.flipDisk(self.board[12],6)
        self.board[24] = self.__index.flipDisk(self.board[24],3)
        self.board[34] = self.__index.flipDisk(self.board[34],4)
        if fliped[0] >= 3:
          self.board[11] = self.__index.flipDisk(self.board[11],6)
          self.board[23] = self.__index.flipDisk(self.board[23],4)
          self.board[35] = self.__index.flipDisk(self.board[35],3)
          if fliped[0] >= 4:
            self.board[10] = self.__index.flipDisk(self.board[10],6)
            self.board[22] = self.__index.flipDisk(self.board[22],5)
            self.board[36] = self.__index.flipDisk(self.board[36],2)
            if fliped[0] >= 5:
              self.board[9] = self.__index.flipDisk(self.board[9],6)
              self.board[21] = self.__index.flipDisk(self.board[21],6)
              self.board[37] = self.__index.flipDisk(self.board[37],1)
    self.board[14],fliped = self.__index.flipLine(self.board[14],6,color)
    if fliped[0] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],6);
      self.board[25] = self.__index.flipDisk(self.board[25],1);
      self.board[31] = self.__index.flipDisk(self.board[31],5);
      if fliped[0] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],6);
        self.board[24] = self.__index.flipDisk(self.board[24],1);
        self.board[30] = self.__index.flipDisk(self.board[30],4);
        if fliped[0] >= 3:
          self.board[3] = self.__index.flipDisk(self.board[3],6);
          self.board[23] = self.__index.flipDisk(self.board[23],1);
          self.board[29] = self.__index.flipDisk(self.board[29],3);
          if fliped[0] >= 4:
            self.board[2] = self.__index.flipDisk(self.board[2],6);
            self.board[22] = self.__index.flipDisk(self.board[22],1);
            self.board[28] = self.__index.flipDisk(self.board[28],2);
            if fliped[0] >= 5:
              self.board[1] = self.__index.flipDisk(self.board[1],6);
              self.board[21] = self.__index.flipDisk(self.board[21],1);
              self.board[27] = self.__index.flipDisk(self.board[27],1);
    self.board[26],fliped = self.__index.flipLine(self.board[26],1,color);
    self.board[32],fliped = self.__index.flipLine(self.board[32],6,color);
    if fliped[0] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],5);
      self.board[13] = self.__index.flipDisk(self.board[13],5);
      self.board[24] = self.__index.flipDisk(self.board[24],2);
      if fliped[0] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],4);
        self.board[12] = self.__index.flipDisk(self.board[12],4);
        self.board[22] = self.__index.flipDisk(self.board[22],3);
        if fliped[0] >= 3:
          self.board[3] = self.__index.flipDisk(self.board[3],3);
          self.board[11] = self.__index.flipDisk(self.board[11],3);
          self.board[20] = self.__index.flipDisk(self.board[20],3);
          if fliped[0] >= 4:
            self.board[2] = self.__index.flipDisk(self.board[2],2);
            self.board[10] = self.__index.flipDisk(self.board[10],2);
            self.board[18] = self.__index.flipDisk(self.board[18],2);
            if fliped[0] >= 5:
              self.board[1] = self.__index.flipDisk(self.board[1],1);
              self.board[9] = self.__index.flipDisk(self.board[9],1);
              self.board[16] = self.__index.flipDisk(self.board[16],1);
  def putAt55(self, color):
    self.board[6],fliped = self.__index.flipLine(self.board[6],7,color)
    if fliped[0] >= 1:
      self.board[14] = self.__index.flipDisk(self.board[14],6)
      self.board[26] = self.__index.flipDisk(self.board[26],1)
      self.board[32] = self.__index.flipDisk(self.board[32],6)
      if fliped[0] >= 2:
        self.board[13] = self.__index.flipDisk(self.board[13],6)
        self.board[25] = self.__index.flipDisk(self.board[25],2)
        self.board[33] = self.__index.flipDisk(self.board[33],5)
        if fliped[0] >= 3:
          self.board[12] = self.__index.flipDisk(self.board[12],6)
          self.board[24] = self.__index.flipDisk(self.board[24],3)
          self.board[34] = self.__index.flipDisk(self.board[34],4)
          if fliped[0] >= 4:
            self.board[11] = self.__index.flipDisk(self.board[11],6)
            self.board[23] = self.__index.flipDisk(self.board[23],4)
            self.board[35] = self.__index.flipDisk(self.board[35],3)
            if fliped[0] >= 5:
              self.board[10] = self.__index.flipDisk(self.board[10],6)
              self.board[22] = self.__index.flipDisk(self.board[22],5)
              self.board[36] = self.__index.flipDisk(self.board[36],2)
              if fliped[0] >= 6:
                self.board[9] = self.__index.flipDisk(self.board[9],6)
                self.board[21] = self.__index.flipDisk(self.board[21],6)
                self.board[37] = self.__index.flipDisk(self.board[37],1)
    self.board[15],fliped = self.__index.flipLine(self.board[15],6,color)
    if fliped[0] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],7);
      self.board[26] = self.__index.flipDisk(self.board[26],0);
      self.board[30] = self.__index.flipDisk(self.board[30],5);
      if fliped[0] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],7);
        self.board[25] = self.__index.flipDisk(self.board[25],0);
        self.board[29] = self.__index.flipDisk(self.board[29],4);
        if fliped[0] >= 3:
          self.board[3] = self.__index.flipDisk(self.board[3],7);
          self.board[24] = self.__index.flipDisk(self.board[24],0);
          self.board[28] = self.__index.flipDisk(self.board[28],3);
          if fliped[0] >= 4:
            self.board[2] = self.__index.flipDisk(self.board[2],7);
            self.board[23] = self.__index.flipDisk(self.board[23],0);
            self.board[27] = self.__index.flipDisk(self.board[27],2);
            if fliped[0] >= 5:
              self.board[1] = self.__index.flipDisk(self.board[1],7);
              self.board[22] = self.__index.flipDisk(self.board[22],0);
    self.board[31],fliped = self.__index.flipLine(self.board[31],6,color);
    if fliped[0] >= 1:
      self.board[5] = self.__index.flipDisk(self.board[5],6);
      self.board[14] = self.__index.flipDisk(self.board[14],5);
      self.board[25] = self.__index.flipDisk(self.board[25],1);
      if fliped[0] >= 2:
        self.board[4] = self.__index.flipDisk(self.board[4],5);
        self.board[13] = self.__index.flipDisk(self.board[13],4);
        self.board[23] = self.__index.flipDisk(self.board[23],2);
        if fliped[0] >= 3:
          self.board[3] = self.__index.flipDisk(self.board[3],4);
          self.board[12] = self.__index.flipDisk(self.board[12],3);
          self.board[21] = self.__index.flipDisk(self.board[21],3);
          if fliped[0] >= 4:
            self.board[2] = self.__index.flipDisk(self.board[2],3);
            self.board[11] = self.__index.flipDisk(self.board[11],2);
            self.board[19] = self.__index.flipDisk(self.board[19],2);
            if fliped[0] >= 5:
              self.board[1] = self.__index.flipDisk(self.board[1],2);
              self.board[10] = self.__index.flipDisk(self.board[10],1);
              self.board[17] = self.__index.flipDisk(self.board[17],1);
  def putAt56(self, color):
    self.board[7],fliped = self.__index.flipLine(self.board[7],0,color)
    if fliped[1] >= 1:
      self.board[9] = self.__index.flipDisk(self.board[9],7)
      self.board[22] = self.__index.flipDisk(self.board[22],6)
      if fliped[1] >= 2:
        self.board[10] = self.__index.flipDisk(self.board[10],7)
        self.board[23] = self.__index.flipDisk(self.board[23],5)
        self.board[37] = self.__index.flipDisk(self.board[37],2)
        if fliped[1] >= 3:
          self.board[11] = self.__index.flipDisk(self.board[11],7)
          self.board[24] = self.__index.flipDisk(self.board[24],4)
          self.board[36] = self.__index.flipDisk(self.board[36],3)
          if fliped[1] >= 4:
            self.board[12] = self.__index.flipDisk(self.board[12],7)
            self.board[25] = self.__index.flipDisk(self.board[25],3)
            self.board[35] = self.__index.flipDisk(self.board[35],4)
            if fliped[1] >= 5:
              self.board[13] = self.__index.flipDisk(self.board[13],7)
              self.board[26] = self.__index.flipDisk(self.board[26],2)
              self.board[34] = self.__index.flipDisk(self.board[34],5)
              if fliped[1] >= 6:
                self.board[14] = self.__index.flipDisk(self.board[14],7)
                self.board[33] = self.__index.flipDisk(self.board[33],6)
    self.board[8],fliped = self.__index.flipLine(self.board[8],7,color)
    if fliped[0] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],0);
      self.board[20] = self.__index.flipDisk(self.board[20],6);
      if fliped[0] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],0);
        self.board[19] = self.__index.flipDisk(self.board[19],5);
        self.board[37] = self.__index.flipDisk(self.board[37],0);
        if fliped[0] >= 3:
          self.board[4] = self.__index.flipDisk(self.board[4],0);
          self.board[18] = self.__index.flipDisk(self.board[18],4);
          self.board[36] = self.__index.flipDisk(self.board[36],0);
          if fliped[0] >= 4:
            self.board[3] = self.__index.flipDisk(self.board[3],0);
            self.board[17] = self.__index.flipDisk(self.board[17],3);
            self.board[35] = self.__index.flipDisk(self.board[35],0);
            if fliped[0] >= 5:
              self.board[2] = self.__index.flipDisk(self.board[2],0);
              self.board[16] = self.__index.flipDisk(self.board[16],2);
              self.board[34] = self.__index.flipDisk(self.board[34],0);
              if fliped[0] >= 6:
                self.board[1] = self.__index.flipDisk(self.board[1],0);
                self.board[33] = self.__index.flipDisk(self.board[33],0);
    self.board[21],fliped = self.__index.flipLine(self.board[21],7,color);
    if fliped[0] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],1);
      self.board[9] = self.__index.flipDisk(self.board[9],6);
      self.board[37] = self.__index.flipDisk(self.board[37],1);
      if fliped[0] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],2);
        self.board[10] = self.__index.flipDisk(self.board[10],5);
        self.board[35] = self.__index.flipDisk(self.board[35],2);
        if fliped[0] >= 3:
          self.board[4] = self.__index.flipDisk(self.board[4],3);
          self.board[11] = self.__index.flipDisk(self.board[11],4);
          self.board[33] = self.__index.flipDisk(self.board[33],3);
          if fliped[0] >= 4:
            self.board[3] = self.__index.flipDisk(self.board[3],4);
            self.board[12] = self.__index.flipDisk(self.board[12],3);
            self.board[31] = self.__index.flipDisk(self.board[31],3);
            if fliped[0] >= 5:
              self.board[2] = self.__index.flipDisk(self.board[2],5);
              self.board[13] = self.__index.flipDisk(self.board[13],2);
              self.board[29] = self.__index.flipDisk(self.board[29],2);
              if fliped[0] >= 6:
                self.board[1] = self.__index.flipDisk(self.board[1],6);
                self.board[14] = self.__index.flipDisk(self.board[14],1);
                self.board[27] = self.__index.flipDisk(self.board[27],1);
  def putAt57(self, color):
    self.board[7],fliped = self.__index.flipLine(self.board[7],1,color)
    if fliped[1] >= 1:
      self.board[10] = self.__index.flipDisk(self.board[10],7)
      self.board[23] = self.__index.flipDisk(self.board[23],5)
      self.board[37] = self.__index.flipDisk(self.board[37],2)
      if fliped[1] >= 2:
        self.board[11] = self.__index.flipDisk(self.board[11],7)
        self.board[24] = self.__index.flipDisk(self.board[24],4)
        self.board[36] = self.__index.flipDisk(self.board[36],3)
        if fliped[1] >= 3:
          self.board[12] = self.__index.flipDisk(self.board[12],7)
          self.board[25] = self.__index.flipDisk(self.board[25],3)
          self.board[35] = self.__index.flipDisk(self.board[35],4)
          if fliped[1] >= 4:
            self.board[13] = self.__index.flipDisk(self.board[13],7)
            self.board[26] = self.__index.flipDisk(self.board[26],2)
            self.board[34] = self.__index.flipDisk(self.board[34],5)
            if fliped[1] >= 5:
              self.board[14] = self.__index.flipDisk(self.board[14],7)
              self.board[33] = self.__index.flipDisk(self.board[33],6)
    self.board[9],fliped = self.__index.flipLine(self.board[9],7,color)
    if fliped[0] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],1);
      self.board[21] = self.__index.flipDisk(self.board[21],6);
      self.board[37] = self.__index.flipDisk(self.board[37],1);
      if fliped[0] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],1);
        self.board[20] = self.__index.flipDisk(self.board[20],5);
        self.board[36] = self.__index.flipDisk(self.board[36],1);
        if fliped[0] >= 3:
          self.board[4] = self.__index.flipDisk(self.board[4],1);
          self.board[19] = self.__index.flipDisk(self.board[19],4);
          self.board[35] = self.__index.flipDisk(self.board[35],1);
          if fliped[0] >= 4:
            self.board[3] = self.__index.flipDisk(self.board[3],1);
            self.board[18] = self.__index.flipDisk(self.board[18],3);
            self.board[34] = self.__index.flipDisk(self.board[34],1);
            if fliped[0] >= 5:
              self.board[2] = self.__index.flipDisk(self.board[2],1);
              self.board[17] = self.__index.flipDisk(self.board[17],2);
              self.board[33] = self.__index.flipDisk(self.board[33],1);
              if fliped[0] >= 6:
                self.board[1] = self.__index.flipDisk(self.board[1],1);
                self.board[16] = self.__index.flipDisk(self.board[16],1);
                self.board[32] = self.__index.flipDisk(self.board[32],1);
    self.board[22],fliped = self.__index.flipLine(self.board[22],6,color);
    if fliped[0] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],2);
      self.board[10] = self.__index.flipDisk(self.board[10],6);
      self.board[36] = self.__index.flipDisk(self.board[36],2);
      if fliped[0] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],3);
        self.board[11] = self.__index.flipDisk(self.board[11],5);
        self.board[34] = self.__index.flipDisk(self.board[34],3);
        if fliped[0] >= 3:
          self.board[4] = self.__index.flipDisk(self.board[4],4);
          self.board[12] = self.__index.flipDisk(self.board[12],4);
          self.board[32] = self.__index.flipDisk(self.board[32],4);
          if fliped[0] >= 4:
            self.board[3] = self.__index.flipDisk(self.board[3],5);
            self.board[13] = self.__index.flipDisk(self.board[13],3);
            self.board[30] = self.__index.flipDisk(self.board[30],3);
            if fliped[0] >= 5:
              self.board[2] = self.__index.flipDisk(self.board[2],6);
              self.board[14] = self.__index.flipDisk(self.board[14],2);
              self.board[28] = self.__index.flipDisk(self.board[28],2);
  def putAt58(self, color):
    self.board[7],fliped = self.__index.flipLine(self.board[7],2,color)
    if fliped[0] >= 1:
      self.board[9] = self.__index.flipDisk(self.board[9],7)
      self.board[22] = self.__index.flipDisk(self.board[22],6)
    if fliped[1] >= 1:
      self.board[11] = self.__index.flipDisk(self.board[11],7)
      self.board[24] = self.__index.flipDisk(self.board[24],4)
      self.board[36] = self.__index.flipDisk(self.board[36],3)
      if fliped[1] >= 2:
        self.board[12] = self.__index.flipDisk(self.board[12],7)
        self.board[25] = self.__index.flipDisk(self.board[25],3)
        self.board[35] = self.__index.flipDisk(self.board[35],4)
        if fliped[1] >= 3:
          self.board[13] = self.__index.flipDisk(self.board[13],7)
          self.board[26] = self.__index.flipDisk(self.board[26],2)
          self.board[34] = self.__index.flipDisk(self.board[34],5)
          if fliped[1] >= 4:
            self.board[14] = self.__index.flipDisk(self.board[14],7)
            self.board[33] = self.__index.flipDisk(self.board[33],6)
    self.board[10],fliped = self.__index.flipLine(self.board[10],7,color)
    if fliped[0] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],2);
      self.board[22] = self.__index.flipDisk(self.board[22],5);
      self.board[36] = self.__index.flipDisk(self.board[36],2);
      if fliped[0] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],2);
        self.board[21] = self.__index.flipDisk(self.board[21],5);
        self.board[35] = self.__index.flipDisk(self.board[35],2);
        if fliped[0] >= 3:
          self.board[4] = self.__index.flipDisk(self.board[4],2);
          self.board[20] = self.__index.flipDisk(self.board[20],4);
          self.board[34] = self.__index.flipDisk(self.board[34],2);
          if fliped[0] >= 4:
            self.board[3] = self.__index.flipDisk(self.board[3],2);
            self.board[19] = self.__index.flipDisk(self.board[19],3);
            self.board[33] = self.__index.flipDisk(self.board[33],2);
            if fliped[0] >= 5:
              self.board[2] = self.__index.flipDisk(self.board[2],2);
              self.board[18] = self.__index.flipDisk(self.board[18],2);
              self.board[32] = self.__index.flipDisk(self.board[32],2);
              if fliped[0] >= 6:
                self.board[1] = self.__index.flipDisk(self.board[1],2);
                self.board[17] = self.__index.flipDisk(self.board[17],1);
                self.board[31] = self.__index.flipDisk(self.board[31],1);
    self.board[23],fliped = self.__index.flipLine(self.board[23],5,color);
    if fliped[0] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],3);
      self.board[11] = self.__index.flipDisk(self.board[11],6);
      self.board[35] = self.__index.flipDisk(self.board[35],3);
      if fliped[0] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],4);
        self.board[12] = self.__index.flipDisk(self.board[12],5);
        self.board[33] = self.__index.flipDisk(self.board[33],4);
        if fliped[0] >= 3:
          self.board[4] = self.__index.flipDisk(self.board[4],5);
          self.board[13] = self.__index.flipDisk(self.board[13],4);
          self.board[31] = self.__index.flipDisk(self.board[31],4);
          if fliped[0] >= 4:
            self.board[3] = self.__index.flipDisk(self.board[3],6);
            self.board[14] = self.__index.flipDisk(self.board[14],3);
            self.board[29] = self.__index.flipDisk(self.board[29],3);
    self.board[37],fliped = self.__index.flipLine(self.board[37],2,color);
    if fliped[0] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],1);
      self.board[9] = self.__index.flipDisk(self.board[9],6);
      self.board[21] = self.__index.flipDisk(self.board[21],6);
  def putAt59(self, color):
    self.board[7],fliped = self.__index.flipLine(self.board[7],3,color)
    if fliped[0] >= 1:
      self.board[10] = self.__index.flipDisk(self.board[10],7)
      self.board[23] = self.__index.flipDisk(self.board[23],5)
      self.board[37] = self.__index.flipDisk(self.board[37],2)
      if fliped[0] >= 2:
        self.board[9] = self.__index.flipDisk(self.board[9],7)
        self.board[22] = self.__index.flipDisk(self.board[22],6)
    if fliped[1] >= 1:
      self.board[12] = self.__index.flipDisk(self.board[12],7)
      self.board[25] = self.__index.flipDisk(self.board[25],3)
      self.board[35] = self.__index.flipDisk(self.board[35],4)
      if fliped[1] >= 2:
        self.board[13] = self.__index.flipDisk(self.board[13],7)
        self.board[26] = self.__index.flipDisk(self.board[26],2)
        self.board[34] = self.__index.flipDisk(self.board[34],5)
        if fliped[1] >= 3:
          self.board[14] = self.__index.flipDisk(self.board[14],7)
          self.board[33] = self.__index.flipDisk(self.board[33],6)
    self.board[11],fliped = self.__index.flipLine(self.board[11],7,color)
    if fliped[0] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],3);
      self.board[23] = self.__index.flipDisk(self.board[23],4);
      self.board[35] = self.__index.flipDisk(self.board[35],3);
      if fliped[0] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],3);
        self.board[22] = self.__index.flipDisk(self.board[22],4);
        self.board[34] = self.__index.flipDisk(self.board[34],3);
        if fliped[0] >= 3:
          self.board[4] = self.__index.flipDisk(self.board[4],3);
          self.board[21] = self.__index.flipDisk(self.board[21],4);
          self.board[33] = self.__index.flipDisk(self.board[33],3);
          if fliped[0] >= 4:
            self.board[3] = self.__index.flipDisk(self.board[3],3);
            self.board[20] = self.__index.flipDisk(self.board[20],3);
            self.board[32] = self.__index.flipDisk(self.board[32],3);
            if fliped[0] >= 5:
              self.board[2] = self.__index.flipDisk(self.board[2],3);
              self.board[19] = self.__index.flipDisk(self.board[19],2);
              self.board[31] = self.__index.flipDisk(self.board[31],2);
              if fliped[0] >= 6:
                self.board[1] = self.__index.flipDisk(self.board[1],3);
                self.board[18] = self.__index.flipDisk(self.board[18],1);
                self.board[30] = self.__index.flipDisk(self.board[30],1);
    self.board[24],fliped = self.__index.flipLine(self.board[24],4,color);
    if fliped[0] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],4);
      self.board[12] = self.__index.flipDisk(self.board[12],6);
      self.board[34] = self.__index.flipDisk(self.board[34],4);
      if fliped[0] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],5);
        self.board[13] = self.__index.flipDisk(self.board[13],5);
        self.board[32] = self.__index.flipDisk(self.board[32],5);
        if fliped[0] >= 3:
          self.board[4] = self.__index.flipDisk(self.board[4],6);
          self.board[14] = self.__index.flipDisk(self.board[14],4);
          self.board[30] = self.__index.flipDisk(self.board[30],4);
    self.board[36],fliped = self.__index.flipLine(self.board[36],3,color);
    if fliped[0] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],2);
      self.board[10] = self.__index.flipDisk(self.board[10],6);
      self.board[22] = self.__index.flipDisk(self.board[22],5);
      if fliped[0] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],1);
        self.board[9] = self.__index.flipDisk(self.board[9],5);
        self.board[20] = self.__index.flipDisk(self.board[20],5);
  def putAt60(self, color):
    self.board[7],fliped = self.__index.flipLine(self.board[7],4,color)
    if fliped[0] >= 1:
      self.board[11] = self.__index.flipDisk(self.board[11],7)
      self.board[24] = self.__index.flipDisk(self.board[24],4)
      self.board[36] = self.__index.flipDisk(self.board[36],3)
      if fliped[0] >= 2:
        self.board[10] = self.__index.flipDisk(self.board[10],7)
        self.board[23] = self.__index.flipDisk(self.board[23],5)
        self.board[37] = self.__index.flipDisk(self.board[37],2)
        if fliped[0] >= 3:
          self.board[9] = self.__index.flipDisk(self.board[9],7)
          self.board[22] = self.__index.flipDisk(self.board[22],6)
    if fliped[1] >= 1:
      self.board[13] = self.__index.flipDisk(self.board[13],7)
      self.board[26] = self.__index.flipDisk(self.board[26],2)
      self.board[34] = self.__index.flipDisk(self.board[34],5)
      if fliped[1] >= 2:
        self.board[14] = self.__index.flipDisk(self.board[14],7)
        self.board[33] = self.__index.flipDisk(self.board[33],6)
    self.board[12],fliped = self.__index.flipLine(self.board[12],7,color)
    if fliped[0] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],4);
      self.board[24] = self.__index.flipDisk(self.board[24],3);
      self.board[34] = self.__index.flipDisk(self.board[34],4);
      if fliped[0] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],4);
        self.board[23] = self.__index.flipDisk(self.board[23],3);
        self.board[33] = self.__index.flipDisk(self.board[33],4);
        if fliped[0] >= 3:
          self.board[4] = self.__index.flipDisk(self.board[4],4);
          self.board[22] = self.__index.flipDisk(self.board[22],3);
          self.board[32] = self.__index.flipDisk(self.board[32],4);
          if fliped[0] >= 4:
            self.board[3] = self.__index.flipDisk(self.board[3],4);
            self.board[21] = self.__index.flipDisk(self.board[21],3);
            self.board[31] = self.__index.flipDisk(self.board[31],3);
            if fliped[0] >= 5:
              self.board[2] = self.__index.flipDisk(self.board[2],4);
              self.board[20] = self.__index.flipDisk(self.board[20],2);
              self.board[30] = self.__index.flipDisk(self.board[30],2);
              if fliped[0] >= 6:
                self.board[1] = self.__index.flipDisk(self.board[1],4);
                self.board[19] = self.__index.flipDisk(self.board[19],1);
                self.board[29] = self.__index.flipDisk(self.board[29],1);
    self.board[25],fliped = self.__index.flipLine(self.board[25],3,color);
    if fliped[0] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],5);
      self.board[13] = self.__index.flipDisk(self.board[13],6);
      self.board[33] = self.__index.flipDisk(self.board[33],5);
      if fliped[0] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],6);
        self.board[14] = self.__index.flipDisk(self.board[14],5);
        self.board[31] = self.__index.flipDisk(self.board[31],5);
    self.board[35],fliped = self.__index.flipLine(self.board[35],4,color);
    if fliped[0] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],3);
      self.board[11] = self.__index.flipDisk(self.board[11],6);
      self.board[23] = self.__index.flipDisk(self.board[23],4);
      if fliped[0] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],2);
        self.board[10] = self.__index.flipDisk(self.board[10],5);
        self.board[21] = self.__index.flipDisk(self.board[21],5);
        if fliped[0] >= 3:
          self.board[4] = self.__index.flipDisk(self.board[4],1);
          self.board[9] = self.__index.flipDisk(self.board[9],4);
          self.board[19] = self.__index.flipDisk(self.board[19],4);
  def putAt61(self, color):
    self.board[7],fliped = self.__index.flipLine(self.board[7],5,color)
    if fliped[0] >= 1:
      self.board[12] = self.__index.flipDisk(self.board[12],7)
      self.board[25] = self.__index.flipDisk(self.board[25],3)
      self.board[35] = self.__index.flipDisk(self.board[35],4)
      if fliped[0] >= 2:
        self.board[11] = self.__index.flipDisk(self.board[11],7)
        self.board[24] = self.__index.flipDisk(self.board[24],4)
        self.board[36] = self.__index.flipDisk(self.board[36],3)
        if fliped[0] >= 3:
          self.board[10] = self.__index.flipDisk(self.board[10],7)
          self.board[23] = self.__index.flipDisk(self.board[23],5)
          self.board[37] = self.__index.flipDisk(self.board[37],2)
          if fliped[0] >= 4:
            self.board[9] = self.__index.flipDisk(self.board[9],7)
            self.board[22] = self.__index.flipDisk(self.board[22],6)
    if fliped[1] >= 1:
      self.board[14] = self.__index.flipDisk(self.board[14],7)
      self.board[33] = self.__index.flipDisk(self.board[33],6)
    self.board[13],fliped = self.__index.flipLine(self.board[13],7,color)
    if fliped[0] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],5);
      self.board[25] = self.__index.flipDisk(self.board[25],2);
      self.board[33] = self.__index.flipDisk(self.board[33],5);
      if fliped[0] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],5);
        self.board[24] = self.__index.flipDisk(self.board[24],2);
        self.board[32] = self.__index.flipDisk(self.board[32],5);
        if fliped[0] >= 3:
          self.board[4] = self.__index.flipDisk(self.board[4],5);
          self.board[23] = self.__index.flipDisk(self.board[23],2);
          self.board[31] = self.__index.flipDisk(self.board[31],4);
          if fliped[0] >= 4:
            self.board[3] = self.__index.flipDisk(self.board[3],5);
            self.board[22] = self.__index.flipDisk(self.board[22],2);
            self.board[30] = self.__index.flipDisk(self.board[30],3);
            if fliped[0] >= 5:
              self.board[2] = self.__index.flipDisk(self.board[2],5);
              self.board[21] = self.__index.flipDisk(self.board[21],2);
              self.board[29] = self.__index.flipDisk(self.board[29],2);
              if fliped[0] >= 6:
                self.board[1] = self.__index.flipDisk(self.board[1],5);
                self.board[20] = self.__index.flipDisk(self.board[20],1);
                self.board[28] = self.__index.flipDisk(self.board[28],1);
    self.board[26],fliped = self.__index.flipLine(self.board[26],2,color);
    if fliped[0] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],6);
      self.board[14] = self.__index.flipDisk(self.board[14],6);
      self.board[32] = self.__index.flipDisk(self.board[32],6);
    self.board[34],fliped = self.__index.flipLine(self.board[34],5,color);
    if fliped[0] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],4);
      self.board[12] = self.__index.flipDisk(self.board[12],6);
      self.board[24] = self.__index.flipDisk(self.board[24],3);
      if fliped[0] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],3);
        self.board[11] = self.__index.flipDisk(self.board[11],5);
        self.board[22] = self.__index.flipDisk(self.board[22],4);
        if fliped[0] >= 3:
          self.board[4] = self.__index.flipDisk(self.board[4],2);
          self.board[10] = self.__index.flipDisk(self.board[10],4);
          self.board[20] = self.__index.flipDisk(self.board[20],4);
          if fliped[0] >= 4:
            self.board[3] = self.__index.flipDisk(self.board[3],1);
            self.board[9] = self.__index.flipDisk(self.board[9],3);
            self.board[18] = self.__index.flipDisk(self.board[18],3);
  def putAt62(self, color):
    self.board[7],fliped = self.__index.flipLine(self.board[7],6,color)
    if fliped[0] >= 1:
      self.board[13] = self.__index.flipDisk(self.board[13],7)
      self.board[26] = self.__index.flipDisk(self.board[26],2)
      self.board[34] = self.__index.flipDisk(self.board[34],5)
      if fliped[0] >= 2:
        self.board[12] = self.__index.flipDisk(self.board[12],7)
        self.board[25] = self.__index.flipDisk(self.board[25],3)
        self.board[35] = self.__index.flipDisk(self.board[35],4)
        if fliped[0] >= 3:
          self.board[11] = self.__index.flipDisk(self.board[11],7)
          self.board[24] = self.__index.flipDisk(self.board[24],4)
          self.board[36] = self.__index.flipDisk(self.board[36],3)
          if fliped[0] >= 4:
            self.board[10] = self.__index.flipDisk(self.board[10],7)
            self.board[23] = self.__index.flipDisk(self.board[23],5)
            self.board[37] = self.__index.flipDisk(self.board[37],2)
            if fliped[0] >= 5:
              self.board[9] = self.__index.flipDisk(self.board[9],7)
              self.board[22] = self.__index.flipDisk(self.board[22],6)
    self.board[14],fliped = self.__index.flipLine(self.board[14],7,color)
    if fliped[0] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],6);
      self.board[26] = self.__index.flipDisk(self.board[26],1);
      self.board[32] = self.__index.flipDisk(self.board[32],6);
      if fliped[0] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],6);
        self.board[25] = self.__index.flipDisk(self.board[25],1);
        self.board[31] = self.__index.flipDisk(self.board[31],5);
        if fliped[0] >= 3:
          self.board[4] = self.__index.flipDisk(self.board[4],6);
          self.board[24] = self.__index.flipDisk(self.board[24],1);
          self.board[30] = self.__index.flipDisk(self.board[30],4);
          if fliped[0] >= 4:
            self.board[3] = self.__index.flipDisk(self.board[3],6);
            self.board[23] = self.__index.flipDisk(self.board[23],1);
            self.board[29] = self.__index.flipDisk(self.board[29],3);
            if fliped[0] >= 5:
              self.board[2] = self.__index.flipDisk(self.board[2],6);
              self.board[22] = self.__index.flipDisk(self.board[22],1);
              self.board[28] = self.__index.flipDisk(self.board[28],2);
              if fliped[0] >= 6:
                self.board[1] = self.__index.flipDisk(self.board[1],6);
                self.board[21] = self.__index.flipDisk(self.board[21],1);
                self.board[27] = self.__index.flipDisk(self.board[27],1);
    self.board[33],fliped = self.__index.flipLine(self.board[33],6,color);
    if fliped[0] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],5);
      self.board[13] = self.__index.flipDisk(self.board[13],6);
      self.board[25] = self.__index.flipDisk(self.board[25],2);
      if fliped[0] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],4);
        self.board[12] = self.__index.flipDisk(self.board[12],5);
        self.board[23] = self.__index.flipDisk(self.board[23],3);
        if fliped[0] >= 3:
          self.board[4] = self.__index.flipDisk(self.board[4],3);
          self.board[11] = self.__index.flipDisk(self.board[11],4);
          self.board[21] = self.__index.flipDisk(self.board[21],4);
          if fliped[0] >= 4:
            self.board[3] = self.__index.flipDisk(self.board[3],2);
            self.board[10] = self.__index.flipDisk(self.board[10],3);
            self.board[19] = self.__index.flipDisk(self.board[19],3);
            if fliped[0] >= 5:
              self.board[2] = self.__index.flipDisk(self.board[2],1);
              self.board[9] = self.__index.flipDisk(self.board[9],2);
              self.board[17] = self.__index.flipDisk(self.board[17],2);
  def putAt63(self, color):
    self.board[7],fliped = self.__index.flipLine(self.board[7],7,color)
    if fliped[0] >= 1:
      self.board[14] = self.__index.flipDisk(self.board[14],7)
      self.board[33] = self.__index.flipDisk(self.board[33],6)
      if fliped[0] >= 2:
        self.board[13] = self.__index.flipDisk(self.board[13],7)
        self.board[26] = self.__index.flipDisk(self.board[26],2)
        self.board[34] = self.__index.flipDisk(self.board[34],5)
        if fliped[0] >= 3:
          self.board[12] = self.__index.flipDisk(self.board[12],7)
          self.board[25] = self.__index.flipDisk(self.board[25],3)
          self.board[35] = self.__index.flipDisk(self.board[35],4)
          if fliped[0] >= 4:
            self.board[11] = self.__index.flipDisk(self.board[11],7)
            self.board[24] = self.__index.flipDisk(self.board[24],4)
            self.board[36] = self.__index.flipDisk(self.board[36],3)
            if fliped[0] >= 5:
              self.board[10] = self.__index.flipDisk(self.board[10],7)
              self.board[23] = self.__index.flipDisk(self.board[23],5)
              self.board[37] = self.__index.flipDisk(self.board[37],2)
              if fliped[0] >= 6:
                self.board[9] = self.__index.flipDisk(self.board[9],7)
                self.board[22] = self.__index.flipDisk(self.board[22],6)
    self.board[15],fliped = self.__index.flipLine(self.board[15],7,color)
    if fliped[0] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],7);
      self.board[31] = self.__index.flipDisk(self.board[31],6);
      if fliped[0] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],7);
        self.board[26] = self.__index.flipDisk(self.board[26],0);
        self.board[30] = self.__index.flipDisk(self.board[30],5);
        if fliped[0] >= 3:
          self.board[4] = self.__index.flipDisk(self.board[4],7);
          self.board[25] = self.__index.flipDisk(self.board[25],0);
          self.board[29] = self.__index.flipDisk(self.board[29],4);
          if fliped[0] >= 4:
            self.board[3] = self.__index.flipDisk(self.board[3],7);
            self.board[24] = self.__index.flipDisk(self.board[24],0);
            self.board[28] = self.__index.flipDisk(self.board[28],3);
            if fliped[0] >= 5:
              self.board[2] = self.__index.flipDisk(self.board[2],7);
              self.board[23] = self.__index.flipDisk(self.board[23],0);
              self.board[27] = self.__index.flipDisk(self.board[27],2);
              if fliped[0] >= 6:
                self.board[1] = self.__index.flipDisk(self.board[1],7);
                self.board[22] = self.__index.flipDisk(self.board[22],0);
    self.board[32],fliped = self.__index.flipLine(self.board[32],7,color);
    if fliped[0] >= 1:
      self.board[6] = self.__index.flipDisk(self.board[6],6);
      self.board[14] = self.__index.flipDisk(self.board[14],6);
      self.board[26] = self.__index.flipDisk(self.board[26],1);
      if fliped[0] >= 2:
        self.board[5] = self.__index.flipDisk(self.board[5],5);
        self.board[13] = self.__index.flipDisk(self.board[13],5);
        self.board[24] = self.__index.flipDisk(self.board[24],2);
        if fliped[0] >= 3:
          self.board[4] = self.__index.flipDisk(self.board[4],4);
          self.board[12] = self.__index.flipDisk(self.board[12],4);
          self.board[22] = self.__index.flipDisk(self.board[22],3);
          if fliped[0] >= 4:
            self.board[3] = self.__index.flipDisk(self.board[3],3);
            self.board[11] = self.__index.flipDisk(self.board[11],3);
            self.board[20] = self.__index.flipDisk(self.board[20],3);
            if fliped[0] >= 5:
              self.board[2] = self.__index.flipDisk(self.board[2],2);
              self.board[10] = self.__index.flipDisk(self.board[10],2);
              self.board[18] = self.__index.flipDisk(self.board[18],2);
              if fliped[0] >= 6:
                self.board[1] = self.__index.flipDisk(self.board[1],1);
                self.board[9] = self.__index.flipDisk(self.board[9],1);
                self.board[16] = self.__index.flipDisk(self.board[16],1);
