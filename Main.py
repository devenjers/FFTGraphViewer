import sys


#Conda 같은 가상환경 X - 별도 세팅하기

#pip install pyqt5
from PyQt5.QtGui import*
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QWidget, QVBoxLayout, QPushButton


#pip install matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvas as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy


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
        canvas2 = FigureCanvas(Figure(figsize=(4, 3)))
        canvas3 = FigureCanvas(Figure(figsize=(4, 3)))
        vbox = QVBoxLayout(self.main_widget)
        vbox.addWidget(canvas)
        vbox.addWidget(canvas2)
        vbox.addWidget(canvas3)


        self.addToolBar(NavigationToolbar(canvas, self))

        self.ax = canvas.figure.subplots()
        #self.ax.plot([0, 1, 2], [1, 5, 3], '-')

        self.ax2 = canvas2.figure.subplots()
        #self.ax2.plot([0, 1, 2], [1, 5, 3], '-')

        self.ax3 = canvas3.figure.subplots()
        #self.ax3.plot([0, 1, 2], [1, 5, 3], '-')


        self.setGeometry(300, 100, 600, 400)


        btnReadFile = QPushButton("파일 찾기", self)
        btnReadFile.clicked.connect(self.onFileDialog)


    def onFileDialog(self):
        self.fileName = QFileDialog.getOpenFileName(self, "파일 열기", './')
        self.ReadWaveFile(self.GetFilePath())
        self.DrawPCMGraph()
        self.FFTGraph()
        self.WavSpectrogram()
        

    def GetFilePath(self):
        return self.fileName[0]

    def ReadWaveFile(self, filePath):
        self.sampleRate, self.pcmData = wavfile.read(filePath)

    def DrawPCMGraph(self):
        dataLen = int(len(self.pcmData.T[0]))
        self.ax2.plot(self.pcmData.T[0][:dataLen], 'r')
        

    def FFTGraph(self):
        n = len(self.pcmData.T[0])
        T = 1 / self.sampleRate
        yf = fft(self.pcmData.T[0])
        xf = numpy.linspace(0, int(1.0/(2.0*T)), int(n/2))
        self.ax.plot(xf, 2.0/n * numpy.abs(yf[:n//2]),'b')

    def WavSpectrogram(self):
        self.ax3.specgram(self.pcmData.T[0], Fs=self.sampleRate)


    
    





if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    
    main.show()
    app.exec_()