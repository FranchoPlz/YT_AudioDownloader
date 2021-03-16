import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QDesktopWidget, QLabel, QVBoxLayout, QFileDialog, QGridLayout, QPushButton
from PyQt5.QtGui import QIcon, QCursor, QPixmap
from PyQt5 import QtGui, QtCore
import urllib.request
import re
import pafy
import os
from pathlib import Path

path_to_download_folder = str(os.path.join(Path.home(), "Downloads"))

class YTDownloader():
    def __init__(self, download_folder=path_to_download_folder):
        self.download_folder = download_folder
        if not os.path.isdir(download_folder):
            os.mkdir(download_folder)
        self.ytq_url = 'https://www.youtube.com/results?search_query='
        self.ytw_url = 'https://www.youtube.com/watch?v='

    def get_video_info(self, query):
        #prepare string to be used in query
        query = query.replace(' ', '_')
        #Query for the first vid in search engine
        html = urllib.request.urlopen(self.ytq_url + query)
        video_ids = re.findall(r'watch\?v=(\S{11})', html.read().decode())
        vid_id = self.ytw_url + video_ids[0]
        return vid_id

    def download_best_audio(self, vid_id):
        #select video
        vid = pafy.new(vid_id)
        print(vid.title)
        #select best audio
        bestaudio = vid.getbestaudio(preftype="mp3, wav", ftypestrict=False)
        #download audio file
        bestaudio.download(self.download_folder)

    def download_song_list(self, song_list):
        for query in song_list:
            vid_id = self.get_video_info(query)
            print(vid_id)
            self.download_best_audio(vid_id)



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
        if text:
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
        logo.setPixmap(QPixmap("./yt_logo.png").scaled(128, 128))
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

def main():
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())