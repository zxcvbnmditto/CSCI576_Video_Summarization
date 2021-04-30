from pydub import AudioSegment  #pip install pydub
import numpy as np
import glob


class Frame:
    def __init__(self):
        self.bgr = None
        self.audio = None

    def __setattr__(self, name, value):
        self.__dict__[name] = value


class Dataloader:
    def __init__(self, video_path, audio_path, fps, width, height):
        self.vpath = video_path
        self.apath = audio_path
        self.fps = fps
        self.width = width
        self.height = height

        self.frame_count = len(glob.glob(self.vpath + "/*.rgb"))
        self.mask = [True] * self.frame_count

        # Audio
        self.audio = AudioSegment.from_file(self.apath)
        # self.duration = (self.frame_count / self.fps) * 1000 # ms
        # self.audio_sample_width = int(self.duration * int(self.audio.frame_rate / 1000) * self.audio.frame_width / self.frame_count)

        self.audio_sample_width = int(192000/30)

        # print(self.frame_count)
        # print(self.audio_sample_width)
        # print(self.audio.frame_width)
        # print(self.duration)

        # Loaded all in memory
        self.frames = []
        for i in range(self.frame_count):
            frame = Frame()
            frame.bgr = self._load_frame(i)
            frame.audio = self._load_audio(i)
            self.frames.append(frame)

    def _load_frame(self, i):
        path = f"{self.vpath}/frame{i}.rgb"
        with open(path, "rb") as f:
            red = np.frombuffer(f.read(self.width * self.height), dtype=np.uint8).reshape(self.height, self.width)
            green = np.frombuffer(f.read(self.width * self.height), dtype=np.uint8).reshape(self.height, self.width)
            blue = np.frombuffer(f.read(self.width * self.height), dtype=np.uint8).reshape(self.height, self.width)

        return np.dstack((blue, green, red))

    def _load_audio(self, i):
        return self.audio._data[i * self.audio_sample_width:
                                (i+1) * self.audio_sample_width]

    def load(self, i):
        # return (self._load_frame(i), self._load_audio(i))
        return self.frames[i]

    def summarize(self):
        self.frames = [d for d, mask in zip(self.frames, self.mask) if mask]

    def __iter__(self):
        return DataloaderIterator(self)


class DataloaderIterator:
    def __init__(self, data):
        self.data = data  # Reference to Dataloader
        self.index = 0

    def __next__(self):
        if self.index < len(self.data.frames):
            result = self.data.load(self.index)
            self.index += 1
            return result
        raise StopIteration
