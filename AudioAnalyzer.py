import numpy as np
import math

class AudioAnalyzer:
    def __init__(self, breaks, data):
        self.breaks = breaks
        self.data = data

    def get_audio_score_per_step(self, step):
        audio_scores = []
        audio_diff_scores = []
        offset = step // 2
        for i in range(offset, self.data.frame_count, step):
            step_score = []
            for j in range(-(step // 2), math.ceil(step / 2), 1):
                if i + j >= self.data.frame_count:
                    break
                audio = np.fromstring(self.data.load(i + j).audio, np.int16)
                score = np.mean(np.absolute(audio)) / 2.0
                step_score.append(score)
            step_score = np.mean(np.array(step_score))
            audio_scores.append(abs(step_score))

            if len(audio_scores) > 1:
                audio_diff_scores.append(abs(audio_scores[-2] - audio_scores[-1]))
            else:
                audio_diff_scores.append(0)
        return np.array(audio_diff_scores)

    def get_audio_score_per_shot(self):
        """
        Get audio score for each shot
        return A list of integer represents score of each shot
        """
        weights = []
        break_points = self.breaks[1:]
        score = 0
        for i in range(self.data.frame_count):
            if len(break_points) > 0 and i > break_points[0]:
                weights.append(score)
                score=0
                break_points.pop(0)
                continue
            score += int(sum(self.data.load(i).audio))
        if score>0: weights.append(score)

        return np.array(weights)
