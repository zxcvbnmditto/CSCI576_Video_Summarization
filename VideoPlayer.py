import pyaudio
import cv2
import threading


class VideoPlayer:
    def __init__(self, data):
        self.data = data

    def play(self):
        print("Play ---")

        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(self.data.audio.sample_width),
                        channels=self.data.audio.channels,
                        rate=self.data.audio.frame_rate,
                        output=True)

        for i, d in enumerate(self.data):
            cv2.imshow('frame', d.bgr)
            stream.write(d.audio) # Sequencial
            key = cv2.waitKey(1)
            if key == 27:
                print('Pressed ESC')
                break

        # Stop Stream
        stream.stop_stream()
        stream.close()

        # Close PyAudio
        p.terminate()

        # Close Image
        cv2.destroyAllWindows()
