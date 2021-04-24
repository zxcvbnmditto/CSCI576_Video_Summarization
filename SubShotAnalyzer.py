import matplotlib.pyplot as plt
import cv2
import numpy as np

from MotionDetector import MotionDetector
from ShotsGenerator import ShotsGenerator
from FaceDetector import FaceDetector

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
        break_points = ShotsGenerator(self.data, 20).get_break_points()
        print('Finished shot seperation ----------')

        '''
            Get motion scores for every step.
            Please make sure that every score array have the same size.
        '''
        start = 0
        end = self.data.frame_count

        motion_detector =  MotionDetector(self.data, self.step, 15)
        motion_score = motion_detector.get_motion_score_per_step(start, end)
        nor_motion_score = self.get_normalization(motion_score)

        faceDetector = FaceDetector(self.data, self.step)
        face_score = faceDetector.get_face_score_per_step()
        nor_face_score = self.get_normalization(face_score)

        '''
            score_per_step collect all kinds of score and give each feature a weight
        '''
        score_per_step = [nor_motion_score * 0.6, nor_face_score*0.4]
        sum_per_step = [sum(x) for x in zip(*score_per_step)]

        '''
            Sum all the score in one shot
        '''
        score_per_shot = self.get_sum_per_shot(sum_per_step, break_points)
        nor_sum_per_shot = self.get_normalization(score_per_shot)

        print('sum_per_shot: ', list(nor_sum_per_shot))
        '''
            Get num of frame per shot
        '''
        frame_per_shot = self.get_frame_per_shot(nor_sum_per_shot)
        print('frames/shot:', list(frame_per_shot))

        '''
            Find the peak in every shot
        '''
        peak_frame = self.get_peak_frame(sum_per_step, break_points)
        print('peak_frame', list(peak_frame))

        '''
            Extract the frames around the peak frame
        '''

        extracted_frames = self.extract_frames(peak_frame, frame_per_shot)

        '''
            Modify self.data.mask
        '''
        self.data.mask = extracted_frames