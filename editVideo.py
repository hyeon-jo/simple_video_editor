import cv2
import os
import sys

if __name__ == "__main__":
	if len(sys.argv) == 1:
		print("Usage : python a.py [file] [starting point] [end point]")
		exit(1)
	else:
		fileName = sys.argv[1]
		outFileName = "out_" + fileName
		startingPoint = sys.argv[2]
		endPoint = sys.argv[3]

	video = cv2.VideoCapture(fileName)
	video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
	video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
	video_fps = cap.get(cv2.CAP_PROP_FPS)

	for _ in range(startingPoint):
		ret, img = video.read(0)
		if ret == False:
			print("Done")
			break

	fourcc = cv2.VideoWriter_fourcc(*'XVID')

	out = cv2.VideoWirter(outFileName, fourcc, video_fps, (video_height, video_width))

	while(True):
		ret, img = video.read(0)
		if ret == False:
			print("Done")
			break

		out.write(img)
	
