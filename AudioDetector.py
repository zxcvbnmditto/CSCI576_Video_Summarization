import numpy as np
import math

class AudioDetector:
    def __init__(self, data, step):
        self.data = data
        self.step = step

    def get_audio_score_per_step(self):
        audio_scores = []
        audio_diff_scores = []
        offset = self.step // 2
        for i in range(offset, self.data.frame_count, self.step):
            step_score = []
            for j in range(-(self.step // 2), math.ceil(self.step / 2), 1):
                if i + j >= self.data.frame_count:
                    break
                audio = np.fromstring(self.data.load(i + j).audio, np.int16)
                score = np.mean(np.absolute(audio)) / 2.0
                step_score.append(score)
            mean_step_score = np.mean(np.array(step_score))
            if mean_step_score > 0:
                step_score = np.log10(mean_step_score)
            else:
                step_score = 0.0
            audio_scores.append(abs(step_score))

            if len(audio_scores) > 1:
                audio_diff_scores.append(abs(audio_scores[-2] - audio_scores[-1]))
            else:
                audio_diff_scores.append(0)

        # Plot
        # self.plot(audio_scores)
        # self.plot(audio_diff_scores)
        return np.array(audio_diff_scores)

    def plot(self, score):
        import matplotlib.pyplot as plt
        plt.plot(score)
        plt.show()
