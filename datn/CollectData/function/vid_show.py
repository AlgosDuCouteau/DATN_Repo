import cv2, time, datetime
from threading import Thread

class VideoShow:

    def __init__(self):
        self.frame = None
        self.stopped = False
        self.t = 0

    def start(self):
        self.stopped = False
        process = Thread(target=self.show, args=())
        process.start()

    def show(self):
        while not self.stopped:
            if self.frame is None:
                continue
            img = self.frame.copy()
            img = img[0:720, 480:1280]
            img = cv2.resize(img, (512, 512))
            cv2.imwrite(f'/home/jetson/DATN-main/val_hand3/palm/{datetime.datetime.now()}.jpeg', img, [cv2.IMWRITE_JPEG_QUALITY, 90])
            self.t += 1
            print(self.t)
            cv2.imshow('result', img)
            if cv2.waitKey(1) & 0xFF == ord('q') or self.t==1408:
                break
        cv2.destroyAllWindows()
                    
    def stop(self):
        self.stopped = True
