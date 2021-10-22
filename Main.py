import sys


#Conda 같은 가상환경 X - 별도 세팅하기

#pip install pyqt5
from PyQt5.QtGui import*
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QWidget, QVBoxLayout, QPushButton


#pip install matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvas as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


#pip install scipy
from scipy.fftpack import fft
from scipy.io import wavfile

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("FFT 그래프 보기")

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)


        canvas = FigureCanvas(Figure(figsize=(4, 3)))
        vbox = QVBoxLayout(self.main_widget)
        vbox.addWidget(canvas)


        self.addToolBar(NavigationToolbar(canvas, self))

        self.ax = canvas.figure.subplots()
        self.ax.plot([0, 1, 2], [1, 5, 3], '-')


        self.setGeometry(300, 100, 600, 400)


        btnReadFile = QPushButton("파일 찾기", self)
        btnReadFile.clicked.connect(self.onFileDialog)


    def onFileDialog(self):
        self.fileName = QFileDialog.getOpenFileName(self, "파일 열기", './')
        self.ReadWaveFile(self.GetFilePath())
        

    def GetFilePath(self):
        return self.fileName[0]

    def ReadWaveFile(self, filePath):
        fs, data = wavfile.read(filePath)
        a = data
        b=[(ele/2**16.)*2-1 for ele in a]
        c = fft(b)
        d = int(len(c)/2)
        print(abs(c[:(d-1)]))
        self.ax.plot(abs(c[:(d-1)]),'r')




if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    
    main.show()
    app.exec_()