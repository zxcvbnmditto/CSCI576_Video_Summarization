"""
This class write an audio file
named 'audio.mp3' and a video file
named 'output.mp4'.
"""
import cv2
import yaml
import moviepy.editor as mpe
from pydub import AudioSegment

class VideoWriter:
    def __init__(self, data):
        self.data = data
        self.write_video()
        self.write_audio()
        self.composite()

    def write_video(self):
        """
        write video output.mp4 to current path.
        :return: None
        """
        # Define the codec and create VideoWriter object
        with open("config.yaml") as f:
            config = yaml.safe_load(f)

        out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'MP4V'), config['fps'],
                              (config['width'], config['height']))

        for d in self.data:
            frame = d.bgr
            out.write(frame)

        # Release everything if job is finished
        out.release()
        cv2.destroyAllWindows()

    def write_audio(self):
        """
        Write audio.mp3 file to current path.
        :return: None
        """
        b_str = b''  # concatenate bytes to a single bytes string for file writing purpose
        for d in self.data:
            b_str += d.audio

        AudioSegment(b_str, sample_width=self.data.audio.sample_width, frame_rate=self.data.audio.frame_rate, channels=self.data.audio.channels).export('audio.wav', format='wav')
        return

    def composite(self):
        """
        Try to composite audio file with video file.
        Composite did not work properly.
        :return:
        """
        videoclip = mpe.VideoFileClip("output.mp4")
        audioclip = mpe.AudioFileClip("audio.wav")

        composite_video = videoclip.set_audio(audioclip)
        composite_video.write_videofile("summarized_video.mp4")




