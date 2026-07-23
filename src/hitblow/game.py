"""ゲームの進行（入力・表示・ループ）。

★ チームで足す機能は 自分の担当の場所 に書く（1機能=1ファイル）。
   下の「ここに足す」場所は3か所（① 開始時 ② 入力コマンド ③ 勝利時）。
   ペアごとに別の場所を直すので、並行作業でも衝突しない。
   import も自分の場所の近くに書くこと（ファイル先頭にまとめない＝衝突回避）。
"""

from .core import judge, make_secret16, make_secret10
from .Games_Hit_and_Brow_GUI import main

def play(digits=3):
        main()
