import numpy as np

class AudioAnalyzer:
    def __init__(self, breaks, data):
        self.breaks = breaks
        self.data = data

    def get_audio_score_per_step(self, step):
        scores = []

        for i in range(self.data.frame_count):
            scores.append(int(sum(self.data.load(i).audio)))

        return np.array(scores)

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
