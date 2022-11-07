# !/usr/bin/env python
# _*_coding:utf-8_*_

# 給任何使用這支程式的人：這支程式是國台語合成的API的client端。具體上會發送最下方變數data
# 給伺服器，並接收一個回傳的wav檔，output.wav
# 客戶端 ，用來呼叫service_Server.py
import socket
import struct
import argparse


class TTSClient:
    def __init__(self):
        self.host = "140.116.245.157"

    def askForService(self, data: str):
        '''
        DO NOT MODIFY THIS PART
        Params:
            data    :(str) Text to be synthesized. If language is chinese, it must be chinese.If language is taiwanese, it can be chinese or tai-luo.
        '''
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if not len(data):
                raise ValueError("Length of data must be bigger than zero")

            sock.connect((self.host, self.__port))
            msg = bytes(self.__token + "@@@" + data +
                        '@@@' + self.__model, "utf-8")
            msg = struct.pack(">I", len(msg)) + msg
            sock.sendall(msg)

            with open('./files/reply.wav', 'wb') as f:
                while True:
                    l = sock.recv(8192)
                    if not l:
                        break
                    f.write(l)
            print("File received complete")

        except Exception as e:
            print(e)
        finally:
            sock.close()

    def set_language(self, language: str, gender: str, token="2022@course@tts@chinese"):
        '''
        Set port and token by language.
        Set model by gender.
        Params:
            language    :(str) chinese or taiwanese.
            gender      :(str) male or female. We don't have female in chinese.
        '''
        if language == 'chinese':
            self.__port = 10015
            self.__token = token
            self.__model = 'M60'

        elif language == 'taiwanese':
            self.__port = 10012
            self.__token = token

            if gender == 'male':
                self.__model = 'M12'
            elif gender == 'female':
                self.__model = 'F14'
            else:
                raise ValueError("'gender' param must be male or female")
        else:
            raise ValueError("'language' param must be taiwanese or chinese")
