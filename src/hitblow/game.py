"""ゲームの進行（入力・表示・ループ）。

★ チームで足す機能は 自分の担当の場所 に書く（1機能=1ファイル）。
   下の「ここに足す」場所は3か所（① 開始時 ② 入力コマンド ③ 勝利時）。
   ペアごとに別の場所を直すので、並行作業でも衝突しない。
   import も自分の場所の近くに書くこと（ファイル先頭にまとめない＝衝突回避）。
"""

from .core import judge, make_secret16, make_secret10
from .Games_Hit_and_Brow_GUI import main

def play(digits=3):
    
    # =========================================================
    # 全体を囲む外側のループ（4が入力されるまでゲームを繰り返す）
    # =========================================================
    while True:
        Max_Limit_Play_16 = 15 
        print(f"\n=== 新しいゲームを開始します ===")
        print(f"Hit & Blow（{digits} 桁・重複なし）")

        # ===== ① 開始時に足す（難易度・あいさつ など）: ここに書く =====
        import random
        from .core import make_secret10, make_secret16  # 追加された関数をインポート

        # モード選択（正しい入力が来るまでループ）
        while True:
            mode = input("モードを選択 (1:10進数, 2:16進数, 3:協力モード, 4:終了, 5:GUIモード) > ").strip()
            if mode in ["1", "2", "3", "4","5"]:
                break
            print("【エラー】1, 2, 3, 4, 5 のいずれかを入力してください。")
        
        # 「4:終了」が選ばれたら、外側のループを抜けてプログラム自体を終わらせる
        if mode == "4":
            print("ゲームを終了します。遊んでくれてありがとう！")
            break
        elif mode == "5":
            break
            
            
        
        # モードに応じた初期設定
        is_coop_mode = (mode == "3")
        coop_hint = "なし"
        valid_chars = "0123456789" # デフォルトは10進数
        
        if mode == "1":
            secret = make_secret10(digits)
            valid_chars = "0123456789"
            print(f"【10進数モード】{digits} 桁の数字を当ててください。")
        elif mode == "2":
            secret = make_secret16(digits)
            valid_chars = "0123456789ABCDEF"
            print(f"【16進数モード】{digits} 桁の16進数を当ててください。")
        elif mode == "3":
            print("\n=== 協力モードを開始します ===")
            theme = "かわいい生物"
            options = ["ライオン", "カワウソ", "犬", "猫", "パンダ"]
            print(f"お題 : {theme}")
            
            # 毎回の入力時に表示するマッピングテキストを作成
            mapping_str = ", ".join([f"{opt} = {i+1}" for i, opt in enumerate(options)])
            
            # 協力モードではシステム側の正解は使わないので空にしておく
            secret = ""
            
            print("\n--- ユーザー1、あなたの順位を入力してください ---")
            print(mapping_str)
            print("=======\n数字を入力してください。")
            u1_guess = ""
            for r in range(1, digits + 1):
                while True:
                    val = input(f"{r}位 : ").strip()
                    if val.isdigit():
                        u1_guess += val
                        break
                    print("【エラー】番号（数字）で入力してください。")
                
            input("\nユーザー2に代わってください。Enterキーを押してください...")
            
            print("\n--- ユーザー2、あなたの順位を入力してください ---")
            print(mapping_str)
            print("=======\n数字を入力してください。")
            u2_guess = ""
            for r in range(1, digits + 1):
                while True:
                    val = input(f"{r}位 : ").strip()
                    if val.isdigit():
                        u2_guess += val
                        break
                    print("【エラー】番号（数字）で入力してください。")
                
            print("\n設定が完了しました。ゲームを開始します！")
            
            # 初回の判定用に初期値を保存しておく
            u1_init = u1_guess
            u2_init = u2_guess
        # =============================================================

        tries = 0
        game_active = True  # ★ breakの代わりにループを制御するフラグ
        
        while game_active:
            # 協力モードの場合は特殊なターン処理を行うため、通常の「予想 >」をスキップする
            if is_coop_mode:
                pass
            else:
                guess = input("予想 > ").strip()

            # ===== ② 入力コマンドに足す（ヒント など）: ここに書く =====
            if is_coop_mode:
                # ==========================
                # ユーザー1のターン
                # ==========================
                input("\nユーザー1に代わってください。Enterキーを押してください...")
                print(f"\n【ターン {tries + 1}】")
                print(mapping_str)
                print("=======")
                
                if coop_hint != "なし":
                    print(f"相手からのヒント: {coop_hint}")
                    
                # 初回のみ、お互いの「初期入力」の比較結果を表示
                if tries == 0:
                    hit_init, blow_init = judge(u2_init, u1_init)
                    print(f"あなたの初期順位の判定結果(相手との一致度) -> Hit: {hit_init} Blow: {blow_init}")

                while True:
                    guess = input(f"ユーザー1、変更後の順位を数値({digits}桁)で入力してください > ").strip()
                    if guess.isdigit() and len(guess) == digits:
                        u1_guess = guess
                        break
                    print(f"【エラー】{digits}桁の数字で入力してください。")
                    
                coop_hint = input("ユーザー2へのヒントを10文字以内で入力してください > ").strip()[:10]
                
                tries += 1
                # ユーザー2の「現在の状態」とユーザー1の「変更後の状態」を比較
                hit, blow = judge(u2_guess, u1_guess)
                print(f"判定結果 -> Hit: {hit} Blow: {blow}")
                print(f"残りの回答回数は{Max_Limit_Play_16 - tries}回です")
                
                # ★ breakの代わりにフラグを操作
                if hit == digits:
                    print(f"正解！お互いの心が通じ合いました！ {tries} 回で達成！")
                    game_active = False
                    continue
                elif (Max_Limit_Play_16 - tries <= 0):
                    print(f"Game_Over! 協力失敗です")
                    game_active = False
                    continue

                # ==========================
                # ユーザー2のターン
                # ==========================
                input("\nユーザー2に代わってください。Enterキーを押してください...")
                print(f"\n【ターン {tries + 1}】")
                print(mapping_str)
                print("=======")
                
                print(f"相手からのヒント: {coop_hint}")
                
                # ユーザー2の初回変更時（tries == 1）のみ、初期入力同士の比較結果を表示
                if tries == 1:
                    hit_init, blow_init = judge(u1_init, u2_init)
                    print(f"あなたの初期順位の判定結果(相手との一致度) -> Hit: {hit_init} Blow: {blow_init}")

                while True:
                    guess = input(f"ユーザー2、変更後の順位を数値({digits}桁)で入力してください > ").strip()
                    if guess.isdigit() and len(guess) == digits:
                        u2_guess = guess
                        break
                    print(f"【エラー】{digits}桁の数字で入力してください。")
                    
                coop_hint = input("ユーザー1へのヒントを10文字以内で入力してください > ").strip()[:10]
                
                tries += 1
                # ユーザー1の「現在の状態」とユーザー2の「変更後の状態」を比較
                hit, blow = judge(u1_guess, u2_guess)
                print(f"判定結果 -> Hit: {hit} Blow: {blow}")
                print(f"残りの回答回数は{Max_Limit_Play_16 - tries}回です")
                
                # ★ breakの代わりにフラグを操作
                if hit == digits:
                    print(f"正解！お互いの心が通じ合いました！ {tries} 回で達成！")
                    game_active = False
                elif (Max_Limit_Play_16 - tries <= 0):
                    print(f"Game_Over! 協力失敗です")
                    game_active = False
                    
                continue
            # =============================================================

            # --- 通常モード（1 or 2）の入力チェック（10進数・16進数両対応） ---
            if len(guess) != digits:
                print(f"{digits} 桁の文字で入力してね")
                continue
                
            is_invalid_char = False
            for i in guess:
                if i not in valid_chars:
                    is_invalid_char = True
                    break
                    
            if is_invalid_char:
                if mode == "1":
                    print(f"10進数の {digits} 桁で入力してね（使える文字: 0-9）")
                else:
                    print(f"16進数の {digits} 桁で入力してね（使える文字: 0-9, A-F）")
                continue
            # ----------------------------------------------------------------

            tries += 1
            hit, blow = judge(secret, guess)
            print(f"  Hit={hit}  Blow={blow}")
            print(f"残りの回答回数は{Max_Limit_Play_16 - tries}回です")
            
            if hit == digits:
                # ===== ③ 勝利時に足す（スコア・履歴 など）: ここに書く =====
                # (勝利時の追加処理があればここに書く)
                # ==========================================================
                print(f"正解！ {tries} 回で当たり（答え {secret}）")
                game_active = False  # ★ breakから変更

            elif (Max_Limit_Play_16 - tries <= 0):
                print(f"Game_Over!（答えは {secret} でした） ")
                game_active = False  # ★ breakから変更

    if mode == "5":
        main()
