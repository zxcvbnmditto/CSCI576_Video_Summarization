import matplotlib.pyplot as plt
import cv2

from MotionDetector import MotionDetector
from ShotsGenerator import ShotsGenerator

class CompoundAnalyzer:
    def __init__(self, data):
        self.data = data
        self.score = []
        '''
            For every n frames, calculae the total score in that step.
        '''
        self.step = 5

    def get_sum_per_step(self, scores, break_points):
        f = break_points[1:]
        sum_per_step = [0] * (len(break_points)-1)
        sum=0
        for i in range(len(scores)):
            if (i+1)*self.step > f[0]:
                sum_per_step[-len(f)] = sum
                sum=0
                f.pop(0)
            sum+=scores[i]
        if sum>0:
            sum_per_step[-len(f)] = sum
        return sum_per_step


    def run(self):
        '''
            Find the video break points
        '''
        # print('start shot seperation --------')
        # break_points = ShotsGenerator(self.data, 20).get_break_points()
        # print('Finished ----------')
        # print(break_points)
        break_points = [0, 55, 205, 355, 532, 4237, 5269, 5581, 6970, 7144, 7294, 7450, 7600, 7753, 7903, 8083, 10534, 10696, 10927, 11101, 11254, 11503, 11653, 11845, 11998, 12175, 12787, 12949, 13789, 14020, 14311, 14899, 15127, 15349, 15577, 16200]

        # for b in break_points:
        #     cv2.imshow('break', self.data.load(b).bgr)
        #     cv2.waitKey(0)
        '''
            Get motion scores for every step.
        '''
        motion_detector =  MotionDetector(self.data)
        motion_score = motion_detector.get_motion_score(0, len(self.data.frames), self.step, 15)

        '''
            Sum all the scores per shot.
        '''

        sum_per_step = self.get_sum_per_step(motion_score, break_points)
        print(sum_per_step, len(sum_per_step))

        '''
            Normalization
        '''

        '''
            Get num of frame per shot
        '''

        '''
            Extract frames in shots
        '''

        '''
            Modify self.data.mask
        '''
