import tkinter as tk
from PIL import Image, ImageTk
import pygame
import os


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

        #バックグラウンドイメージの設定とボタンの初期設定
        try:
            img = Image.open(os.path.join(os.path.dirname(__file__), "Main_UI", "HitBrow_mainUI.jpg"))
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
                fg="white",             # 文字を白くして見やすくする
                font=("Arial", 30),  # ここでフォントサイズを調整
                command=self.Go_to_mode1 # クリック時の処理
            )
            self.to_mode1_button.pack()

            self.to_mode2_button = tk.Button(
                self.canvas, 
                text="モード2へ", 
                bg="red", 
                fg="white",             # 文字を白くして見やすくする
                font=("Arial", 30),  # ここでフォントサイズを調整
                command=self.Go_to_mode2 # クリック時の処理
            )
            self.to_mode2_button.pack()

            self.to_mode3_button = tk.Button(
                self.canvas, 
                text="モード３へ", 
                bg="blue", 
                fg="white",             # 文字を白くして見やすくする
                font=("Arial", 30),  # ここでフォントサイズを調整
                command=self.Go_to_mode3 # クリック時の処理
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
            
        #ボタンの配置
        try:
            self.to_mode1_button_window = self.canvas.create_window(
                self.engine.DisplayX // 2 + 400,
                self.engine.DisplayY // 2 - 100, 
                anchor="center",         # 基準点を左上(North-West)にする（これがないと中央基準になります）
                width=300,            # ボタンの幅
                height=70,           # ボタンの高さ
                window=self.to_mode1_button, # 埋め込むウィジェットを指定
                tags="Mode1_Button"       # 四角形と同じようにタグを設定可能
            )
            self.to_mode2_button_window = self.canvas.create_window(
                self.engine.DisplayX // 2 + 400,
                self.engine.DisplayY // 2, 
                anchor="center",         # 基準点を左上(North-West)にする（これがないと中央基準になります）
                width=300,            # ボタンの幅
                height=70,           # ボタンの高さ
                window=self.to_mode2_button, # 埋め込むウィジェットを指定
                tags="Mode2_Button"       # 四角形と同じようにタグを設定可能
            )
            self.to_mode3_button_window = self.canvas.create_window(
                self.engine.DisplayX // 2 + 400,
                self.engine.DisplayY // 2 + 100, 
                anchor="center",         # 基準点を左上(North-West)にする（これがないと中央基準になります）
                width=300,            # ボタンの幅
                height=70,           # ボタンの高さ
                window=self.to_mode3_button, # 埋め込むウィジェットを指定
                tags="Mode3_Button"       # 四角形と同じようにタグを設定可能
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
            pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), "Main_BGM", "hatena.mp3"))
            pygame.mixer.music.play(-1)
            print("BGM再生開始!")

        except pygame.error:
            print("BGMファイル(hatena.mp3)が見つかりません。無音で進行します。")

    def exit(self):
        # 次の画面に行く前に、自分の出した画像とキー設定を綺麗にお掃除
        self.canvas.delete(os.path.join(os.path.dirname(__file__), "Main_UI", "HitBrow_mainUI.jpg"))
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

        BackGround_img = Image.open(os.path.join(os.path.dirname(__file__), "Main_UI", "test_image_Normal.PNG"))
        BackGround_img = BackGround_img.resize((self.engine.DisplayX, self.engine.DisplayY))
        self.BackGround_img = ImageTk.PhotoImage(BackGround_img)
        self.canvas.create_image(
            self.engine.DisplayX // 2,
            self.engine.DisplayY // 2,
            image=self.BackGround_img,
            tag="BackGround_img",
        )

        #タイトルバックボタン設定------------------------------------
        self.Return_Title_button = tk.Button(
                self.canvas, 
                text="タイトルへ", 
                bg="green", 
                fg="white",             # 文字を白くして見やすくする
                font=("Arial", 30),  # ここでフォントサイズを調整
                command=self.Return_to_title # クリック時の処理
            )
        self.Return_Title_Button_window = self.canvas.create_window(
                self.engine.DisplayX // 2 + 400,
                self.engine.DisplayY // 2 + 200, 
                anchor="center",         # 基準点を左上(North-West)にする（これがないと中央基準になります）
                width=300,            # ボタンの幅
                height=70,           # ボタンの高さ
                window=self.Return_Title_button, # 埋め込むウィジェットを指定
                tags="Return_Title_Button"       # 四角形と同じようにタグを設定可能
            )
        #タイトルバックボタン設定(ここまで)------------------------------------

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

        BackGround_img = Image.open(os.path.join(os.path.dirname(__file__), "Main_UI", "test_image_Normal.PNG"))
        BackGround_img = BackGround_img.resize((self.engine.DisplayX, self.engine.DisplayY))
        self.BackGround_img = ImageTk.PhotoImage(BackGround_img)
        self.canvas.create_image(
            self.engine.DisplayX // 2,
            self.engine.DisplayY // 2,
            image=self.BackGround_img,
            tag="BackGround_img",
        )
        #タイトルバックボタン設定------------------------------------
        self.Return_Title_button = tk.Button(
                self.canvas, 
                text="タイトルへ", 
                bg="red", 
                fg="white",             # 文字を白くして見やすくする
                font=("Arial", 30),  # ここでフォントサイズを調整
                command=self.Return_to_title # クリック時の処理
            )

        self.Return_Title_Button_window = self.canvas.create_window(
                self.engine.DisplayX // 2 + 400,
                self.engine.DisplayY // 2 + 200, 
                anchor="center",         # 基準点を左上(North-West)にする（これがないと中央基準になります）
                width=300,            # ボタンの幅
                height=70,           # ボタンの高さ
                window=self.Return_Title_button, # 埋め込むウィジェットを指定
                tags="Return_Title_Button"       # 四角形と同じようにタグを設定可能
            )
        #タイトルバックボタン設定(ここまで)------------------------------------

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

        BackGround_img = Image.open(os.path.join(os.path.dirname(__file__), "Main_UI", "test_image_Normal.PNG"))
        BackGround_img = BackGround_img.resize((self.engine.DisplayX, self.engine.DisplayY))
        self.BackGround_img = ImageTk.PhotoImage(BackGround_img)
        self.canvas.create_image(
            self.engine.DisplayX // 2,
            self.engine.DisplayY // 2,
            image=self.BackGround_img,
            tag="BackGround_img",
        )


        #タイトルバックボタン設定------------------------------------
        self.Return_Title_button = tk.Button(
                self.canvas, 
                text="タイトルへ", 
                bg="blue", 
                fg="white",             # 文字を白くして見やすくする
                font=("Arial", 30),  # ここでフォントサイズを調整
                command=self.Return_to_title # クリック時の処理
            )
        self.Return_Title_Button_window = self.canvas.create_window(
                self.engine.DisplayX // 2 + 400,
                self.engine.DisplayY // 2 + 200, 
                anchor="center",         # 基準点を左上(North-West)にする（これがないと中央基準になります）
                width=300,            # ボタンの幅
                height=70,           # ボタンの高さ
                window=self.Return_Title_button, # 埋め込むウィジェットを指定
                tags="Return_Title_Button"       # 四角形と同じようにタグを設定可能
            )
        #タイトルバックボタン設定(ここまで)------------------------------------

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

