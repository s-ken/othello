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
    def __init__(self):
      self.child = {} # key=位置,val=Nodeの辞書型?

  def __init__(self):
    self.__currentNode = self.__initBook()  # 木のrootで初期化
    self.__valid = True

  # <概要> file入力からBookを構築する
  def __initBook(self): # TODO
    root = OpeningBook.Node()
    node = self.__addChild(root, self.__pos2key(2, 3))  # (2,3)に黒
    self.__addChild(node, self.__pos2key(2, 2))         # (2,2)に白
    return root

  def __pos2key(self, x, y):
    return x + y * othello.Config.CELL_NUM

  def __key2pos(self, key):
    return (key % othello.Config.CELL_NUM, key / othello.Config.CELL_NUM)

  # <概要> nodeに子Nodeを追加
  # <返値> 新規追加した子Node
  def __addChild(self, parentNode, key):
    parentNode.child[key] = OpeningBook.Node()
    return parentNode.child[key]

  # <概要> 相手(You)が定石通りにコマを置いているか判定しながらbookを読み進める
  #        この関数は,YouクラスのtakeTurn()内でboard.put()が呼ばれた後に実行される
  # <引数> x:int, y:int
  def proceed(self, x, y):
    key = self.__pos2key(x, y)
    if key in self.__currentNode.child:
      self.__currentNode = self.__currentNode.child[key]  # 相手(You)が定石通り(bookに載ってるパターン)に打ってきたら先に進む
      if not len(self.__currentNode.child):
        self.__valid = False  # 葉Nodeに到達
    else:
      self.__valid = False  # 相手(You)が定石から外れたらOpenBookを捨てて次のphaseへ

  # <概要> bookを読んでコマを置くべき位置を得る
  def readBook(self):
    key = self.__currentNode.child.keys()[0]
    self.__currentNode = self.__currentNode.child[key]
    return self.__key2pos(key) # 候補の一番目を返す(仮)

  # <概要> 現状定石通りかどうかの真偽値を返す
  def isValid(self):
    return self.__valid