from threading import Thread
from function import *
import time

class yolo_thread:
    
    def __init__(self, source):
        self.gimg = VideoGet(source)
        self.simg = VideoShow()
        self.stopped = False
        
    def start(self):
        print("starting")
        self.stopped = False
        Thread(target=self.thread_transfer_image, args=()).start()
        return self

    def thread_transfer_image(self):
        print("thread1")
        self.gimg.start()
        print("thread2")
        self.simg.start()
        while True:
            time.sleep(1/60)
            if self.stopped:
                self.gimg.stop()
                self.simg.stop()
                break
            if self.gimg.frame is None:
                continue

            self.simg.frame = self.gimg.frame
            
    def stop(self):
        self.stopped = True
        self.x, self.y = None, None 

if __name__ == "__main__":
    video_thread = yolo_thread(f'nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM),width=1920,height=1080, format=(string)NV12, framerate=60/1 ! nvvidconv flip-method=0 ! video/x-raw, width=1280, height=720, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink')
    video_thread.start()
