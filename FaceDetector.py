import cv2
import numpy as np

class FaceDetector:
    def __init__(self, data, step):
        self.data = data
        self.step = step
        self.faceCascade = cv2.CascadeClassifier('face_lib/haarcascade_frontalface_default.xml')

    def get_face_score_img(self, gray):

        score = self.faceCascade.detectMultiScale(
            gray,
            scaleFactor = 1.1,
            minNeighbors=5,
            minSize=(20, 20),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # if len(faces)!=0:
        #     self.show(faces, frame)
        return score


    def show(self, faces, image):
        print('Found {0} faces'.format(len(faces)))
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.imshow("Faces found", image)
        cv2.waitKey(0)

    def get_face_score_per_step(self):
        face_scores = []
        for i in range(int(self.data.frame_count/self.step)):
            frame = self.data.load(self.step*i).bgr
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = self.get_face_score_img(gray)
            face_scores.append(len(faces))
        return np.array(face_scores)


    def get_face_score_per_shot(self, break_points, avg=True):
        '''
            When avg is true, return nums of faces per frame
        '''
        scores_per_step = self.get_face_score_per_step()
        queue = break_points[1:]
        scores_per_shot = [0] * (len(break_points)-1)

        total=0
        for i in range(len(scores_per_step)):
            if (i)*self.step > queue[0]:
                scores_per_shot[-len(queue)] = float(total) if not avg else float(total)/(break_points[-len(queue)] - break_points[-(len(queue)+1)])

                total=0
                queue.pop(0)
            total+=scores_per_step[i]

        if total>0: scores_per_shot[-len(queue)] = float(total)

        # print(scores_per_shot, len(scores_per_shot))
        return np.array(scores_per_shot)
