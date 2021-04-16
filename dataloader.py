import numpy as np
import glob
from pydub import AudioSegment #pip install pydub


class Dataloader:
    def __init__(self, video_path, audio_path, fps, width, height):
        self.vpath = video_path
        self.apath = audio_path
        self.fps = fps
        self.width = width
        self.height = height

        # Image
        self.frame_count = len(glob.glob(self.vpath + "/*.rgb"))

        # Audio
        self.audio = AudioSegment.from_file(self.apath)
        self.duration = (self.frame_count / self.fps) * 1000  # ms
        self.audio_sample_width = int(self.audio.frame_rate / 1000) * self.audio.frame_width

    def _load_frame(self, i):
        path = f"{self.vpath}/frame{i}.rgb"
        with open(path, "rb") as f:
            raw = f.read(self.width * self.height * 3)
        return np.frombuffer(raw, dtype=np.uint8).reshape(self.height, self.width, 3)

    def _load_audio(self, i):
        return self.audio._data[i * self.audio_sample_width: (i+1) * self.audio_sample_width]

    def load(self, i):
        return (self._load_frame(i), self._load_audio(i))

    def __iter__(self):
        return DataloaderIterator(self)


class DataloaderIterator:
    def __init__(self, data):
        self.data = data  # Reference to Dataloader
        self.index = 0

    def __next__(self):
        if self.index < self.data.frame_count:
            result = self.data.load(self.index)
            self.index += 1
            return result
        raise StopIteration
