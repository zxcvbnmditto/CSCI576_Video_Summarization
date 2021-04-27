import matplotlib.pyplot as plt
import cv2
import numpy as np

from MotionDetector import MotionDetector
from ShotsGenerator import ShotsGenerator
from FaceDetector import FaceDetector
from AudioAnalyzer import AudioAnalyzer

class FullShotAnalyzer:
    def __init__(self, data):
        self.data = data
        self.score = []
        '''
            For every n frames, calculae the total score in that step.
        '''
        self.step = 5

    def get_normalization(self, scores):
        min_score = min(scores)
        max_score = max(scores)
        return (scores - min_score) / float(max_score-min_score)

    def get_weights_info(self, break_points, sum_per_shot):
        prev_break = 0
        weights = []
        for i in range(1, len(break_points)):
            weights.append((sum_per_shot[i-1], break_points[i-1], break_points[i]))

        weights.sort(reverse=True)

        return weights

    def run(self):
        '''
            Find the video break points
        '''
        # break_points = ShotsGenerator(self.data, 20).get_break_points()
        break_points = [0, 481, 1381, 1567, 2338, 2530, 3145, 3652, 3805, 5059, 5209, 5554, 5707, 6139, 6304, 7150, 7438, 7741, 8041, 8617, 8857, 9013, 9271,
 9499, 9772, 9931, 10177, 10588, 10738, 10888, 11038, 11209, 11359, 11557, 11725, 11953, 12103, 12370, 12736, 12973, 13396, 13639, 13789, 14335, 14551, 15073, 15367, 16153, 16200]
        print('Finished shot seperation ----------')

        '''
            Get motion scores for every shot.
        '''
        start = 0
        end = self.data.frame_count

        motion_detector =  MotionDetector(self.data, self.step, 15)
        motion_score = motion_detector.get_motion_score_per_shot(break_points, start, end)
        nor_motion_score = self.get_normalization(motion_score)

        faceDetector = FaceDetector(self.data, self.step)
        face_score = faceDetector.get_face_score_per_shot(break_points)
        nor_face_score = self.get_normalization(face_score)

        audio_analyzer = AudioAnalyzer(break_points, self.data)
        audio_score = audio_analyzer.get_audio_score_per_shot()
        nor_audio_score = self.get_normalization(audio_score)

        print(len(nor_motion_score), len(face_score), len(audio_score))
        '''
            score_per_step collect all kinds of score and give each feature a weight
        '''
        score_per_shot = [nor_motion_score*0.5, nor_audio_score * 0.2, nor_face_score*0.3]
        sum_per_shot = [sum(x) for x in zip(*score_per_shot)]

        print(sum_per_shot)

        weights = self.get_weights_info(break_points, sum_per_shot)

        # Take only needed amounts of shots based on weights
        SUMMARIZED_SIZE = 90 * self.data.fps
        cur_len = 0
        final_weight = []
        for s in weights:
            _, start, end = s
            if cur_len < SUMMARIZED_SIZE:
                cur_len += end - start
                final_weight.append(s)

        # Make mask based shots intervals on hand
        new_mask = [False] * self.data.frame_count
        final_weight.sort(key=lambda x: x[1])
        for i in range(len(final_weight)):
            _, start, end = final_weight[i]
            for j in range(start, end):
                new_mask[j] = True

        self.data.mask  = new_mask
