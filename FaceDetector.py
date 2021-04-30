import cv2
import numpy as np

face_lib_path = './lib/face_lib/haarcascade_frontalface_default.xml'

class FaceDetector:
    def __init__(self, data, step):
        self.data = data
        self.step = step
        self.faceCascade = cv2.CascadeClassifier(face_lib_path)

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
