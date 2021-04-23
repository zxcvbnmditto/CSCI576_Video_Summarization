class AudioAnalyzer:
    def __init__(self, breaks, audio_data):
        self.breaks = breaks
        self.audio_data= audio_data
    
    def get_audio_score(self):
        """
        return each shots a score
        """
        audio_score = []
        prev_break = 0
        for break_ in self.breaks:
            if break_ == 0:
                continue
            shot_score = self._get_score(prev_break, break_)
            audio_score.append(shot_score)

        return audio_score

    def _get_score(self, start: int, end: int) -> int:
        """
        :param start: start index of a short
        :param end: end index of a shot
        :return score
        """
        print(self.audio_data)
        print(type(self.audio_data))
        print(type(self.audio_data[0]))
        return 0
