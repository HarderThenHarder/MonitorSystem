import cv2
from FaceDetector import FaceDetector


class Drawer:

    @staticmethod
    def label_face(frame, face_rect: tuple, color=(0, 0, 250)):
        x, y, w, h = face_rect
        horizon_line_length = int(w / 8)
        vertical_line_length = int(h / 8)
        center = (int(x + w / 2), int(y + h / 2))
        cv2.line(frame, (x - horizon_line_length, center[1]), (x + horizon_line_length, center[1]), color, 2)
        cv2.line(frame, (x + w - horizon_line_length, center[1]), (x + w + horizon_line_length, center[1]), color, 2)
        cv2.line(frame, (center[0], y - vertical_line_length), (center[0], y + vertical_line_length), color, 2)
        cv2.line(frame, (center[0], y + h - vertical_line_length), (center[0], y + h + vertical_line_length), color, 2)
        cv2.circle(frame, center, int(h / 2), color, 2)


if __name__ == '__main__':
    img = cv2.imread("assets/timg2.jpg")
    face_detector = FaceDetector()
    face_detector.detect_face(img)
    face_list = face_detector.get_face_list()
    if len(face_list) > 0:
        for face in face_list:
            Drawer.label_face(img, face.get_rect(), color=(0, 0, 200))
    cv2.imshow("test Drawer", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
