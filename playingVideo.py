import cv2, time
import matplotlib.pyplot as plt
from pydub import AudioSegment #pip install pydub
from pydub.playback import play

import threading

def playVideo(path):
    i = 1
    while True:
        frame = cv2.imread(path+str(i)+'.jpg')
        if frame.size == 0:
            print('Reached the end of the video')
            break

        cv2.imshow('frame', frame)

        key = cv2.waitKey(32) #30 fps
        i+=1
        if key == 27:
            print('Pressed Esc')
            break
    cv2.destroyAllWindows()

def playSound(path):
    audio = AudioSegment.from_wav(path)
    import pdb; pdb.set_trace()
    t= threading.Thread(target=play, args=(audio, ))
    time.sleep(0.05)
    t.start()

if __name__ == '__main__':

    playSound('project_dataset/audio/meridian.wav')

    path = 'project_dataset/frames/meridian/frame'
    playVideo(path)