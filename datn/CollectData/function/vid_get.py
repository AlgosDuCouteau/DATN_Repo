import cv2, time
from threading import Thread

class VideoGet:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """

    def __init__(self, src=0):
        self.stopped = False
        self.src = src
        self.frame = None

    def start(self):
        self.stopped = False
        process = Thread(target=self.get, args=())
        process.start()

    def get(self):
        stream = cv2.VideoCapture(self.src)
        try:
            while not self.stopped:
                grabbed, frame = stream.read()
                if grabbed is False:
                    continue
                self.frame = frame
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            stream.release()
        except Exception as e:
            print("Error: " + str(e))

    def stop(self):
        self.stopped = True
