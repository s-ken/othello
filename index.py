# -*- coding:utf-8 -*-

import othello

# matrix[code][x].fliped[color] = (-a, b) :
#   a = codeに符号化されるマス列の位置xにcolor色の駒を置いたときに裏返る負(左?)方向の駒の数
#   b = codeに符号化されるマス列の位置xにcolor色の駒を置いたときに裏返る正(右?)方向の駒の数
# matrix[code][x].takes[color] :
#   codeに符号化されるマス列の位置xにcolor色の駒を置いたときに裏返る駒の数
# matrix[code][x].putCode[color] :
#   codeに符号化されるマス列の位置xにcolor色の駒を置いたあとのマス列を符号化した値
# matrix[code][x].flipCode :
#   codeに符号化されるマス列の位置xの駒が裏返ったあとのマス列を符号化した値

class Index:

  class Element:
    def __init__(self):
      self.fliped = [None, None]
      self.takes = [0, 0]
      self.putCode = [None, None]
      self.flipCode = None

  def __init__(self):
    PATTERNS_NUM = 3 ** 8
    self.__matrix = [[Index.Element() for i in range(8)] for j in range(PATTERNS_NUM)]
    for code in range(PATTERNS_NUM):
      self.__initRow(code)

  # <概要> __matrix[code]を初期化する
  # <引数> code:int(0~6560)
  def __initRow(self, code):
    line = Index.__decode(code)  # codeをデコード
    for x in range(8):
      self.__initElement(code, x, line)  # lineの位置xに駒を置くときの処理を計算する

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
        self.__matrix[code][x].fliped[color]  = (-takesLeft, takesRight)
        self.__matrix[code][x].takes[color]   = takesLeft + takesRight
        self.__matrix[code][x].putCode[color] = Index.__encode(flipedLine)
    else:
      flipedLine = list(line)
      flipedLine[x] = not flipedLine[x]
      self.__matrix[code][x].flipCode = Index.__encode(flipedLine)

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
    return self.__matrix[code][x].takes[color]

  # <概要> codeに符号化されるマス列の位置xにcolor色の駒を置いたあとのマス列を符号化した値と,
  #        codeに符号化されるマス列の位置xにcolor色の駒を置いたときに裏返る左右それぞれの駒の数を返す
  def flipLine(self, code, x, color):
    return (self.__matrix[code][x].putCode[color], self.__matrix[code][x].fliped[color])

  # <概要> codeに符号化されるマス列の位置xの駒が裏返ったあとのマス列を符号化した値を返す
  def flipCell(self, code, x):
    return self.__matrix[code][x].flipCode