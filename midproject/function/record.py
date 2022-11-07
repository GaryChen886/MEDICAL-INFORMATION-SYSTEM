import time
import threading
import socket
import struct
import re
import os
import sys
from subprocess import call
from enum import Enum, unique
from traceback import print_exc


from aiy.voice.audio import AudioFormat, play_wav, record_file, Recorder

Lab = AudioFormat(sample_rate_hz=16000, num_channels=1, bytes_per_sample=2)


def record():

    def wait():
        start = time.monotonic()
        duration = 0.0
        while duration <= 4.0:
            duration = time.monotonic() - start
            time.sleep(0.5)

    record_file(Lab, filename='./files/question.wav', wait=wait, filetype='wav')
