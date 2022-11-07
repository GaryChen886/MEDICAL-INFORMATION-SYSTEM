import speech_recognition as sr

def chinese_recognize(wav_file):

    r = sr.Recognizer()
    with sr.WavFile(wav_file) as source:
        audio = r.record(source)

    try:
        result = r.recognize_google(audio, language='zh-tw')
        return result
    except LookupError:
        print("Could not understand audio:" , wav_file)
        return None
