import numpy as np
import math

class AudioDetector:
    def __init__(self, breaks, data, step):
        self.break_points = breaks
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
        audio_diff_scores = self.get_audio_score_per_step()
        f = self.break_points[1:]
        sum_per_shot = [0] * (len(self.break_points)-1)

        total=0
        for i in range(len(audio_diff_scores)):
            if i*self.step > f[0]:
                sum_per_shot[-len(f)] = total
                total=0
                f.pop(0)
            total+=audio_diff_scores[i]

        if total>0:
            sum_per_shot[-len(f)] = total
        return np.array(sum_per_shot)
