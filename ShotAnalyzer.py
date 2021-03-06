import matplotlib.pyplot as plt
import cv2
import numpy as np

from MotionDetector import MotionDetector
from ShotsGenerator import ShotsGenerator
from FaceDetector import FaceDetector
from AudioDetector import AudioDetector

class ShotAnalyzer:
    def __init__(self, data, break_points=None):
        self.data = data
        self.score = []
        '''
            For every n frames, calculae the total score in that step.
        '''
        self.step = 5
        self.break_points = break_points

    def get_sum_per_shot(self, sum_per_step):
        '''
            Sum all the scores per shot.
        '''
        f = self.break_points[1:]
        sum_per_shot = [0] * (len(self.break_points)-1)

        total=0
        for i in range(len(sum_per_step)):
            if i*self.step > f[0]:
                sum_per_shot[-len(f)] = total
                total=0
                f.pop(0)
            total+= (sum_per_step[i] / (self.break_points[-len(f)] - self.break_points[-(len(f)+1)]))

        if total>0:
            sum_per_shot[-len(f)] = total
        return np.array(sum_per_shot)

    def get_normalization(self, scores):
        min_score = min(scores)
        max_score = max(scores)
        return (scores - min_score) / float(max_score-min_score)

    def length_filter(self, nor_sum_per_shot):
        total_frame = 90 * self.data.fps
        total = sum(nor_sum_per_shot)
        for i in range(len(nor_sum_per_shot)):
            f_num = nor_sum_per_shot[i]/total * total_frame
            if f_num < 25: nor_sum_per_shot[i] = 0

    def get_frame_per_shot(self, nor_sum_per_shot):
        total_frame = 90 * self.data.fps
        total = sum(nor_sum_per_shot)
        return np.round(nor_sum_per_shot / total * total_frame)

    def get_peak_frame(self, sum_per_step):
        peak = 0
        max_score = float("-inf")
        peak_frame = []
        queue = self.break_points[1:]
        for i in range(len(sum_per_step)):
            if i*self.step > queue[0]:
                queue.pop(0)
                peak_frame.append(peak)
                peak = i*self.step
                max_score = sum_per_step[i]
            elif sum_per_step[i] > max_score:
                peak = i*self.step
                max_score = sum_per_step[i]
        peak_frame.append(peak)
        return np.array(peak_frame)

    def extract_frames(self, peak_frame, frame_per_shot):
        res_mask = [False] * self.data.frame_count
        total_frame = 0
        for i in range(len(peak_frame)):
            peak = peak_frame[i]
            counter = 0
            left_p = 0
            right_p=0
            lower_bound = self.break_points[i]
            upper_bound = self.break_points[i+1]
            while frame_per_shot[i]>counter and total_frame <self.data.frame_count:
                if peak-left_p >= lower_bound and not res_mask[peak-left_p]:
                    res_mask[peak-left_p] = True
                    counter+=1
                if peak+right_p <= upper_bound and not res_mask[peak+right_p]:
                    res_mask[peak+right_p] = True
                    counter+=1
                left_p+=1
                right_p+=1
                if peak-left_p < lower_bound and peak+right_p > upper_bound:
                    extra = frame_per_shot[i] - counter
                    if i+1 < len(frame_per_shot):
                        for j in range(i+1, len(frame_per_shot)):
                            if frame_per_shot[j] > 0: frame_per_shot[j] += extra
                            break
                    break
            total_frame+=counter

        return res_mask

    def get_weights_info(self, sum_per_shot):
        prev_break = 0
        weights = []
        for i in range(1, len(self.break_points)):
            weights.append((sum_per_shot[i-1], self.break_points[i-1], self.break_points[i]))

        weights.sort(reverse=True)

        return weights

    def get_key_shots(self, weights):
        SUMMARIZED_SIZE = 90 * self.data.fps
        cur_len = 0
        final_weight = []
        for s in weights:
            _, start, end = s
            if cur_len < SUMMARIZED_SIZE:
                cur_len += end - start
                final_weight.append(s)
        return final_weight

    def get_new_mask(self, final_weight):
        new_mask = [False] * self.data.frame_count
        final_weight.sort(key=lambda x: x[1])
        for i in range(len(final_weight)):
            _, start, end = final_weight[i]
            for j in range(start, end):
                new_mask[j] = True
        return new_mask

    def extract_frames_sub_shot(self, score_per_shot, sum_per_step):
        '''
            Filter: if the score is too low in one shot, skip it.
        '''
        self.length_filter(score_per_shot)

        '''
            Get num of frame per shot
        '''
        frame_per_shot = self.get_frame_per_shot(score_per_shot)
        print('frames/shot:', list(frame_per_shot))

        '''
            Find the peak in every shot
        '''
        peak_frame = self.get_peak_frame(sum_per_step)
        print('peak_frame', list(peak_frame))

        print(len(self.break_points), len(frame_per_shot), len(peak_frame), sum(frame_per_shot))
        '''
            Extract the frames around the peak frame
        '''
        return self.extract_frames(peak_frame, frame_per_shot)

    def extract_frames_full_shot(self, sum_per_shot):
        weights = self.get_weights_info(sum_per_shot)

        # Take only needed amounts of shots based on weights
        final_weight = self.get_key_shots(weights)

        # Make mask based shots intervals on hand
        return self.get_new_mask(final_weight)

    def run(self):
        '''
            Find the video break points
        '''
        if self.break_points==None:
            self.break_points = ShotsGenerator(self.data, 25).get_break_points()
            print('Finished shot seperation ----------')

        '''
            Get motion scores for every step.
            Please make sure that every score array have the same size.
        '''
        start = 0
        end = self.data.frame_count

        motion_detector = MotionDetector(self.data, self.step, 15)
        motion_score = motion_detector.get_motion_score_per_step(start, end)
        nor_motion_score = self.get_normalization(motion_score)

        face_detector = FaceDetector(self.data, self.step)
        face_score = face_detector.get_face_score_per_step()
        nor_face_score = self.get_normalization(face_score)

        audio_detector = AudioDetector(self.data, self.step)
        audio_score = audio_detector.get_audio_score_per_step()
        nor_audio_score = self.get_normalization(audio_score)

        print('length check:', len(nor_motion_score), len(nor_face_score), len(nor_audio_score))
        '''
            score_per_step collect all kinds of score and give each feature a weight
        '''
        score_per_step = [nor_motion_score*1., nor_face_score*0.05, nor_audio_score * np.mean(nor_motion_score) / np.mean(nor_audio_score)]
        sum_per_step = [sum(x) for x in zip(*score_per_step)]

        '''
            Sum all the scores in one shot
        '''
        score_per_shot = self.get_sum_per_shot(sum_per_step)
        print('sum_per_shot: ', list(score_per_shot))

        self.data.mask = self.extract_frames_sub_shot(score_per_shot, sum_per_step)
