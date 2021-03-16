import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QDesktopWidget, QLabel, QVBoxLayout, QFileDialog, QGridLayout, QPushButton
from PyQt5.QtGui import QIcon, QCursor, QPixmap
from PyQt5 import QtGui, QtCore
from YTDownloader import YTDownloader

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'YouTube Downloader'
        self.width = 720
        self.height = 480
        self.grid = QGridLayout()
        self.widgets = {}
        self.YTDownloader = YTDownloader()
        self.initUI()

    def handleClick(self):
        text = self.widgets['text_input'].text()
        song_list = []
        song_list.extend(text.split(','))
        self.YTDownloader.download_song_list(song_list)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, self.width, self.height)
        self.center()
        self.styleUI()
        self.layoutUI()
        self.show()
    
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def styleUI(self):
        self.setStyleSheet("background: #161219;")

    def layoutUI(self):
        #logo
        logo = QLabel()
        logo.setPixmap(QPixmap("yt_logo.png").scaled(128, 128))
        logo.setAlignment(QtCore.Qt.AlignCenter)
        logo.setStyleSheet("margin-top: 12px;")
        #download-button
        button = QPushButton("Download")
        button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button.setStyleSheet(
            "*{border: 4px solid '#BC006C'; border-radius: 45px; font-size: 20px; color: 'white'; padding: 30px; margin: 100px 200px}"+
            "*:hover{background: '#BC006C';}"
        )
        button.clicked.connect(self.handleClick)
        #Text
        text = QLabel("Write the name of the songs you wish to download separated by commas")
        text.setAlignment(QtCore.Qt.AlignLeft)
        text.setStyleSheet(
            "font-size: 20px; color: white; padding: 25px 15px; border: 1px solid '#BC006C'; border-radius: 40px;"
        )
        text.setWordWrap(True)
        #text_input
        text_input = QLineEdit()
        text_input.resize(120, 120)
        text_input.setStyleSheet(
            "font-size: 20px; color: white; padding: 10px; margin-top: 20px; border: 1px solid '#BC006C'; border-radius: 40px;"
        )
        #store items
        self.widgets.update([('logo', logo), ('button', button), ('text', text), ('text_input', text_input)])
        #Init items
        self.grid.addWidget(logo, 0, 0)
        self.grid.addWidget(text, 1, 0)
        self.grid.addWidget(text_input, 2, 0)
        self.grid.addWidget(button, 3, 0)
        self.setLayout(self.grid)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())