import cv2
from Face import Face


class FaceDetector:

    def __init__(self):
        self.__face_cascade = cv2.CascadeClassifier("assets/haarcascade_frontalface_alt2.xml")
        self.__face_list = []

    def detect_face(self, frame):
        """
        return the Face Object with the max size
        :param frame: camera frame, np.array
        :return: Face Object
        """
        self.__face_list.clear()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.__face_cascade.detectMultiScale(gray, 1.1, 2)

        if len(faces) > 0:
            for face in faces:
                self.__face_list.append(Face(face))
            sorted(self.__face_list, key=lambda x: x.calculate_size(), reverse=True)
            return self.__face_list[0]
        return None

    def get_face_list(self):
        return self.__face_list


# Test function
if __name__ == '__main__':
    # # Test Img
    # img = cv2.imread("assets/timg2.jpg")
    # face_detector = FaceDetector()
    # # max size face
    # face_detector.detect_face(img)
    # face_list = face_detector.get_face_list()
    # if len(face_list) > 0:
    #     for face in face_list:
    #         x, y, w, h = face.get_rect()
    #         cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
    # cv2.imshow("test Face Recognize", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    cap = cv2.VideoCapture(0)
    face_detector = FaceDetector()

    while True:
        ret, frame = cap.read()

        face = face_detector.detect_face(frame)

        if face is not None:
            x, y, w, h = face.get_rect()
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow("test", frame)
        if cv2.waitKey(1) == ord('q'):
            break
    cv2.destroyAllWindows()

