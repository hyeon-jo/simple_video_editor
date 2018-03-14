import cv2
import os
import sys
import argparse
import zipfile

def VideoProcessing(fileName, startingPoint, endPoint, numbering):
	# Read original video and get information of original video
	outFileName = os.getcwd() + "/output/" + "out_" + str(numbering) + ".avi"
	video = cv2.VideoCapture(sys.argv[1] +'/' +fileName) # Read video from hdd
	if video.isOpened() != True:
		print("Error to open video")
		print(fileName)
		return 0
	video_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH)) # video width
	video_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)) # video height
	video_fps = video.get(cv2.CAP_PROP_FPS) # fps

	print("video width : %d, video_height : %d, video_fps : %d" % (video_width, video_height, video_fps))

	for _ in range(startingPoint*int(video_fps)): # frame skipping until the starting point
		ret, frame = video.read()
		if ret == False:
			print("Error : Starting point value is bigger than video length")
			break

	fourcc = cv2.VideoWriter_fourcc(*'XVID') # Encode with XVID codec
	print(outFileName)
	out = cv2.VideoWriter(outFileName, fourcc, video_fps, (video_width, video_height)) # video writer for making video clip

	for i in range(endPoint*int(video_fps)):
		ret, frame = video.read() # read information from original video
		if ret == False : # if original video is shorter than end point.
			print("End of this video.")
			break
		out.write(frame)
#		cv2.imshow('frame', frame)
#		if cv2.waitKey(1) & 0xFF==ord('q'):
#			break
	
	out.release()
	print("Done")

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("file")
	parser.add_argument("start")
	parser.add_argument("finish")
	args = parser.parse_args()

	print(args.file)
	flag = 0
	prevSubFolder = None
	for root, subFolders, files in os.walk(args.file):
		if root == "./done" or root == "./output" or root == "./":
			continue
		i = 0
		for file in files:
			filepath = os.path.join(root, file)
			if os.path.isfile(filepath) and filepath[-3:] != 'zip':
				print("Now cutting " + file)
				VideoProcessing(filepath, int(args.start), int(args.finish), i)
				flag = 1
				i += 1
		rootsplit = root.split('/')
		if flag == 1:
			zipname = "zip done/" + rootsplit[-1] + ".zip " + "output/*"
			os.system(zipname)
			print("Zipping is done : " + zipname)
			os.system("rm output/*")
			print("File is deleted")
			flag = 0
		