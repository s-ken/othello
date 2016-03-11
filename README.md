# othello

<b>動作環境：</b><br>
Python2.7 + pygame

<b>Boardクラス：</b><br>
board : オセロの盤面の実体 (int(short?)型のインデックスが水平11個,垂直11個,斜め8*2=16個,合計38次元int(short?)型リスト)<br>
...インデックスボードについての詳細は http://sealsoft.jp/thell/algorithm.html<br>
at(x, y) : 盤面の2次元平面の位置(x, y)に対応するマスの状態(黒=0,白=1,空=2)を返す<br>
takes(pos, color) : 位置pos(=x+y*8)にcolor色のコマを置いた場合に取れる相手のコマの数を返す<br>
put(pos, color) : 位置posにcolor色のコマを置く->boardの関係するインデックスが書き換わる<br>
placeable(pos) : 位置posにコマを置けるか判定．TrueかFalseを返す<br>
placeableCells() : コマを置くことができるマスの位置(x+y*8)のリストを返す<br>

<b>Indexクラス</b><br>
takes(code, x, color) : codeに符号化されるマス列の位置xにcolor色の駒を置いたときに裏返る駒の数を返す<br>
flipLine(code, x, color) : codeに符号化されるマス列の位置xにcolor色の駒を置いたあとのマス列を符号化した値と,codeに符号化されるマス列の位置xにcolor色の駒を置いたときに裏返る左右それぞれの駒の数のタプルを返す<br>
flipCell(code, x) : codeに符号化されるマス列の位置xの駒が裏返ったあとのマス列を符号化した値を返す<br>

<b>AIクラス</b><br>
takeTurn() : evaluate()を実行してコマを置く<br>
__evauate() : AIの思考関数の本体．毎ターンで盤面を評価し，次にコマを置くべき位置(x, y)を返す<br>
__evaluateCell(cell) : 引数で与えられたCellにコマを置いたときの評価値を返す.評価値を計算する評価関数はphase毎に変更可能<br>
__alphaBeta(color, height, alpha, beta) : AlphaBeta法による評価関数.(http://uguisu.skr.jp/othello/alpha-beta.html)<br>
探索過程のBoard操作ではDeepCopyでなく各Cellのstateのコピーを採用している.(DeepCopyの場合,処理時間が非常に大きくなるため)<br>
__evaluateLeaf(color) : 呼び出された時点のBoardの状態で,手番がcolorのときの盤面の評価値を返す.現時点では簡易的な重み付けによる実装にしてある(http://uguisu.skr.jp/othello/5-1.html)
canPut() : コマを置ける場所があるかどうかを返す<br>

<b>Youクラス</b><br>
takeTurn() : クリックされた位置にコマを置く<br>
canPut() : コマを置ける場所があるかどうかを返す<br>

<b>Gameクラス</b><br>
run() : ゲームの進行<br>
output() : 結果を出力する<br>

<b>TODO :<br>
<s>・takes関数の実装</s><br>
・evaluate関数の実装<br>
<s>・AIの先攻後攻を決めれるように</s><br>
<s>・Undo機能の実装</s> (BackSpaceでUndo)<br>
・探索アルゴリズムの改良<br>
	→MoveOrderingの実装<br>
	→NegaScout法の実装<br>
	→置換表の実装<br>
	→並列化<br>
・evaluateLeaf関数の本実装<br>
・phase毎の評価関数の実装<br>
	→OpeningBook(定石)の実装<br>
・Indexクラスの行列圧縮<br>
</b>
