import numpy as np
from ShotsGenerator import *
from AudioAnalyzer import *
SUMMARIZED_SIZE = 1620
class AlgorithmDemo:
    def __init__(self, data):
        self.data = data
        self.score = []

    def run(self):
        '''
        First get the shots interval. Then evaluate each shot and give it a weight use audio and motion analyzer.
        Calculate each shot's total weight and form a tuple (weight, start, end).
        Sort the list of shots weight tuples in reverse order. Take top 10% portion of the tuples from list. Then
        sort them based on start index. Generate mask based on the tuple.
        :return:
        '''
        print("Running AlgorithmDemo")
        # Get shots
        sg = ShotsGenerator(self.data, 20)
        breaks = sg.get_break_points()

        # Get audio weights
        aa = AudioAnalyzer(breaks, self.data)
        audio_weights = aa.get_audio_score()

        # TODO
        # ma = MotionAnalyzer(breaks, self.data)   #Get video weights.
        # video_weights = ma.get_video_score()
        # Add total video and audio score to total weights.
        prev_break = 0
        weights = []
        for break_ in breaks:
            if break_ == 0:
                continue
            start = prev_break
            end = break_
            prev_break = break_
            total_weight = audio_weights.pop(0)
            weights.append((total_weight, start, end))

        weights.sort(reverse=True)
        print(weights)
        final_weight = []


        # Take only needed amounts of shots based on weights
        cur_len = 0
        for s in weights:
            _, start, end = s
            if cur_len < SUMMARIZED_SIZE:
                cur_len += end - start
                final_weight.append(s)

        # Make mask based shots intervals on hand
        final_weight.sort(key=lambda x: x[1])
        for i in range(len(final_weight)):
            _, start, end = final_weight[i]
            for j in range(start, end):
                self.data.mask[j] = True
        return
