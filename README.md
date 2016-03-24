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
takeTurn() : 序盤中盤終盤毎の評価関数を実行してコマを置く<br>
canPut() : コマを置ける場所があるかどうかを返す<br>
__changeBrain() : phase進行<br>

<b>BookBrainクラス</b><br>
 OpeningBookを読みながらゲーム進行する<br>

<b>AlphaBetaBrain</b><br>
ゲーム木をAlphaBeta探索する.葉での盤面評価関数と探索過程でのMoveOrdering関数はコンストラクタ引数で与えられる.<br>

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
->OpeningBook進行への対応<br>
・探索アルゴリズムの改良<br>
	→MoveOrderingの実装<br>
	→NegaScout法の実装<br>
	→置換表の実装<br>
	→並列化<br>
・evaluateLeaf関数の本実装<br>
	<s>→中盤:古典的評価関数(駒の位置,着手可能マス数,確定石数)<br>
	→中盤:統計的評価関数(Logistelloパターンの回帰分析)...python遅すぎて無理ぽい<br>
	<s>→終盤:石差<br>
・phase毎の探索アルゴリズム実装<br>
	→序盤:OpeningBook(定石)の実装<br>
	→中盤:NegaScout法,置換表,浅い探索によるMoveOrdering<br>
	→終盤:WPNS or 速さ優先AlpaBeta<br>
・Indexクラスの行列圧縮...キャッシュヒット率上昇で高速化?<br>
・BitBoardの実装<br>
</b>
