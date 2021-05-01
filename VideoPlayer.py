import pyaudio
import cv2

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import PIL.Image, PIL.ImageTk
import threading

class VideoPlayer:
    def __init__(self, data, window):
        self.data = data

        self.window = window
        self.window.title('Control Center')
        self.window.configure(pady=5)
        self.window.overrideredirect(True)

        # Pause/Play Button
        self.pause = False
        self.btn_pause=ttk.Button(self.window, text='Pause/Play' , width=15, command=self.pause_video)
        self.btn_pause.pack(side=LEFT)

        # Resume Button
        self.index = 0
        self.btn_resume=ttk.Button(self.window, text="Resume", width=15, command=self.resume_video)
        self.btn_resume.pack(side=LEFT)

        self.offset = 5*self.data.fps
        # Forward Button
        self.btn_forward=ttk.Button(self.window, text="Forward", width=15, command=self.forward)
        self.btn_forward.pack(side=LEFT)

        # Backward Button
        self.btn_backward=ttk.Button(self.window, text="Backward", width=15, command=self.backward)
        self.btn_backward.pack(side=LEFT)

        # Control position
        w = self.window.winfo_reqwidth()
        h = self.window.winfo_reqheight()
        ws = self.window.winfo_screenwidth()
        hs = self.window.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.window.geometry('+%d+%d' % (x, y))

        # cv2 window position
        cv2.namedWindow('film')
        cv2.moveWindow('film', int(x), int(y-self.data.height/2))

    def pause_video(self):
        self.pause = not self.pause

    def resume_video(self):
        self.index = 0

    def forward(self):
        if self.index+self.offset<len(self.data.frames):
            self.index+=self.offset

    def backward(self):
        if self.index-self.offset>0:
            self.index-=self.offset

    def play(self):
        print("Play ---")

        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(self.data.audio.sample_width),
                        channels=self.data.audio.channels,
                        rate=self.data.audio.frame_rate,
                        output=True)

        self.index = 0
        while self.index<len(self.data.frames):
            if not self.pause:
                d = self.data.load(self.index)
                cv2.imshow('film', d.bgr)
                stream.write(d.audio) # Sequencial

                key = cv2.waitKey(1)
                if key == 27:
                    print('Pressed ESC')
                    break
                self.index+=1
            self.window.update()

        # Stop Stream
        stream.stop_stream()
        stream.close()

        # Close PyAudio
        p.terminate()

        # Close Image
        cv2.destroyAllWindows()
