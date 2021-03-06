# -*- coding:utf-8 -*-

import othello

class Index:
  
  def __init__(self):
    PATTERNS_NUM = 3 ** 8
    self.__matrix     = [[[ [[0,0],[0,0]], [0, 0], [0, 0], 0] for j in range(8)] for i in range(PATTERNS_NUM)]
    self.__mobility   = [0 for i in range(PATTERNS_NUM)]
    self.__settled    = [0 for i in range(PATTERNS_NUM)]
    self.__difference = [0 for i in range(PATTERNS_NUM)]
    self.__eval       = [[0 for i in range(PATTERNS_NUM)] for j in range(8)]
    for code in range(PATTERNS_NUM):
      self.__initRow(code)

  # <概要> __matrix[code]を初期化する
  # <引数> code:int(0~6560)
  def __initRow(self, code):
    line = Index.__decode(code)  # codeをデコード
    for x in range(8):
      self.__initElement(code, x, line)  # lineの位置xに駒を置くときの処理を計算する
    for color in [0, 1]:
      flag = True
      for cell in line:
        if cell == color:
          if cell == 0:
            self.__settled[code] += 1
          else:
            self.__settled[code] -= 1
        else:
          flag = False
          break
      for cell in line[::-1]:
        if cell == color:
          if cell == 0:
            self.__settled[code] += 1
          else:
            self.__settled[code] -= 1
        else:
          break
    for cell in line:
      if cell == 0:
        self.__difference[code] += 1
      elif cell == 1:
        self.__difference[code] -= 1
    for i, cell in enumerate(line):
      if cell == 0:
        for j in range(8):
          self.__eval[j][code] += othello.Config.WEIGHTS[j][i]
      elif cell == 1:
        for j in range(8):
          self.__eval[j][code] -= othello.Config.WEIGHTS[j][i]

  # <概要> __matrix[i][j]を初期化する
  # <引数> i:int(0~6560), j:int(0~7), line:Cell型List[8]
  # <詳細> lineを駒を置く位置の右側と左側に分割して計算している.
  def __initElement(self, code, x, line):
    if line[x] == 2: # Cell.EMPTY
      for color in (0, 1):
        flipedLine = list(line)
        flipedLine[x] = color
        takesLeft  = Index.__flipOneSide(line[:x][::-1], color)  # 左側を計算する
        takesRight = Index.__flipOneSide(line[x+1:], color)      # 右側を計算する
        for i in range(takesLeft):
          flipedLine[x - i - 1] = color
        for i in range(takesRight):
          flipedLine[x + i + 1] = color
        self.__matrix[code][x][0][color] = (takesLeft, takesRight)
        self.__matrix[code][x][1][color] = takesLeft + takesRight
        self.__matrix[code][x][2][color] = Index.__encode(flipedLine)
        if takesLeft or takesRight:
          if color:
            self.__mobility[code] -= 1
          else:
            self.__mobility[code] += 1

    else:
      flipedLine = list(line)
      flipedLine[x] = not flipedLine[x]
      self.__matrix[code][x][3] = Index.__encode(flipedLine)

  # <概要> デコード結果を返す
  # <引数> code:int(0~6560)
  # <返値> int型List[8]
  @classmethod
  def __decode(cls, code):
    res = [0] * 8
    for i in range(8)[::-1]:
      res[i] = code / 3 ** i
      code %= 3 ** i
    return res

  # <概要> エンコード結果を返す
  # <引数> line:int型List[8]
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
  #        X○○●- の位置Xに●を置く場合を考えるので
  #        返り値は2となる
  @classmethod
  def __flipOneSide(cls, line, color):
    for i, cell in enumerate(line):
      if cell == 2:
        return 0
      if cell == color:
        return i
    return 0

  # <概要> codeに符号化されるマス列の位置xにcolor色の駒を置いたときに裏返る駒の数を返す
  def takes(self, code, x, color):
    return self.__matrix[code][x][1][color]

  # <概要> codeに符号化されるマス列の位置xにcolor色の駒を置いたあとのマス列を符号化した値と,
  #        codeに符号化されるマス列の位置xにcolor色の駒を置いたときに裏返る左右それぞれの駒の数を返す
  def flipLine(self, code, x, color):
    return (self.__matrix[code][x][2][color], self.__matrix[code][x][0][color])

  # <概要> codeに符号化されるマス列の位置xの駒が裏返ったあとのマス列を符号化した値を返す
  def flipDisk(self, code, x):
    return self.__matrix[code][x][3]

  # <概要> codeに符号化されるマス列に対してcolor色の駒を置くことのできる場所の数を返す
  def getMobility(self, code, color):
    if color:
      return -self.__mobility[code]
    else:
      return self.__mobility[code]

   # <概要> codeに符号化される端のマス列に対してcolor色の確定石数の近似値を返す
  def getSettled(self, code, color):
    if color:
      return -self.__settled[code]
    else:
      return self.__settled[code]
  # <概要> codeに符号化されるマス列に対して駒の差を返す
  def getDifference(self, code, color):
    if color:
      return -self.__difference[code]
    else:
      return self.__difference[code]

  # <概要> codeに符号化されるi番目の水平マス列に対して評価値を返す
  def getEval(self, i, code, color):
    if color:
      return -self.__eval[i][code]
    else:
      return self.__eval[i][code]
