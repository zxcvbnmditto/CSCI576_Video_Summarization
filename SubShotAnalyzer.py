import matplotlib.pyplot as plt
import cv2
import numpy as np

from MotionDetector import MotionDetector
from ShotsGenerator import ShotsGenerator

class SubShotAnalyzer:
    def __init__(self, data):
        self.data = data
        self.score = []
        '''
            For every n frames, calculae the total score in that step.
        '''
        self.step = 5

    def get_sum_per_shot(self, sum_per_step, break_points):
        '''
            Sum all the scores per shot.
        '''
        f = break_points[1:]
        sum_per_shot = [0] * (len(break_points)-1)
        # if len(scores) < 1: return sum_per_shot
        #
        # sum_per_step = [sum(x) for x in zip(*scores)]
        total=0
        for i in range(len(sum_per_step)):
            if (i+1)*self.step > f[0]:
                sum_per_shot[-len(f)] = total
                total=0
                f.pop(0)
            total+=sum_per_step[i]

        if total>0:
            sum_per_shot[-len(f)] = total
        return np.array(sum_per_shot)

    def get_normalization(self, scores):
        min_score = min(scores)
        max_score = max(scores)
        return (scores - min_score) / float(max_score-min_score)

    def get_frame_per_shot(self, nor_sum_per_shot):
        total_frame = 90 * self.data.fps
        total = sum(nor_sum_per_shot)
        return np.round(nor_sum_per_shot / total * total_frame)

    def get_peak_frame(self, sum_per_step, break_points):
        peak = 0
        max_score = 0
        peak_frame = []
        queue = break_points[1:]
        for i in range(len(sum_per_step)):
            if i*self.step > queue[0]:
                queue.pop(0)
                peak_frame.append(peak)
                peak = i*self.step
                max_score = sum_per_step[i]
            elif sum_per_step[i] > max_score:
                peak = i*self.step
                max_score = sum_per_step[i]
        return np.array(peak_frame)

    def extract_frames(self, peak_frame, frame_per_shot):
        res_mask = [False] * self.data.frame_count
        total_frame = 0
        for i in range(len(peak_frame)):
            peak = peak_frame[i]
            counter = 0
            left_p = 0
            right_p=0
            while frame_per_shot[i]>counter and total_frame <self.data.frame_count:
                if peak-left_p >= 0 and not res_mask[peak-left_p]:
                    res_mask[peak-left_p] = True
                    counter+=1
                if peak+right_p < self.data.frame_count and not res_mask[peak+right_p]:
                    res_mask[peak+right_p] = True
                    counter+=1
                left_p+=1
                right_p+=1
            total_frame+=counter

        return res_mask

    def run(self):
        '''
            Find the video break points
        '''
        # print('start shot seperation --------')
        # break_points = ShotsGenerator(self.data, 20).get_break_points()
        # print('Finished ----------')
        # print(break_points)
        # break_points = [0, 55, 205, 355, 532, 4237, 5269, 5581, 6970, 7144, 7294, 7450, 7600, 7753, 7903, 8083, 10534, 10696, 10927, 11101, 11254, 11503, 11653, 11845, 11998, 12175, 12787, 12949, 13789, 14020, 14311, 14899, 15127, 15349, 15577, 16200]

        # for b in break_points:
        #     cv2.imshow('break', self.data.load(b).bgr)
        #     cv2.waitKey(0)
        '''
            Get motion scores for every step.
            Please make sure that every score array have the same size.
        '''
        # motion_detector =  MotionDetector(self.data)
        # motion_score = motion_detector.get_motion_score(0, self.data.frame_count, self.step, 15)
        # nor_motion_score = self.get_normalization(motion_score)

        '''
            scores array collect all kinds of score and give each feature a weight
        '''
        # score_per_step = [nor_motion_score * 1]
        # sum_per_step = [sum(x) for x in zip(*score_per_step)]
        #
        # score_per_shot = self.get_sum_per_shot(sum_per_step, break_points)
        #
        # nor_sum_per_shot = self.get_normalization(score_per_shot)
        #
        # print(nor_sum_per_shot)


        '''
            Get num of frame per shot
        '''
        # frame_per_shot = self.get_frame_per_shot(nor_sum_per_shot)
        # print(frame_per_shot)

        '''
            Find the peak in every shot
        '''
        # peak_frame = self.get_peak_frame(sum_per_step, break_points)
        # print(peak_frame)
        '''
            Extract the frames around the peak frame
        '''
# meridian
        frame_per_shot = [ 17.,  80., 112.,  86., 515.,  76.,  21., 124.,  68., 116.,  88.,  53., 119., 113.,
                    92., 290.,   9.,  97.,  59.,  38.,  11.,  17.,  42.,  40.,  28.,  35.,   8.,  42.,
                    32.,  39., 102.,  12.,   0.,   5., 114.,]
        peak_frame = [30,155,275,525,890,  4970,  5575,  5735,  7105,  7170,  7340,  7595,
  7680,  7800,  7975,  8160, 10535, 10915, 10970, 11215, 11300, 11635, 11845, 11870,
 12040, 12455, 12795, 13135, 14015, 14090, 14895, 15120, 15345, 15575]

 # soccer
 #        frame_per_shot = [ 17.,   9.,   6.,  26.,  68.,  43.,  33., 128., 195., 125.,  68.,  46.,  29.,  72.,
 #  25.,   8.,   5.,   6.,  10.,  29., 149.,  62.,  37.,  41., 102.,  18., 109.,  75.,
 # 115., 139.,  83.,  97.,  92.,   9.,  18.,  27.,  82.,  39.,  32., 121.,  94.,  49.,
 #  89.,  18.,  44.,   4.,   8.,   0.]
 #        peak_frame = [  315,   705,  1545,  2330,  2480,  2630,  3645,  3795,  3975,  5105,  5255,  5705,
 #  5715,  6230,  6305,  7245,  7740,  8040,  8610,  8850,  8970,  9060,  9405,  9760,
 #  9870, 10170, 10255, 10710, 10785, 11015, 11205, 11260, 11485, 11720, 11925, 12100,
 # 12105, 12735, 12960, 13040, 13630, 13785, 13860, 14545, 14575, 15365, 15855]

        extracted_frames = self.extract_frames(peak_frame, frame_per_shot)

        '''
            Modify self.data.mask
        '''
        self.data.mask = extracted_frames
