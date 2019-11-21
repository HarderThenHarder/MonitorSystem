"""
@author: P_k_y
"""
import tkinter as tk
from CameraWindow import CameraWindow

sub_window_list = []


def main():

    window = tk.Tk()
    window.title("Camera Monitor System")
    window.geometry("1030x480")

    # title
    title = tk.Label(window, text="Camera Monitor - v1.0", bg='green', fg="white", font=('Arial', 12), width=30, height=2)
    title.grid(row=1, column=2, ipadx=10)

    # blank gap
    blank_label = tk.Label(window, height=4)
    blank_label.grid(row=2, column=1)

    for i in range(3):
        sub_window_list.append(CameraWindow(i, window))

    for win in sub_window_list:
        win.join_all_threads()

    window.mainloop()


if __name__ == '__main__':
    main()



