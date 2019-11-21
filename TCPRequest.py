"""
@author: P_k_y
"""
import socket
import time
import struct
import numpy as np
import cv2
import threading


class TCPRequest:

    def __init__(self, addr: tuple):
        """
        an TCP class to get the image from the raspberry pi
        :param addr: ip of raspberry pi
        """
        self.addr = addr
        self.frame = None
        self.run_flag = True
        self.fps = 0

    def receive_video(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(self.addr)

        def recv_all(sock, count):
            buf = b''
            while count:
                newbuf = sock.recv(count)
                if not newbuf:
                    return None
                buf += newbuf
                count -= len(newbuf)
            return buf

        while True:
            start = time.time()
            fhead_size = struct.calcsize('l')
            length = sock.recv(fhead_size)
            if not length:
                continue
            string_data = recv_all(sock, struct.unpack('l', length)[0])
            data = np.frombuffer(string_data, np.uint8)
            self.frame = cv2.imdecode(data, cv2.IMREAD_COLOR)

            time_elapsed = time.time() - start
            self.fps = int(1 / time_elapsed)
            sock.send(struct.pack('l', self.fps))

            if not self.run_flag:
                sock.send(struct.pack('l', -1))
                break
        sock.close()

    def start(self):
        self.run_flag = True
        self.receive_video()

    def stop(self):
        self.run_flag = False


# Test Function
if __name__ == '__main__':
    tcp1 = TCPRequest(('192.168.10.16', 7777))
    t = threading.Thread(target=tcp1.start)
    t.start()

    while True:
        if tcp1.frame is not None:
            cv2.imshow("test", tcp1.frame)
        if cv2.waitKey(10) == ord('q'):
            tcp1.stop()
            break
    t.join()
    cv2.destroyAllWindows()
