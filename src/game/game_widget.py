from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer, Qt, QRect
from PyQt5.QtGui import QPainter, QPixmap

class GameWidget(QWidget):
    def __init__(self, player_img_path: str, bg_img_path: str = ""):
        super().__init__()
        self.setFocusPolicy(Qt.StrongFocus)

        self.player_pix = QPixmap(player_img_path)
        self.bg_pix = QPixmap(bg_img_path) if bg_img_path else QPixmap()

        # player 狀態
        self.x = 80
        self.y = 80
        self.vx = 0
        self.vy = 0
        self.speed = 4

        # 60 FPS 更新
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(16)

    def tick(self):
        # 更新位置
        self.x += self.vx
        self.y += self.vy

        # 邊界限制
        w = self.width()
        h = self.height()
        pw = self.player_pix.width() if not self.player_pix.isNull() else 30
        ph = self.player_pix.height() if not self.player_pix.isNull() else 30

        self.x = max(0, min(self.x, w - pw))
        self.y = max(0, min(self.y, h - ph))

        self.update()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_A:
            self.vx = -self.speed
        elif e.key() == Qt.Key_D:
            self.vx = self.speed
        elif e.key() == Qt.Key_W:
            self.vy = -self.speed
        elif e.key() == Qt.Key_S:
            self.vy = self.speed
        else:
            super().keyPressEvent(e)

    def keyReleaseEvent(self, e):
        if e.key() in (Qt.Key_A, Qt.Key_D):
            self.vx = 0
        elif e.key() in (Qt.Key_W, Qt.Key_S):
            self.vy = 0
        else:
            super().keyReleaseEvent(e)

    def paintEvent(self, e):
        painter = QPainter(self)

        # 背景
        if not self.bg_pix.isNull():
            painter.drawPixmap(self.rect(), self.bg_pix)
        else:
            painter.fillRect(self.rect(), Qt.black)

        # player
        if not self.player_pix.isNull():
            painter.drawPixmap(self.x, self.y, self.player_pix)
        else:
            painter.fillRect(QRect(self.x, self.y, 30, 30), Qt.white)
