#!/usr/bin/env python3

from jetson.inference import imageNet
from jetson.utils import videoSource, videoOutput, cudaFont, cudaCrop, cudaAllocMapped, cudaResize, cudaMemcpy
import argparse, sys, serial, time

# parse the command line
parser = argparse.ArgumentParser(description="Classify a live camera stream using an image recognition DNN.", 
                                 formatter_class=argparse.RawTextHelpFormatter, 
                                 epilog=imageNet.Usage() + videoSource.Usage() + videoOutput.Usage())

parser.add_argument("input", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="googlenet", help="pre-trained model to load (see below for options)")
parser.add_argument("--topK", type=int, default=1, help="show the topK number of class predictions (default: 1)")

try:
	args = parser.parse_known_args()[0]
except:
	print("")
	parser.print_help()
	sys.exit(0)


# load the recognition network
net = imageNet(argv=['--model=resnet50_run3_28.onnx', '--labels=labels.txt', '--input-blob=input_0', '--output_blob=output_0'])
#net = imageNet(argv=['--model=hand3_resnet18.onnx', '--labels=labels.txt', '--input-blob=input_0', '--output_blob=output_0'])
# create video sources & outputs
input = videoSource("csi://0", argv=['--input-flip=rotate-180', '--framerate=60/1'])
output = videoOutput(args.output, argv=sys.argv)
font = cudaFont()

# init arduino instance
arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.1)
def write(x):
    arduino.write(bytes(x, 'utf-8'))

# init cmd
def reset_all():
    global fw, left, right, bw, stop, fw_flag, left_flag, right_flag, bw_flag, stop_flag
    fw, left, right, bw, stop = 0, 0, 0, 0, 0
    fw_flag, left_flag, right_flag, bw_flag, stop_flag = False, False, False, False, False

reset_all()

# process frames until EOS or the user exits
while True:
    # capture the next image
    img = input.Capture()

    if img is None: # timeout
        continue
    crop_roi = (480, 0, 1280, 720)
    imgCropped = cudaAllocMapped(width=800, height=720, format=img.format)
    cudaCrop(img, imgCropped, crop_roi)

    imgResized = cudaAllocMapped(width=512, height=512, format=imgCropped.format)
    cudaResize(imgCropped, imgResized)

    # classify the image and get the topK predictions
    # if you only want the top class, you can simply run:
    class_id, confidence = net.Classify(imgResized)

    classLabel = net.GetClassDesc(class_id)
    confidence *= 100.0

    if class_id == 0 or class_id == 4:
        if stop == 0:
             reset_all()
        stop += 1
        if stop >= 20:
             stop = 20
             if not stop_flag:
                print('stop')
                write(str(class_id))
                stop_flag = True
    elif class_id == 1:
        if fw == 0:
             reset_all()
        fw += 1
        if fw >= 20:
             fw = 20
             if not fw_flag:
                print('fw')
                write(str(class_id))
                fw_flag = True
    elif class_id == 3:
        if bw == 0:
             reset_all()
        bw += 1
        if bw >= 20:
             bw = 20
             if not bw_flag:
                print('bw')
                write(str(class_id))
                bw_flag = True
    elif class_id == 2:
        if left == 0:
             reset_all()
        left += 1
        if left >= 20:
             left = 20
             if not left_flag:
                print('left')
                write(str(class_id))
                left_flag = True
    else:
        if right == 0:
             reset_all()
        right += 1
        if right >= 20:
             right = 20
             if not right_flag:
                print('right')
                write(str(class_id))
                right_flag = True
    font.OverlayText(imgCropped, text=f"{confidence:05.2f}% {classLabel}", 
                         x=5, y=5 + 1 *5,
                         color=font.White, background=font.Gray40)
                         
    # render the image
    output.Render(imgCropped)

    # update the title bar
    output.SetStatus("{:s} | Network {:.0f} FPS".format(net.GetNetworkName(), net.GetNetworkFPS()))

    # print out performance info
    net.PrintProfilerTimes()

    # exit on input/output EOS
    if not input.IsStreaming() or not output.IsStreaming():
        break
