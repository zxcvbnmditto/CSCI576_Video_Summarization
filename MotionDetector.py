import cv2
import numpy as np

class MotionDetector:
    def __init__(self, data, step, threshold):
        self.data = data
        self.step =step
        self.threshold =threshold

    def get_motion_score_per_shot(self, break_points, start, end, avg=True):
        '''
            When avg is true, return nums of faces per frame
        '''
        motion_score = self.get_motion_score_per_step(start, end)
        queue = break_points[1:]
        motion_per_shot = [0]*(len(break_points)-1)
        total=0
        for i in range(len(motion_score)):
            if start+(i+1)*self.step > queue[0]:
                motion_per_shot[-len(queue)] = float(total) if not avg else float(total)/(break_points[-len(queue)] - break_points[-(len(queue)+1)])
                total=0
                queue.pop(0)
            total+=motion_score[i]
        if total>0: motion_per_shot[-len(queue)] = float(total)
        # print(motion_per_shot, len(motion_per_shot))
        return motion_per_shot


    def get_motion_score_per_step(self, start, end):
        last_frame = None
        motion_score = []

        for i in range(int((end-start)/self.step)):
            frame = self.data.load(start + self.step*i).bgr

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            if last_frame is None:
                last_frame = gray
                continue

            frame_delta = cv2.absdiff(last_frame, gray)

            thresh = cv2.threshold(frame_delta, self.threshold, 255, cv2.THRESH_BINARY)[1]

            thresh = cv2.dilate(thresh, None, iterations=1)

            last_frame = gray

            total = sum(list(map(sum, thresh))) / 255

            motion_score.append(total)

        return np.array(motion_score)

    def show(self, frame, thresh):
        cv2.imshow('frame', frame)
        cv2.imshow('thresh', thresh)
        cv2.waitKey(0)
