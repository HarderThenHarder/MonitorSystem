"""
@author: P_k_y
"""
from TCPRequest import TCPRequest
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
from functools import partial
import threading
import cv2
import time
import tkinter.messagebox as msg


MONITOR_ADDR = [('192.168.10.16', 7777)]

btn_list = []
frame_list = []
label_list = []
split_btn_list = []

thread_list = []
update_frame_label_thread_list = []

tcp_list = []

update_flag = True


def update_frame_label(tcp, frame_label, info_label):
    global update_flag
    while True:
        frame = tcp.frame
        fps = tcp.fps
        if frame is not None:
            frame = cv2.resize(frame, (320, 240))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img_tk = ImageTk.PhotoImage(img)
            frame_label.configure(image=img_tk)
            info_text = "Monitor [ %d ] @ %2d (fps)" % (label_list.index(info_label) + 1, fps)
            info_label.configure(text=info_text)
        if not update_flag:
            break
        time.sleep(0.5)


def run_monitor(btn_idx, frame_label, info_label):
    global update_flag
    print("Connecting to the monitor...")
    tcp = TCPRequest(MONITOR_ADDR[btn_idx], btn_idx)
    print("Connected!")
    print("Waiting for Image...")
    tcp_list.append(tcp)
    t = threading.Thread(target=tcp.start)
    thread_list.append(t)
    t.start()

    update_flag = True
    t2 = threading.Thread(target=update_frame_label, args=(tcp, frame_label, info_label))
    update_frame_label_thread_list.append(t2)
    t2.start()


def stop_monitor(btn_idx):
    global update_flag
    update_flag = False
    select_tcp = None

    for tcp in tcp_list:
        if tcp.idx == btn_idx:
            select_tcp = tcp
    if select_tcp:
        print("Stop the monitor...")
        select_tcp.stop()
        print("Stopped!")
        tcp_list.remove(select_tcp)
    else:
        msg.showwarning("Warning", "Can't stop monitor, no matched monitor is running.")


def click_button(btn_idx):
    frame_label = frame_list[btn_idx]
    info_label = label_list[btn_idx]
    btn = btn_list[btn_idx]
    text = btn.cget("text")

    # Start to Run monitor
    if text == "Start":
        btn.configure(text="Stop")
        run_monitor(btn_idx, frame_label, info_label)
    # Stop run monitor
    else:
        btn.configure(text="Start")
        stop_monitor(btn_idx)


def show_max_window(tcp, btn_idx):
    while True:
        cv2.imshow("Split@Monitor %d" % (btn_idx + 1), tcp.frame)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break


def split_window(btn_idx):
    tcp = None
    try:
        for t in tcp_list:
            if t.idx == btn_idx:
                tcp = t
    except:
        msg.showwarning("Warning", "You need to start the monitor at first!")
        return
    t = threading.Thread(target=show_max_window, args=(tcp, btn_idx))
    thread_list.append(t)
    t.start()


def main():

    window = tk.Tk()
    window.title("Camera Monitor System")
    window.geometry("1030x480")

    title = tk.Label(window, text="Camera Monitor - v1.0", bg='green', fg="white", font=('Arial', 12), width=30, height=2)
    title.grid(row=1, column=2, ipadx=10)

    blank_label = tk.Label(window, height=4)
    blank_label.grid(row=2, column=1)

    for i in range(3):
        label = tk.Label(window, text="Monitor [ %d ] @ %2d (fps)" % (i+1, 0), font=('Arial', 10))
        label.grid(row=3, column=i+1)
        label_list.append(label)

        img = Image.fromarray(np.full((240, 320), 240))
        img_tk = ImageTk.PhotoImage(img)
        img_label = tk.Label(window)
        img_label.configure(image=img_tk)
        img_label.grid(row=4, column=i+1, ipadx=5, ipady=10)
        frame_list.append(img_label)

        click_function_with_arg = partial(click_button, i)
        btn = tk.Button(window, text='Start', command=click_function_with_arg, width=39, font=('Arial', 10))
        btn.grid(row=5, column=i+1)
        btn_list.append(btn)

        click_function_with_arg = partial(split_window, i)
        btn = tk.Button(window, text='Split This Window', command=click_function_with_arg, width=39, font=('Arial', 10))
        btn.grid(row=6, column=i + 1)
        split_btn_list.append(btn)

    for t in thread_list:
        t.join()
    for t in update_frame_label_thread_list:
        t.join()
    window.mainloop()


if __name__ == '__main__':
    main()



