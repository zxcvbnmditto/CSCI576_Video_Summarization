pusg

SAMPLE_PER_FRAME = 640
class AudioAnalyzer:
    def __init__(self, breaks, data):
        self.breaks = breaks
        self.data = data
        self.raw_data = self.data.raw_data

    def get_audio_score(self):
        """
        Get audio score for each shot
        return A list of integer represents score of each shot
        """
        weights = []
        prev_break = 0
        for break_ in self.breaks:
            if break_ == 0:
                continue
            score = sum(self.raw_data[prev_break*SAMPLE_PER_FRAME:break_*SAMPLE_PER_FRAME])
            weights.append(score//(break_ - prev_break + 1))

        return weights

