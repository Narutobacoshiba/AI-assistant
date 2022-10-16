import speech_recognition as sr
from understand import Handle

"""
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

Microphone(device_index=3)
"""

ai_ear = sr.Recognizer()
hd = Handle()

while True:
    with sr.Microphone() as mic:
        ai_ear.adjust_for_ambient_noise(mic)
        print("listenning.")
        audio = ai_ear.listen(mic)
    print(".....")
    try:
        text = ai_ear.recognize_google(audio,language="vi-VN").lower()
        print("command: "+text)
        hd.handle(text)
    except:
        pass

