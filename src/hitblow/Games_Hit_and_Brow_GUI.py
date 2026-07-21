import tkinter as tk
from PIL import Image, ImageTk
import pygame
import os
import time
from .core import judge, make_secret16


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

        # バックグラウンドイメージの設定とボタンの初期設定
        try:
            img = Image.open(
                os.path.join(os.path.dirname(__file__), "Main_UI", "HitBrow_mainUI.jpg")
            )
            img = img.resize((self.engine.DisplayX, self.engine.DisplayY))
            self.title_photo = ImageTk.PhotoImage(img)
            self.canvas.create_image(
                self.engine.DisplayX // 2,
                self.engine.DisplayY // 2,
                image=self.title_photo,
                tag="title_screen",
            )

            self.to_mode1_button = tk.Button(
                self.canvas,
                text="モード１へ",
                bg="green",
                fg="white",  # 文字を白くして見やすくする
                font=("Arial", 30),  # ここでフォントサイズを調整
                command=self.Go_to_mode1,  # クリック時の処理
            )
            self.to_mode1_button.pack()

            self.to_mode2_button = tk.Button(
                self.canvas,
                text="モード2へ",
                bg="red",
                fg="white",  # 文字を白くして見やすくする
                font=("Arial", 30),  # ここでフォントサイズを調整
                command=self.Go_to_mode2,  # クリック時の処理
            )
            self.to_mode2_button.pack()

            self.to_mode3_button = tk.Button(
                self.canvas,
                text="モード３へ",
                bg="blue",
                fg="white",  # 文字を白くして見やすくする
                font=("Arial", 30),  # ここでフォントサイズを調整
                command=self.Go_to_mode3,  # クリック時の処理
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
                self.engine.DisplayY // 2 - 100,
                anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
                width=300,  # ボタンの幅
                height=70,  # ボタンの高さ
                window=self.to_mode1_button,  # 埋め込むウィジェットを指定
                tags="Mode1_Button",  # 四角形と同じようにタグを設定可能
            )
            self.to_mode2_button_window = self.canvas.create_window(
                self.engine.DisplayX // 2 + 400,
                self.engine.DisplayY // 2,
                anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
                width=300,  # ボタンの幅
                height=70,  # ボタンの高さ
                window=self.to_mode2_button,  # 埋め込むウィジェットを指定
                tags="Mode2_Button",  # 四角形と同じようにタグを設定可能
            )
            self.to_mode3_button_window = self.canvas.create_window(
                self.engine.DisplayX // 2 + 400,
                self.engine.DisplayY // 2 + 100,
                anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
                width=300,  # ボタンの幅
                height=70,  # ボタンの高さ
                window=self.to_mode3_button,  # 埋め込むウィジェットを指定
                tags="Mode3_Button",  # 四角形と同じようにタグを設定可能
            )

        except FileNotFoundError:
            print("ボタンの配置ができませんでした")

        self.Sound_BGM()

    def Go_to_mode1(self):
        print("モード1を開始します")
        self.engine.change_scene(GameScene1(self.engine))

    def Go_to_mode2(self):
        print("モード2を開始します")
        self.engine.change_scene(GameScene2(self.engine))

    def Go_to_mode3(self):
        print("モード3を開始します")
        self.engine.change_scene(GameScene3(self.engine))

    def Sound_BGM(self):
        try:
            # BGMファイルをロード
            pygame.mixer.music.load(
                os.path.join(os.path.dirname(__file__), "Main_BGM", "hatena.mp3")
            )
            pygame.mixer.music.play(-1)
            print("BGM再生開始!")

        except pygame.error:
            print("BGMファイル(hatena.mp3)が見つかりません。無音で進行します。")

    def exit(self):
        # 次の画面に行く前に、自分の出した画像とキー設定を綺麗にお掃除
        self.canvas.delete(
            os.path.join(os.path.dirname(__file__), "Main_UI", "HitBrow_mainUI.jpg")
        )
        self.root.unbind("<Return>")
        self.canvas.delete("Mode1_Button")
        self.canvas.delete("Mode2_Button")
        self.canvas.delete("Mode3_Button")
        self.canvas.delete("Mode1_Button_window")
        self.canvas.delete("Mode2_Button_window")
        self.canvas.delete("Mode3_Button_window")
        pygame.mixer.music.stop()


# --- ゲーム本編のシーン ---
class GameScene1(BaseScene):
    def enter(self):
        print("ゲームシーン1を開始します")
        self.Start_time = time.time()
        self.secret = make_secret16(3)
        self.result_list = []

        self.keyNumber_STR1 = "0"
        self.keyNumber_STR2 = "0"
        self.keyNumber_STR3 = "0"

        self.check_number = (
            self.keyNumber_STR1 + self.keyNumber_STR2 + self.keyNumber_STR3
        )

        BackGround_img = Image.open(
            os.path.join(os.path.dirname(__file__), "Main_UI", "test_image_Normal.PNG")
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
        self.Return_Title_button = tk.Button(
            self.canvas,
            text="タイトルへ",
            bg="green",
            fg="white",  # 文字を白くして見やすくする
            font=("Arial", 30),  # ここでフォントサイズを調整
            command=self.Return_to_title,  # クリック時の処理
        )
        self.Return_Title_Button_window = self.canvas.create_window(
            self.engine.DisplayX // 2 + 400,
            self.engine.DisplayY // 2 + 200,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=300,  # ボタンの幅
            height=70,  # ボタンの高さ
            window=self.Return_Title_button,  # 埋め込むウィジェットを指定
            tags="Return_Title_Button",  # 四角形と同じようにタグを設定可能
        )

        self.SubMit = tk.Button(
            self.canvas,
            text="Submit",
            bg="green",
            fg="white",  # 文字を白くして見やすくする
            font=("Arial", 30),  # ここでフォントサイズを調整
            command=self.Create_Result_Chacks,  # クリック時の処理
        )
        self.SubMit_window = self.canvas.create_window(
            self.engine.DisplayX // 2,
            self.engine.DisplayY // 2 - 200,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=200,  # ボタンの幅
            height=70,  # ボタンの高さ
            window=self.SubMit,  # 埋め込むウィジェットを指定
            tags="SubMit",  # 四角形と同じようにタグを設定可能
        )

        # NumberUpボタン1
        self.UpNumber1 = tk.Button(
            self.canvas,
            text="上",
            bg="green",
            fg="white",  # 文字を白くして見やすくする
            font=("Arial", 30),  # ここでフォントサイズを調整
            command=self.NumberBox_UP1,  # クリック時の処理
        )
        self.UpNumber1_window = self.canvas.create_window(
            self.engine.DisplayX // 2,
            self.engine.DisplayY // 2,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=100,  # ボタンの幅
            height=70,  # ボタンの高さ
            window=self.UpNumber1,  # 埋め込むウィジェットを指定
            tags="UpNumber1",  # 四角形と同じようにタグを設定可能
        )
        # NumberUpボタン2
        self.UpNumber2 = tk.Button(
            self.canvas,
            text="上",
            bg="green",
            fg="white",  # 文字を白くして見やすくする
            font=("Arial", 30),  # ここでフォントサイズを調整
            command=self.NumberBox_UP2,  # クリック時の処理
        )
        self.UpNumber2_window = self.canvas.create_window(
            self.engine.DisplayX // 2 + 110,
            self.engine.DisplayY // 2,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=100,  # ボタンの幅
            height=70,  # ボタンの高さ
            window=self.UpNumber2,  # 埋め込むウィジェットを指定
            tags="UpNumber2",  # 四角形と同じようにタグを設定可能
        )
        # NumberUpボタン3
        self.UpNumber3 = tk.Button(
            self.canvas,
            text="上",
            bg="green",
            fg="white",  # 文字を白くして見やすくする
            font=("Arial", 30),  # ここでフォントサイズを調整
            command=self.NumberBox_UP3,  # クリック時の処理
        )
        self.UpNumber3_window = self.canvas.create_window(
            self.engine.DisplayX // 2 + 220,
            self.engine.DisplayY // 2,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=100,  # ボタンの幅
            height=70,  # ボタンの高さ
            window=self.UpNumber3,  # 埋め込むウィジェットを指定
            tags="UpNumber3",  # 四角形と同じようにタグを設定可能
        )
        # NumberDownボタン1
        self.DownNumber1 = tk.Button(
            self.canvas,
            text="下",
            bg="green",
            fg="white",  # 文字を白くして見やすくする
            font=("Arial", 30),  # ここでフォントサイズを調整
            command=self.NumberBox_Down1,  # クリック時の処理
        )
        self.DownNumber1_window = self.canvas.create_window(
            self.engine.DisplayX // 2,
            self.engine.DisplayY // 2 - 80,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=100,  # ボタンの幅
            height=70,  # ボタンの高さ
            window=self.DownNumber1,  # 埋め込むウィジェットを指定
            tags="DownNumber1",  # 四角形と同じようにタグを設定可能
        )
        # NumberDownボタン2
        self.DownNumber2 = tk.Button(
            self.canvas,
            text="下",
            bg="green",
            fg="white",  # 文字を白くして見やすくする
            font=("Arial", 30),  # ここでフォントサイズを調整
            command=self.NumberBox_Down2,  # クリック時の処理
        )
        self.DownNumber2_window = self.canvas.create_window(
            self.engine.DisplayX // 2 + 110,
            self.engine.DisplayY // 2 - 80,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=100,  # ボタンの幅
            height=70,  # ボタンの高さ
            window=self.DownNumber2,  # 埋め込むウィジェットを指定
            tags="DownNumber2",  # 四角形と同じようにタグを設定可能
        )
        # NumberDownボタン3
        self.DownNumber3 = tk.Button(
            self.canvas,
            text="下",
            bg="green",
            fg="white",  # 文字を白くして見やすくする
            font=("Arial", 30),  # ここでフォントサイズを調整
            command=self.NumberBox_Down3,  # クリック時の処理
        )
        self.DownNumber3_window = self.canvas.create_window(
            self.engine.DisplayX // 2 + 220,
            self.engine.DisplayY // 2 - 80,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=100,  # ボタンの幅
            height=70,  # ボタンの高さ
            window=self.DownNumber3,  # 埋め込むウィジェットを指定
            tags="DownNumber3",  # 四角形と同じようにタグを設定可能
        )

        self.TimeText = self.canvas.create_text(
            self.engine.DisplayX // 2 - 100,
            self.engine.DisplayY // 2,
            text="0",
            fill="black",  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 30),  # フォントとサイズ
            anchor="center",  # 基準点
            tags="TimeText",  # タグをつけて管理可能
        )

        self.Number1_text = self.canvas.create_text(
            self.engine.DisplayX // 2 - 300,
            self.engine.DisplayY // 2,
            text="0",
            fill="black",  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 30),  # フォントとサイズ
            anchor="center",  # 基準点
            tags="Number1_text",  # タグをつけて管理可能
        )
        self.Number2_text = self.canvas.create_text(
            self.engine.DisplayX // 2 - 240,
            self.engine.DisplayY // 2,
            text="0",
            fill="black",  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 30),  # フォントとサイズ
            anchor="center",  # 基準点
            tags="Number2_text",  # タグをつけて管理可能
        )
        self.Number3_text = self.canvas.create_text(
            self.engine.DisplayX // 2 - 160,
            self.engine.DisplayY // 2,
            text="0",
            fill="black",  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 30),  # フォントとサイズ
            anchor="center",  # 基準点
            tags="Number3_text",  # タグをつけて管理可能
        )
        self.Result_text = self.canvas.create_text(
            self.engine.DisplayX // 2 + 400,
            self.engine.DisplayY // 2 - 300,
            text="",
            fill="black",  # 文字の色（fgの代わりにfillを使います）
            font=("Arial", 30),  # フォントとサイズ
            anchor="n",  # 基準点
            tags="Result_text",  # タグをつけて管理可能
        )

    def Return_to_title(self):
        print("タイトルバックボタンが押されました。タイトル画面に戻ります")
        self.engine.change_scene(TitleScene(self.engine))

    def NumberBox_UP1(self):
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
        self.canvas.itemconfig("TimeText", text=str(round(TimeUp_Time - delta_time)))
        if delta_time >= TimeUp_Time:
            print("タイムアップ")
            self.engine.change_scene(TitleScene(self.engine))

    def Create_Result_Chacks(self):
        self.check_number = (
            self.keyNumber_STR1 + self.keyNumber_STR2 + self.keyNumber_STR3
        )
        hit, blow = judge(self.secret, self.check_number)
        result = {"hit": hit, "blow": blow}
        self.result_list.append(result)

        log_lines = [
            f"Hit: {log['hit']}, Blow: {log['blow']}" for log in self.result_list
        ]
        log_text = "\n".join(log_lines)
        self.canvas.itemconfig("Result_text", text=log_text)

    def update(self):
        self.Timer(180)

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


class GameScene2(BaseScene):
    def enter(self):
        self.box_x, self.box_y = 175, 125
        self.player_box = self.canvas.create_rectangle(
            self.box_x,
            self.box_y,
            self.box_x + 50,
            self.box_y + 50,
            fill="green",
            tag="game_ui",
        )
        self.tick_counter = 0
        self.move_counter = 0

        BackGround_img = Image.open(
            os.path.join(os.path.dirname(__file__), "Main_UI", "test_image_Normal.PNG")
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
        self.Return_Title_button = tk.Button(
            self.canvas,
            text="タイトルへ",
            bg="red",
            fg="white",  # 文字を白くして見やすくする
            font=("Arial", 30),  # ここでフォントサイズを調整
            command=self.Return_to_title,  # クリック時の処理
        )

        self.Return_Title_Button_window = self.canvas.create_window(
            self.engine.DisplayX // 2 + 400,
            self.engine.DisplayY // 2 + 200,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=300,  # ボタンの幅
            height=70,  # ボタンの高さ
            window=self.Return_Title_button,  # 埋め込むウィジェットを指定
            tags="Return_Title_Button",  # 四角形と同じようにタグを設定可能
        )
        # タイトルバックボタン設定(ここまで)------------------------------------

    def Return_to_title(self):
        print("タイトルバックボタンが押されました。タイトル画面に戻ります")
        self.engine.change_scene(TitleScene(self.engine))

    def update(self):
        # 箱を動かす処理（以前の game_loop の中身）
        self.tick_counter += 1
        if self.tick_counter % 30 == 0:
            if self.move_counter >= 3:
                self.move_counter = 0
                self.tick_counter = 0
            else:
                self.move_counter += 1

            new_x = self.box_x + (self.move_counter * 50)
            self.canvas.coords(
                self.player_box, new_x, self.box_y, new_x + 50, self.box_y + 50
            )

    def exit(self):
        self.canvas.delete("game_ui")
        self.canvas.delete("BackGround_img")
        self.canvas.delete("Return_Title_Button")


class GameScene3(BaseScene):
    def enter(self):
        self.box_x, self.box_y = 175, 125
        self.player_box = self.canvas.create_rectangle(
            self.box_x,
            self.box_y,
            self.box_x + 50,
            self.box_y + 50,
            fill="green",
            tag="game_ui",
        )
        self.tick_counter = 0
        self.move_counter = 0

        BackGround_img = Image.open(
            os.path.join(os.path.dirname(__file__), "Main_UI", "test_image_Normal.PNG")
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
        self.Return_Title_button = tk.Button(
            self.canvas,
            text="タイトルへ",
            bg="blue",
            fg="white",  # 文字を白くして見やすくする
            font=("Arial", 30),  # ここでフォントサイズを調整
            command=self.Return_to_title,  # クリック時の処理
        )
        self.Return_Title_Button_window = self.canvas.create_window(
            self.engine.DisplayX // 2 + 400,
            self.engine.DisplayY // 2 + 200,
            anchor="center",  # 基準点を左上(North-West)にする（これがないと中央基準になります）
            width=300,  # ボタンの幅
            height=70,  # ボタンの高さ
            window=self.Return_Title_button,  # 埋め込むウィジェットを指定
            tags="Return_Title_Button",  # 四角形と同じようにタグを設定可能
        )
        # タイトルバックボタン設定(ここまで)------------------------------------

    def Return_to_title(self):
        print("タイトルバックボタンが押されました。タイトル画面に戻ります")
        self.engine.change_scene(TitleScene(self.engine))

    def update(self):
        # 箱を動かす処理（以前の game_loop の中身）
        self.tick_counter += 1
        if self.tick_counter % 30 == 0:
            if self.move_counter >= 3:
                self.move_counter = 0
                self.tick_counter = 0
            else:
                self.move_counter += 1

            new_x = self.box_x + (self.move_counter * 50)
            self.canvas.coords(
                self.player_box, new_x, self.box_y, new_x + 50, self.box_y + 50
            )

    def exit(self):
        self.canvas.delete("game_ui")
        self.canvas.delete("BackGround_img")
        self.canvas.delete("Return_Title_Button")


# --- ゲームエンジン（マネージャー） ---
class GameEngine:
    def __init__(self, root):
        # ... (初期化処理) ...
        self.root = root
        self.root.title("Hit and Brow")
        self.root.geometry("1280x720")
        self.DisplayX, self.DisplayY = 1280, 720

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
