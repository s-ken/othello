# othello

<b>動作環境：</b><br>
Python2.7 + pygame

<b>Cellクラス:</b><br>
x, y  : セルの位置 (0~7, 0~7)<br>
state : セルの状態 (WHITE / BLACK / EMPTY)<br>

<b>Boardクラス：</b><br>
board :　オセロの盤面の実体 (Cellが8*8=64個の1次元リスト)<br>
at(x, y) : 盤面の2次元平面の位置(x, y)に対応するCellを返す<br>
takes(x, y, color) : (x, y)の位置にcolor色のコマを置いた場合に取れる相手のコマの数を返す<br>
put(x, y, color) : (x, y)の位置にcolor色のコマを置く->boardの各Cellのstateが書き換わる<br>
placeable(x, y) : 位置(x, y)にコマを置けるか判定．TrueかFalseを返す<br>
placeableCells() : コマを置くことができるセルのリストを返す<br>

<b>Indexクラス</b><br>
takes(line, x, color) : Cell列であるlineに対してx番目の位置にcolor色のコマを置いた際に取れる相手のコマの数を返す<br>
flip(line, x, color) : Cell列であるlineに対してx番目の位置にcolor色のコマを置いた際に裏返されるべきコマを裏返す(line内のCell.stateを直接書き換える)<br>

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
・evaluateLeaf関数の本実装<br>
・phase毎の評価関数の実装(序盤は定石(棋譜)使用とか?)<br>
・Indexクラスの行列圧縮<br>
</b>
