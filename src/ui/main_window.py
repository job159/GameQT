from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QMessageBox, QLabel
)
from PyQt5.QtCore import Qt
from utils.paths import pic_dir
from ui.image_viewer import ImageViewer
from game.game_widget import GameWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Demo App")
        self.resize(1000, 650)

        # 第二視窗（看圖）
        self.viewer = ImageViewer()

        # 預設圖片路徑（pic 資料夾）
        pdir = pic_dir()
        self.player_path = str(pdir / "player.png")
        self.bg_path = str(pdir / "bg.png")

        # 中央 UI
        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout()
        central.setLayout(root)

        # 左側：控制面板
        left = QVBoxLayout()
        root.addLayout(left, 1)

        self.info = QLabel(
            "操作：W/A/S/D 移動\n"
            "功能：選單、選圖、開第二視窗預覽\n"
            "圖片預設讀 pic/player.png、pic/bg.png"
        )
        self.info.setWordWrap(True)
        left.addWidget(self.info)

        btn_row = QHBoxLayout()
        left.addLayout(btn_row)

        self.btn_open_img = QPushButton("選擇圖片並預覽")
        self.btn_open_img.clicked.connect(self.open_image_dialog)
        btn_row.addWidget(self.btn_open_img)

        self.btn_open_viewer = QPushButton("開啟預覽視窗")
        self.btn_open_viewer.clicked.connect(self.show_viewer)
        btn_row.addWidget(self.btn_open_viewer)

        self.btn_reload_game = QPushButton("重載遊戲(用目前圖片)")
        self.btn_reload_game.clicked.connect(self.reload_game)
        left.addWidget(self.btn_reload_game)

        left.addStretch(1)

        # 右側：遊戲畫面
        self.game = GameWidget(player_img_path=self.player_path, bg_img_path=self.bg_path)
        root.addWidget(self.game, 3)

        # 建立選單
        self._create_menu()

    def _create_menu(self):
        menu_file = self.menuBar().addMenu("File")
        act_open = menu_file.addAction("Open Image...")
        act_open.triggered.connect(self.open_image_dialog)

        act_exit = menu_file.addAction("Exit")
        act_exit.triggered.connect(self.close)

        menu_help = self.menuBar().addMenu("Help")
        act_about = menu_help.addAction("About")
        act_about.triggered.connect(self.about)

    def about(self):
        QMessageBox.information(self, "About", "PyQt5 Demo: multi-window, menu, file dialog, game update (QTimer).")

    def show_viewer(self):
        self.viewer.show()
        self.viewer.raise_()
        self.viewer.activateWindow()

    def open_image_dialog(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select an image",
            str(pic_dir()),
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if not path:
            return

        # 直接拿你選的圖給預覽視窗看
        self.viewer.set_image(path)
        self.show_viewer()

        # 同時把 player 圖也換成你選的（你也可以改成只更新預覽不影響遊戲）
        self.player_path = path

    def reload_game(self):
        # 重新建立 game widget（簡單粗暴但很好懂）
        parent_layout = self.centralWidget().layout()
        # parent_layout 是 root(HBoxLayout)，game 在 index 1
        old_game = self.game
        self.game = GameWidget(player_img_path=self.player_path, bg_img_path=self.bg_path)
        parent_layout.replaceWidget(old_game, self.game)
        old_game.setParent(None)
        self.game.setFocus()
