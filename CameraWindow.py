import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
from TCPRequest import TCPRequest
import threading
import cv2
import time
import tkinter.messagebox as msg
from FaceDetector import FaceDetector
from Drawer import Drawer


MONITOR_ADDR = [('192.168.1.102', 7777), ('192.168.10.16', 7777), ("127.0.0.1", 7777)]


class CameraWindow:

    def __init__(self, idx, window):
        self.idx = idx
        self.update_flag = True
        self.info_label = tk.Label(window, text="Monitor [ %d ] @ %2d (fps)" % (idx + 1, 0), font=('Arial', 10))
        self.info_label.grid(row=3, column=idx + 1)
        img = Image.fromarray(np.full((240, 320), 100))
        img_tk = ImageTk.PhotoImage(img)
        self.frame_label = tk.Label(window)
        self.frame_label.configure(image=img_tk)
        self.frame_label.grid(row=4, column=idx + 1, ipadx=5, ipady=10)
        self.start_btn = tk.Button(window, text='Start', command=self.click_button, width=39, font=('Arial', 10))
        self.start_btn.grid(row=5, column=idx + 1)
        self.split_btn = tk.Button(window, text='Split This Window', command=self.split_window, width=39, font=('Arial', 10))
        self.split_btn.grid(row=6, column=idx + 1)
        self.thread_list = []
        self.tcp = None

    def update_frame_label(self):
        while self.update_flag:
            frame = self.tcp.frame
            fps = self.tcp.fps
            if frame is not None:
                frame = cv2.resize(frame, (320, 240))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img_tk = ImageTk.PhotoImage(img)
                self.frame_label.configure(image=img_tk)
                info_text = "Monitor [ %d ] @ %2d (fps)" % (self.idx + 1, fps)
                self.info_label.configure(text=info_text)
            time.sleep(0.5)

    def run_monitor(self):
        try:
            print("Connecting to the monitor...")
            self.tcp = TCPRequest(MONITOR_ADDR[self.idx])
            t = threading.Thread(target=self.tcp.start)
            print("Connected!")
            print("Waiting for Image...")
            self.thread_list.append(t)
            t.start()

            self.update_flag = True
            t2 = threading.Thread(target=self.update_frame_label)
            self.thread_list.append(t2)
            t2.start()
        except:
            msg.showwarning("Warning", "You must set the monitor before use!")

    def stop_monitor(self):
        self.update_flag = False

        if self.tcp is not None:
            print("Stop the monitor...")
            self.tcp.stop()
            print("Stopped!")
            self.tcp = None
        else:
            msg.showwarning("Warning", "Can't stop monitor, no matched monitor is running.")

    def click_button(self):
        text = self.start_btn.cget("text")

        # Start to Run monitor
        if text == "Start":
            self.start_btn.configure(text="Stop")
            self.run_monitor()
        # Stop run monitor
        else:
            self.start_btn.configure(text="Start")
            self.stop_monitor()

    def show_max_window(self):
        while True:
            frame = self.tcp.frame.copy()

            # detect the face and label
            face_detector = FaceDetector()
            face_max = face_detector.detect_face(frame)
            print(face_max)
            face_list = face_detector.get_face_list()
            if len(face_list) > 0:
                for face in face_list:
                    Drawer.label_face(frame, face.get_rect())

            # Write Text on the frame
            localtime = time.asctime(time.localtime(time.time()))
            width = frame.shape[0]
            cv2.putText(frame, localtime, (int(0.9 * width), 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0))
            cv2.putText(frame, "Person(s) Number: %2d" % len(face_list), (int(0.9 * width), 35), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0))

            cv2.imshow("Split@Monitor %d" % (self.idx + 1), frame)
            if cv2.waitKey(1) == ord('q'):
                cv2.destroyAllWindows()
                break

    def split_window(self):
        if self.tcp is None:
            msg.showwarning("Warning", "You need to start the monitor at first!")
            return
        t = threading.Thread(target=self.show_max_window)
        self.thread_list.append(t)
        t.start()

    def join_all_threads(self):
        for t in self.thread_list:
            t.join()