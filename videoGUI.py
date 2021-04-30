from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import PIL.Image, PIL.ImageTk
import cv2
import pygame

FRAME_STEP = 3   # play this number of frames then play sounds
AUDIO_FRAME_RATE = 10  # each time sound playing duration, unit is 1/1000 seconds

class videoGUI:

    def __init__(self, window, window_title):

        self.window = window
        self.window.title(window_title)

        top_frame = Frame(self.window)
        top_frame.pack(side=TOP, pady=5)

        bottom_frame = Frame(self.window)
        bottom_frame.pack(side=BOTTOM, pady=5)

        self.pause = False   # Parameter that controls pause button

        self.begun = False
        self.past_frame_cnt = 0

        self.canvas = Canvas(top_frame)
        self.canvas.pack()

        # Select Button
        self.btn_select=Button(bottom_frame, text="Select video file", width=15, command=self.open_file)
        self.btn_select.grid(row=0, column=0)

        # Play Button
        self.btn_play=Button(bottom_frame, text="Play", width=15, command=self.play_video)
        # self.btn_play=Button(bottom_frame, text="Play", width=15, command=self.combine_funcs(self.play_video, self.play_audio))
        self.btn_play.grid(row=0, column=1)

        # Pause Button
        self.btn_pause=Button(bottom_frame, text="Pause", width=15, command=self.pause_video)
        self.btn_pause.grid(row=0, column=2)

        # Resume Button
        self.btn_resume=Button(bottom_frame, text="resume", width=15, command=self.resume_video)
        self.btn_resume.grid(row=0, column=3)

        self.delay = 15   # ms

        self.window.mainloop()

        self.audio_file = r'audio.mp3'




    def open_file(self):

        self.pause = False

        self.filename = filedialog.askopenfilename(title="Select file", filetypes=(("MP4 files", "*.mp4"),
                                                                                         ("WMV files", "*.wmv"), ("AVI files", "*.avi")))
        print(self.filename)

        # Open the video file
        self.cap = cv2.VideoCapture(self.filename)

        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        self.canvas.config(width = self.width, height = self.height)


    def get_frame(self):   # get only one frame
        try:
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        except:
            messagebox.showerror(title='Video file not found', message='Please select a video file.')


    def play_video(self):
        # Get a frame from the video source, and go to the next frame automatically
        ret, frame = self.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = NW)

        if not self.pause:
            if not self.begun:
                self.begun = True
                pygame.init()
                pygame.mixer.init()
                # pygame.display.set_mode((200, 100))
                pygame.mixer.music.load('audio.mp3')
                pygame.mixer.music.play()
            else:
                if self.past_frame_cnt > FRAME_STEP:
                    self.past_frame_cnt = 0
                    pygame.mixer.music.unpause()
                else:
                    self.past_frame_cnt += 1
            music_played = 0
            while pygame.mixer.music.get_busy() and not music_played:
                pygame.time.Clock().tick(AUDIO_FRAME_RATE)
                music_played = 1
            pygame.mixer.music.pause()
            self.window.after(self.delay, self.play_video)


    def pause_video(self):
        self.pause = True
        pygame.mixer.music.pause()

    #Addition
    def resume_video(self):
        self.pause = False
        self.play_video()


    # Release the video source when the object is destroyed
    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()

