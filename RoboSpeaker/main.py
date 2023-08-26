# import os
#
# if __name__ == '__main__':
#     print("Welcome to RoboSpeaker")
#     x = input("What do you want to pronounce : ")
#     command = f"say {x}"
#     os.system(command)

import pyttsx3


def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


if __name__ == "__main__":

    while True:
        print("Welcome to RoboSpeaker")
        x = input("What do you want to pronounce : ")
        if x == "quit":
            break
        text_to_speech(x)
