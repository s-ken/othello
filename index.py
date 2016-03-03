# -*- coding:utf-8 -*-

import othello

class Index:
  class Element:
    def __init__(self):
      self.to = -1
      self.takes = 0
  def __init__(self):
    self.__matrix = [[[Index.Element(), Index.Element()] for i in range(othello.Config.CELL_NUM)] for j in range(othello.Config.PATTERNS_NUM)]
    for code in range(othello.Config.PATTERNS_NUM):
      self.__initRow(code)

  # <概要> __matrix[code]を初期化する
  # <引数> code:int(0~6560)
  def __initRow(self, code):
    line = [othello.Cell(0, 0) for i in range(othello.Config.CELL_NUM)]
    Index.__decode(code, line)  # lineにcodeのデコード結果を格納する
    for x in range(othello.Config.CELL_NUM):
     if line[x].state != othello.Cell.EMPTY:
      continue
     self.__initElement(code, x, line)  # lineの位置xに駒を置くときの処理を計算する

  # <概要> __matrix[i][j]を初期化する
  # <引数> i:int(0~6560), j:int(0~7), line:Cell型List[8]
  # <詳細> lineを駒を置く位置の右側と左側に分割して計算している.
  def __initElement(self, i, j, line):
    for color in [othello.Cell.BLACK, othello.Cell.WHITE]:
      lineCpy = [othello.Cell(0, 0) for k in range(othello.Config.CELL_NUM)]
      for (cellCpy, cell) in zip(lineCpy, line):  # lineをコピーする
        cellCpy.state = cell.state
      lineCpy[j].state = color
      takesLeft  = Index.__flipOneSide(lineCpy[:j][::-1], color)  # 左側を計算する
      takesRight = Index.__flipOneSide(lineCpy[j+1:], color)      # 右側を計算する
      self.__matrix[i][j][color].to    = Index.__encode(lineCpy)
      self.__matrix[i][j][color].takes = takesLeft + takesRight

  # <概要> デコード結果をlistの各要素のstateに反映させる
  # <引数> code:int(0~6560), line:Cell型List[8]
  @classmethod
  def __decode(cls, code, line):
    for i in range(othello.Config.CELL_NUM)[::-1]:
      line[i].state = code / 3 ** i
      code %= 3 ** i

  # <概要> エンコード結果を返す
  # <引数> line:Cell型List[8]
  # <返値> int(0~6560)
  @classmethod
  def __encode(cls, line):
    res = 0
    for i, c in enumerate(line):
      res += c * 3 ** i
    return res

  # <概要> 駒を裏返してそのとき取れる相手の駒数を返す
  # <引数> line:Cell型List[0~7] color:int(0~2)
  # <返値> int(0~6)
  # <詳細> line[0]の隣にcolor色の駒を置いたときのことを考える
  #        (例)        
  #        line = ○○●-, color = ●のとき
  #        X○○○●- の位置Xに●を置く場合を考えるので
  #        line = ●●●- に書き換えられ
  #        2が返り値となる.
  @classmethod
  def __flipOneSide(cls, line, color):
    for i, c in enumerate(line):
      if c.state == othello.Cell.EMPTY:
        return 0
      if c.state == color:
        for d in line[:i]:
          d.state = color
        return i
    return 0

  # <概要> lineの位置xにcolor色の駒を置いたときに得られる相手の駒数を返す
  # <引数> line:Cell型List[8], x:int(0~7), color:int(0~2)
  # <返値> int(0~6)
  def takes(self, line, x, color):
    return self.__matrix[Index.__encode(line)][x][color].takes

  # <概要> lineの各Cellのstateを,位置xにcolor色の駒を置いたときの適切な状態に書き換える
  # <引数> line:Cell型List[8], x:int(0~7), color:int(0~2)
  # <詳細> 引数lineの中身が書き換わるので注意
  def flip(self, line, x, color):
    Index.__decode(self.__matrix[Index.__encode(line)][x][color].to, line)