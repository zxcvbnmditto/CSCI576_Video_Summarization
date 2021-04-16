import cv2, time, os
import wave, pyaudio, math
import matplotlib.pyplot as plt
import numpy as np

video_fps = 30
audio_data_offset_per_frame=int(192000/video_fps)
width = 320
height = 180

def reorderRGBSeq(frames):
    res  = []
    for bytes in frames:
        image = np.empty((height, width, 3))
        imgSize = width*height
        for h in range(height):
            for w in range(width):
                # t = (bytes[h*width+w]/255.0, bytes[h*width+w+imgSize]/255.0, bytes[h*width+w+imgSize*2]/255.0)
                #bgr
                t = (bytes[h*width+w+imgSize*2]/255.0, bytes[h*width+w+imgSize]/255.0, bytes[h*width+w]/255.0)
                image[h, w, :] =t
        res += [image]
        print(len(res))
    return res

def readBytes(path):
    f = open(path, "rb")
    bytes = f.read(width*height*3)
    f.close()
    return bytes

def getFrames(path):
    frames = []
    i=0
    while True:
        fPath = path+str(i)+'.rgb'
        if not os.path.isfile(fPath):
            break;
        frames += [readBytes(fPath)]
        i+=1
    return frames

def playVideo(frames, stream, audioData):
    # for frame in frames:
    for i in range(len(frames)):
        frame = frames[i]
        cv2.imshow('frame', frame)

        # plt.imshow(frame)
        # plt.show(block=False)
        # plt.pause(0.00001)
        stream.write(audioData[i*audio_data_offset_per_frame:(i+1)*audio_data_offset_per_frame])
        # plt.close()
        key = cv2.waitKey(1) #30 fps
        if key == 27:
            print('Pressed Esc')
            break
    cv2.destroyAllWindows()

def getAudio(p, path, f_num):
    wf = wave.open(audio_path)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    sec = math.ceil(f_num / video_fps)
    data = wf.readframes(wf.getframerate() * sec)
    wf.close()
    return data, stream

def playAudio(audio):
    t= threading.Thread(target=play, args=(audio, ))
    t.start()

if __name__ == '__main__':
    audio_path = 'project_dataset/audio/meridian.wav'
    frame_path = 'project_dataset/frames_rgb/meridian/frame'
    #get fraames
    frames = getFrames(frame_path)
    clipped_frames  = reorderRGBSeq(frames[:240])
    #get audio
    p = pyaudio.PyAudio()
    audioData, stream = getAudio(p, audio_path, len(frames))

    # extract last few second
    # frames  = reorderRGBSeq(frames[-120:])
    # audioData = audioData[-(120*audio_data_offset_per_frame):]

    playVideo(clipped_frames, stream, audioData)

    stream.stop_stream()
    stream.close()
    p.terminate()
