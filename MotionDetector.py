import cv2
import matplotlib.pyplot as plt

class MotionDetector:
    def __init__(self, data):
        self.data = data
        self.score = []

    def run(self):
        start = 0
        end = 6000
        step = 5
        test_frames = []
        for i in range(int((end-start)/step)):
            test_frames.append(self.data.load(start+step*i).bgr)

        last_frame = None
        motion_score = []
        for frame in test_frames:
            cv2.imshow('frame', frame)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            if last_frame is None:
                last_frame = gray
                continue

            frame_delta = cv2.absdiff(last_frame, gray)

            thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
            cv2.imshow('thresh', thresh)
            cv2.waitKey(0)

            thresh = cv2.dilate(thresh, None, iterations=2)
            last_frame = gray

            sum = 0
            for h in range(self.data.height):
                for w in range(self.data.width):
                    if(thresh[h][w] != 0):
                        sum+=1


            motion_score.append(sum)

        plt.plot(motion_score)
        plt.show()
