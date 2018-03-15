import cv2
import os
import sys
import argparse
import zipfile

def VideoProcessing(fileName, startingPoint, endPoint, numbering):
	# Read original video and get information of original video
	endFile = 0
	outFileName = os.getcwd() + "/output/" + "out_" + str(numbering) + ".avi"
	video = cv2.VideoCapture(fileName) # Read video from hdd
	if video.isOpened() != True:
		print("Error to open video")
		print(fileName)
		return 0
	video_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH)) # video width
	video_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)) # video height
	video_fps = video.get(cv2.CAP_PROP_FPS) # fps

	print("video width : %d, video_height : %d, video_fps : %d" % (video_width, video_height, video_fps))
	fourcc = cv2.VideoWriter_fourcc(*'XVID') # Encode with XVID codec

	if endPoint != 0:
		for _ in range(startingPoint*int(video_fps)): # frame skipping until the starting point
			ret, frame = video.read()
			if ret == False:
				print("Error : Starting point value is bigger than video length")
				break

		print(outFileName)
		out = cv2.VideoWriter(outFileName, fourcc, video_fps, (video_width, video_height)) # video writer for making video clip

		for i in range(endPoint*int(video_fps)):
			ret, frame = video.read() # read information from original video
			if ret == False : # if original video is shorter than end point.
				print("End of this video.")
				endFile = 1
				break
			out.write(frame)
	else:
		i = 0
		while(True):
			outFileName = os.getcwd() + "/output/" + "out_" + str(i) + ".avi"
			out = cv2.VideoWriter(outFileName, fourcc, video_fps, (video_width, video_height)) # video writer for making video clip
			for _ in range(startingPoint*int(video_fps)):
				ret, frame = video.read()
				if ret == False:
					print("End of this video.")
					endFile = 1
					return endFile
				out.write(frame)
			out.release()
			print("Save out_" + str(i) + ".avi sucessfully")
			i += 1
#		cv2.imshow('frame', frame)
#		if cv2.waitKey(1) & 0xFF==ord('q'):
#			break
	
	out.release()
	print("Done")
	return endFile

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("file")
	parser.add_argument("start")
	parser.add_argument("finish")
	args = parser.parse_args()
	if(os.path.isdir("output") == 0):
		os.system("mkdir output")
		print("Making output directory is complete.")

	if(os.path.isdir("done") == 0):
		os.system("mkdir done")
		print("Making done directory is complete.")
	start = 0
	finish = 0
	jump = None

	flag = 0
	start = int(args.start)
	finish = int(args.finish)
	for root, subFolders, files in os.walk(args.file):
		if root == "./done" or root == "./output" or root == "./":
			continue
		i = 0
		for file in files:
			filepath = os.path.join(root, file)
			print(filepath)
			if os.path.isfile(filepath) and filepath[-3:] != 'zip':
				print("Now cutting " + file)
				VideoProcessing(filepath, start, finish, i)
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
		