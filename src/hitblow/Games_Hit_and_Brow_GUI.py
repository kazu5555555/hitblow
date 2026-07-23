import tkinter as tk
from PIL import Image, ImageTk
import pygame
import os
import time
from .core import judge, make_secret16, make_secret10
import random


# --- シーンの基本となるクラス（設計図） ---
class BaseScene:
    def __init__(self, engine):
        self.engine = engine  # GameEngine本体（canvasやrootを操作するため）
        self.canvas = engine.canvas
        self.root = engine.root

    def enter(self):
        """シーン開始時に呼ばれる（画像の描画やキーのバインドなど）"""
        pass

    def update(self):
        """毎フレーム（game_loop）呼ばれる処理"""
        pass

    def exit(self):
        """シーン終了時に呼ばれる（描画したものを消す、バインドを解除するなど）"""
        pass


# --- タイトル画面のシーン ---
class TitleScene(BaseScene):
    def enter(self):
        self.BGM_list = ["hatena.mp3", "Yuuhi.mp3", "irai.mp3"]
        random.shuffle(self.BGM_list)

        # バックグラウンドイメージの設定とボタンの初期設定
        try:
            img = Image.open(
                os.path.join(
                    os.path.dirname(__file__), "Main_UI", "HitBrow_mainUI_F.jpg"
                )
            )
            img = img.resize((self.engine.DisplayX, self.engine.DisplayY))
            self.title_photo = ImageTk.PhotoImage(img)
            self.canvas.create_image(
                self.engine.DisplayX // 2,
                self.engine.DisplayY // 2,
                image=self.title_photo,
                tag="title_screen",
            )

            Image_mode1 = Image.open(
            os.path.join(os.path.dirname(__file__), "Main_UI", "mode1.png")
            )
            Image_mode1 = Image_mode1.resize((400, 132))
            self.Image_mode1 = ImageTk.PhotoImage(Image_mode1)

            Image_mode2 = Image.open(
            os.path.join(os.path.dirname(__file__), "Main_UI", "mode2.png")
            )
            Image_mode2 = Image_mode2.resize((400, 132))
            self.Image_mode2 = ImageTk.PhotoImage(Image_mode2)

            Image_mode3 = Image.open(
            os.path.join(os.path.dirname(__file__), "Main_UI", "mode3.png")
            )
            Image_mode3 = Image_mode3.resize((400, 132))
            self.Image_mode3 = ImageTk.PhotoImage(Image_mode3)

            self.to_mode1_button = tk.Button(
                self.canvas,
                image=self.Image_mode1,
                bg="white",
                activebackground="#CCCCCC",
                command=self.Go_to_mode1,  # クリック時の処理
                borderwidth=0,  # 枠線を消す（0にすると完全に画像だけになります）
                highlightthickness=0,  # 選択時の枠線も消す
            )
            self.to_mode1_button.pack()

            self.to_mode2_button = tk.Button(
                 self.canvas,
                image=self.Image_mode2,
                bg="white",
                activebackground="#CCCCCC",
                command=self.Go_to_mode2,  # クリック時の処理
                borderwidth=0,  # 枠線を消す（0にすると完全に画像だけになります）
                highlightthickness=0,  # 選択時の枠線も消す
            )
            self.to_mode2_button.pack()

            self.to_mode3_button = tk.Button(
                 self.canvas,
                image=self.Image_mode3,
                bg="white",
                activebackground="#CCCCCC",
                command=self.Go_to_mode3,  # クリック時の処理
                borderwidth=0,  # 枠線を消す（0にすると完全に画像だけになります）
                highlightthickness=0,  # 選択時の枠線も消す
            )
            self.to_mode3_button.pack()

        except FileNotFoundError:
            self.canvas.create_text(
                self.engine.DisplayX // 2,
                self.engine.DisplayY // 2,
                text="Title Image Not Found\nPress Enter to Start",
                font=("Arial", 50),
                tag="title_screen",
            )

        # ボタンの配置
        try:
            self.to_mode1_button_window = self.canvas.create_window(
                self.engine.DisplayX // 2 + 400,
                self.engine.DisplayY // 2 - 150,
                anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
                width=400,  # ボタンの幅
                height=132,  # ボタンの高さ
                window=self.to_mode1_button,  # 埋め込むウィジェットを指定
                tags="Mode1_Button",  # 四角形と同じようにタグを設定可能
            )
            self.to_mode2_button_window = self.canvas.create_window(
                self.engine.DisplayX // 2 + 400,
                self.engine.DisplayY // 2,
                anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
                width=400,  # ボタンの幅
                height=132,  # ボタンの高さ
                window=self.to_mode2_button,  # 埋め込むウィジェットを指定
                tags="Mode2_Button",  # 四角形と同じようにタグを設定可能
            )
            self.to_mode3_button_window = self.canvas.create_window(
                self.engine.DisplayX // 2 + 400,
                self.engine.DisplayY // 2 + 150,
                anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
                width=400,  # ボタンの幅
                height=132,  # ボタンの高さ
                window=self.to_mode3_button,  # 埋め込むウィジェットを指定
                tags="Mode3_Button",  # 四角形と同じようにタグを設定可能
            )

        except FileNotFoundError:
            print("ボタンの配置ができませんでした")

        self.sound_number = 0
        self.Sound_BGM(self.BGM_list[self.sound_number])

    def Go_to_mode1(self):
        print("モード1を開始します")
        self.engine.change_scene(GameScene1(self.engine))

    def Go_to_mode2(self):
        print("モード2を開始します")
        self.engine.change_scene(GameScene2(self.engine))

    def Go_to_mode3(self):
        print("モード3を開始します")
        self.engine.change_scene(GameScene3(self.engine))

    def Sound_BGM(self, filename):
        try:
            # BGMファイルをロード
            pygame.mixer.music.load(
                os.path.join(os.path.dirname(__file__), "Main_BGM", filename)
            )
            pygame.mixer.music.play()
            print("BGM再生開始!")

        except pygame.error:
            print(f"BGMファイル({filename})が見つかりません。無音で進行します。")

    def play_next_bgm(self):
        # 次の曲番号へ進める（リストの長さで割った余りにすることで 0->1->2->3->0 とループ）
        self.sound_number = (self.sound_number + 1) % len(self.BGM_list)
        # 次の曲を再生
        self.Sound_BGM(self.BGM_list[self.sound_number])

    def update(self):
        if not pygame.mixer.music.get_busy():
            print("曲が終わったので次の曲へ切り替えます")
            self.play_next_bgm()

    def exit(self):
        # 次の画面に行く前に、自分の出した画像とキー設定を綺麗にお掃除
        self.canvas.delete("title_screen")
        self.canvas.delete("Mode1_Button")
        self.canvas.delete("Mode2_Button")
        self.canvas.delete("Mode3_Button")
        pygame.mixer.music.stop()


# --- ゲーム本編のシーン ---
class GameScene1(BaseScene):
    def enter(self):
        print("ゲームシーン1を開始します")
        self.Start_time = time.time()
        self.secret = make_secret16(3)
        self.result_list = []
        self.Clear_flag = False
        self.flag_TimeUp = False

        self.keyNumber_STR1 = "0"
        self.keyNumber_STR2 = "0"
        self.keyNumber_STR3 = "0"

        self.engine.Try_score1 = 0
        self.engine.Time_score1 = 0
        self.engine.result_score1 = 0

        self.check_number = (
            self.keyNumber_STR1 + self.keyNumber_STR2 + self.keyNumber_STR3
        )

        # メインUI
        BackGround_img = Image.open(
            os.path.join(
                os.path.dirname(__file__), "Main_UI", "GameMode1_16_mainUI.png"
            )
        )
        BackGround_img = BackGround_img.resize(
            (self.engine.DisplayX, self.engine.DisplayY)
        )
        self.BackGround_img = ImageTk.PhotoImage(BackGround_img)

        self.canvas.create_image(
            self.engine.DisplayX // 2,
            self.engine.DisplayY // 2,
            image=self.BackGround_img,
            tag="BackGround_img",
        )

        # 矢印UI_UP
        Image_UP_Yajirushi = Image.open(
            os.path.join(os.path.dirname(__file__), "Main_UI", "UP_Yajirushi.png")
        )
        Image_UP_Yajirushi = Image_UP_Yajirushi.resize((100, 25))
        self.Image_UP_Yajirushi = ImageTk.PhotoImage(Image_UP_Yajirushi)

        # 矢印UI_Down
        Image_Down_Yajirushi = Image.open(
            os.path.join(os.path.dirname(__file__), "Main_UI", "DOWN_Yajirushi.png")
        )
        Image_Down_Yajirushi = Image_Down_Yajirushi.resize((100, 25))
        self.Image_Down_Yajirushi = ImageTk.PhotoImage(Image_Down_Yajirushi)

        # タイトルバックボタン
        Image_TitleBack = Image.open(
            os.path.join(os.path.dirname(__file__), "Main_UI", "Return_To_Title.png")
        )
        Image_TitleBack = Image_TitleBack.resize((400, 88))
        self.Image_TitleBack = ImageTk.PhotoImage(Image_TitleBack)

        # タイトルバックボタン設定------------------------------------
        self.Return_Title_button = tk.Button(
            self.canvas,
            image=self.Image_TitleBack,
            bg="white",
            activebackground="#CCCCCC",
            command=self.Return_to_title,  # クリック時の処理
            borderwidth=0,  # 枠線を消す（0にすると完全に画像だけになります）
            highlightthickness=0,  # 選択時の枠線も消す
        )
        self.Return_Title_Button_window = self.canvas.create_window(
            self.engine.DisplayX // 2 - 430,
            self.engine.DisplayY // 2 - 270,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=400,  # ボタンの幅
            height=88,  # ボタンの高さ
            window=self.Return_Title_button,  # 埋め込むウィジェットを指定
            tags="Return_Title_Button",  # 四角形と同じようにタグを設定可能
        )

        # SUBMITボタン
        Image_SUBMIT = Image.open(
            os.path.join(os.path.dirname(__file__), "Main_UI", "SUBMIT.png")
        )
        Image_SUBMIT = Image_SUBMIT.resize((260, 50))
        self.Image_SUBMIT = ImageTk.PhotoImage(Image_SUBMIT)

        self.SubMit = tk.Button(
            self.canvas,
            image=self.Image_SUBMIT,
            bg="white",
            activebackground="#CCCCCC",
            command=self.Create_Result_Chacks,  # クリック時の処理  # クリック時の処理
            borderwidth=0,  # 枠線を消す（0にすると完全に画像だけになります）
            highlightthickness=0,  # 選択時の枠線も消す
        )
        self.SubMit_window = self.canvas.create_window(
            self.engine.DisplayX // 2 - 50,
            self.engine.DisplayY // 2 + 210,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=260,  # ボタンの幅
            height=50,  # ボタンの高さ
            window=self.SubMit,  # 埋め込むウィジェットを指定
            tags="SubMit",  # 四角形と同じようにタグを設定可能
        )

        # NumberUpボタン1
        self.UpNumber1 = tk.Button(
            self.canvas,
            image=self.Image_UP_Yajirushi,
            bg="white",
            activebackground="#CCCCCC",
            command=self.NumberBox_UP1,  # クリック時の処理
            borderwidth=0,  # 枠線を消す（0にすると完全に画像だけになります）
            highlightthickness=0,  # 選択時の枠線も消す
        )
        self.UpNumber1_window = self.canvas.create_window(
            self.engine.DisplayX // 2 - 385,
            self.engine.DisplayY // 2 - 70,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=100,  # ボタンの幅
            height=25,  # ボタンの高さ
            window=self.UpNumber1,  # 埋め込むウィジェットを指定
            tags="UpNumber1",  # 四角形と同じようにタグを設定可能
        )
        # NumberUpボタン2
        self.UpNumber2 = tk.Button(
            self.canvas,
            image=self.Image_UP_Yajirushi,
            bg="white",
            activebackground="#CCCCCC",
            command=self.NumberBox_UP2,  # クリック時の処理
            borderwidth=0,  # 枠線を消す（0にすると完全に画像だけになります）
            highlightthickness=0,  # 選択時の枠線も消す
        )
        self.UpNumber2_window = self.canvas.create_window(
            self.engine.DisplayX // 2 - 225,
            self.engine.DisplayY // 2 - 70,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=100,  # ボタンの幅
            height=25,  # ボタンの高さ
            window=self.UpNumber2,  # 埋め込むウィジェットを指定
            tags="UpNumber2",  # 四角形と同じようにタグを設定可能
        )
        # NumberUpボタン3
        self.UpNumber3 = tk.Button(
            self.canvas,
            image=self.Image_UP_Yajirushi,
            bg="white",
            activebackground="#CCCCCC",
            command=self.NumberBox_UP3,  # クリック時の処理
            borderwidth=0,  # 枠線を消す（0にすると完全に画像だけになります）
            highlightthickness=0,  # 選択時の枠線も消す
        )
        self.UpNumber3_window = self.canvas.create_window(
            self.engine.DisplayX // 2 - 70,
            self.engine.DisplayY // 2 - 70,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=100,  # ボタンの幅
            height=25,  # ボタンの高さ
            window=self.UpNumber3,  # 埋め込むウィジェットを指定
            tags="UpNumber3",  # 四角形と同じようにタグを設定可能
        )
        # NumberDownボタン1
        self.DownNumber1 = tk.Button(
            self.canvas,
            image=self.Image_Down_Yajirushi,
            bg="white",
            activebackground="#CCCCCC",
            command=self.NumberBox_Down1,  # クリック時の処理
            borderwidth=0,  # 枠線を消す（0にすると完全に画像だけになります）
            highlightthickness=0,
        )
        self.DownNumber1_window = self.canvas.create_window(
            self.engine.DisplayX // 2 - 385,
            self.engine.DisplayY // 2 + 135,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=100,  # ボタンの幅
            height=25,  # ボタンの高さ
            window=self.DownNumber1,  # 埋め込むウィジェットを指定
            tags="DownNumber1",  # 四角形と同じようにタグを設定可能
        )
        # NumberDownボタン2
        self.DownNumber2 = tk.Button(
            self.canvas,
            image=self.Image_Down_Yajirushi,
            bg="white",
            activebackground="#CCCCCC",
            command=self.NumberBox_Down2,  # クリック時の処理
            borderwidth=0,  # 枠線を消す（0にすると完全に画像だけになります）
            highlightthickness=0,
        )
        self.DownNumber2_window = self.canvas.create_window(
            self.engine.DisplayX // 2 - 225,
            self.engine.DisplayY // 2 + 135,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=100,  # ボタンの幅
            height=25,  # ボタンの高さ
            window=self.DownNumber2,  # 埋め込むウィジェットを指定
            tags="DownNumber2",  # 四角形と同じようにタグを設定可能
        )
        # NumberDownボタン3
        self.DownNumber3 = tk.Button(
            self.canvas,
            image=self.Image_Down_Yajirushi,
            bg="white",
            activebackground="#CCCCCC",
            command=self.NumberBox_Down3,  # クリック時の処理
            borderwidth=0,  # 枠線を消す（0にすると完全に画像だけになります）
            highlightthickness=0,
        )
        self.DownNumber3_window = self.canvas.create_window(
            self.engine.DisplayX // 2 - 70,
            self.engine.DisplayY // 2 + 135,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=100,  # ボタンの幅
            height=25,  # ボタンの高さ
            window=self.DownNumber3,  # 埋め込むウィジェットを指定
            tags="DownNumber3",  # 四角形と同じようにタグを設定可能
        )

        self.TimeText = self.canvas.create_text(
            self.engine.DisplayX // 2 + 10,
            self.engine.DisplayY // 2 - 230,
            text="0",
            fill="white",  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 40),  # フォントとサイズ
            anchor="center",  # 基準点
            tags="TimeText",  # タグをつけて管理可能
        )

        self.Number1_text = self.canvas.create_text(
            self.engine.DisplayX // 2 - 385,
            self.engine.DisplayY // 2 + 40,
            text="0",
            fill="black",  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 100),  # フォントとサイズ
            anchor="center",  # 基準点
            tags="Number1_text",  # タグをつけて管理可能
        )
        self.Number2_text = self.canvas.create_text(
            self.engine.DisplayX // 2 - 225,
            self.engine.DisplayY // 2 + 40,
            text="0",
            fill="black",  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 100),  # フォントとサイズ
            anchor="center",  # 基準点
            tags="Number2_text",  # タグをつけて管理可能
        )
        self.Number3_text = self.canvas.create_text(
            self.engine.DisplayX // 2 - 70,
            self.engine.DisplayY // 2 + 40,
            text="0",
            fill="black",  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 100),  # フォントとサイズ
            anchor="center",  # 基準点
            tags="Number3_text",  # タグをつけて管理可能
        )
        self.Result_text = self.canvas.create_text(
            self.engine.DisplayX // 2 + 360,
            self.engine.DisplayY // 2 - 10,
            text="",
            fill="white",  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 14),  # フォントとサイズ
            anchor="n",  # 基準点
            tags="Result_text",  # タグをつけて管理可能
        )
        self.Sound_BGM()

    def Sound_BGM(self):
        try:
            # BGMファイルをロード
            pygame.mixer.music.load(
                os.path.join(
                    os.path.dirname(__file__), "Main_BGM", "HitBrow_Games_Limit.mp3"
                )
            )
            pygame.mixer.music.play(1)
            print("BGM再生開始!")

        except pygame.error:
            print(
                "BGMファイル(HitBrow_Games_Limit.mp3)が見つかりません。無音で進行します。"
            )

    def Return_to_title(self):
        print("タイトルバックボタンが押されました。タイトル画面に戻ります")
        self.engine.change_scene(TitleScene(self.engine))

    def Go_to_Result(self):
        print("ゲームモード1が通常終了されました")
        self.engine.change_scene(GameScene1_Result(self.engine))

    def NumberBox_UP1(self):
        if self.flag_TimeUp:
            return

        Number_list = [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
        ]
        self.keyNumber_STR1 = Number_list[
            (Number_list.index(self.keyNumber_STR1) + 1) % 16
        ]
        self.canvas.itemconfig("Number1_text", text=self.keyNumber_STR1)

    def NumberBox_UP2(self):
        if self.flag_TimeUp:
            return
        Number_list = [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
        ]
        self.keyNumber_STR2 = Number_list[
            (Number_list.index(self.keyNumber_STR2) + 1) % 16
        ]
        self.canvas.itemconfig("Number2_text", text=self.keyNumber_STR2)

    def NumberBox_UP3(self):
        if self.flag_TimeUp:
            return
        Number_list = [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
        ]
        self.keyNumber_STR3 = Number_list[
            (Number_list.index(self.keyNumber_STR3) + 1) % 16
        ]
        self.canvas.itemconfig("Number3_text", text=self.keyNumber_STR3)

    def NumberBox_Down1(self):
        if self.flag_TimeUp:
            return
        Number_list = [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
        ]
        self.keyNumber_STR1 = Number_list[
            (Number_list.index(self.keyNumber_STR1) + 15) % 16
        ]
        self.canvas.itemconfig("Number1_text", text=self.keyNumber_STR1)

    def NumberBox_Down2(self):
        if self.flag_TimeUp:
            return
        Number_list = [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
        ]
        self.keyNumber_STR2 = Number_list[
            (Number_list.index(self.keyNumber_STR2) + 15) % 16
        ]
        self.canvas.itemconfig("Number2_text", text=self.keyNumber_STR2)

    def NumberBox_Down3(self):
        if self.flag_TimeUp:
            return
        Number_list = [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
        ]
        self.keyNumber_STR3 = Number_list[
            (Number_list.index(self.keyNumber_STR3) + 15) % 16
        ]
        self.canvas.itemconfig("Number3_text", text=self.keyNumber_STR3)

    def Timer(self, TimeUp_Time):
        delta_time = -(self.Start_time - time.time())

        if delta_time < TimeUp_Time:
            self.canvas.itemconfig(
                "TimeText", text=str(round(TimeUp_Time - delta_time))
            )
            self.engine.Time_score1 = TimeUp_Time - delta_time
        if delta_time >= TimeUp_Time:
            self.engine.Time_score1 = 0
            self.flag_TimeUp = True
            if delta_time > TimeUp_Time + 8:
                print("タイムアップ")
                self.engine.Try_score1 = 0
                self.Go_to_Result()

    def Create_Result_Chacks(self):
        if self.flag_TimeUp:
            return
        self.engine.Try_score1 += 1
        self.check_number = (
            self.keyNumber_STR1 + self.keyNumber_STR2 + self.keyNumber_STR3
        )
        hit, blow = judge(self.secret, self.check_number)
        result = {"user_number": self.check_number, "hit": hit, "blow": blow}
        self.result_list.append(result)

        if len(self.result_list) > 14:
            self.result_list.pop(0)

        log_lines = [
            f"あなたの選択した数字: {log['user_number']}, Hit: {log['hit']}, Blow: {log['blow']}"
            for log in self.result_list
        ]
        log_text = "\n".join(log_lines)
        self.canvas.itemconfig("Result_text", text=log_text)

        if hit == 3:
            self.Clear_flag = True
            self.engine.result_score1 = (
                self.engine.Time_score1 * 100 - self.engine.Try_score1 * 100
            )
            self.Go_to_Result()

    def update(self):
        self.Timer(120)
        # デバッグ用
        # self.engine.change_scene(GameScene1_Result(self.engine))

    def exit(self):
        self.canvas.delete("BackGround_img")
        self.canvas.delete("Return_Title_Button")
        self.canvas.delete("UpNumber1")
        self.canvas.delete("UpNumber2")
        self.canvas.delete("UpNumber3")
        self.canvas.delete("DownNumber1")
        self.canvas.delete("DownNumber2")
        self.canvas.delete("DownNumber3")
        self.canvas.delete("TimeText")
        self.canvas.delete("Number1_text")
        self.canvas.delete("Number2_text")
        self.canvas.delete("Number3_text")
        self.canvas.delete("SubMit")
        self.canvas.delete("Result_text")
        pygame.mixer.music.stop()


class GameScene1_Result(BaseScene):
    def enter(self):
        self.Rank_text = "D"
        self.Score_text = 0

        BackGround_img = Image.open(
            os.path.join(
                os.path.dirname(__file__), "Main_UI", "HitBrow_Mode1_Result.PNG"
            )
        )
        BackGround_img = BackGround_img.resize(
            (self.engine.DisplayX, self.engine.DisplayY)
        )
        self.BackGround_img = ImageTk.PhotoImage(BackGround_img)
        self.canvas.create_image(
            self.engine.DisplayX // 2,
            self.engine.DisplayY // 2,
            image=self.BackGround_img,
            tag="BackGround_img",
        )
        # タイトルバックボタン設定------------------------------------
        Image_TitleBack = Image.open(
            os.path.join(os.path.dirname(__file__), "Main_UI", "Return_To_Title.png")
        )
        Image_TitleBack = Image_TitleBack.resize((400, 88))
        self.Image_TitleBack = ImageTk.PhotoImage(Image_TitleBack)

        self.Return_Title_button = tk.Button(
            self.canvas,
            image=self.Image_TitleBack,
            bg="white",
            activebackground="#CCCCCC",
            command=self.Return_to_title,  # クリック時の処理
            borderwidth=0,  # 枠線を消す（0にすると完全に画像だけになります）
            highlightthickness=0,  # 選択時の枠線も消す
        )
        self.Return_Title_Button_window = self.canvas.create_window(
            self.engine.DisplayX // 2 + 400,
            self.engine.DisplayY // 2 + 300,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=400,  # ボタンの幅
            height=88,  # ボタンの高さ
            window=self.Return_Title_button,  # 埋め込むウィジェットを指定
            tags="Return_Title_Button",  # 四角形と同じようにタグを設定可能
        )
        # タイトルバックボタン設定(ここまで)-----------------------------------

        print(f"トータルスコア : {5000 + self.engine.result_score1}")
        print(f"タイムスコア : {self.engine.Time_score1}")
        print(f"トライスコア : -{self.engine.Try_score1}")

        if self.engine.Time_score1 <= 0:
            self.Sound_BGM_D_score()
        else:
            self.Sound_BGM_S_score()

        self.Result_text_comment = "Thank You For Playing!"
        if self.engine.result_score1 + 5000 >= 14000:
            self.Rank_text = "S"
            self.color = "yellow"
            self.Result_text_comment = "一言コメント : \n天才！秀才！大合唱！"
        elif self.engine.result_score1 + 5000 >= 12000:
            self.Rank_text = "A"
            self.color = "red"
            self.Result_text_comment = "一言コメント : \nSランクまでもう一歩！"
        elif self.engine.result_score1 + 5000 >= 11000:
            self.Rank_text = "B"
            self.color = "blue"
            self.Result_text_comment = (
                "一言コメント : \n試行回数が増えると点数は減ります"
            )
        elif self.engine.result_score1 + 5000 >= 9000:
            self.Rank_text = "C"
            self.color = "orange"
            self.Result_text_comment = "一言コメント : \n早く正解すると点数が上がるよ！"
        elif self.engine.Time_score1 > 0:
            self.Rank_text = "D"
            self.color = "green"
            self.Result_text_comment = (
                "一言コメント : \n残念...。もう少し頑張りましょう！"
            )

        else:
            self.Rank_text = "D"
            self.color = "green"
            self.Result_text_comment = "一言コメント : \nもしかして放置した？"

        if self.engine.Try_score1 == 1:
            self.Result_text_comment = (
                "一言コメント : \n一発クリアの確率は約0.03%! 豪運!"
            )
        elif self.engine.Try_score1 == 2:
            self.Result_text_comment = "一言コメント : \n早くないですか？当てるの。"
        elif self.engine.Try_score1 == 3:
            self.Result_text_comment = (
                "一言コメント : \n期待値は5回らしいよ(gemini調べ)"
            )

        self.Rank_text = self.canvas.create_text(
            self.engine.DisplayX // 2 + 400,
            self.engine.DisplayY // 2 - 100,
            text=self.Rank_text,
            fill=self.color,  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 270),  # フォントとサイズ
            anchor="center",  # 基準点
            tags="Rank_text",  # タグをつけて管理可能
        )

        self.TimeScore_text = self.canvas.create_text(
            self.engine.DisplayX // 2 - 185,
            self.engine.DisplayY // 2 - 50,
            text=f"{round(self.engine.Time_score1, 2)}s",
            fill="black",  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 40),  # フォントとサイズ
            anchor="center",  # 基準点
            tags="TimeScore_text",  # タグをつけて管理可能
        )
        self.TryScore_text = self.canvas.create_text(
            self.engine.DisplayX // 2 - 430,
            self.engine.DisplayY // 2 - 160,
            text=f"{round(self.engine.Try_score1, 2)}回",
            fill="black",  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 50),  # フォントとサイズ
            anchor="center",  # 基準点
            tags="TryScore_text",  # タグをつけて管理可能
        )
        self.Score_text = self.canvas.create_text(
            self.engine.DisplayX // 2 + 130,
            self.engine.DisplayY // 2 + 10,
            text="",
            fill="black",  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 50),  # フォントとサイズ
            anchor="center",  # 基準点
            tags="Score_text",  # タグをつけて管理可能
        )
        self.Comment_text = self.canvas.create_text(
            self.engine.DisplayX // 2 - 300,
            self.engine.DisplayY // 2 + 230,
            text=self.Result_text_comment,
            fill="white",  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 25),  # フォントとサイズ
            anchor="center",  # 基準点
            tags="Comment_text",  # タグをつけて管理可能
        )

    def Return_to_title(self):
        print("タイトルバックボタンが押されました。タイトル画面に戻ります")
        self.engine.change_scene(TitleScene(self.engine))

    def Sound_BGM_S_score(self):
        try:
            # BGMファイルをロード
            pygame.mixer.music.load(
                os.path.join(os.path.dirname(__file__), "Main_BGM", "S_ranks_BGM.mp3")
            )
            pygame.mixer.music.play(-1)
            print("BGM再生開始!")

        except pygame.error:
            print("BGMファイル(S_ranks_BGM.mp3)が見つかりません。無音で進行します。")

    def Sound_BGM_D_score(self):
        try:
            # BGMファイルをロード
            pygame.mixer.music.load(
                os.path.join(os.path.dirname(__file__), "Main_BGM", "Oh_my_god.mp3")
            )
            pygame.mixer.music.play(-1)
            print("BGM再生開始!")

        except pygame.error:
            print("BGMファイル(Oh_my_god.mp3)が見つかりません。無音で進行します。")

    def update(self):
        if self.Score_text < round(self.engine.result_score1 + 5000, 2):
            self.Score_text = round(self.Score_text + 70, 0)
            self.canvas.itemconfig("Score_text", text=f"{self.Score_text}点")
        else:
            self.canvas.itemconfig(
                "Score_text", text=f"{round(self.engine.result_score1 + 5000, 0)}点"
            )

    def exit(self):
        self.canvas.delete("BackGround_img")
        self.canvas.delete("Return_Title_Button")
        self.canvas.delete("Rank_text")
        self.canvas.delete("TimeScore_text")
        self.canvas.delete("TryScore_text")
        self.canvas.delete("Score_text")
        self.canvas.delete("Comment_text")
        self.engine.result_score1 = 0
        self.engine.Time_score1 = 0
        self.engine.Try_score1 = 0
        pygame.mixer.music.stop()


class GameScene2(BaseScene):
    def enter(self):
        print("ゲームシーン1を開始します")
        self.Start_time = time.time()
        self.secret = make_secret10(3)
        self.result_list = []
        self.Clear_flag = False
        self.flag_TimeUp = False

        self.keyNumber_STR1 = "0"
        self.keyNumber_STR2 = "0"
        self.keyNumber_STR3 = "0"

        self.engine.Try_score1 = 0
        self.engine.Time_score1 = 0
        self.engine.result_score1 = 0

        self.check_number = (
            self.keyNumber_STR1 + self.keyNumber_STR2 + self.keyNumber_STR3
        )

        # メインUI
        BackGround_img = Image.open(
            os.path.join(
                os.path.dirname(__file__), "Main_UI", "GameMode2_10_mainUI.png"
            )
        )
        BackGround_img = BackGround_img.resize(
            (self.engine.DisplayX, self.engine.DisplayY)
        )
        self.BackGround_img = ImageTk.PhotoImage(BackGround_img)

        self.canvas.create_image(
            self.engine.DisplayX // 2,
            self.engine.DisplayY // 2,
            image=self.BackGround_img,
            tag="BackGround_img",
        )

        # 矢印UI_UP
        Image_UP_Yajirushi = Image.open(
            os.path.join(os.path.dirname(__file__), "Main_UI", "UP_Yajirushi.png")
        )
        Image_UP_Yajirushi = Image_UP_Yajirushi.resize((100, 25))
        self.Image_UP_Yajirushi = ImageTk.PhotoImage(Image_UP_Yajirushi)

        # 矢印UI_Down
        Image_Down_Yajirushi = Image.open(
            os.path.join(os.path.dirname(__file__), "Main_UI", "DOWN_Yajirushi.png")
        )
        Image_Down_Yajirushi = Image_Down_Yajirushi.resize((100, 25))
        self.Image_Down_Yajirushi = ImageTk.PhotoImage(Image_Down_Yajirushi)

        # タイトルバックボタン
        Image_TitleBack = Image.open(
            os.path.join(os.path.dirname(__file__), "Main_UI", "Return_To_Title.png")
        )
        Image_TitleBack = Image_TitleBack.resize((400, 88))
        self.Image_TitleBack = ImageTk.PhotoImage(Image_TitleBack)

        # タイトルバックボタン設定------------------------------------
        self.Return_Title_button = tk.Button(
            self.canvas,
            image=self.Image_TitleBack,
            bg="white",
            activebackground="#CCCCCC",
            command=self.Return_to_title,  # クリック時の処理
            borderwidth=0,  # 枠線を消す（0にすると完全に画像だけになります）
            highlightthickness=0,  # 選択時の枠線も消す
        )
        self.Return_Title_Button_window = self.canvas.create_window(
            self.engine.DisplayX // 2 - 430,
            self.engine.DisplayY // 2 - 270,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=400,  # ボタンの幅
            height=88,  # ボタンの高さ
            window=self.Return_Title_button,  # 埋め込むウィジェットを指定
            tags="Return_Title_Button",  # 四角形と同じようにタグを設定可能
        )

        # SUBMITボタン
        Image_SUBMIT = Image.open(
            os.path.join(os.path.dirname(__file__), "Main_UI", "SUBMIT.png")
        )
        Image_SUBMIT = Image_SUBMIT.resize((260, 50))
        self.Image_SUBMIT = ImageTk.PhotoImage(Image_SUBMIT)

        self.SubMit = tk.Button(
            self.canvas,
            image=self.Image_SUBMIT,
            bg="white",
            activebackground="#CCCCCC",
            command=self.Create_Result_Chacks,  # クリック時の処理  # クリック時の処理
            borderwidth=0,  # 枠線を消す（0にすると完全に画像だけになります）
            highlightthickness=0,  # 選択時の枠線も消す
        )
        self.SubMit_window = self.canvas.create_window(
            self.engine.DisplayX // 2 - 50,
            self.engine.DisplayY // 2 + 210,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=260,  # ボタンの幅
            height=50,  # ボタンの高さ
            window=self.SubMit,  # 埋め込むウィジェットを指定
            tags="SubMit",  # 四角形と同じようにタグを設定可能
        )

        # NumberUpボタン1
        self.UpNumber1 = tk.Button(
            self.canvas,
            image=self.Image_UP_Yajirushi,
            bg="white",
            activebackground="#CCCCCC",
            command=self.NumberBox_UP1,  # クリック時の処理
            borderwidth=0,  # 枠線を消す（0にすると完全に画像だけになります）
            highlightthickness=0,  # 選択時の枠線も消す
        )
        self.UpNumber1_window = self.canvas.create_window(
            self.engine.DisplayX // 2 - 385,
            self.engine.DisplayY // 2 - 70,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=100,  # ボタンの幅
            height=25,  # ボタンの高さ
            window=self.UpNumber1,  # 埋め込むウィジェットを指定
            tags="UpNumber1",  # 四角形と同じようにタグを設定可能
        )
        # NumberUpボタン2
        self.UpNumber2 = tk.Button(
            self.canvas,
            image=self.Image_UP_Yajirushi,
            bg="white",
            activebackground="#CCCCCC",
            command=self.NumberBox_UP2,  # クリック時の処理
            borderwidth=0,  # 枠線を消す（0にすると完全に画像だけになります）
            highlightthickness=0,  # 選択時の枠線も消す
        )
        self.UpNumber2_window = self.canvas.create_window(
            self.engine.DisplayX // 2 - 225,
            self.engine.DisplayY // 2 - 70,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=100,  # ボタンの幅
            height=25,  # ボタンの高さ
            window=self.UpNumber2,  # 埋め込むウィジェットを指定
            tags="UpNumber2",  # 四角形と同じようにタグを設定可能
        )
        # NumberUpボタン3
        self.UpNumber3 = tk.Button(
            self.canvas,
            image=self.Image_UP_Yajirushi,
            bg="white",
            activebackground="#CCCCCC",
            command=self.NumberBox_UP3,  # クリック時の処理
            borderwidth=0,  # 枠線を消す（0にすると完全に画像だけになります）
            highlightthickness=0,  # 選択時の枠線も消す
        )
        self.UpNumber3_window = self.canvas.create_window(
            self.engine.DisplayX // 2 - 70,
            self.engine.DisplayY // 2 - 70,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=100,  # ボタンの幅
            height=25,  # ボタンの高さ
            window=self.UpNumber3,  # 埋め込むウィジェットを指定
            tags="UpNumber3",  # 四角形と同じようにタグを設定可能
        )
        # NumberDownボタン1
        self.DownNumber1 = tk.Button(
            self.canvas,
            image=self.Image_Down_Yajirushi,
            bg="white",
            activebackground="#CCCCCC",
            command=self.NumberBox_Down1,  # クリック時の処理
            borderwidth=0,  # 枠線を消す（0にすると完全に画像だけになります）
            highlightthickness=0,
        )
        self.DownNumber1_window = self.canvas.create_window(
            self.engine.DisplayX // 2 - 385,
            self.engine.DisplayY // 2 + 135,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=100,  # ボタンの幅
            height=25,  # ボタンの高さ
            window=self.DownNumber1,  # 埋め込むウィジェットを指定
            tags="DownNumber1",  # 四角形と同じようにタグを設定可能
        )
        # NumberDownボタン2
        self.DownNumber2 = tk.Button(
            self.canvas,
            image=self.Image_Down_Yajirushi,
            bg="white",
            activebackground="#CCCCCC",
            command=self.NumberBox_Down2,  # クリック時の処理
            borderwidth=0,  # 枠線を消す（0にすると完全に画像だけになります）
            highlightthickness=0,
        )
        self.DownNumber2_window = self.canvas.create_window(
            self.engine.DisplayX // 2 - 225,
            self.engine.DisplayY // 2 + 135,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=100,  # ボタンの幅
            height=25,  # ボタンの高さ
            window=self.DownNumber2,  # 埋め込むウィジェットを指定
            tags="DownNumber2",  # 四角形と同じようにタグを設定可能
        )
        # NumberDownボタン3
        self.DownNumber3 = tk.Button(
            self.canvas,
            image=self.Image_Down_Yajirushi,
            bg="white",
            activebackground="#CCCCCC",
            command=self.NumberBox_Down3,  # クリック時の処理
            borderwidth=0,  # 枠線を消す（0にすると完全に画像だけになります）
            highlightthickness=0,
        )
        self.DownNumber3_window = self.canvas.create_window(
            self.engine.DisplayX // 2 - 70,
            self.engine.DisplayY // 2 + 135,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=100,  # ボタンの幅
            height=25,  # ボタンの高さ
            window=self.DownNumber3,  # 埋め込むウィジェットを指定
            tags="DownNumber3",  # 四角形と同じようにタグを設定可能
        )

        self.TimeText = self.canvas.create_text(
            self.engine.DisplayX // 2 + 10,
            self.engine.DisplayY // 2 - 230,
            text="0",
            fill="white",  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 40),  # フォントとサイズ
            anchor="center",  # 基準点
            tags="TimeText",  # タグをつけて管理可能
        )

        self.Number1_text = self.canvas.create_text(
            self.engine.DisplayX // 2 - 385,
            self.engine.DisplayY // 2 + 40,
            text="0",
            fill="black",  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 100),  # フォントとサイズ
            anchor="center",  # 基準点
            tags="Number1_text",  # タグをつけて管理可能
        )
        self.Number2_text = self.canvas.create_text(
            self.engine.DisplayX // 2 - 225,
            self.engine.DisplayY // 2 + 40,
            text="0",
            fill="black",  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 100),  # フォントとサイズ
            anchor="center",  # 基準点
            tags="Number2_text",  # タグをつけて管理可能
        )
        self.Number3_text = self.canvas.create_text(
            self.engine.DisplayX // 2 - 70,
            self.engine.DisplayY // 2 + 40,
            text="0",
            fill="black",  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 100),  # フォントとサイズ
            anchor="center",  # 基準点
            tags="Number3_text",  # タグをつけて管理可能
        )
        self.Result_text = self.canvas.create_text(
            self.engine.DisplayX // 2 + 360,
            self.engine.DisplayY // 2 - 10,
            text="",
            fill="white",  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 14),  # フォントとサイズ
            anchor="n",  # 基準点
            tags="Result_text",  # タグをつけて管理可能
        )
        self.Sound_BGM()

    def Sound_BGM(self):
        try:
            # BGMファイルをロード
            pygame.mixer.music.load(
                os.path.join(
                    os.path.dirname(__file__), "Main_BGM", "HitBrow_Games_Limit.mp3"
                )
            )
            pygame.mixer.music.play(1)
            print("BGM再生開始!")

        except pygame.error:
            print(
                "BGMファイル(HitBrow_Games_Limit.mp3)が見つかりません。無音で進行します。"
            )

    def Return_to_title(self):
        print("タイトルバックボタンが押されました。タイトル画面に戻ります")
        self.engine.change_scene(TitleScene(self.engine))

    def Go_to_Result(self):
        print("ゲームモード2が通常終了されました")
        self.engine.change_scene(GameScene2_Result(self.engine))

    def NumberBox_UP1(self):
        if self.flag_TimeUp:
            return

        Number_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.keyNumber_STR1 = Number_list[
            (Number_list.index(self.keyNumber_STR1) + 1) % 10
        ]
        self.canvas.itemconfig("Number1_text", text=self.keyNumber_STR1)

    def NumberBox_UP2(self):
        if self.flag_TimeUp:
            return
        Number_list = [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
        ]
        self.keyNumber_STR2 = Number_list[
            (Number_list.index(self.keyNumber_STR2) + 1) % 10
        ]
        self.canvas.itemconfig("Number2_text", text=self.keyNumber_STR2)

    def NumberBox_UP3(self):
        if self.flag_TimeUp:
            return
        Number_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.keyNumber_STR3 = Number_list[
            (Number_list.index(self.keyNumber_STR3) + 1) % 10
        ]
        self.canvas.itemconfig("Number3_text", text=self.keyNumber_STR3)

    def NumberBox_Down1(self):
        if self.flag_TimeUp:
            return
        Number_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.keyNumber_STR1 = Number_list[
            (Number_list.index(self.keyNumber_STR1) + 9) % 10
        ]
        self.canvas.itemconfig("Number1_text", text=self.keyNumber_STR1)

    def NumberBox_Down2(self):
        if self.flag_TimeUp:
            return
        Number_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.keyNumber_STR2 = Number_list[
            (Number_list.index(self.keyNumber_STR2) + 9) % 10
        ]
        self.canvas.itemconfig("Number2_text", text=self.keyNumber_STR2)

    def NumberBox_Down3(self):
        if self.flag_TimeUp:
            return
        Number_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.keyNumber_STR3 = Number_list[
            (Number_list.index(self.keyNumber_STR3) + 9) % 10
        ]
        self.canvas.itemconfig("Number3_text", text=self.keyNumber_STR3)

    def Timer(self, TimeUp_Time):
        delta_time = -(self.Start_time - time.time())

        if delta_time < TimeUp_Time:
            self.canvas.itemconfig(
                "TimeText", text=str(round(TimeUp_Time - delta_time))
            )
            self.engine.Time_score2 = TimeUp_Time - delta_time
        if delta_time >= TimeUp_Time:
            self.engine.Time_score2 = 0
            self.flag_TimeUp = True
            if delta_time > TimeUp_Time + 8:
                print("タイムアップ")
                self.engine.Try_score2 = 0
                self.Go_to_Result()

    def Create_Result_Chacks(self):
        if self.flag_TimeUp:
            return
        self.engine.Try_score2 += 1
        self.check_number = (
            self.keyNumber_STR1 + self.keyNumber_STR2 + self.keyNumber_STR3
        )
        hit, blow = judge(self.secret, self.check_number)
        result = {"user_number": self.check_number, "hit": hit, "blow": blow}
        self.result_list.append(result)

        if len(self.result_list) > 14:
            self.result_list.pop(0)

        log_lines = [
            f"あなたの選択した数字: {log['user_number']}, Hit: {log['hit']}, Blow: {log['blow']}"
            for log in self.result_list
        ]
        log_text = "\n".join(log_lines)
        self.canvas.itemconfig("Result_text", text=log_text)

        if hit == 3:
            self.Clear_flag = True
            self.engine.result_score2 = (
                self.engine.Time_score2 * 100 - self.engine.Try_score2 * 100
            )
            self.Go_to_Result()

    def update(self):
        self.Timer(120)
        # デバッグ用
        # self.engine.change_scene(GameScene2_Result(self.engine))

    def exit(self):
        self.canvas.delete("BackGround_img")
        self.canvas.delete("Return_Title_Button")
        self.canvas.delete("UpNumber1")
        self.canvas.delete("UpNumber2")
        self.canvas.delete("UpNumber3")
        self.canvas.delete("DownNumber1")
        self.canvas.delete("DownNumber2")
        self.canvas.delete("DownNumber3")
        self.canvas.delete("TimeText")
        self.canvas.delete("Number1_text")
        self.canvas.delete("Number2_text")
        self.canvas.delete("Number3_text")
        self.canvas.delete("SubMit")
        self.canvas.delete("Result_text")
        pygame.mixer.music.stop()


class GameScene2_Result(BaseScene):
    def enter(self):
        self.Rank_text = "D"
        self.Score_text = 0

        BackGround_img = Image.open(
            os.path.join(
                os.path.dirname(__file__), "Main_UI", "HitBrow_Mode1_Result.PNG"
            )
        )
        BackGround_img = BackGround_img.resize(
            (self.engine.DisplayX, self.engine.DisplayY)
        )
        self.BackGround_img = ImageTk.PhotoImage(BackGround_img)
        self.canvas.create_image(
            self.engine.DisplayX // 2,
            self.engine.DisplayY // 2,
            image=self.BackGround_img,
            tag="BackGround_img",
        )
        # タイトルバックボタン設定------------------------------------
        Image_TitleBack = Image.open(
            os.path.join(os.path.dirname(__file__), "Main_UI", "Return_To_Title.png")
        )
        Image_TitleBack = Image_TitleBack.resize((400, 88))
        self.Image_TitleBack = ImageTk.PhotoImage(Image_TitleBack)

        self.Return_Title_button = tk.Button(
            self.canvas,
            image=self.Image_TitleBack,
            bg="white",
            activebackground="#CCCCCC",
            command=self.Return_to_title,  # クリック時の処理
            borderwidth=0,  # 枠線を消す（0にすると完全に画像だけになります）
            highlightthickness=0,  # 選択時の枠線も消す
        )
        self.Return_Title_Button_window = self.canvas.create_window(
            self.engine.DisplayX // 2 + 400,
            self.engine.DisplayY // 2 + 300,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=400,  # ボタンの幅
            height=88,  # ボタンの高さ
            window=self.Return_Title_button,  # 埋め込むウィジェットを指定
            tags="Return_Title_Button",  # 四角形と同じようにタグを設定可能
        )
        # タイトルバックボタン設定(ここまで)-----------------------------------

        print(f"トータルスコア : {5000 + self.engine.result_score2}")
        print(f"タイムスコア : {self.engine.Time_score2}")
        print(f"トライスコア : -{self.engine.Try_score2}")

        if self.engine.Time_score2 <= 0:
            self.Sound_BGM_D_score()
        else:
            self.Sound_BGM_S_score()

        self.Result_text_comment = "Thank You For Playing!"
        if self.engine.result_score2 + 5000 >= 15000:
            self.Rank_text = "S"
            self.color = "yellow"
            self.Result_text_comment = (
                "一言コメント : \n天才！次は16進数モードに挑戦だ！"
            )
        elif self.engine.result_score2 + 5000 >= 13000:
            self.Rank_text = "A"
            self.color = "red"
            self.Result_text_comment = "一言コメント : \nSランクまであと一歩！"
        elif self.engine.result_score2 + 5000 >= 11000:
            self.Rank_text = "B"
            self.color = "blue"
            self.Result_text_comment = (
                "一言コメント : \n試行回数が増えると点数は減ります"
            )
        elif self.engine.result_score2 + 5000 >= 9000:
            self.Rank_text = "C"
            self.color = "orange"
            self.Result_text_comment = "一言コメント : \n早く正解すると点数が上がるよ！"
        elif self.engine.Time_score2 > 0:
            self.Rank_text = "D"
            self.color = "green"
            self.Result_text_comment = (
                "一言コメント : \n残念...。もう少し頑張りましょう！"
            )

        else:
            self.Rank_text = "D"
            self.color = "green"
            self.Result_text_comment = "一言コメント : \nもしかして放置した？"

        if self.engine.Try_score2 == 1:
            self.Result_text_comment = (
                "一言コメント : \n一発クリアの確率は約0.1%! 幸運!"
            )
        elif self.engine.Try_score2 == 2:
            self.Result_text_comment = "一言コメント : \n早くないですか？当てるの。"
        elif self.engine.Try_score2 == 3:
            self.Result_text_comment = (
                "一言コメント : \n期待値は5回らしいよ(gemini調べ)"
            )

        self.Rank_text = self.canvas.create_text(
            self.engine.DisplayX // 2 + 400,
            self.engine.DisplayY // 2 - 100,
            text=self.Rank_text,
            fill=self.color,  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 270),  # フォントとサイズ
            anchor="center",  # 基準点
            tags="Rank_text",  # タグをつけて管理可能
        )

        self.TimeScore_text = self.canvas.create_text(
            self.engine.DisplayX // 2 - 185,
            self.engine.DisplayY // 2 - 50,
            text=f"{round(self.engine.Time_score2, 2)}s",
            fill="black",  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 40),  # フォントとサイズ
            anchor="center",  # 基準点
            tags="TimeScore_text",  # タグをつけて管理可能
        )
        self.TryScore_text = self.canvas.create_text(
            self.engine.DisplayX // 2 - 430,
            self.engine.DisplayY // 2 - 160,
            text=f"{round(self.engine.Try_score2, 0)}回",
            fill="black",  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 50),  # フォントとサイズ
            anchor="center",  # 基準点
            tags="TryScore_text",  # タグをつけて管理可能
        )
        self.Score_text = self.canvas.create_text(
            self.engine.DisplayX // 2 + 130,
            self.engine.DisplayY // 2 + 10,
            text="",
            fill="black",  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 50),  # フォントとサイズ
            anchor="center",  # 基準点
            tags="Score_text",  # タグをつけて管理可能
        )
        self.Comment_text = self.canvas.create_text(
            self.engine.DisplayX // 2 - 300,
            self.engine.DisplayY // 2 + 230,
            text=self.Result_text_comment,
            fill="white",  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 25),  # フォントとサイズ
            anchor="center",  # 基準点
            tags="Comment_text",  # タグをつけて管理可能
        )

    def Return_to_title(self):
        print("タイトルバックボタンが押されました。タイトル画面に戻ります")
        self.engine.change_scene(TitleScene(self.engine))

    def Sound_BGM_S_score(self):
        try:
            # BGMファイルをロード
            pygame.mixer.music.load(
                os.path.join(os.path.dirname(__file__), "Main_BGM", "S_ranks_BGM.mp3")
            )
            pygame.mixer.music.play(-1)
            print("BGM再生開始!")

        except pygame.error:
            print("BGMファイル(S_ranks_BGM.mp3)が見つかりません。無音で進行します。")

    def Sound_BGM_D_score(self):
        try:
            # BGMファイルをロード
            pygame.mixer.music.load(
                os.path.join(os.path.dirname(__file__), "Main_BGM", "Oh_my_god.mp3")
            )
            pygame.mixer.music.play(-1)
            print("BGM再生開始!")

        except pygame.error:
            print("BGMファイル(Oh_my_god.mp3)が見つかりません。無音で進行します。")

    def update(self):
        if self.Score_text < round(self.engine.result_score2 + 5000, 2):
            self.Score_text = round(self.Score_text + 70, 0)
            self.canvas.itemconfig("Score_text", text=f"{self.Score_text}点")
        else:
            self.canvas.itemconfig(
                "Score_text", text=f"{round(self.engine.result_score2 + 5000, 0)}点"
            )

    def exit(self):
        self.canvas.delete("BackGround_img")
        self.canvas.delete("Return_Title_Button")
        self.canvas.delete("Rank_text")
        self.canvas.delete("TimeScore_text")
        self.canvas.delete("TryScore_text")
        self.canvas.delete("Score_text")
        self.canvas.delete("Comment_text")
        self.engine.result_score1 = 0
        self.engine.Time_score1 = 0
        self.engine.Try_score1 = 0
        pygame.mixer.music.stop()


class GameScene3(BaseScene):
    def enter(self):
        Answerlist = []
        Question, Answerlist, Answer = "リンゴの生産量日本1は？", ["青森","岩手","長野","福岡","北海道","山形","宮城","福島","新潟","山梨"], "123"

        
        Question, Answerlist, Answer = self.questions(random.randint(0, 9))
        print("ゲームシーン3を開始します")
        self.Start_time = time.time()
        self.secret = Answer
        Question_list_text = self.make_Question_List(Answerlist)
        self.result_list = []
        self.Clear_flag = False
        self.flag_TimeUp = False

        self.keyNumber_STR1 = "0"
        self.keyNumber_STR2 = "0"
        self.keyNumber_STR3 = "0"

        self.check_number = (
            self.keyNumber_STR1 + self.keyNumber_STR2 + self.keyNumber_STR3
        )

        BackGround_img = Image.open(
            os.path.join(os.path.dirname(__file__), "Main_UI", "GameMode3_mainUI.png")
        )
        BackGround_img = BackGround_img.resize(
            (self.engine.DisplayX, self.engine.DisplayY)
        )
        self.BackGround_img = ImageTk.PhotoImage(BackGround_img)
        self.canvas.create_image(
            self.engine.DisplayX // 2,
            self.engine.DisplayY // 2,
            image=self.BackGround_img,
            tag="BackGround_img",
        )

        Image_UP_Yajirushi = Image.open(
            os.path.join(os.path.dirname(__file__), "Main_UI", "UP_Yajirushi.png")
        )
        Image_UP_Yajirushi = Image_UP_Yajirushi.resize((100, 25))
        self.Image_UP_Yajirushi = ImageTk.PhotoImage(Image_UP_Yajirushi)

        # 矢印UI_Down
        Image_Down_Yajirushi = Image.open(
            os.path.join(os.path.dirname(__file__), "Main_UI", "DOWN_Yajirushi.png")
        )
        Image_Down_Yajirushi = Image_Down_Yajirushi.resize((100, 25))
        self.Image_Down_Yajirushi = ImageTk.PhotoImage(Image_Down_Yajirushi)

        # タイトルバックボタン
        Image_TitleBack = Image.open(
            os.path.join(os.path.dirname(__file__), "Main_UI", "Return_To_Title.png")
        )
        Image_TitleBack = Image_TitleBack.resize((200, 44))
        self.Image_TitleBack = ImageTk.PhotoImage(Image_TitleBack)

        # タイトルバックボタン設定------------------------------------
        self.Return_Title_button = tk.Button(
            self.canvas,
            image=self.Image_TitleBack,
            bg="white",
            activebackground="#CCCCCC",
            command=self.Return_to_title,  # クリック時の処理
            borderwidth=0,  # 枠線を消す（0にすると完全に画像だけになります）
            highlightthickness=0,  # 選択時の枠線も消す
        )
        self.Return_Title_Button_window = self.canvas.create_window(
            self.engine.DisplayX // 2 + 500,
            self.engine.DisplayY // 2 - 50,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=200,  # ボタンの幅
            height=44,  # ボタンの高さ
            window=self.Return_Title_button,  # 埋め込むウィジェットを指定
            tags="Return_Title_Button",  # 四角形と同じようにタグを設定可能
        )

        # SUBMITボタン
        Image_SUBMIT = Image.open(
            os.path.join(os.path.dirname(__file__), "Main_UI", "SUBMIT.png")
        )
        Image_SUBMIT = Image_SUBMIT.resize((260, 50))
        self.Image_SUBMIT = ImageTk.PhotoImage(Image_SUBMIT)

        self.SubMit = tk.Button(
            self.canvas,
            image=self.Image_SUBMIT,
            bg="white",
            activebackground="#CCCCCC",
            command=self.Create_Result_Chacks,  # クリック時の処理  # クリック時の処理
            borderwidth=0,  # 枠線を消す（0にすると完全に画像だけになります）
            highlightthickness=0,  # 選択時の枠線も消す
        )
        self.SubMit_window = self.canvas.create_window(
            self.engine.DisplayX // 2 + 20,
            self.engine.DisplayY // 2 + 330,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=260,  # ボタンの幅
            height=50,  # ボタンの高さ
            window=self.SubMit,  # 埋め込むウィジェットを指定
            tags="SubMit",  # 四角形と同じようにタグを設定可能
        )

        # NumberUpボタン1
        self.UpNumber1 = tk.Button(
            self.canvas,
            image=self.Image_UP_Yajirushi,
            bg="white",
            activebackground="#CCCCCC",
            command=self.NumberBox_UP1,  # クリック時の処理
            borderwidth=0,  # 枠線を消す（0にすると完全に画像だけになります）
            highlightthickness=0,  # 選択時の枠線も消す
        )
        self.UpNumber1_window = self.canvas.create_window(
            self.engine.DisplayX // 2 - 450,
            self.engine.DisplayY // 2 + 70 ,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=100,  # ボタンの幅
            height=25,  # ボタンの高さ
            window=self.UpNumber1,  # 埋め込むウィジェットを指定
            tags="UpNumber1",  # 四角形と同じようにタグを設定可能
        )
        # NumberUpボタン2
        self.UpNumber2 = tk.Button(
            self.canvas,
            image=self.Image_UP_Yajirushi,
            bg="white",
            activebackground="#CCCCCC",
            command=self.NumberBox_UP2,  # クリック時の処理
            borderwidth=0,  # 枠線を消す（0にすると完全に画像だけになります）
            highlightthickness=0,  # 選択時の枠線も消す
        )
        self.UpNumber2_window = self.canvas.create_window(
            self.engine.DisplayX // 2 - 285,
            self.engine.DisplayY // 2 + 70,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=100,  # ボタンの幅
            height=25,  # ボタンの高さ
            window=self.UpNumber2,  # 埋め込むウィジェットを指定
            tags="UpNumber2",  # 四角形と同じようにタグを設定可能
        )
        # NumberUpボタン3
        self.UpNumber3 = tk.Button(
            self.canvas,
            image=self.Image_UP_Yajirushi,
            bg="white",
            activebackground="#CCCCCC",
            command=self.NumberBox_UP3,  # クリック時の処理
            borderwidth=0,  # 枠線を消す（0にすると完全に画像だけになります）
            highlightthickness=0,  # 選択時の枠線も消す
        )
        self.UpNumber3_window = self.canvas.create_window(
            self.engine.DisplayX // 2 - 130,
            self.engine.DisplayY // 2 + 70,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=100,  # ボタンの幅
            height=25,  # ボタンの高さ
            window=self.UpNumber3,  # 埋め込むウィジェットを指定
            tags="UpNumber3",  # 四角形と同じようにタグを設定可能
        )
        # NumberDownボタン1
        self.DownNumber1 = tk.Button(
            self.canvas,
            image=self.Image_Down_Yajirushi,
            bg="white",
            activebackground="#CCCCCC",
            command=self.NumberBox_Down1,  # クリック時の処理
            borderwidth=0,  # 枠線を消す（0にすると完全に画像だけになります）
            highlightthickness=0,
        )
        self.DownNumber1_window = self.canvas.create_window(
            self.engine.DisplayX // 2 - 450,
            self.engine.DisplayY // 2 + 280,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=100,  # ボタンの幅
            height=25,  # ボタンの高さ
            window=self.DownNumber1,  # 埋め込むウィジェットを指定
            tags="DownNumber1",  # 四角形と同じようにタグを設定可能
        )
        # NumberDownボタン2
        self.DownNumber2 = tk.Button(
            self.canvas,
            image=self.Image_Down_Yajirushi,
            bg="white",
            activebackground="#CCCCCC",
            command=self.NumberBox_Down2,  # クリック時の処理
            borderwidth=0,  # 枠線を消す（0にすると完全に画像だけになります）
            highlightthickness=0,
        )
        self.DownNumber2_window = self.canvas.create_window(
            self.engine.DisplayX // 2 - 285,
            self.engine.DisplayY // 2 + 280,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=100,  # ボタンの幅
            height=25,  # ボタンの高さ
            window=self.DownNumber2,  # 埋め込むウィジェットを指定
            tags="DownNumber2",  # 四角形と同じようにタグを設定可能
        )
        # NumberDownボタン3
        self.DownNumber3 = tk.Button(
            self.canvas,
            image=self.Image_Down_Yajirushi,
            bg="white",
            activebackground="#CCCCCC",
            command=self.NumberBox_Down3,  # クリック時の処理
            borderwidth=0,  # 枠線を消す（0にすると完全に画像だけになります）
            highlightthickness=0,
        )
        self.DownNumber3_window = self.canvas.create_window(
            self.engine.DisplayX // 2 - 130,
            self.engine.DisplayY // 2 + 280,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=100,  # ボタンの幅
            height=25,  # ボタンの高さ
            window=self.DownNumber3,  # 埋め込むウィジェットを指定
            tags="DownNumber3",  # 四角形と同じようにタグを設定可能
        )

        self.TimeText = self.canvas.create_text(
            self.engine.DisplayX // 2 + 515,
            self.engine.DisplayY // 2 - 180,
            text="0",
            fill="white",  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 40),  # フォントとサイズ
            anchor="center",  # 基準点
            tags="TimeText",  # タグをつけて管理可能
        )

        self.Number1_text = self.canvas.create_text(
            self.engine.DisplayX // 2 - 450,
            self.engine.DisplayY // 2 + 180,
            text="0",
            fill="black",  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 100),  # フォントとサイズ
            anchor="center",  # 基準点
            tags="Number1_text",  # タグをつけて管理可能
        )
        self.Number2_text = self.canvas.create_text(
            self.engine.DisplayX // 2 - 285,
            self.engine.DisplayY // 2 + 180,
            text="0",
            fill="black",  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 100),  # フォントとサイズ
            anchor="center",  # 基準点
            tags="Number2_text",  # タグをつけて管理可能
        )
        self.Number3_text = self.canvas.create_text(
            self.engine.DisplayX // 2 - 130,
            self.engine.DisplayY // 2 + 180,
            text="0",
            fill="black",  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 100),  # フォントとサイズ
            anchor="center",  # 基準点
            tags="Number3_text",  # タグをつけて管理可能
        )
        self.Result_text = self.canvas.create_text(
            self.engine.DisplayX // 2 + 380,
            self.engine.DisplayY // 2 + 70,
            text="",
            fill="white",  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 14),  # フォントとサイズ
            anchor="n",  # 基準点
            tags="Result_text",  # タグをつけて管理可能
        )

        self.Question_text = self.canvas.create_text(
            self.engine.DisplayX // 2 - 150,
            self.engine.DisplayY // 2 - 280,
            text=Question,
            fill="white",  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 14),  # フォントとサイズ
            anchor="n",  # 基準点
            tags="Question_text",  # タグをつけて管理可能
        )
        self.Question_List_text = self.canvas.create_text(
            self.engine.DisplayX // 2 - 150,
            self.engine.DisplayY // 2 - 100,
            text=Question_list_text,
            fill="white",  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 14),  # フォントとサイズ
            anchor="n",  # 基準点
            tags="Question_list_text",  # タグをつけて管理可能
        )
        
        self.Sound_BGM()

    def questions(self, n: int):
    # 初期化
        Question = ""
        Answerlist = []
        Answer = ""  # 「0」から始まる答えに対応できるよう、文字列で定義するのがおすすめです

        if n == 0:
            Question = "大学生5000人が選んだ「おすすめのアルバイト」ランキングトップ3を、1位から順番に答えてください。"
            Answerlist = [
                "0: 塾講師", "1: 居酒屋", "2: イベントスタッフ", "3: カフェ", "4: コンビニ",
                "5: アパレル", "6: スーパー", "7: 家庭教師", "8: コールセンター", "9: カラオケ"
            ]
            # 1位: カフェ(3)、 2位: 塾講師(0)、 3位: アパレル(5)
            Answer = "305"
        
        elif n == 1:
            Question = "日本の「リンゴの生産量」上位3県を、1位から順番に答えてください。"
            Answerlist = [
                "0: 秋田県", "1: 山形県", "2: 岩手県", "3: 北海道", "4: 青森県",
                "5: 福島県", "6: 群馬県", "7: 宮城県", "8: 長野県", "9: 茨城県"
            ]
            # 1位: 青森県(4)、 2位: 長野県(8)、 3位: 岩手県(2)
            Answer = "482"

        elif n == 2:
            Question = "FIFA男子サッカー世界ランキングの上位3か国を、1位から順番に答えてください。2026/7/23現在"
            Answerlist = [
                "0: フランス", "1: ブラジル", "2: イングランド", "3: イタリア", "4: モロッコ",
                "5: スペイン", "6: アルゼンチン", "7: オランダ", "8: ポルトガル", "9: ベルギー"
            ]
            # 1位: スペイン(5)、 2位: アルゼンチン(6)、 3位: フランス(0)
            Answer = "560"
            
        elif n == 3:
            Question = "「2026年、小中学生女子が将来就きたい職業」トップ3を、1位から順番に答えてください。"
            Answerlist = [
                "0: YouTuber・動画投稿者", "1: イラストレーター", "2: パティシエ（お菓子職人）", "3: 医者", "4: 警察官",
                "5: 保育士", "6: 看護師", "7: 先生（教員）", "8: 芸能人", "9: 美容師"
            ]
            # 1位: パティシエ(2)、 2位: 先生(7)、 3位: 看護師(6)
            Answer = "276"

        elif n == 4:
            Question = "2025年の「M-1グランプリ」最終順位トップ3のコンビを、1位から順番に答えてください。"
            Answerlist = [
                "0: ヤーレンズ", "1: めぞん", "2: カナメストーン", "3: エバース", "4: 真空ジェシカ",
                "5: ヨネダ2000", "6: たくろう", "7: ドンデコルテ", "8: 豪快キャプテン", "9: ママタルト"
            ]
            # 1位: たくろう(6)、 2位: ドンデコルテ(7)、 3位: エバース(3)
            Answer = "673"
        
        elif n == 5:
            Question = "2025年の「Billboard JAPAN」年間総合ソング・チャートトップ3の楽曲を、\n1位から順番に答えてください。"
            Answerlist = [
                "0: 怪獣（サカナクション）", "1: APT.（ロゼ＆ブルーノ・マーズ）", "2: IRIS OUT（米津玄師）", "3: クスシキ（Mrs. GREEN APPLE）", "4: ライラック（Mrs. GREEN APPLE）",
                "5: ROSE（HANA）", "6: ダーリン（Mrs. GREEN APPLE）", "7: Bling-Bang-Bang-Born（Creepy Nuts）", "8: オトノケ（Creepy Nuts）", "9: ビターバカンス（Mrs. GREEN APPLE）"
            ]
            # 1位: ライラック(4)、 2位: ダーリン(6)、 3位: APT.(1)
            Answer = "461"

        elif n == 6:
            Question = "世界の「消費税（付加価値税）の標準税率が高い国」上位3か国を、\n1位から順番に答えてください。（2025年時点）"
            Answerlist = [
                "0: スウェーデン", "1: フィンランド", "2: 日本", "3: デンマーク", "4: イギリス",
                "5: イタリア", "6: ドイツ", "7: ハンガリー", "8: ノルウェー", "9: フランス"
            ]
            # 1位: ハンガリー(27%)[7]、 2位: フィンランド(25.5%)[1]、 3位: デンマーク(25%)[3] ※同率3位の国もありますが代表としてデンマークを設定
            Answer = "713"

        elif n == 7:
            Question = "対米ドルで見た「世界で最も価値の低い通貨」を発行している国ワースト3を、\n価値が低い順（1位が一番価値が低い）に答えてください。"
            Answerlist = [
                "0: インドネシア", "1: ベトナム", "2: コロンビア", "3: ウズベキスタン", "4: レバノン",
                "5: イラン", "6: パラグアイ", "7: ラオス", "8: ギニア", "9: アルゼンチン"
            ]
            # 1位: イラン(5)、 2位: レバノン(4)、 3位: ベトナム(1)
            Answer = "541"

        elif n == 8:
            Question = "世界の「スポーツ競技人口」が多い競技トップ3を、1位から順番に答えてください。"
            Answerlist = [
                "0: サッカー", "1: 野球", "2: テニス", "3: バレーボール", "4: バスケットボール",
                "5: 卓球", "6: クリケット", "7: ゴルフ", "8: ラグビー", "9: バドミントン"
            ]
            # 1位: バレーボール(3)、 2位: バスケットボール(4)、 3位: 卓球(5)
            Answer = "345"

        elif n == 9:
            Question = "小中学生の「好きな給食のメニュー」トップ3を、1位から順番に答えてください。"
            Answerlist = [
                "0: 冷凍みかん", "1: フルーツポンチ", "2: わかめごはん", "3: ソフト麺", "4: カレーライス",
                "5: ラーメン", "6: からあげ", "7: あげパン", "8: ミルメーク", "9: ケーキ・タルト"
            ]
            # 1位: あげパン(7)、 2位: カレーライス(4)、 3位: フルーツポンチ(1)
            Answer = "741"

        else:
            Question = "エラー: 該当する問題がありません"
            Answerlist = []
            Answer = "000"

        return Question, Answerlist, Answer

    def Sound_BGM(self):
        try:
            # BGMファイルをロード
            pygame.mixer.music.load(
                os.path.join(
                    os.path.dirname(__file__), "Main_BGM", "HitBrow_Games_Limit.mp3"
                )
            )
            pygame.mixer.music.play(1)
            print("BGM再生開始!")

        except pygame.error:
            print(
                "BGMファイル(HitBrow_Games_Limit.mp3)が見つかりません。無音で進行します。"
            )

    def make_Question_List(self, Question_list):
        text = ""
        for i in range(len(Question_list)):
            if i < 4:
                text += f"{Question_list[i]},"
            elif i == 4:
                text += f"{Question_list[i]}, \n"
            else:
                text += f"{Question_list[i]}, "
        return text

    def Return_to_title(self):
        print("タイトルバックボタンが押されました。タイトル画面に戻ります")
        self.engine.change_scene(TitleScene(self.engine))

    def Go_to_Result(self):
        print("ゲームモード3が通常終了されました")
        self.engine.change_scene(GameScene3_Result(self.engine))

    def NumberBox_UP1(self):
        if self.flag_TimeUp:
            return

        Number_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.keyNumber_STR1 = Number_list[
            (Number_list.index(self.keyNumber_STR1) + 1) % 10
        ]
        self.canvas.itemconfig("Number1_text", text=self.keyNumber_STR1)

    def NumberBox_UP2(self):
        if self.flag_TimeUp:
            return
        Number_list = [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
        ]
        self.keyNumber_STR2 = Number_list[
            (Number_list.index(self.keyNumber_STR2) + 1) % 10
        ]
        self.canvas.itemconfig("Number2_text", text=self.keyNumber_STR2)

    def NumberBox_UP3(self):
        if self.flag_TimeUp:
            return
        Number_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.keyNumber_STR3 = Number_list[
            (Number_list.index(self.keyNumber_STR3) + 1) % 10
        ]
        self.canvas.itemconfig("Number3_text", text=self.keyNumber_STR3)

    def NumberBox_Down1(self):
        if self.flag_TimeUp:
            return
        Number_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.keyNumber_STR1 = Number_list[
            (Number_list.index(self.keyNumber_STR1) + 9) % 10
        ]
        self.canvas.itemconfig("Number1_text", text=self.keyNumber_STR1)

    def NumberBox_Down2(self):
        if self.flag_TimeUp:
            return
        Number_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.keyNumber_STR2 = Number_list[
            (Number_list.index(self.keyNumber_STR2) + 9) % 10
        ]
        self.canvas.itemconfig("Number2_text", text=self.keyNumber_STR2)

    def NumberBox_Down3(self):
        if self.flag_TimeUp:
            return
        Number_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.keyNumber_STR3 = Number_list[
            (Number_list.index(self.keyNumber_STR3) + 9) % 10
        ]
        self.canvas.itemconfig("Number3_text", text=self.keyNumber_STR3)

    def Timer(self, TimeUp_Time):
        delta_time = -(self.Start_time - time.time())

        if delta_time < TimeUp_Time:
            self.canvas.itemconfig(
                "TimeText", text=str(round(TimeUp_Time - delta_time))
            )
            self.engine.Time_score3 = TimeUp_Time - delta_time
        if delta_time >= TimeUp_Time:
            self.engine.Time_score3 = 0
            self.flag_TimeUp = True
            if delta_time > TimeUp_Time + 8:
                print("タイムアップ")
                self.engine.Try_score3 = 0
                self.Go_to_Result()

    def Create_Result_Chacks(self):
        if self.flag_TimeUp:
            return
        self.engine.Try_score3 += 1
        self.check_number = (
            self.keyNumber_STR1 + self.keyNumber_STR2 + self.keyNumber_STR3
        )
        hit, blow = judge(self.secret, self.check_number)
        result = {"user_number": self.check_number, "hit": hit, "blow": blow}
        self.result_list.append(result)

        if len(self.result_list) > 11:
            self.result_list.pop(0)

        log_lines = [
            f"あなたの選択した数字: {log['user_number']}, Hit: {log['hit']}, Blow: {log['blow']}"
            for log in self.result_list
        ]
        log_text = "\n".join(log_lines)
        self.canvas.itemconfig("Result_text", text=log_text)

        if hit == 3:
            self.Clear_flag = True
            self.engine.result_score3 = (
                self.engine.Time_score3 * 100 - self.engine.Try_score3 * 100
            )
            self.Go_to_Result()

    def update(self):
        self.Timer(120)
        # デバッグ用
        # self.engine.change_scene(GameScene2_Result(self.engine))

    def exit(self):
        self.canvas.delete("BackGround_img")
        self.canvas.delete("Return_Title_Button")
        self.canvas.delete("UpNumber1")
        self.canvas.delete("UpNumber2")
        self.canvas.delete("UpNumber3")
        self.canvas.delete("DownNumber1")
        self.canvas.delete("DownNumber2")
        self.canvas.delete("DownNumber3")
        self.canvas.delete("TimeText")
        self.canvas.delete("Number1_text")
        self.canvas.delete("Number2_text")
        self.canvas.delete("Number3_text")
        self.canvas.delete("SubMit")
        self.canvas.delete("Result_text")
        self.canvas.delete("Question_list_text")
        pygame.mixer.music.stop()


class GameScene3_Result(BaseScene):
    def enter(self):
        self.Rank_text = "D"
        self.Score_text = 0

        BackGround_img = Image.open(
            os.path.join(
                os.path.dirname(__file__), "Main_UI", "HitBrow_Mode1_Result.PNG"
            )
        )
        BackGround_img = BackGround_img.resize(
            (self.engine.DisplayX, self.engine.DisplayY)
        )
        self.BackGround_img = ImageTk.PhotoImage(BackGround_img)
        self.canvas.create_image(
            self.engine.DisplayX // 2,
            self.engine.DisplayY // 2,
            image=self.BackGround_img,
            tag="BackGround_img",
        )
        # タイトルバックボタン設定------------------------------------
        Image_TitleBack = Image.open(
            os.path.join(os.path.dirname(__file__), "Main_UI", "Return_To_Title.png")
        )
        Image_TitleBack = Image_TitleBack.resize((400, 88))
        self.Image_TitleBack = ImageTk.PhotoImage(Image_TitleBack)

        self.Return_Title_button = tk.Button(
            self.canvas,
            image=self.Image_TitleBack,
            bg="white",
            activebackground="#CCCCCC",
            command=self.Return_to_title,  # クリック時の処理
            borderwidth=0,  # 枠線を消す（0にすると完全に画像だけになります）
            highlightthickness=0,  # 選択時の枠線も消す
        )
        self.Return_Title_Button_window = self.canvas.create_window(
            self.engine.DisplayX // 2 + 400,
            self.engine.DisplayY // 2 + 300,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=400,  # ボタンの幅
            height=88,  # ボタンの高さ
            window=self.Return_Title_button,  # 埋め込むウィジェットを指定
            tags="Return_Title_Button",  # 四角形と同じようにタグを設定可能
        )
        # タイトルバックボタン設定(ここまで)-----------------------------------

        print(f"トータルスコア : {5000 + self.engine.result_score3}")
        print(f"タイムスコア : {self.engine.Time_score3}")
        print(f"トライスコア : -{self.engine.Try_score3}")

        if self.engine.Time_score3 <= 0:
            self.Sound_BGM_D_score()
        else:
            self.Sound_BGM_S_score()

        self.Result_text_comment = "Thank You For Playing!"
        if self.engine.result_score3 + 5000 >= 15000:
            self.Rank_text = "S"
            self.color = "yellow"
            self.Result_text_comment = (
                "一言コメント : \n博識ですね！さすが！"
            )
        elif self.engine.result_score3 + 5000 >= 13000:
            self.Rank_text = "A"
            self.color = "red"
            self.Result_text_comment = "一言コメント : \nSランクまであと一歩！"
        elif self.engine.result_score3 + 5000 >= 11000:
            self.Rank_text = "B"
            self.color = "blue"
            self.Result_text_comment = (
                "一言コメント : \n試行回数が増えると点数は減ります"
            )
        elif self.engine.result_score3 + 5000 >= 9000:
            self.Rank_text = "C"
            self.color = "orange"
            self.Result_text_comment = "一言コメント : \n早く正解すると点数が上がるよ！"
        elif self.engine.Time_score3 > 0:
            self.Rank_text = "D"
            self.color = "green"
            self.Result_text_comment = (
                "一言コメント : \n残念...。もう少し頑張りましょう！"
            )

        else:
            self.Rank_text = "D"
            self.color = "green"
            self.Result_text_comment = "一言コメント : \nもしかして放置した？"

        if self.engine.Try_score3 == 1:
            self.Result_text_comment = (
                "一言コメント : \n確率なのか知識なのか？"
            )
        elif self.engine.Try_score3 == 2:
            self.Result_text_comment = "一言コメント : \n早かったね"
        elif self.engine.Try_score3 == 3:
            self.Result_text_comment = (
                "一言コメント : \n問題が簡単だった？"
            )

        self.Rank_text = self.canvas.create_text(
            self.engine.DisplayX // 2 + 400,
            self.engine.DisplayY // 2 - 100,
            text=self.Rank_text,
            fill=self.color,  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 270),  # フォントとサイズ
            anchor="center",  # 基準点
            tags="Rank_text",  # タグをつけて管理可能
        )

        self.TimeScore_text = self.canvas.create_text(
            self.engine.DisplayX // 2 - 185,
            self.engine.DisplayY // 2 - 50,
            text=f"{round(self.engine.Time_score3, 2)}s",
            fill="black",  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 40),  # フォントとサイズ
            anchor="center",  # 基準点
            tags="TimeScore_text",  # タグをつけて管理可能
        )
        self.TryScore_text = self.canvas.create_text(
            self.engine.DisplayX // 2 - 430,
            self.engine.DisplayY // 2 - 160,
            text=f"{round(self.engine.Try_score3, 0)}回",
            fill="black",  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 50),  # フォントとサイズ
            anchor="center",  # 基準点
            tags="TryScore_text",  # タグをつけて管理可能
        )
        self.Score_text = self.canvas.create_text(
            self.engine.DisplayX // 2 + 130,
            self.engine.DisplayY // 2 + 10,
            text="",
            fill="black",  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 50),  # フォントとサイズ
            anchor="center",  # 基準点
            tags="Score_text",  # タグをつけて管理可能
        )
        self.Comment_text = self.canvas.create_text(
            self.engine.DisplayX // 2 - 300,
            self.engine.DisplayY // 2 + 230,
            text=self.Result_text_comment,
            fill="white",  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 25),  # フォントとサイズ
            anchor="center",  # 基準点
            tags="Comment_text",  # タグをつけて管理可能
        )

    def Return_to_title(self):
        print("タイトルバックボタンが押されました。タイトル画面に戻ります")
        self.engine.change_scene(TitleScene(self.engine))

    def Sound_BGM_S_score(self):
        try:
            # BGMファイルをロード
            pygame.mixer.music.load(
                os.path.join(os.path.dirname(__file__), "Main_BGM", "S_ranks_BGM.mp3")
            )
            pygame.mixer.music.play(-1)
            print("BGM再生開始!")

        except pygame.error:
            print("BGMファイル(S_ranks_BGM.mp3)が見つかりません。無音で進行します。")

    def Sound_BGM_D_score(self):
        try:
            # BGMファイルをロード
            pygame.mixer.music.load(
                os.path.join(os.path.dirname(__file__), "Main_BGM", "Oh_my_god.mp3")
            )
            pygame.mixer.music.play(-1)
            print("BGM再生開始!")

        except pygame.error:
            print("BGMファイル(Oh_my_god.mp3)が見つかりません。無音で進行します。")

    def update(self):
        if self.Score_text < round(self.engine.result_score3 + 5000, 2):
            self.Score_text = round(self.Score_text + 70, 0)
            self.canvas.itemconfig("Score_text", text=f"{self.Score_text}点")
        else:
            self.canvas.itemconfig(
                "Score_text", text=f"{round(self.engine.result_score3 + 5000, 0)}点"
            )

    def exit(self):
        self.canvas.delete("BackGround_img")
        self.canvas.delete("Return_Title_Button")
        self.canvas.delete("Rank_text")
        self.canvas.delete("TimeScore_text")
        self.canvas.delete("TryScore_text")
        self.canvas.delete("Score_text")
        self.canvas.delete("Comment_text")
        self.engine.result_score3 = 0
        self.engine.Time_score3 = 0
        self.engine.Try_score3 = 0
        pygame.mixer.music.stop()



# --- ゲームエンジン（マネージャー） ---
class GameEngine:
    def __init__(self, root):
        # ... (初期化処理) ...
        self.root = root
        self.root.title("Hit and Brow")
        self.root.geometry("1280x720")
        self.DisplayX, self.DisplayY = 1280, 720

        self.result_score1 = 0
        self.Time_score1 = 0
        self.Try_score1 = 0

        self.result_score2 = 0
        self.Time_score2 = 0
        self.Try_score2 = 0

        self.result_score3 = 0
        self.Time_score3 = 0
        self.Try_score3 = 0

        self.root.bind("<Escape>", self.Exit_Scean)

        pygame.mixer.init()

        self.canvas = tk.Canvas(
            self.root, width=self.DisplayX, height=self.DisplayY, bg="white"
        )
        self.canvas.pack()
        self.now_scene = None
        self.next_scene = None

        # タイトルシーンを「予約」する
        self.change_scene(TitleScene(self))
        self.game_loop()

    def change_scene(self, next_scene):
        """すぐに切り替えず、予約だけしておく"""
        self.next_scene = next_scene

    def game_loop(self):
        # 1. ループの「一番最初」に、予約されたシーンがあるかチェックして安全に切り替える
        if self.next_scene is not None:
            if self.now_scene is not None:
                self.now_scene.exit()  # 古いシーンのお掃除

            self.now_scene = self.next_scene
            self.now_scene.enter()  # 新しいシーンの準備
            self.next_scene = None  # 予約を空に戻す

        # 2. その後、現在のシーンの update を呼ぶ（これで絶対に衝突しない！）
        if self.now_scene is not None:
            self.now_scene.update()

        self.root.after(16, self.game_loop)

    def Exit_Scean(self, event):
        print("ゲームを終了します。Thank you for playing!")
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = GameEngine(root)
    root.mainloop()


def main():
    root = tk.Tk()
    app = GameEngine(root)
    root.mainloop()
