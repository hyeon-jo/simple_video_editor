import cv2
import os
import sys

if __name__ == "__main__":
	if len(sys.argv) == 1:
		print("Usage : python a.py [file] [starting point] [end point]")
		exit(1)
	else: #argument parsing; video file name, starting and end point for making video clip
		try:
			fileName = sys.argv[1]
			outFileName = "out_" + fileName
			startingPoint = int(sys.argv[2])
			endPoint = int(sys.argv[3])
		except:
			print("Arguments are not enough.")
			exit(1)

	# Read original video and get information of original video
	video = cv2.VideoCapture(fileName) # Read video from hdd
	video_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH)) # video width
	video_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)) # video height
	video_fps = video.get(cv2.CAP_PROP_FPS) # fps

	print("video width : %d, video_height : %d, video_fps : %d" % (video_width, video_height, video_fps))

	for _ in range(startingPoint*int(video_fps)): # frame skipping until the starting point
		ret, frame = video.read()
		if ret == False:
			print("Done")
			break

	fourcc = cv2.VideoWriter_fourcc(*'MJPG') # Encode with XVID codec
	out = cv2.VideoWriter(outFileName, fourcc, video_fps, (video_width, video_height)) # video writer for making video clip

	for i in range(endPoint*int(video_fps)):
		ret, frame = video.read() # read information from original video
		if ret == False : # if original video is shorter than end point.
			print("Done")
			break
		out.write(frame)
		cv2.imshow('frame', frame)
		if cv2.waitKey(1) & 0xFF==ord('q'):
			break
	
	out.release()
	print("Done")
