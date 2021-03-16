from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QDesktopWidget, QLabel, QVBoxLayout, QFileDialog, QGridLayout, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon, QCursor, QPixmap
from PyQt5 import QtGui, QtCore
import urllib.request
import sys
import re
import pafy
import os
from pathlib import Path

path_to_download_folder = str(os.path.join(Path.home(), "Downloads/YT_AUDIO_DOWNLOADS"))

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

    def download_best_video(self, vid_id):
        #select video
        vid = pafy.new(vid_id)
        print(vid.title)
        #select best audio
        bestvideo = vid.getbestvideo(preftype="mp4, mov, wmv, avi", ftypestrict=False)
        #download video file
        bestvideo.download(self.download_folder)

    def download_song_list(self, song_list):
        try:
            for query in song_list:
                vid_id = self.get_video_info(query)
                print(vid_id)
                self.download_best_audio(vid_id)
                return 1
        except Exception:
            return 0

    def download_video_list(self, video_list):
        try:
            for query in video_list:
                vid_id = self.get_video_info(query)
                print(vid_id)
                self.download_best_video(vid_id)
                return 1
        except Exception:
            return 0


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

    def handleAudioBtn(self):
        text = self.widgets['text_input'].text()
        if text:
            msg = QMessageBox()
            msg.setWindowTitle('Downloading')
            msg.setText('Songs are beeing downloaded, please hold on!')
            msg.show()
            song_list = []
            song_list.extend(text.split(','))
            isDownloaded = self.YTDownloader.download_song_list(song_list)
            if isDownloaded:
                msg.setWindowTitle('Downloaded!')
                msg.setText('Songs have been downloaded')
            else:
                msg.setWindowTitle('Error!')
                msg.setText('There was an error with your download, please try again.\nWatch your grammar!')
            msg.exec_()
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Please enter some input')
            msg.exec_()

    def handleVideoBtn(self):
        text = self.widgets['text_input'].text()
        if text:
            msg = QMessageBox()
            msg.setWindowTitle('Downloading')
            msg.setText('Songs are beeing downloaded, please hold on!')
            msg.show()
            video_list = []
            video_list.extend(text.split(','))
            isDownloaded = self.YTDownloader.download_video_list(video_list)
            if isDownloaded:
                msg.setWindowTitle('Downloaded!')
                msg.setText('Songs have been downloaded')
            else:
                msg.setWindowTitle('Error!')
                msg.setText('There was an error with your download, please try again.\nWatch your grammar!')
            msg.exec_()
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Please enter some input')
            msg.exec_()

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
        #download-audio-button
        button_audio = QPushButton("Download\nAudio")
        button_audio.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button_audio.setStyleSheet(
            "*{border: 4px solid '#BC006C'; border-radius: 45px; font-size: 20px; color: 'white'; padding: 30px; margin: 100px 200px}"+
            "*:hover{background: '#BC006C';}"
        )
        button_audio.clicked.connect(self.handleAudioBtn)
        #download-video-button
        button_video = QPushButton("Download\nVideo")
        button_video.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button_video.setStyleSheet(
            "*{border: 4px solid '#BC006C'; border-radius: 45px; font-size: 20px; color: 'white'; padding: 30px; margin: 100px 200px}"+
            "*:hover{background: '#BC006C';}"
        )
        button_video.clicked.connect(self.handleVideoBtn)
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
        self.widgets.update([('logo', logo), ('button_audio', button_audio), ('button_video', button_video), ('text', text), ('text_input', text_input)])
        #Init items
        self.grid.addWidget(logo, 0, 0, 1, 2)
        self.grid.addWidget(text, 1, 0, 1, 2)
        self.grid.addWidget(text_input, 2, 0, 1, 2)
        self.grid.addWidget(button_audio, 3, 0)
        self.grid.addWidget(button_video, 3, 1)
        self.setLayout(self.grid)

def main():
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())