# -*- coding:utf-8 -*-

# OpeningBook : 序盤の最善手(定石)を記録したもの.
#               相手が定石通りにゲームを進めている間はOpeningBookの記述通りにコマを置く.
#               定石から外れた時点でOpeningBookを放棄してゲーム木探索を開始する. 
# OpeningBookについて詳しくは https://skatgame.net/mburo/ps/book.pdf
# Bookのソースファイルは http://www.amy.hi-ho.ne.jp/okuhara/edax.htm のリンク先から.
# リンク先にある Wzebraの Extra-large book テキストデータ は解析しやすそう 
# (http://tosapy.merrymall.net/othello/wzebra/extra-large-txt-20080301.zip)

import othello

# <メンバ> __currentNode:木構造上の現盤面のNode
#          __valid:ゲームが定石通りに進行中か否か
class OpeningBook:

  # 木のNode
  class Node:
    def __init__(self, score=0):
      self.child = {} # key=位置,val=Nodeの辞書型?
      self.score = score

  def __init__(self):
    self.__currentNode = self.__root = self.__initBook()  # 木のrootで初期化
    self.__valid = True
    self.__symm = False
    self.__rote = False

  # <概要> file入力からBookを構築する
  def __initBook(self): # TODO
    #input_file = open("./extra-large-20080301.txt")
    input_file = open("./book_test.txt")
    root = OpeningBook.Node()
    for row in input_file:
      nodes = self.__row2nodes(row)
      self.__addNodes(root, nodes) 
    #node = self.__addChild(root, self.__pos2key(2, 3))  # (2,3)に黒
    #self.__addChild(node, self.__pos2key(2, 2))         # (2,2)に白
    
    currentNode = root
    #print currentNode.child.keys()
    
    return root

  def __pos2key(self, x, y):
    return x + y * othello.Config.CELL_NUM

  def __key2pos(self, key): 
    return (key % othello.Config.CELL_NUM, key / othello.Config.CELL_NUM)

  def __pos2correctedPos(self, x, y):
    if self.__symm:
      x,y = y,x
    if self.__rote:
      x,y = othello.Config.CELL_NUM-1-x, othello.Config.CELL_NUM-1-y
    return x,y

  def __pos2correctedKey(self, x, y):
    x,y = self.__pos2correctedPos(x,y)
    return self.__pos2key(x,y)

  def __key2correctedPos(self, key):
    x,y = self.__key2pos(key)
    return self.__pos2correctedPos(x,y)

  # <概要> "C4"等の位置 --> key
  def __charpos2key(self, charpos): #TODO (implemented, not tested)
    alphabets = ['A','B','C','D','E','F','G','H']
    x = alphabets.index(charpos[0])
    y = int(charpos[1])-1
    return self.__pos2key(x, y)

  # <概要> stringのrow --> (key, score)のリスト
  def __row2nodes(self, row): #TODO (implemented, not tested)
    sep = row.split(" ; ")
    nodes = [(self.__charpos2key(sep[0][i: i+2]), 0) for i in range(0, len(sep[0]), 2)]
    nodes[-1] = (nodes[-1][0], float(sep[1]))
    return nodes

  # <概要> nodeに子Nodeを追加
  # <返値> 新規追加した子Node
  def __addChild(self, parentNode, key, score=0):
    parentNode.child[key] = OpeningBook.Node(score)
    return parentNode.child[key]

  def __addNodes(self, parentNode, nodes): #TODO (implemented, not tested)
    currentNode = parentNode
    for node in nodes:
      keys = currentNode.child.keys()
      if not node[0] in keys:
        currentNode = self.__addChild(currentNode, node[0], node[1])
      else:
        currentNode = currentNode.child[node[0]]

  # <概要> 相手(You)が定石通りにコマを置いているか判定しながらbookを読み進める
  #        この関数は,YouクラスのtakeTurn()内でboard.put()が呼ばれた後に実行される
  # <引数> x:int, y:int
  def proceed(self, x, y):
    if self.__currentNode is self.__root:   # 相手が黒の一手目を打ったらbookとの対称性を記録する
      key = self.__pos2key(x, y)
      if key == 19: # = D3(3,2)
        self.__symm = True
      elif key == 37:  # = F5(5,4)
        self.__rote = True
      elif key == 44: # = E6(4,5)
        self.__symm = True
        self.__rote = True

    key = self.__pos2correctedKey(x,y)
    if key in self.__currentNode.child:
      self.__currentNode = self.__currentNode.child[key]  # 相手(You)が定石通り(bookに載ってるパターン)に打ってきたら先に進む
      if not len(self.__currentNode.child):
        self.__valid = False  # 葉Nodeに到達
    else:
      self.__valid = False  # 相手(You)が定石から外れたらOpenBookを捨てて次のphaseへ

  # <概要> bookを読んでコマを置くべき位置を得る
  def readBook(self):
  
    key = max(self.__currentNode.child.items(), key=lambda x:x[1].score)[0] # score最大ノードのキーを返す
    #key = self.__currentNode.child.keys()[0] # 候補の一番目を返す
    
    self.__currentNode = self.__currentNode.child[key]
    print "On Book"
    return self.__key2correctedPos(key)

  # <概要> 現状定石通りかどうかの真偽値を返す
  def isValid(self):
    return self.__valid
