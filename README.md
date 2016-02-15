# othello

<b>Cellクラス:</b><br>
x, y  : セルの位置 (0~7, 0~7)<br>
state : セルの状態 (WHITE / BLACK / EMPTY)<br>

<b>Boardクラス：</b><br>
board : オセロの盤面の実体 (Cellが8*8=64個の1次元リスト)<br>
at(x, y) : 盤面の2次元平面の位置(x, y)に対応するCellを返す<br>
takes(x, y) : (x, y)の位置にコマを置いた場合に取れる相手のコマの数を返す<br>
evauate() : AIの思考関数の本体．毎ターンで盤面を評価し，次にコマを置くべき位置(x, y)を返す<br>
placeable(x, y) : 位置(x, y)にコマを置けるか判定．TrueかFalseを返す<br>
placeableCells() : コマを置くことができるセルのリストを返す<br>

<b>TODO :<br>
・takes関数の実装<br>
・evaluate関数の実装<br>
・AIの先攻後攻を決めれるように<br>
・Undo機能の実装<br>
</b>

<b>動作環境：</b>
Python2.7 + pygame
