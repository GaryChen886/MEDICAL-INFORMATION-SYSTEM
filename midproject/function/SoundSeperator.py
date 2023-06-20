import numpy as np
import soundfile as sf
from scipy import signal
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtMultimedia import QSound

class SoundSeparator(QWidget):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.channels = None
        self.initUI()
        
    def initUI(self):
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Sound Separator')
        
        btn_separate = QPushButton('Separate Channels', self)
        btn_separate.setGeometry(50, 50, 200, 30)
        btn_separate.clicked.connect(self.separateChannels)
        
        btn_combine = QPushButton('Combine Channels', self)
        btn_combine.setGeometry(50, 100, 200, 30)
        btn_combine.clicked.connect(self.combineChannels)
        
    def separateChannels(self):
        data, samplerate = sf.read(self.filename)
        
        if len(data.shape) > 1:
            data = np.mean(data, axis=1)
        
        ica = FastICA(n_components=4)  # 假設有4個聲道
        self.channels = ica.fit_transform(data.reshape(-1, 1))
        
        for i, channel in enumerate(self.channels.T):
            sf.write(f'channel_{i+1}.wav', channel, samplerate)
    
    def combineChannels(self):
        if self.channels is None:
            return
        
        combined = np.column_stack(self.channels)
        sf.write('combined.wav', combined, samplerate)
        
    def playSound(self, idx):
        QSound.play(f'channel_{idx+1}.wav')

if __name__ == '__main__':
    app = QApplication([])
    separator = SoundSeparator('record.wav')
    separator.show()
    app.exec_()
